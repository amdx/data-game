FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Build the Vue.js application
RUN npm run build

# Use the official Nginx image to serve the built application
FROM nginx:1.27-bookworm
COPY --from=builder /app/dist /usr/share/nginx/html/tablet
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
