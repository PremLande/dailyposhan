import { useState, useEffect } from "react";
import { api } from "./api/client";

const C = {
  darkGreen: "#1B3A1F",
  green: "#2D5A27",
  lightGreen: "#4A7C3F",
  cream: "#F5F0E8",
  creamDark: "#EDE6D3",
  yellow: "#F5C518",
  yellowLight: "#FDD835",
  white: "#FFFFFF",
  offWhite: "#FAFAF5",
  text: "#1a1a1a",
  muted: "#6B7B6E",
};

function useFonts() {
  useEffect(() => {
    const el = document.createElement("link");
    el.rel = "stylesheet";
    el.href = "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600;700&family=Dancing+Script:wght@700&display=swap";
    document.head.appendChild(el);
  }, []);
}

const PRODUCTS = [
  {
    id: 1,
    name: "Muscle Fuel Jar",
    hindi: "??? ?????",
    tagline: "High protein salad for strength & recovery",
    desc: "Grilled chicken, boiled eggs, quinoa, kidney beans, broccoli, cherry tomatoes with herb vinaigrette",
    price: 249, original: 299,
    cal: 420, protein: "34g", fiber: "8g",
    badge: "?? Bestseller",
    badgeColor: C.darkGreen,
    tag: "High Protein",
    bg: "linear-gradient(135deg, #E8F5E9, #C8E6C9)",
    accent: "#2D5A27",
    icon: "??",
  },
  {
    id: 2,
    name: "Glow & Flow Jar",
    hindi: "???? & ????",
    tagline: "Women special salad for glow, balance & energy",
    desc: "Pomegranate seeds, avocado, beetroot, walnuts, spinach, feta, cucumber with lemon-turmeric dressing",
    price: 229, original: 279,
    cal: 310, protein: "14g", fiber: "11g",
    badge: "? Women's Pick",
    badgeColor: "#7B3F8A",
    tag: "Glow & Balance",
    bg: "linear-gradient(135deg, #FCE4EC, #E1BEE7)",
    accent: "#7B3F8A",
    icon: "??",
  },
  {
    id: 3,
    name: "Chatori Jar",
    hindi: "????? ???",
    tagline: "Chatpata, desi twist with a healthy punch",
    desc: "Sprouts, corn, raw mango, onion, green chutney, sev, chaat masala � the ultimate desi jar salad",
    price: 199, original: 249,
    cal: 260, protein: "12g", fiber: "9g",
    badge: "??? Spicy Fav",
    badgeColor: "#C62828",
    tag: "Desi Chatpata",
    bg: "linear-gradient(135deg, #FFF8E1, #FFECB3)",
    accent: "#E65100",
    icon: "???",
  },
];

const FEATURES = [
  { icon: "??", label: "Fresh & Natural", sub: "Sourced daily" },
  { icon: "??", label: "Nutritious & Balanced", sub: "Dietitian approved" },
  { icon: "??", label: "No Preservatives", sub: "Zero junk" },
  { icon: "??", label: "High Protein", sub: "Fiber rich" },
];

function useCart() {
  const [cart, setCart] = useState([]);
  const add = (p) => setCart(c => {
    const ex = c.find(x => x.id === p.id);
    return ex ? c.map(x => x.id === p.id ? { ...x, qty: x.qty + 1 } : x) : [...c, { ...p, qty: 1 }];
  });
  const remove = (id) => setCart(c => c.filter(x => x.id !== id));
  const update = (id, qty) => qty < 1 ? remove(id) : setCart(c => c.map(x => x.id === id ? { ...x, qty } : x));
  const clear = () => setCart([]);
  const total = cart.reduce((s, x) => s + x.price * x.qty, 0);
  const count = cart.reduce((s, x) => s + x.qty, 0);
  return { cart, add, remove, update, clear, total, count };
}

