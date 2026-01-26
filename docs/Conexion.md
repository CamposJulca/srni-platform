Abrir proyecto
1. Abre Docker Desktop y espera a que esté “Running”.
2. Abre PowerShell.
3. Ve a la raíz del repo:

```powershell
cd C:\Users\JC\Desktop\srni-platform
2) Levantar infraestructura (Postgres/Mongo/Elastic/Kibana)
powershell
Copiar código
docker compose -f infra/docker-compose.yml up -d
Verifica que estén arriba:

powershell
Copiar código
docker ps
3) Levantar backend Django (rni_backend)
powershell
Copiar código
docker compose -f backend/rni_web/docker-compose.yml up -d --build
Ver logs del backend:

powershell
Copiar código
docker logs -n 120 rni_backend
Verifica que responde:

powershell
Copiar código
curl.exe -i "http://localhost:8000/api/auth/csrf/"
4) Reiniciar rápido (si algo se queda raro)
powershell
Copiar código
docker compose -f infra/docker-compose.yml restart
docker compose -f backend/rni_web/docker-compose.yml restart

continuo
docker compose -f backend/rni_web/docker-compose.yml logs -f --tail=200 

5) Apagar todo (cuando termines)
powershell
Copiar código
docker compose -f backend/rni_web/docker-compose.yml down
docker compose -f infra/docker-compose.yml down
6) Si docker-compose dice “orphan containers”
powershell
Copiar código
docker compose -f infra/docker-compose.yml up -d --remove-orphans
docker compose -f backend/rni_web/docker-compose.yml up -d --remove-orphans
7) Notas duras (para evitar pérdidas de tiempo)
El backend se conecta a Postgres por red Docker usando el host postgres_local:5432 (no depende del puerto expuesto al host).

Si ves error de “port is already allocated” en Postgres, hay otro servicio usando ese puerto del host. Cambia el puerto expuesto en infra/docker-compose.yml o apaga el servicio que lo ocupa.