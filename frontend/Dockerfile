FROM node:14-alpine
WORKDIR /app
COPY package.json .
ENV NODE_PATH=/app/node_modules
RUN npm install --verbose
COPY . .