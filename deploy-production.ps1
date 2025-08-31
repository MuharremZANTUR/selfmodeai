# SelfMode Platform Production Deployment Script (PowerShell)
# This script deploys the application to production on Windows

param(
    [string]$Domain = "",
    [switch]$SkipSSL = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting SelfMode Platform Production Deployment..." -ForegroundColor Green

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if required tools are installed
function Test-Requirements {
    Write-Status "Checking deployment requirements..."
    
    # Check Docker
    try {
        $dockerVersion = docker --version
        Write-Status "Docker found: $dockerVersion"
    }
    catch {
        Write-Error "Docker is not installed or not in PATH. Please install Docker Desktop first."
        exit 1
    }
    
    # Check Docker Compose
    try {
        $composeVersion = docker-compose --version
        Write-Status "Docker Compose found: $composeVersion"
    }
    catch {
        Write-Error "Docker Compose is not installed or not in PATH. Please install Docker Compose first."
        exit 1
    }
    
    Write-Status "Requirements check passed ✓"
}

# Create necessary directories
function New-Directories {
    Write-Status "Creating necessary directories..."
    
    $directories = @(
        "logs\nginx",
        "nginx\ssl",
        "mysql\init"
    )
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Status "Created directory: $dir"
        }
    }
    
    Write-Status "Directories created ✓"
}

# Check environment file
function Test-Environment {
    Write-Status "Checking environment configuration..."
    
    if (!(Test-Path "backend\env.production")) {
        Write-Error "Production environment file not found: backend\env.production"
        Write-Warning "Please create this file with your production configuration"
        exit 1
    }
    
    # Read environment file and check required variables
    $envContent = Get-Content "backend\env.production" -Raw
    
    if ($envContent -match "DB_PASSWORD=your_production_db_password") {
        Write-Error "Please set a proper database password in backend\env.production"
        exit 1
    }
    
    if ($envContent -match "JWT_SECRET=your_super_secret_production_jwt_key_change_this_immediately") {
        Write-Error "Please set a proper JWT secret in backend\env.production"
        exit 1
    }
    
    if ($envContent -match "IYZICO_API_KEY=your_production_iyzico_api_key") {
        Write-Warning "iyzico API key not set. Payment functionality will not work."
    }
    
    Write-Status "Environment configuration check passed ✓"
}

# Update domain configuration
function Update-Domain {
    param([string]$Domain)
    
    Write-Status "Updating domain configuration..."
    
    if ([string]::IsNullOrEmpty($Domain)) {
        $Domain = Read-Host "Enter your production domain (e.g., yourdomain.com)"
    }
    
    if (![string]::IsNullOrEmpty($Domain)) {
        # Update nginx configuration
        $nginxContent = Get-Content "nginx\nginx.conf" -Raw
        $nginxContent = $nginxContent -replace "yourdomain\.com", $Domain
        Set-Content "nginx\nginx.conf" $nginxContent
        
        # Update environment file
        $envContent = Get-Content "backend\env.production" -Raw
        $envContent = $envContent -replace "FRONTEND_URL=https://yourdomain\.com", "FRONTEND_URL=https://$Domain"
        Set-Content "backend\env.production" $envContent
        
        Write-Status "Domain configuration updated to: $Domain ✓"
    }
    else {
        Write-Warning "No domain provided, using default configuration"
    }
}

# Setup SSL certificates
function Setup-SSL {
    param([bool]$SkipSSL)
    
    Write-Status "Setting up SSL certificates..."
    
    if ($SkipSSL) {
        Write-Warning "SSL setup skipped as requested"
        return
    }
    
    if (!(Test-Path "nginx\ssl\cert.pem") -or !(Test-Path "nginx\ssl\key.pem")) {
        Write-Warning "SSL certificates not found in nginx\ssl\"
        Write-Status "You can use Let's Encrypt to generate free SSL certificates:"
        Write-Host ""
        Write-Host "1. Install certbot: sudo apt-get install certbot"
        Write-Host "2. Generate certificate: sudo certbot certonly --standalone -d yourdomain.com"
        Write-Host "3. Copy certificates:"
        Write-Host "   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem"
        Write-Host "   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem"
        Write-Host "4. Set proper permissions: sudo chown -R `$USER:`$USER nginx/ssl/"
        Write-Host ""
        Write-Warning "Continuing without SSL (HTTP only)..."
    }
    else {
        Write-Status "SSL certificates found ✓"
    }
}

# Build and deploy with Docker
function Deploy-Docker {
    Write-Status "Building and deploying with Docker..."
    
    # Stop existing containers
    Write-Status "Stopping existing containers..."
    docker-compose down --remove-orphans
    
    # Build and start services
    Write-Status "Building and starting services..."
    docker-compose up -d --build
    
    # Wait for services to be ready
    Write-Status "Waiting for services to be ready..."
    Start-Sleep -Seconds 30
    
    # Check service health
    Write-Status "Checking service health..."
    
    # Check backend health
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Status "Backend is healthy ✓"
        }
        else {
            throw "Backend returned status code: $($response.StatusCode)"
        }
    }
    catch {
        Write-Error "Backend health check failed: $_"
        docker-compose logs backend
        exit 1
    }
    
    # Check nginx health
    try {
        $response = Invoke-WebRequest -Uri "http://localhost/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Status "Nginx is healthy ✓"
        }
        else {
            throw "Nginx health check failed: $_"
        }
    }
    catch {
        Write-Error "Nginx health check failed: $_"
        docker-compose logs nginx
        exit 1
    }
    
    Write-Status "Docker deployment completed ✓"
}

# Main deployment function
function Main {
    Write-Host "SelfMode Platform Production Deployment" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    
    Test-Requirements
    New-Directories
    Update-Domain -Domain $Domain
    Test-Environment
    Setup-SSL -SkipSSL $SkipSSL
    Deploy-Docker
    
    Write-Host ""
    Write-Status "🎉 Deployment completed successfully!"
    Write-Host ""
    Write-Host "Your application is now running at:" -ForegroundColor White
    Write-Host "  - Frontend: http://localhost (or your domain)" -ForegroundColor White
    Write-Host "  - Backend API: http://localhost:5000" -ForegroundColor White
    Write-Host "  - Health Check: http://localhost/health" -ForegroundColor White
    Write-Host ""
    Write-Host "To view logs:" -ForegroundColor White
    Write-Host "  - All services: docker-compose logs -f" -ForegroundColor White
    Write-Host "  - Backend only: docker-compose logs -f backend" -ForegroundColor White
    Write-Host "  - Nginx only: docker-compose logs -f nginx" -ForegroundColor White
    Write-Host ""
    Write-Host "To stop services: docker-compose down" -ForegroundColor White
    Write-Host "To restart services: docker-compose restart" -ForegroundColor White
}

# Run main function
Main
