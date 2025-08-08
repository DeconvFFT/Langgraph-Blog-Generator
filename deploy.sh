#!/bin/bash

# Blog Generator Deployment Script
# This script helps deploy the blog generator application

set -e

echo "🚀 Blog Generator Deployment Script"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# Blog Generator Environment Variables
GROQ_API_KEY=your_groq_api_key_here
LANGSMITH_API_KEY=your_langsmith_key_here

# API Configuration
API_BASE_URL=http://localhost:8000
PORT=8000
HOST=0.0.0.0
EOF
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "   Required: GROQ_API_KEY"
    echo "   Optional: LANGSMITH_API_KEY"
    exit 1
fi

# Load environment variables
source .env

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_groq_api_key_here" ]; then
    echo "❌ GROQ_API_KEY is not set in .env file."
    echo "   Please add your Groq API key to the .env file."
    exit 1
fi

echo "✅ Environment variables loaded successfully"

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."

# Check API service
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API service is running at http://localhost:8000"
else
    echo "❌ API service is not responding"
    echo "   Check logs with: docker-compose logs blog-generator-api"
fi

# Check UI service
if curl -f http://localhost:7860 > /dev/null 2>&1; then
    echo "✅ UI service is running at http://localhost:7860"
else
    echo "❌ UI service is not responding"
    echo "   Check logs with: docker-compose logs blog-generator-ui"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📱 Access your application:"
echo "   - Web UI: http://localhost:7860"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Update and redeploy: ./deploy.sh"
