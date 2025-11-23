FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy application files
COPY . .

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host"]
