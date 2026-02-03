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
  await fetch("/api/auth/csrf/", {
    method: "GET",
    credentials: "include",
  });

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
  // 1️⃣ CSRF antes del login
  let csrf = await getCSRF();

  const res = await fetch("/api/auth/login/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });

  const payload = await res.json();

  if (!res.ok || !payload.ok) {
    throw new Error("Usuario o contraseña incorrectos");
  }

  // 2️⃣ CSRF rota después del login → refrescamos
  await getCSRF();

  return payload.data; // { authenticated: true, id, username, email }
}

// ===============================
// ME (validar sesión)
// ===============================
export async function me() {
  const res = await fetch("/api/auth/me/", {
    method: "GET",
    credentials: "include",
  });

  const payload = await res.json();

  if (!res.ok || !payload.ok) {
    throw new Error("No autenticado");
  }

  return payload.data;
}

// ===============================
// LOGOUT
// ===============================
export async function logout() {
  const csrf = await getCSRF();

  const res = await fetch("/api/auth/logout/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({}),
  });

  const payload = await res.json();

  if (!res.ok || !payload.ok) {
    throw new Error("Error al cerrar sesión");
  }

  return payload.data;
}
