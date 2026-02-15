#!/bin/bash

# AutoBlogger Production Deployment Script
set -e

echo "🚀 AutoBlogger Production Deployment"
echo "====================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create .env file with required environment variables."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting AutoBlogger..."
docker-compose up -d

echo "⏳ Waiting for application to start..."
sleep 10

# Health check
echo "🏥 Performing health check..."
if curl -f http://localhost:5001/health > /dev/null 2>&1; then
    echo "✅ AutoBlogger is running successfully!"
    echo "🌐 Access the application at: http://localhost:5001"
    echo "📊 Health check: http://localhost:5001/health"
    echo "🔗 API Base: http://localhost:5001/api"
else
    echo "❌ Health check failed. Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "🎉 AutoBlogger deployment completed successfully!"
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"