function Logo({ size = 48, dark = false }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}>
      <div style={{
        width: size, height: size,
        background: dark ? C.cream : C.darkGreen,
        borderRadius: "50%", display: "flex", alignItems: "center",
        justifyContent: "center", fontSize: size * 0.5, flexShrink: 0,
        boxShadow: dark ? "none" : "0 4px 15px rgba(27,58,31,0.3)",
      }}>??</div>
      <div>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: size * 0.28,
          fontWeight: 300, color: dark ? C.cream : C.darkGreen,
          letterSpacing: 2, textTransform: "uppercase", lineHeight: 1,
        }}>daily</div>
        <div style={{
          fontFamily: "serif", fontSize: size * 0.52, fontWeight: 900,
          color: dark ? C.yellowLight : C.darkGreen, lineHeight: 1,
          letterSpacing: -1,
        }}>????</div>
      </div>
    </div>
  );
}

function Nav({ page, setPage, cartCount, onCartOpen, isAdmin, onAdminToggle }) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", h);
    return () => window.removeEventListener("scroll", h);
  }, []);

  return (
    <>
      <div style={{
        background: C.yellow, color: C.darkGreen,
        textAlign: "center", padding: "8px 20px",
        fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 13,
        letterSpacing: 0.5, position: "fixed", top: 0, left: 0, right: 0, zIndex: 1001,
      }}>
        ?? LAUNCH OFFER � Flat 20% OFF on all orders for a week! Use code: <strong>POSHAN20</strong> &nbsp;�&nbsp; Order on WhatsApp: <strong>9326251314</strong>
      </div>
      <nav style={{
        position: "fixed", top: 36, left: 0, right: 0, zIndex: 1000,
        background: scrolled ? "rgba(245,240,232,0.97)" : "transparent",
        backdropFilter: scrolled ? "blur(20px)" : "none",
        boxShadow: scrolled ? "0 2px 30px rgba(27,58,31,0.12)" : "none",
        transition: "all 0.4s ease", padding: "0 5%",
        display: "flex", alignItems: "center", justifyContent: "space-between", height: 68,
        borderBottom: scrolled ? `1px solid ${C.creamDark}` : "none",
      }}>
        <div onClick={() => setPage("home")}><Logo size={48} /></div>
        <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
          {["home", "menu"].map(p => (
            <button key={p} onClick={() => setPage(p)} style={{
              background: page === p ? C.darkGreen : "transparent",
              color: page === p ? C.cream : C.darkGreen,
              border: page === p ? "none" : `1.5px solid ${C.darkGreen}30`,
              borderRadius: 100, padding: "8px 22px",
              fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 600,
              cursor: "pointer", textTransform: "capitalize",
            }}>{p === "home" ? "Home" : "Menu"}</button>
          ))}
          {isAdmin && (
            <button onClick={() => setPage("admin")} style={{
              background: page === "admin" ? C.lightGreen : "transparent",
              color: page === "admin" ? C.white : C.darkGreen,
              border: "none", borderRadius: 100, padding: "8px 22px",
              fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 600, cursor: "pointer",
            }}>Admin</button>
          )}
          <button onClick={onCartOpen} style={{
            background: C.darkGreen, color: C.yellow,
            border: "none", borderRadius: 100, padding: "10px 22px",
            display: "flex", alignItems: "center", gap: 8,
            fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700,
            cursor: "pointer",
          }}>
            ?? Cart
            {cartCount > 0 && (
              <span style={{
                background: C.yellow, color: C.darkGreen, borderRadius: "50%",
                width: 22, height: 22, display: "flex", alignItems: "center",
                justifyContent: "center", fontSize: 11, fontWeight: 800,
              }}>{cartCount}</span>
            )}
          </button>
          <button onClick={onAdminToggle} style={{
            background: "none", border: `1px solid ${C.darkGreen}40`,
            borderRadius: 8, padding: "6px 12px", fontSize: 11, cursor: "pointer",
            color: C.muted, fontFamily: "'DM Sans', sans-serif",
          }}>{isAdmin ? "Exit Admin" : "Admin ?"}</button>
        </div>
      </nav>
    </>
  );
}

