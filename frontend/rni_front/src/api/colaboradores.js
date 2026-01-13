import { api } from "./http";

export async function getColaboradores() {
  console.debug("[SERVICE] getColaboradores()");
  const response = await api.get("colaboradores/");
  return response.data;
}

