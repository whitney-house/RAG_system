
FROM node:22 as build
WORKDIR /app


COPY package.json package-lock.json ./


RUN npm install


COPY . .

RUN npm run build

# Nginx 
FROM nginx:alpine
# new
WORKDIR /etc/nginx

COPY --from=build /app/dist /usr/share/nginx/html


#COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.template /etc/nginx/nginx.template

CMD envsubst '$VITE_BACKEND_URL' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf && \
    nginx -g 'daemon off;'

EXPOSE 80
