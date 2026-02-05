const API_BASE = "/api/sinapsis";

export async function fetchProjects() {
  const res = await fetch(`${API_BASE}/projects/`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("No se pudo cargar SINAPSIS");
  return res.json();
}
