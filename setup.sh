#!/bin/bash

# AJLA Project Setup Script

echo "🚀 AJLA Concierge Platform - Setup Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://www.docker.com/get-started"
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Start PostgreSQL and pgAdmin
echo "📦 Starting PostgreSQL container..."
docker-compose up -d postgres pgadmin

echo ""
sleep 5

# Check if database is ready
docker-compose exec -T postgres pg_isready -U ajla_user -d ajla_db > /dev/null 2>&1
while [ $? -ne 0 ]; do
    echo "⏳ Still waiting for PostgreSQL..."
    sleep 2
    docker-compose exec -T postgres pg_isready -U ajla_user -d ajla_db > /dev/null 2>&1
done

echo "✅ PostgreSQL is ready!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Update it with your settings if needed."
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📊 Database Info:"
echo "   Host: localhost"
echo "   Port: 5432"
echo "   User: ajla_user"
echo "   Password: ajla_password"
echo "   Database: ajla_db"
echo ""
echo "🔍 pgAdmin Access:"
echo "   URL: http://localhost:5050"
echo "   Email: admin@ajla.com"
echo "   Password: admin"
echo ""
echo "🚀 To start the FastAPI server:"
echo "   source .venv/bin/activate"
echo "   python main.py"
echo ""
echo "📚 API Documentation:"
echo "   URL: http://localhost:8000/docs"
echo ""
