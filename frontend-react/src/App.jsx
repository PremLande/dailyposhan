import { useState, useEffect } from "react";
import { api } from "./api/client";

const PRODUCTS = [
  {
    id: 1,
    name: "Chatori Jar",
    tagline: "Chatpata, desi twist with a healthy punch.",
    desc: "A crunchy jar salad with chaat spices, sev, fresh veggies and tangy chutney.",
    price: 250,
    cal: 270,
    protein: "8g",
    type: "Jar Salad",
  },
  {
    id: 2,
    name: "Muscle Fuel Jar",
    tagline: "High-protein, plant-forward bowl for strength & recovery.",
    desc: "Power bowl with paneer, sprouts, nuts and greens — fully plant-forward protein, no meat.",
    price: 250,
    cal: 320,
    protein: "22g",
    type: "Jar Salad",
  },
  {
    id: 3,
    name: "Glow & Flow Jar",
    tagline: "Women special salad for glow, balance & energy.",
    desc: "Radiance jar made with berries, avocado, seeds and greens for natural glow.",
    price: 250,
    cal: 280,
    protein: "10g",
    type: "Jar Salad",
  },
  {
    id: 4,
    name: "Extra Dips",
    tagline: "Add-on dressings to complete every jar.",
    desc: "Choose from mint chutney, creamy tahini, or spicy schezwan dip.",
    price: 25,
    cal: 35,
    protein: "0g",
    type: "Add-on",
  },
];

function useCart() {
  const [cart, setCart] = useState([]);

  const add = (product) => {
    setCart((current) => {
      const existing = current.find((item) => item.id === product.id);
      if (existing) {
        return current.map((item) =>
          item.id === product.id ? { ...item, qty: item.qty + 1 } : item
        );
      }
      return [...current, { ...product, qty: 1 }];
    });
  };

  const update = (id, qty) =>
    setCart((current) =>
      current
        .map((item) =>
          item.id === id ? { ...item, qty: Math.max(1, qty) } : item
        )
        .filter((item) => item.qty > 0)
    );

  const remove = (id) => setCart((current) => current.filter((item) => item.id !== id));

  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  const count = cart.reduce((sum, item) => sum + item.qty, 0);

  return { cart, add, update, remove, total, count };
}

function Header({ count, onCartOpen }) {
  return (
    <header className="site-header">
      <div className="brand">
        <span className="brand-mark">🍃</span>
        <div>
          <div className="brand-name">Daily Poshan</div>
          <div className="brand-tag">Nutritious. Fresh. Wholesome.</div>
        </div>
      </div>
      <button type="button" className="cart-button" onClick={onCartOpen}>
        Cart {count > 0 ? `(${count})` : ""}
      </button>
    </header>
  );
}

function Hero({ onBrowse }) {
  return (
    <section className="hero-section">
      <div className="hero-copy">
        <div className="hero-banner">Launch Day! Flat 20% off on all orders for a week</div>
        <span className="eyebrow">Daily Poshan Jar Salads</span>
        <h1>Your daily dose of poshan, packed fresh in every jar.</h1>
        <p>100% pure veg and vegan-friendly jar salads made with fresh greens, seeds, and clean ingredients.</p>
        <div className="hero-actions">
          <button type="button" className="primary-button" onClick={onBrowse}>Browse Menu</button>
          <a className="secondary-link" href="https://wa.me/919326251314" target="_blank" rel="noreferrer">Order on WhatsApp</a>
        </div>
        <div className="hero-logo-strip">
          <div className="logo-badge">
            <span className="logo-icon">🌿</span>
            <span>Pure Veg</span>
          </div>
          <div className="logo-badge">
            <span className="logo-icon">🥗</span>
            <span>Vegan-friendly</span>
          </div>
          <div className="logo-badge">
            <span className="logo-icon">✔️</span>
            <span>100% fresh ingredients</span>
          </div>
        </div>
      </div>
      <div className="hero-tray">
        <div className="hero-chip">₹250 per jar</div>
        <div className="hero-chip">Freshly made</div>
        <div className="hero-chip">No preservatives</div>
      </div>
    </section>
  );
}

function ProductCard({ product, onAdd }) {
  const badge = product.tag || product.type || "Signature";

  return (
    <article className="product-card">
      <div className="product-card-main">
        <div>
          <div className="product-badge">{badge}</div>
          <h2>{product.name}</h2>
          <p className="product-tagline">{product.tagline}</p>
          <p className="product-desc">{product.desc}</p>
        </div>
        <div className="product-price-block">
          <strong className="product-price">₹{product.price}</strong>
          <button type="button" className="product-action" onClick={() => onAdd(product)}>ADD</button>
        </div>
      </div>
      <div className="product-footer">
        <span>{product.cal} cal</span>
        <span>{product.protein} protein</span>
      </div>
    </article>
  );
}

