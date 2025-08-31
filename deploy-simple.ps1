# Simple SelfMode Platform Production Deployment Script

Write-Host "🚀 Starting SelfMode Platform Production Deployment..." -ForegroundColor Green

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check Docker Compose
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker Compose not found." -ForegroundColor Red
    exit 1
}

# Create directories
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
$directories = @("logs\nginx", "nginx\ssl", "mysql\init")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Deploy with Docker
Write-Host "Starting Docker deployment..." -ForegroundColor Yellow

# Stop existing containers
Write-Host "Stopping existing containers..." -ForegroundColor Yellow
docker-compose down --remove-orphans

# Build and start services
Write-Host "Building and starting services..." -ForegroundColor Yellow
docker-compose up -d --build

# Wait for services
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check status
Write-Host "Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "🎉 Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Your application is now running at:" -ForegroundColor White
Write-Host "  - Frontend: http://localhost" -ForegroundColor White
Write-Host "  - Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "  - Health Check: http://localhost/health" -ForegroundColor White
Write-Host ""
Write-Host "To view logs: docker-compose logs -f" -ForegroundColor White
Write-Host "To stop: docker-compose down" -ForegroundColor White