function Hero({ setPage }) {
  const [vis, setVis] = useState(false);
  useEffect(() => { setTimeout(() => setVis(true), 80); }, []);
  return (
    <section style={{ minHeight: "100vh", background: C.cream, paddingTop: 104, position: "relative", overflow: "hidden", display: "flex", alignItems: "center" }}>
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, pointerEvents: "none", overflow: "hidden" }}>
        <div style={{ position: "absolute", top: -60, right: -60, fontSize: 220, opacity: 0.05, transform: "rotate(20deg)" }}>??</div>
        <div style={{ position: "absolute", bottom: 40, left: -40, fontSize: 180, opacity: 0.05, transform: "rotate(-15deg)" }}>??</div>
        <div style={{ position: "absolute", top: 0, right: 0, width: "45%", height: "100%", background: C.darkGreen, clipPath: "ellipse(90% 100% at 100% 50%)" }} />
      </div>
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 5%", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 60, alignItems: "center", width: "100%", position: "relative", zIndex: 1 }}>
        <div style={{ opacity: vis ? 1 : 0, transform: vis ? "translateY(0)" : "translateY(32px)", transition: "all 0.8s ease" }}>
          <h1 style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: "clamp(38px, 4.5vw, 60px)", fontWeight: 900, lineHeight: 1.08, color: C.darkGreen, margin: "0 0 8px" }}>
            Eat Clean.<br /><span style={{ color: C.lightGreen, fontStyle: "italic" }}>Live Well.</span>
          </h1>
          <p style={{ fontSize: 32, fontFamily: "serif", fontWeight: 700, color: C.darkGreen, margin: "0 0 20px", letterSpacing: -0.5 }}>Your Daily Dose of Poshan ??</p>
          <p style={{ fontSize: 17, color: C.muted, lineHeight: 1.75, marginBottom: 36, maxWidth: 480, fontFamily: "'DM Sans', sans-serif" }}>
            Freshly crafted jar salads � Nutritious � Fresh � Wholesome. No preservatives. No junk. Just real food, every day.
          </p>
          <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 40 }}>
            <button onClick={() => setPage("menu")} style={{ background: C.darkGreen, color: C.yellow, border: "none", borderRadius: 100, padding: "16px 36px", fontSize: 16, fontWeight: 700, cursor: "pointer", fontFamily: "'DM Sans', sans-serif" }}>Order Now ?</button>
            <a href="https://wa.me/919326251314" style={{ background: "#25D366", color: C.white, textDecoration: "none", borderRadius: 100, padding: "16px 28px", fontSize: 16, fontWeight: 700, display: "flex", alignItems: "center", gap: 8, fontFamily: "'DM Sans', sans-serif" }}>?? WhatsApp</a>
          </div>
          <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
            {FEATURES.map(f => (
              <div key={f.label} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <div style={{ width: 36, height: 36, borderRadius: "50%", background: `${C.darkGreen}15`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>{f.icon}</div>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: C.darkGreen }}>{f.label}</div>
                  <div style={{ fontSize: 10, color: C.muted }}>{f.sub}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function ProductCard({ product, onAdd }) {
  const [added, setAdded] = useState(false);
  const handleAdd = () => { onAdd(product); setAdded(true); setTimeout(() => setAdded(false), 1200); };
  return (
    <div style={{ background: C.white, borderRadius: 28, overflow: "hidden", boxShadow: "0 4px 40px rgba(27,58,31,0.08)", border: `1px solid ${C.creamDark}` }}>
      <div style={{ background: product.bg, padding: "40px 24px 28px", display: "flex", flexDirection: "column", alignItems: "center", position: "relative" }}>
        <span style={{ position: "absolute", top: 16, left: 16, background: product.badgeColor, color: C.white, borderRadius: 100, padding: "5px 14px", fontSize: 11, fontWeight: 700 }}>{product.badge}</span>
        <div style={{ fontSize: 80, marginBottom: 8 }}>{product.icon}</div>
        <div style={{ fontSize: 22, fontWeight: 900, color: C.darkGreen, fontFamily: "'Playfair Display', serif", textAlign: "center" }}>{product.name}</div>
        <div style={{ fontSize: 14, color: product.accent, fontStyle: "italic" }}>{product.hindi}</div>
      </div>
      <div style={{ padding: "22px 24px 26px" }}>
        <p style={{ fontSize: 13, color: C.muted, lineHeight: 1.65, marginBottom: 18 }}>{product.desc}</p>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <span style={{ fontSize: 28, fontWeight: 900, color: C.darkGreen }}>?{product.price}</span>
            <span style={{ fontSize: 14, color: "#bbb", textDecoration: "line-through", marginLeft: 8 }}>?{product.original}</span>
          </div>
          <button onClick={handleAdd} style={{ background: added ? "#4A7C3F" : C.darkGreen, color: added ? C.white : C.yellow, border: "none", borderRadius: 100, padding: "12px 24px", fontSize: 14, fontWeight: 700, cursor: "pointer" }}>{added ? "? Added!" : "+ Add to Cart"}</button>
        </div>
      </div>
    </div>
  );
}

function MenuPage({ products, onAdd }) {
  return (
    <div style={{ minHeight: "100vh", background: C.offWhite, paddingTop: 104 }}>
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "60px 5% 80px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 32 }}>
          {products.map(p => <ProductCard key={p.id} product={p} onAdd={onAdd} />)}
        </div>
      </div>
    </div>
  );
}

function CartSidebar({ cart, onUpdate, onRemove, total, onClose, onCheckout }) {
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 2000 }}>
      <div onClick={onClose} style={{ position: "absolute", inset: 0, background: "rgba(27,58,31,0.5)", backdropFilter: "blur(6px)" }} />
      <div style={{ position: "absolute", right: 0, top: 0, bottom: 0, width: 420, background: C.cream, display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "28px", borderBottom: `1px solid ${C.creamDark}`, display: "flex", justifyContent: "space-between", alignItems: "center", background: C.darkGreen }}>
          <h2 style={{ fontSize: 24, margin: 0, color: C.cream }}>Your Cart ??</h2>
          <button onClick={onClose} style={{ background: "rgba(255,255,255,0.1)", border: "none", borderRadius: "50%", width: 36, height: 36, fontSize: 18, cursor: "pointer", color: C.cream }}>�</button>
        </div>
        <div style={{ flex: 1, overflowY: "auto", padding: "20px 28px" }}>
          {cart.length === 0 ? <p style={{ color: C.muted }}>Your cart is empty.</p> : cart.map(item => (
            <div key={item.id} style={{ display: "flex", gap: 10, alignItems: "center", padding: "12px 0", borderBottom: `1px solid ${C.creamDark}` }}>
              <span style={{ fontSize: 28 }}>{item.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 700 }}>{item.name}</div>
                <div style={{ fontSize: 12, color: C.muted }}>?{item.price} each</div>
              </div>
              <button onClick={() => onUpdate(item.id, item.qty - 1)}>?</button>
              <span>{item.qty}</span>
              <button onClick={() => onUpdate(item.id, item.qty + 1)}>+</button>
              <button onClick={() => onRemove(item.id)}>?</button>
            </div>
          ))}
        </div>
        {cart.length > 0 && (
          <div style={{ padding: "20px 28px", borderTop: `1px solid ${C.creamDark}`, background: C.white }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}><span>Total</span><span>?{total}</span></div>
            <button onClick={onCheckout} style={{ width: "100%", background: C.darkGreen, color: C.yellow, border: "none", borderRadius: 14, padding: "14px", fontSize: 16, fontWeight: 700, cursor: "pointer" }}>Proceed to Checkout ?</button>
          </div>
        )}
      </div>
    </div>
  );
}

