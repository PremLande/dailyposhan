"""
Groww Algo Trading Bot - SMA Crossover Strategy (Intraday, Single Stock)
==========================================================================

WHAT THIS DOES
--------------
Watches one NSE stock, computes a fast/slow Simple Moving Average (SMA)
crossover on recent candles, and places MARKET orders through the Groww
Trading API when the fast SMA crosses the slow SMA:
  - Fast SMA crosses ABOVE slow SMA  -> BUY
  - Fast SMA crosses BELOW slow SMA  -> SELL (exit long)

It also enforces basic risk controls: a stop-loss and target per trade,
a hard daily loss limit, and a daily profit target that stops new entries
once hit.

BEFORE YOU RUN THIS WITH REAL MONEY
------------------------------------
1. Run with DRY_RUN = True for at least several trading sessions. It will
   log every signal and simulated fill without touching your account.
2. Backtest the SMA parameters on get_historical_candle_data for the
   stock(s) you care about. A crossover strategy that hasn't been tested
   on your target stock's actual volatility is a guess, not a strategy.
3. Understand costs: brokerage, STT, exchange charges, GST, stamp duty,
   and slippage all eat into small intraday gains. At low capital these
   fixed-ish costs can be a large % of any profit target like 200-500/day.
4. This is not financial advice and comes with no expectation of profit.
   You are responsible for testing, monitoring, and any losses.
5. Never hardcode real credentials into a script you might commit to git
   or share. Use environment variables (shown below).

INSTALL
-------
    pip install growwapi pyotp

CREDENTIALS
-----------
Use the TOTP flow (no daily re-approval needed) or the API key+secret
flow per the docs: https://groww.in/trade-api/docs/python-sdk
Set these as environment variables rather than pasting them into the file:
    export GROWW_API_KEY="..."
    export GROWW_API_SECRET="..."          # if using key+secret flow
    export GROWW_TOTP_SECRET="..."         # if using TOTP flow
"""

import os
import sys
import time
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time as dtime

from growwapi import GrowwAPI

try:
    import pyotp
except ImportError:
    pyotp = None


# =============================================================================
# CONFIG - tune all of this before running
# =============================================================================

DRY_RUN = True  # <-- Keep True until you trust the logs. Flip manually.

TRADING_SYMBOL = "RELIANCE"     # Stock to trade
EXCHANGE = "NSE"
SEGMENT = "CASH"
PRODUCT = "MIS"                 # MIS = intraday margin product (auto square-off)

FAST_SMA_PERIOD = 9
SLOW_SMA_PERIOD = 21
CANDLE_INTERVAL_MINUTES = 5     # 5-min candles
LOOKBACK_CANDLES = max(SLOW_SMA_PERIOD * 3, 50)  # enough history to warm up SMA

CAPITAL_ALLOCATED = 1000.0     # Rupees you're willing to deploy, NOT your full account
RISK_PER_TRADE_PCT = 10.0        # % of CAPITAL_ALLOCATED risked per trade (via stop loss)
STOP_LOSS_PCT = 5             # % below entry price for stop loss
TARGET_PCT = 10.0                # % above entry price for target (optional take-profit)

DAILY_PROFIT_TARGET = 500.0     # Stop opening new trades once realized P&L hits this
DAILY_LOSS_LIMIT = 500.0        # Stop trading entirely if realized loss hits this (circuit breaker)

POLL_INTERVAL_SECONDS = 60      # How often to check for a new signal
MARKET_OPEN = dtime(9, 15)
MARKET_CLOSE = dtime(15, 20)    # Stop new entries a bit before actual close (15:30)
SQUARE_OFF_TIME = dtime(15, 20) # Force-exit any open position by this time

LOG_FILE = "groww_algo_trader.log"


# =============================================================================
# LOGGING
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("groww_algo")


# =============================================================================
# AUTH
# =============================================================================

def get_groww_client() -> GrowwAPI:
    api_key = os.environ.get("GROWW_API_KEY")
    if not api_key:
        raise RuntimeError("Set GROWW_API_KEY environment variable.")

    totp_secret = os.environ.get("GROWW_TOTP_SECRET")
    api_secret = os.environ.get("GROWW_API_SECRET")

    if totp_secret:
        if pyotp is None:
            raise RuntimeError("pip install pyotp to use the TOTP auth flow.")
        totp = pyotp.TOTP(totp_secret).now()
        access_token = GrowwAPI.get_access_token(api_key=api_key, totp=totp)
    elif api_secret:
        access_token = GrowwAPI.get_access_token(api_key=api_key, secret=api_secret)
    else:
        raise RuntimeError(
            "Set either GROWW_TOTP_SECRET (TOTP flow) or GROWW_API_SECRET "
            "(key+secret flow) as an environment variable."
        )

    return GrowwAPI(access_token)


