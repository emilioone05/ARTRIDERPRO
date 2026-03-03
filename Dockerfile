# Etapa 1: Compilación
FROM node:20-alpine as build
WORKDIR /app

# 1. Habilitamos corepack (la herramienta oficial de Node para manejar pnpm/yarn)
RUN corepack enable && corepack prepare pnpm@latest --activate

# 2. Copiamos el package.json y el pnpm-lock.yaml (¡MUY IMPORTANTE!)
COPY package.json pnpm-lock.yaml ./

# 3. Instalamos las dependencias usando pnpm
# --frozen-lockfile asegura que instale exactamente lo que dice el lock sin modificarlo
RUN pnpm install --frozen-lockfile

# Copiamos el resto del código fuente
COPY . .

# Construimos la aplicación de Angular
RUN pnpm run build --configuration=production

# Etapa 2: Servidor de producción (Esto no cambia)
FROM nginx:alpine
# Verifica que la ruta /dist/artrider/browser coincida con lo que genera tu Angular 17+
COPY --from=build /app/dist/artrider/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