function CheckoutPage({ cart, total, user, onOrderPlaced }) {
  const [form, setForm] = useState({ name: "", phone: "", address: "", pincode: "", payment: "cod" });
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [placedOrder, setPlacedOrder] = useState(null);

  const validate = () => {
    if (!form.name.trim() || !form.phone.trim() || !form.address.trim() || !form.pincode.trim()) return "Please fill all delivery details.";
    if (!/^\d{10}$/.test(form.phone.trim())) return "Phone must be 10 digits.";
    if (!/^\d{6}$/.test(form.pincode.trim())) return "Pincode must be 6 digits.";
    return "";
  };

  const handlePlace = async () => {
    const v = validate();
    if (v) return setError(v);
    setError("");
    setLoading(true);
    try {
      const paymentCreate = await api.createPayment({ method: form.payment });
      await api.verifyPayment({ payment_id: paymentCreate.payment_id });
      const created = await api.createOrder({
        user_id: user?.id || null,
        customer_name: form.name,
        phone: form.phone,
        address: `${form.address} - ${form.pincode}`,
        items: cart,
        total,
        payment_method: form.payment,
        payment_status: paymentCreate.status,
      });
      setPlacedOrder(created);
      setStep(3);
      onOrderPlaced();
    } catch (e) {
      setError(e.message || "Could not place order");
    } finally {
      setLoading(false);
    }
  };

  if (step === 3) return (
    <div style={{ minHeight: "100vh", background: C.cream, paddingTop: 104, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ background: C.white, borderRadius: 28, padding: "64px 56px", textAlign: "center", maxWidth: 480, border: `1px solid ${C.creamDark}` }}>
        <div style={{ fontSize: 80, marginBottom: 20 }}>??</div>
        <h2 style={{ fontSize: 34, color: C.darkGreen }}>Order Placed!</h2>
        <div style={{ background: C.cream, borderRadius: 16, padding: "16px 24px", marginBottom: 28, border: `1px solid ${C.creamDark}` }}>
          <div style={{ fontSize: 12, color: C.muted }}>Order ID</div>
          <div style={{ fontSize: 26, fontWeight: 900, color: C.darkGreen }}>{placedOrder?.id}</div>
        </div>
      </div>
    </div>
  );

  return (
    <div style={{ minHeight: "100vh", background: C.offWhite, paddingTop: 104 }}>
      <div style={{ maxWidth: 920, margin: "0 auto", padding: "40px 5% 80px", display: "grid", gridTemplateColumns: "1fr 360px", gap: 32 }}>
        <div>
          <h1 style={{ fontSize: 36, color: C.darkGreen, marginBottom: 32 }}>Checkout</h1>
          <div style={{ background: C.white, borderRadius: 20, padding: "28px", marginBottom: 20, border: `1px solid ${C.creamDark}` }}>
            <h3 style={{ marginBottom: 20, color: C.darkGreen }}>?? Delivery Address</h3>
            {[["name", "Full Name", "text"], ["phone", "Phone Number", "tel"], ["address", "Full Address", "text"], ["pincode", "Pincode", "text"]].map(([key, label, type]) => (
              <div key={key} style={{ marginBottom: 16 }}>
                <label style={{ fontSize: 12, color: C.muted, display: "block", marginBottom: 6 }}>{label}</label>
                <input type={type} value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
                  style={{ width: "100%", border: `2px solid ${C.creamDark}`, borderRadius: 10, padding: "12px 14px", fontSize: 15, boxSizing: "border-box", background: C.cream, color: C.darkGreen }} />
              </div>
            ))}
          </div>
        </div>
        <div>
          <div style={{ background: C.white, borderRadius: 20, padding: "28px", border: `1px solid ${C.creamDark}`, position: "sticky", top: 110 }}>
            <h3 style={{ marginBottom: 20, color: C.darkGreen }}>Order Summary</h3>
            {cart.map(item => (
              <div key={item.id} style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
                <span>{item.name} x{item.qty}</span>
                <span>?{item.price * item.qty}</span>
              </div>
            ))}
            <div style={{ borderTop: `2px solid ${C.creamDark}`, paddingTop: 16, marginTop: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 22, fontWeight: 900, marginBottom: 20, color: C.darkGreen }}><span>Total</span><span>?{total}</span></div>
              <button onClick={handlePlace} disabled={loading} style={{ width: "100%", background: loading ? C.muted : C.darkGreen, color: C.yellow, border: "none", borderRadius: 14, padding: "16px", fontSize: 16, fontWeight: 700, cursor: loading ? "not-allowed" : "pointer" }}>{loading ? "Placing Order�" : "?? Place Order"}</button>
              {!!error && <div style={{ marginTop: 12, fontSize: 12, color: "#C62828" }}>{error}</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const MOCK_ORDERS = [
  { id: "DP10234", customer: "Priya Sharma", itemsText: "Muscle Fuel Jar x2", total: 498, status: "Delivered", time: "10:30 AM", address: "Andheri West, Mumbai" },
  { id: "DP10235", customer: "Rohan Mehta", itemsText: "Glow & Flow Jar x1, Chatori Jar x1", total: 428, status: "Out for Delivery", time: "11:15 AM", address: "Bandra, Mumbai" },
];
const SCOL = { Pending: "#FFA726", Preparing: "#42A5F5", "Out for Delivery": "#AB47BC", Delivered: "#4A7C3F" };

function AdminDashboard({ products }) {
  const [orders, setOrders] = useState([]);
  const [tab, setTab] = useState("overview");

  const normalizeOrder = (o) => ({
    id: o.id,
    customer: o.customer || o.customer_name || "Customer",
    itemsText: o.itemsText || (Array.isArray(o.items) ? o.items.map((i) => `${i.name} x${i.qty || i.quantity || 1}`).join(", ") : o.items || "-"),
    total: o.total || 0,
    status: o.status || "Pending",
    address: o.address || "-",
    time: o.time || (o.created_at ? new Date(o.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "-"),
  });

  useEffect(() => {
    (async () => {
      try {
        const list = await api.adminOrders();
        setOrders(list.length ? list.map(normalizeOrder) : MOCK_ORDERS);
      } catch {
        setOrders(MOCK_ORDERS);
      }
    })();
  }, []);

  const update = async (id, status) => {
    try {
      await api.updateOrderStatus(id, { status });
      setOrders((o) => o.map((x) => (x.id === id ? { ...x, status } : x)));
    } catch {
      // no-op on API failure
    }
  };

  const stats = [
    { label: "Total Orders", value: `${orders.length}`, icon: "??", color: C.darkGreen },
    { label: "Revenue", value: `?${orders.reduce((s, o) => s + o.total, 0)}`, icon: "??", color: "#E65100" },
    { label: "Active Deliveries", value: `${orders.filter((o) => o.status !== "Delivered").length}`, icon: "??", color: "#1565C0" },
    { label: "Avg Rating", value: "4.9 ?", icon: "?", color: "#F57F17" },
  ];

  return (
    <div style={{ minHeight: "100vh", background: "#F0F4F0", paddingTop: 104 }}>
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "32px 5%" }}>
        <h1 style={{ fontSize: 34, color: C.darkGreen }}>Admin Dashboard</h1>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 20, marginBottom: 32 }}>
          {stats.map(s => <div key={s.label} style={{ background: C.white, borderRadius: 20, padding: "24px", border: `1px solid ${C.creamDark}` }}><div>{s.icon}</div><div style={{ fontSize: 24, fontWeight: 900, color: s.color }}>{s.value}</div><div style={{ fontSize: 12 }}>{s.label}</div></div>)}
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
          {["overview", "orders", "products"].map(t => <button key={t} onClick={() => setTab(t)}>{t}</button>)}
        </div>
        {(tab === "orders" || tab === "overview") && (
          <table style={{ width: "100%", background: C.white }}>
            <thead><tr><th>Order</th><th>Customer</th><th>Items</th><th>Total</th><th>Status</th><th>Update</th></tr></thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.id}>
                  <td>{o.id}</td><td>{o.customer}</td><td>{o.itemsText}</td><td>?{o.total}</td>
                  <td><span style={{ color: SCOL[o.status] }}>{o.status}</span></td>
                  <td><select value={o.status} onChange={e => update(o.id, e.target.value)}>{Object.keys(SCOL).map(s => <option key={s}>{s}</option>)}</select></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {tab === "products" && <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 20 }}>{products.map(p => <div key={p.id} style={{ background: C.white, borderRadius: 20, padding: 20 }}>{p.icon} {p.name} � ?{p.price}</div>)}</div>}
      </div>
    </div>
  );
}

