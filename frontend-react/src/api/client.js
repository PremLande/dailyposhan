const BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path, options = {}) {
  try {
    const res = await fetch(`${BASE}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const data = await res.json();
    if (!res.ok) {
      const error = new Error(data.error || data.message || `API Error: ${res.status}`);
      error.status = res.status;
      throw error;
    }
    return data;
  } catch (error) {
    console.error(`[API Error] ${options.method || 'GET'} ${path}:`, error.message);
    throw error;
  }
}

export const api = {
  login: (payload) => request("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  register: (payload) => request("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  products: () => request("/products/"),
  getProduct: (id) => request(`/products/${id}/`),
  createPayment: (payload) => request("/payments/create", { method: "POST", body: JSON.stringify(payload) }),
  verifyPayment: (payload) => request("/payments/verify", { method: "POST", body: JSON.stringify(payload) }),
  createOrder: (payload) => request("/orders/", { method: "POST", body: JSON.stringify(payload) }),
  getOrder: (id) => request(`/orders/${id}/`),
  adminOrders: () => request("/admin/orders"),
  updateOrderStatus: (id, payload) => request(`/admin/orders/${id}/status`, { method: "PUT", body: JSON.stringify(payload) }),
};
