const API_BASE = "http://localhost:8000/api/sinapsis";

export async function fetchProjects() {
  const res = await fetch(`${API_BASE}/projects/`);
  if (!res.ok) {
    throw new Error("No se pudo cargar SINAPSIS");
  }
  return res.json();
}
