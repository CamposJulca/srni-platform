// src/api/nlquery.js
import { getCSRF } from "./auth";

async function parseJson(res) {
  const payload = await res.json().catch(() => null);
  if (!res.ok || !payload?.ok) {
    const msg = payload?.error?.message || "Error inesperado";
    throw new Error(msg);
  }
  return payload.data;
}

export async function nlqHealth() {
  const res = await fetch("/api/nlquery/health/", {
    method: "GET",
    credentials: "include",
  });
  return parseJson(res);
}

export async function nlqSchema() {
  const res = await fetch("/api/nlquery/schema/", {
    method: "GET",
    credentials: "include",
  });
  return parseJson(res);
}

export async function nlqRun({ sql, question }) {
  const csrf = await getCSRF();
  const res = await fetch("/api/nlquery/run/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({ ...(sql ? { sql } : {}), ...(question ? { question } : {}) }),
  });
  return parseJson(res);
}

export async function nlqGenerateSQL(question) {
  const csrf = await getCSRF();
  const res = await fetch("/api/nlquery/generate-sql/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({ question }),
  });
  return parseJson(res);
}
