const API = import.meta.env.VITE_API_URL;

// ===============================
// Cookies helpers
// ===============================
export function getCookie(name) {
  const match = document.cookie.match(
    new RegExp("(^| )" + name + "=([^;]+)")
  );
  return match ? decodeURIComponent(match[2]) : null;
}

// ===============================
// CSRF
// ===============================
export async function getCSRF() {
  const res = await fetch(`${API}/api/auth/csrf/`, {
    method: "GET",
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("No se pudo obtener CSRF");
  }

  const token = getCookie("csrftoken");
  if (!token) {
    throw new Error("CSRF token no encontrado");
  }

  return token;
}

// ===============================
// LOGIN
// ===============================
export async function login(username, password) {
  const csrf = await getCSRF();

  const res = await fetch(`${API}/api/auth/login/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    throw new Error("Error HTTP en login");
  }

  const payload = await res.json();

  if (!payload.ok) {
    throw new Error(payload?.error?.message || "Credenciales inválidas");
  }

  await getCSRF(); // refresca token

  return payload.data;
}

// ===============================
// ME
// ===============================
export async function me() {
  const res = await fetch(`${API}/api/auth/me/`, {
    method: "GET",
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("No autenticado");
  }

  const payload = await res.json();

  if (!payload.ok) {
    throw new Error("No autenticado");
  }

  return payload.data;
}

// ===============================
// LOGOUT
// ===============================
export async function logout() {
  const csrf = await getCSRF();

  const res = await fetch(`${API}/api/auth/logout/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({}),
  });

  if (!res.ok) {
    throw new Error("Error HTTP en logout");
  }

  const payload = await res.json();

  if (!payload.ok) {
    throw new Error("Error al cerrar sesión");
  }

  return payload.data;
}