# =============================================================================
# STRATEGY STATE
# =============================================================================

@dataclass
class DayState:
    realized_pnl: float = 0.0
    trades_today: int = 0
    position_open: bool = False
    entry_price: float = 0.0
    quantity: int = 0
    stop_loss_price: float = 0.0
    target_price: float = 0.0
    groww_order_id: str = ""
    last_signal: str = "NONE"  # "NONE" | "BUY" | "SELL"
    trading_halted: bool = False


# =============================================================================
# MARKET DATA HELPERS
# =============================================================================

def fetch_recent_closes(groww: GrowwAPI, symbol: str) -> list:
    """Fetch recent candles and return list of close prices, oldest first."""
    end_time = datetime.now()
    start_time = end_time - timedelta(
        minutes=CANDLE_INTERVAL_MINUTES * LOOKBACK_CANDLES * 2  # buffer for gaps
    )
    resp = groww.get_historical_candle_data(
        trading_symbol=symbol,
        exchange=groww.EXCHANGE_NSE,
        segment=groww.SEGMENT_CASH,
        start_time=start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time=end_time.strftime("%Y-%m-%d %H:%M:%S"),
        interval_in_minutes=CANDLE_INTERVAL_MINUTES,
    )
    candles = resp.get("candles", [])
    closes = [c[4] for c in candles]  # [timestamp, open, high, low, close, volume]
    return closes[-LOOKBACK_CANDLES:]


def sma(values: list, period: int) -> float:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def get_ltp(groww: GrowwAPI, symbol: str) -> float:
    key = f"{EXCHANGE}_{symbol}"
    resp = groww.get_ltp(segment=groww.SEGMENT_CASH, exchange_trading_symbols=key)
    return resp[key]


# =============================================================================
# ORDER HELPERS
# =============================================================================

def compute_quantity(capital: float, entry_price: float) -> int:
    """
    Size position so that a stop-loss hit loses ~RISK_PER_TRADE_PCT of capital.
    Falls back to a capital-based cap if that would exceed available capital.
    """
    risk_amount = capital * (RISK_PER_TRADE_PCT / 100.0)
    stop_distance = entry_price * (STOP_LOSS_PCT / 100.0)
    if stop_distance <= 0:
        return 0
    qty_by_risk = int(risk_amount / stop_distance)
    qty_by_capital = int(capital / entry_price)
    return max(0, min(qty_by_risk, qty_by_capital))


def place_market_order(groww: GrowwAPI, symbol: str, quantity: int, side: str, ref_id: str):
    if DRY_RUN:
        log.info(f"[DRY_RUN] Would place {side} MARKET order: {quantity} x {symbol} (ref={ref_id})")
        return {"groww_order_id": "DRYRUN", "order_status": "EXECUTED"}

    transaction_type = groww.TRANSACTION_TYPE_BUY if side == "BUY" else groww.TRANSACTION_TYPE_SELL
    resp = groww.place_order(
        trading_symbol=symbol,
        quantity=quantity,
        validity=groww.VALIDITY_DAY,
        exchange=groww.EXCHANGE_NSE,
        segment=groww.SEGMENT_CASH,
        product=groww.PRODUCT_MIS,
        order_type=groww.ORDER_TYPE_MARKET,
        transaction_type=transaction_type,
        order_reference_id=ref_id,
    )
    log.info(f"Order placed: {resp}")
    return resp


def make_ref_id(prefix: str) -> str:
    # 8-20 alphanumeric chars, at most two hyphens
    return f"{prefix}-{int(time.time())}"[:20]


# =============================================================================
# MAIN LOOP
# =============================================================================

def within_trading_hours() -> bool:
    now = datetime.now().time()
    return MARKET_OPEN <= now <= MARKET_CLOSE


