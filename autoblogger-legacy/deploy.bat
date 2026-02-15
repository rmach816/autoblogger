@echo off
REM AutoBlogger Production Deployment Script for Windows

echo 🚀 AutoBlogger Production Deployment
echo =====================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found. Please create .env file with required environment variables.
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Build and start the application
echo 🔨 Building Docker image...
docker-compose build

echo 🚀 Starting AutoBlogger...
docker-compose up -d

echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Health check
echo 🏥 Performing health check...
curl -f http://localhost:5001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ AutoBlogger is running successfully!
    echo 🌐 Access the application at: http://localhost:5001
    echo 📊 Health check: http://localhost:5001/health
    echo 🔗 API Base: http://localhost:5001/api
) else (
    echo ❌ Health check failed. Check logs with: docker-compose logs
    exit /b 1
)

echo.
echo 🎉 AutoBlogger deployment completed successfully!
echo 📝 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down

