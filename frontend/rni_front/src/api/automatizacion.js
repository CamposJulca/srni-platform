// src/api/automatizacion.js
import { getCSRF } from "./auth";

// Helper para parseo estándar {ok,data,error}
async function parseJson(res) {
  const payload = await res.json().catch(() => null);
  if (!res.ok || !payload?.ok) {
    const msg = payload?.error?.message || "Error inesperado";
    throw new Error(msg);
  }
  return payload.data;
}

export async function autoHealth() {
  const res = await fetch("/api/automatizacion/health/", {
    method: "GET",
    credentials: "include",
  });
  return parseJson(res);
}

export async function autoPreviewInfo() {
  const res = await fetch("/api/automatizacion/preview/", {
    method: "GET",
    credentials: "include",
  });
  return parseJson(res);
}

// Enfoque B: convertir 1 docx a pdf preview
export async function autoPreviewConvert() {
  const csrf = await getCSRF();
  const res = await fetch("/api/automatizacion/preview/convert/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({}),
  });
  return parseJson(res);
}

export async function autoUpload({ zipFile, firmaFile }) {
  const csrf = await getCSRF();

  const form = new FormData();
  form.append("zip_file", zipFile);
  form.append("firma_file", firmaFile);

  const res = await fetch("/api/automatizacion/upload/", {
    method: "POST",
    credentials: "include",
    headers: {
      "X-CSRFToken": csrf,
    },
    body: form,
  });

  return parseJson(res);
}

export async function autoSaveFirmaPosition(payload) {
  const csrf = await getCSRF();

  const res = await fetch("/api/automatizacion/firma/position/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify(payload),
  });

  return parseJson(res);
}

export async function autoGenerate() {
  const csrf = await getCSRF();

  const res = await fetch("/api/automatizacion/generate/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    body: JSON.stringify({}),
  });

  return parseJson(res);
}

export async function autoDownload() {
  const res = await fetch("/api/automatizacion/download/", {
    method: "GET",
    credentials: "include",
  });

  if (!res.ok) {
    const payload = await res.json().catch(() => null);
    const msg = payload?.error?.message || "No se pudo descargar el ZIP";
    throw new Error(msg);
  }

  const blob = await res.blob();
  const disposition = res.headers.get("content-disposition") || "";
  const match = disposition.match(/filename="?([^"]+)"?/);
  const filename = match?.[1] || "pdf_firmados.zip";

  return { blob, filename };
}

export function autoPreviewPdfUrlBusted() {
  return `/api/automatizacion/preview/pdf/?t=${Date.now()}`;
}

export function autoFirmaPreviewUrlBusted() {
  return `/api/automatizacion/preview/firma/?t=${Date.now()}`;
}