function LoginModal({ onLogin, onClose }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handle = async () => {
    setError("");
    setLoading(true);
    try {
      const user = await api.login(form);
      if (user.role !== "admin") throw new Error("Admin login failed");
      onLogin(user);
    } catch (e) {
      setError(e.message || "Admin login failed. Use admin@dailyposhan.in / admin123");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 3000, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div onClick={onClose} style={{ position: "absolute", inset: 0, background: "rgba(27,58,31,0.6)", backdropFilter: "blur(8px)" }} />
      <div style={{ position: "relative", background: C.cream, borderRadius: 28, padding: "52px 44px", width: 400, border: `1px solid ${C.creamDark}` }}>
        <div style={{ textAlign: "center", marginBottom: 36 }}>
          <Logo size={56} />
          <h2 style={{ fontSize: 26, margin: "20px 0 4px", color: C.darkGreen }}>Admin Login</h2>
        </div>
        {[["email", "Email", "email"], ["password", "Password", "password"]].map(([key, label, type]) => (
          <div key={key} style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 12, color: C.muted, display: "block", marginBottom: 6 }}>{label}</label>
            <input type={type} value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))} style={{ width: "100%", border: `2px solid ${C.creamDark}`, borderRadius: 10, padding: "12px 14px", fontSize: 15, boxSizing: "border-box", background: C.white, color: C.darkGreen }} />
          </div>
        ))}
        <button onClick={handle} disabled={loading} style={{ width: "100%", background: C.darkGreen, color: C.yellow, border: "none", borderRadius: 12, padding: "14px", fontSize: 16, fontWeight: 700, cursor: "pointer" }}>{loading ? "Signing in�" : "Sign In ?"}</button>
        {!!error && <p style={{ textAlign: "center", fontSize: 11, color: "#C62828", marginTop: 12 }}>{error}</p>}
      </div>
    </div>
  );
}

