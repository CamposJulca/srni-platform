// Colaboradores API (Lectura: list + filtros + paginación)
// Endpoint: GET /api/colaboradores/?page=1&page_size=20&q=texto&estado=ACTIVO
// Respuesta:
// { ok:true, data:{ items:[], pagination:{page,page_size,total,total_pages}, filters:{q,estado} }, error:null }

export async function getColaboradores({
  page = 1,
  page_size = 20,
  q = "",
  estado = "",
} = {}) {
  const params = new URLSearchParams();
  params.set("page", String(page));
  params.set("page_size", String(page_size));
  if (q && q.trim()) params.set("q", q.trim());
  if (estado && estado.trim()) params.set("estado", estado.trim());

  const res = await fetch(`/api/colaboradores/?${params.toString()}`, {
    method: "GET",
    credentials: "include",
  });

  const json = await res.json().catch(() => null);

  if (!res.ok || !json?.ok) {
    const msg =
      json?.error?.message ||
      `No se pudieron cargar los colaboradores (HTTP ${res.status})`;
    throw new Error(msg);
  }

  // data = { items, pagination, filters }
  return json.data;
}
