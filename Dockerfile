# Base image
FROM docker:latest 

# Install docker-compose
RUN apk add --no-cache docker-compose

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Expose the necessary ports
EXPOSE 8000 80

# Run docker-compose
CMD ["docker-compose", "up"]