function CartDrawer({ open, cart, total, onClose, onUpdate, onRemove }) {
  if (!open) return null;

  return (
    <div className="cart-drawer-overlay">
      <div className="cart-drawer">
        <div className="cart-header">
          <h2>Your cart</h2>
          <button type="button" className="close-button" onClick={onClose}>&times;</button>
        </div>
        <div className="cart-list">
          {cart.length === 0 && <p className="empty-cart">Your cart is empty.</p>}
          {cart.map((item) => (
            <div key={item.id} className="cart-item">
              <div>
                <div className="cart-item-name">{item.name}</div>
                <div className="cart-item-meta">₹{item.price} × {item.qty}</div>
              </div>
              <div className="cart-actions">
                <button type="button" onClick={() => onUpdate(item.id, item.qty - 1)}>-</button>
                <span>{item.qty}</span>
                <button type="button" onClick={() => onUpdate(item.id, item.qty + 1)}>+</button>
                <button type="button" className="remove-button" onClick={() => onRemove(item.id)}>Remove</button>
              </div>
            </div>
          ))}
        </div>
        <div className="cart-summary">
          <div className="summary-row">
            <span>Total</span>
            <strong>₹{total}</strong>
          </div>
          <a className="checkout-button" href="https://wa.me/919326251314?text=I%20want%20to%20order%20jar%20salads" target="_blank" rel="noreferrer">
            Order on WhatsApp
          </a>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [products, setProducts] = useState(PRODUCTS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [cartOpen, setCartOpen] = useState(false);
  const { cart, add, update, remove, total, count } = useCart();

  useEffect(() => {
    async function loadProducts() {
      try {
        setLoading(true);
        const apiProducts = await api.products();
        if (Array.isArray(apiProducts) && apiProducts.length > 0) {
          setProducts(apiProducts.map((item, index) => ({
            id: item.id || index + 1,
            name: item.name || PRODUCTS[index]?.name || `Salad ${index + 1}`,
            tagline: item.tagline || item.description || "Fresh and tasty.",
            desc: item.description || PRODUCTS[index]?.desc || "A tasty jar salad made with wholesome ingredients.",
            price: item.price || PRODUCTS[index]?.price || 249,
            cal: item.calories || PRODUCTS[index]?.cal || 320,
            protein: item.protein || PRODUCTS[index]?.protein || "14g",
            tag: item.tag || PRODUCTS[index]?.type || "Signature",
          })));
        }
        setError("");
      } catch (err) {
        console.warn("Product fetch failed, using fallback data.", err);
        setError("Unable to load live menu. Showing featured items.");
        setProducts(PRODUCTS);
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  const handleBrowse = () => {
    document.getElementById("menu-section")?.scrollIntoView({ behavior: "smooth" });
  };

  const handleCartOpen = () => {
    if (window.innerWidth <= 760) {
      setCartOpen(true);
      return;
    }
    document.getElementById("order-summary")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="app">
      <Header count={count} onCartOpen={handleCartOpen} />
      <main>
        <Hero onBrowse={handleBrowse} />
        <section className="section" id="menu-section">
          <div className="section-header">
            <div>
              <p className="eyebrow">Today's Specials</p>
              <h2>Choose your nutrient-rich jar for energy, glow, or digestion.</h2>
            </div>
            <p className="section-note">100% pure veg & vegan-friendly jars with fresh ingredients, balanced macros, and simple WhatsApp ordering.</p>
          </div>

          <div className="menu-layout">
            <div className="menu-list">
              <div className="restaurant-card">
                <div className="restaurant-meta">
                  <div>
                    <h3>Daily Poshan</h3>
                    <p>Freshly prepared jar salads with clean ingredients and bold flavours.</p>
                  </div>
                  <span className="rating-pill">4.9 ★</span>
                </div>
                <div className="restaurant-stats">
                  <span>₹250 per jar</span>
                  <span>Launch offer</span>
                  <span>100% pure veg & vegan-friendly</span>
                </div>
              </div>

              {loading ? (
                <div className="status-message">Loading menu...</div>
              ) : (
                <div className="product-grid">
                  {products.map((product) => (
                    <ProductCard key={product.id} product={product} onAdd={add} />
                  ))}
                </div>
              )}

              {error && <div className="status-message error">{error}</div>}
            </div>

            <aside className="order-summary" id="order-summary">
              <div className="summary-head">
                <div>
                  <p className="eyebrow">Order summary</p>
                  <h3>{count ? `${count} item${count > 1 ? 's' : ''}` : 'No items yet'}</h3>
                </div>
                <span className="summary-tag">Your jar order</span>
              </div>

              <div className="summary-body">
                {cart.length === 0 ? (
                  <p className="empty-cart">Add jars to your cart to see the totals here.</p>
                ) : (
                  cart.map((item) => (
                    <div key={item.id} className="summary-item">
                      <div>
                        <div className="summary-item-name">{item.name}</div>
                        <div className="summary-item-meta">₹{item.price} × {item.qty}</div>
                      </div>
                      <div className="summary-item-actions">
                        <button type="button" onClick={() => update(item.id, item.qty - 1)}>-</button>
                        <span>{item.qty}</span>
                        <button type="button" onClick={() => update(item.id, item.qty + 1)}>+</button>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="summary-foot">
                <div className="summary-row">
                  <span>Subtotal</span>
                  <strong>₹{total}</strong>
                </div>
                <div className="summary-row small-row">
                  <span>Delivery</span>
                  <span>Free</span>
                </div>
                <div className="summary-row total-row">
                  <span>Total</span>
                  <strong>₹{total}</strong>
                </div>
                <a className="checkout-button" href="https://wa.me/919326251314?text=I%20want%20to%20order%20jar%20salads" target="_blank" rel="noreferrer">
                  Order on WhatsApp
                </a>
              </div>
            </aside>
          </div>
        </section>
      </main>
      <footer className="site-footer">
        <div>
          <strong>Daily Poshan</strong>
          <p>Simple, healthy meals delivered with a clean aesthetic.</p>
        </div>
        <a href="https://wa.me/919326251314" target="_blank" rel="noreferrer">Chat on WhatsApp</a>
      </footer>
      <CartDrawer
        open={cartOpen}
        cart={cart}
        total={total}
        onClose={() => setCartOpen(false)}
        onUpdate={update}
        onRemove={remove}
      />
    </div>
  );
}
