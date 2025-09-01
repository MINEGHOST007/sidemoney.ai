# Use Node.js 18 image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files and entrypoint
COPY package.json pnpm-lock.yaml ./
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]