def run():
    groww = get_groww_client()
    state = DayState()
    log.info(
        f"Starting bot | symbol={TRADING_SYMBOL} | DRY_RUN={DRY_RUN} | "
        f"capital={CAPITAL_ALLOCATED} | fast={FAST_SMA_PERIOD} slow={SLOW_SMA_PERIOD}"
    )

    if DRY_RUN:
        log.warning("Running in DRY_RUN mode. No real orders will be placed.")

    while True:
        try:
            now = datetime.now().time()

            if now >= SQUARE_OFF_TIME and state.position_open:
                exit_position(groww, state, reason="EOD square-off")

            if not within_trading_hours():
                log.info("Outside trading hours. Sleeping.")
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            if state.trading_halted:
                log.info("Trading halted for the day (limit hit). Idle.")
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            check_daily_limits(state)
            if state.trading_halted:
                continue

            closes = fetch_recent_closes(groww, TRADING_SYMBOL)
            fast = sma(closes, FAST_SMA_PERIOD)
            slow = sma(closes, SLOW_SMA_PERIOD)

            if fast is None or slow is None:
                log.info("Not enough candle history yet to compute SMAs. Waiting.")
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            signal = "BUY" if fast > slow else "SELL"
            ltp = get_ltp(groww, TRADING_SYMBOL)
            log.info(f"fast_sma={fast:.2f} slow_sma={slow:.2f} ltp={ltp:.2f} signal={signal}")

            if state.position_open:
                manage_open_position(groww, state, ltp, signal)
            elif signal == "BUY" and state.last_signal != "BUY":
                enter_position(groww, state, ltp)

            state.last_signal = signal

        except Exception as e:
            log.exception(f"Error in main loop: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)


def enter_position(groww: GrowwAPI, state: DayState, ltp: float):
    qty = compute_quantity(CAPITAL_ALLOCATED, ltp)
    if qty <= 0:
        log.warning("Computed quantity is 0 — capital too low for this stock's price. Skipping entry.")
        return

    ref_id = make_ref_id("ENTRY")
    resp = place_market_order(groww, TRADING_SYMBOL, qty, "BUY", ref_id)

    state.position_open = True
    state.entry_price = ltp
    state.quantity = qty
    state.stop_loss_price = ltp * (1 - STOP_LOSS_PCT / 100.0)
    state.target_price = ltp * (1 + TARGET_PCT / 100.0)
    state.groww_order_id = resp.get("groww_order_id", "")
    state.trades_today += 1

    log.info(
        f"ENTERED long {qty} x {TRADING_SYMBOL} @ ~{ltp:.2f} | "
        f"SL={state.stop_loss_price:.2f} TGT={state.target_price:.2f}"
    )


def manage_open_position(groww: GrowwAPI, state: DayState, ltp: float, signal: str):
    hit_stop = ltp <= state.stop_loss_price
    hit_target = ltp >= state.target_price
    trend_flipped = signal == "SELL"

    if hit_stop:
        exit_position(groww, state, reason=f"Stop-loss hit @ {ltp:.2f}")
    elif hit_target:
        exit_position(groww, state, reason=f"Target hit @ {ltp:.2f}")
    elif trend_flipped:
        exit_position(groww, state, reason="SMA trend flipped bearish")


def exit_position(groww: GrowwAPI, state: DayState, reason: str):
    if not state.position_open:
        return

    ref_id = make_ref_id("EXIT")
    ltp = get_ltp(groww, TRADING_SYMBOL)
    place_market_order(groww, TRADING_SYMBOL, state.quantity, "SELL", ref_id)

    pnl = (ltp - state.entry_price) * state.quantity
    state.realized_pnl += pnl
    log.info(f"EXITED position | reason={reason} | exit_price~={ltp:.2f} | trade_pnl={pnl:.2f} | "
              f"day_pnl={state.realized_pnl:.2f}")

    state.position_open = False
    state.entry_price = 0.0
    state.quantity = 0
    state.stop_loss_price = 0.0
    state.target_price = 0.0
    state.groww_order_id = ""


def check_daily_limits(state: DayState):
    if state.realized_pnl <= -abs(DAILY_LOSS_LIMIT):
        log.warning(f"Daily loss limit hit ({state.realized_pnl:.2f}). Halting new trades.")
        state.trading_halted = True
    elif state.realized_pnl >= DAILY_PROFIT_TARGET and not state.position_open:
        log.info(f"Daily profit target hit ({state.realized_pnl:.2f}). Halting new entries.")
        state.trading_halted = True


if __name__ == "__main__":
    run()