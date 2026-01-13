import { useEffect, useState } from "react";
import { getColaboradores } from "../api/colaboradores";

export default function Colaboradores() {
  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.debug("[UI] Colaboradores mounted");

    async function cargar() {
      try {
        console.debug("[UI] Fetching colaboradores...");
        const data = await getColaboradores();

        console.debug("[UI] Data recibida:", data);
        setColaboradores(data);
      } catch (e) {
        console.error("[UI] Error cargando colaboradores:", e);
      } finally {
        console.debug("[UI] Loading false");
        setLoading(false);
      }
    }

    cargar();
  }, []);

  if (loading) return <p>Cargando colaboradores...</p>;

  if (!colaboradores.length)
    return <p>No hay colaboradores registrados.</p>;

  return (
    <div>
      <h1>Colaboradores</h1>
      <ul>
        {colaboradores.map((c) => (
          <li key={c.id}>
            {c.cedula} — {c.nombres} {c.apellidos} ({c.estado})
          </li>
        ))}
      </ul>
    </div>
  );
}