function Footer({ setPage }) {
  return (
    <footer style={{ background: C.darkGreen, color: C.cream, padding: "64px 5% 32px" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr", gap: 60, marginBottom: 52 }}>
          <div><Logo size={52} dark /></div>
          <div>{["Home", "Menu"].map(l => <div key={l} onClick={() => setPage(l.toLowerCase())} style={{ marginBottom: 12, cursor: "pointer" }}>{l}</div>)}</div>
          <div>{["?? Mumbai, Maharashtra", "?? 9326251314"].map(l => <div key={l} style={{ marginBottom: 12 }}>{l}</div>)}</div>
        </div>
      </div>
    </footer>
  );
}

export default function App() {
  useFonts();
  const [page, setPage] = useState("home");
  const [cartOpen, setCartOpen] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [user, setUser] = useState(null);
  const [products, setProducts] = useState(PRODUCTS);
  const { cart, add, remove, update, clear, total, count } = useCart();

  useEffect(() => {
    (async () => {
      try {
        const live = await api.products();
        const merged = PRODUCTS.map((p) => {
          const m = live.find((x) => x.id === p.id);
          return m ? { ...p, name: m.name || p.name, price: m.price || p.price } : p;
        });
        setProducts(merged);
      } catch {
        setProducts(PRODUCTS);
      }
    })();
  }, []);

  const handleCheckout = () => { setCartOpen(false); setPage("checkout"); };
  const handleOrderPlaced = () => { clear(); setTimeout(() => setPage("home"), 5000); };
  const handleAdminToggle = () => { if (isAdmin) { setIsAdmin(false); setUser(null); setPage("home"); } else setShowLogin(true); };

  return (
    <div style={{ fontFamily: "'DM Sans', system-ui, sans-serif", color: C.text, minHeight: "100vh" }}>
      <Nav page={page} setPage={setPage} cartCount={count} onCartOpen={() => setCartOpen(true)} isAdmin={isAdmin} onAdminToggle={handleAdminToggle} />
      {page === "home" && (
        <>
          <Hero setPage={setPage} />
          <section style={{ padding: "80px 5%", background: C.offWhite }}>
            <div style={{ maxWidth: 1100, margin: "0 auto" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 28 }}>
                {products.map(p => <ProductCard key={p.id} product={p} onAdd={add} />)}
              </div>
            </div>
          </section>
          <Footer setPage={setPage} />
        </>
      )}
      {page === "menu" && <><MenuPage products={products} onAdd={add} /><Footer setPage={setPage} /></>}
      {page === "checkout" && cart.length > 0 && <CheckoutPage cart={cart} total={total} user={user} onOrderPlaced={handleOrderPlaced} />}
      {page === "admin" && isAdmin && <AdminDashboard products={products} />}
      {cartOpen && <CartSidebar cart={cart} onUpdate={update} onRemove={remove} total={total} onClose={() => setCartOpen(false)} onCheckout={handleCheckout} />}
      {showLogin && <LoginModal onLogin={(authUser) => { setUser(authUser); setIsAdmin(true); setShowLogin(false); setPage("admin"); }} onClose={() => setShowLogin(false)} />}
    </div>
  );
}
