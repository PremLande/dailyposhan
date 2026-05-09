const BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

export const api = {
  login: (payload) => request("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  register: (payload) => request("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  products: () => request("/products/"),
  createPayment: (payload) => request("/payments/create", { method: "POST", body: JSON.stringify(payload) }),
  verifyPayment: (payload) => request("/payments/verify", { method: "POST", body: JSON.stringify(payload) }),
  createOrder: (payload) => request("/orders/", { method: "POST", body: JSON.stringify(payload) }),
  adminOrders: () => request("/admin/orders"),
  updateOrderStatus: (id, payload) => request(`/admin/orders/${id}/status`, { method: "PUT", body: JSON.stringify(payload) }),
};
