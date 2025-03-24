
FROM node:22 as build
WORKDIR /app


COPY package.json package-lock.json ./


RUN npm install


COPY . .

RUN npm run build

# Nginx 
FROM nginx:alpine


COPY --from=build /app/dist /usr/share/nginx/html


COPY nginx.conf /etc/nginx/nginx.conf


EXPOSE 80


CMD ["nginx", "-g", "daemon off;"]