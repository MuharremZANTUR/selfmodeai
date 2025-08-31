#!/bin/bash

# SelfMode Platform Production Deployment Script
# This script deploys the application to production

set -e

echo "🚀 Starting SelfMode Platform Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking deployment requirements..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Requirements check passed ✓"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs/nginx
    mkdir -p nginx/ssl
    mkdir -p mysql/init
    
    print_status "Directories created ✓"
}

# Check environment file
check_environment() {
    print_status "Checking environment configuration..."
    
    if [ ! -f "backend/env.production" ]; then
        print_error "Production environment file not found: backend/env.production"
        print_warning "Please create this file with your production configuration"
        exit 1
    fi
    
    # Check if required environment variables are set
    source backend/env.production
    
    if [ -z "$DB_PASSWORD" ] || [ "$DB_PASSWORD" = "your_production_db_password" ]; then
        print_error "Please set a proper database password in backend/env.production"
        exit 1
    fi
    
    if [ -z "$JWT_SECRET" ] || [ "$JWT_SECRET" = "your_super_secret_production_jwt_key_change_this_immediately" ]; then
        print_error "Please set a proper JWT secret in backend/env.production"
        exit 1
    fi
    
    if [ -z "$IYZICO_API_KEY" ] || [ "$IYZICO_API_KEY" = "your_production_iyzico_api_key" ]; then
        print_warning "iyzico API key not set. Payment functionality will not work."
    fi
    
    print_status "Environment configuration check passed ✓"
}

# Build and deploy with Docker
deploy_docker() {
    print_status "Building and deploying with Docker..."
    
    # Stop existing containers
    print_status "Stopping existing containers..."
    docker-compose down --remove-orphans
    
    # Build and start services
    print_status "Building and starting services..."
    docker-compose up -d --build
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    print_status "Checking service health..."
    
    # Check backend health
    if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
        print_status "Backend is healthy ✓"
    else
        print_error "Backend health check failed"
        docker-compose logs backend
        exit 1
    fi
    
    # Check nginx health
    if curl -f http://localhost/health > /dev/null 2>&1; then
        print_status "Nginx is healthy ✓"
    else
        print_error "Nginx health check failed"
        docker-compose logs nginx
        exit 1
    fi
    
    print_status "Docker deployment completed ✓"
}

# Setup SSL certificates (Let's Encrypt)
setup_ssl() {
    print_status "Setting up SSL certificates..."
    
    if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
        print_warning "SSL certificates not found in nginx/ssl/"
        print_status "You can use Let's Encrypt to generate free SSL certificates:"
        echo ""
        echo "1. Install certbot: sudo apt-get install certbot"
        echo "2. Generate certificate: sudo certbot certonly --standalone -d yourdomain.com"
        echo "3. Copy certificates:"
        echo "   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem"
        echo "   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem"
        echo "4. Set proper permissions: sudo chown -R $USER:$USER nginx/ssl/"
        echo ""
        print_warning "Continuing without SSL (HTTP only)..."
    else
        print_status "SSL certificates found ✓"
    fi
}

# Update domain configuration
update_domain() {
    print_status "Updating domain configuration..."
    
    # Get domain from user
    read -p "Enter your production domain (e.g., yourdomain.com): " DOMAIN
    
    if [ -n "$DOMAIN" ]; then
        # Update nginx configuration
        sed -i "s/yourdomain.com/$DOMAIN/g" nginx/nginx.conf
        
        # Update environment file
        sed -i "s|FRONTEND_URL=https://yourdomain.com|FRONTEND_URL=https://$DOMAIN|g" backend/env.production
        
        print_status "Domain configuration updated to: $DOMAIN ✓"
    else
        print_warning "No domain provided, using default configuration"
    fi
}

# Main deployment function
main() {
    print_status "SelfMode Platform Production Deployment"
    echo "=============================================="
    
    check_requirements
    create_directories
    update_domain
    check_environment
    setup_ssl
    deploy_docker
    
    echo ""
    print_status "🎉 Deployment completed successfully!"
    echo ""
    echo "Your application is now running at:"
    echo "  - Frontend: http://localhost (or your domain)"
    echo "  - Backend API: http://localhost:5000"
    echo "  - Health Check: http://localhost/health"
    echo ""
    echo "To view logs:"
    echo "  - All services: docker-compose logs -f"
    echo "  - Backend only: docker-compose logs -f backend"
    echo "  - Nginx only: docker-compose logs -f nginx"
    echo ""
    echo "To stop services: docker-compose down"
    echo "To restart services: docker-compose restart"
}

# Run main function
main "$@"
