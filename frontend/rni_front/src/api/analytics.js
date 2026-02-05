// src/api/analytics.js
import { getCSRF } from "./auth";

async function parseJson(res) {
  const payload = await res.json().catch(() => null);
  if (!res.ok || !payload?.ok) {
    const msg = payload?.error?.message || "Error inesperado";
    throw new Error(msg);
  }
  return payload.data;
}

export async function analyticsHealth() {
  const res = await fetch("/api/analytics/health/", {
    method: "GET",
    credentials: "include",
  });
  return parseJson(res);
}

export async function analyticsExecuteSQL(sql) {
  const csrf = await getCSRF();
  const res = await fetch("/api/analytics/sql/execute/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({ sql }),
  });
  return parseJson(res);
}
