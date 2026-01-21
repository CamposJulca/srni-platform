# =========================
# Stage 1 – Build
# =========================
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# =========================
# Stage 2 – Runtime
# =========================
FROM nginx:alpine

# El build de Vite queda en /app/dist
COPY --from=build /app/dist /usr/share/nginx/html

# Config mínima para SPA
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
