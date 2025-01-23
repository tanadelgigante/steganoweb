FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies including dev dependencies
RUN npm install

# Copy source code
COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 3000

# Run in development mode
ENV NODE_ENV=development

ENTRYPOINT ["/entrypoint.sh"]
CMD ["npm", "start"]
