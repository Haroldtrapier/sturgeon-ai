FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy app files
COPY . .

# Build app
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
