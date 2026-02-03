export async function getKpis(limit = 10) {
  const res = await fetch(`/api/dashboard/kpis/?limit=${limit}`, {
    method: "GET",
    credentials: "include",
  });

  const payload = await res.json();

  if (!res.ok || !payload.ok) {
    const msg = payload?.error?.message || "No se pudo cargar KPIs";
    throw new Error(msg);
  }

  return payload.data;
}
