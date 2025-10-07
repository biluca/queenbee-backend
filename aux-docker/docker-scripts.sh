#!/bin/bash

# Bee Management System - Docker Helper Scripts

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to start the application
start_app() {
    print_status "Starting Bee Management System..."
    check_docker
    
    docker-compose up --build -d
    
    print_success "Application started successfully!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:8000/api"
    print_status "Django Admin: http://localhost:8000/admin"
    print_status "Default admin credentials: admin/admin123"
}

# Function to stop the application
stop_app() {
    print_status "Stopping Bee Management System..."
    check_docker
    
    docker-compose down
    
    print_success "Application stopped successfully!"
}

# Function to restart the application
restart_app() {
    print_status "Restarting Bee Management System..."
    stop_app
    start_app
}

# Function to view logs
view_logs() {
    local service=${1:-""}
    
    if [ -n "$service" ]; then
        print_status "Viewing logs for $service..."
        docker-compose logs -f "$service"
    else
        print_status "Viewing logs for all services..."
        docker-compose logs -f
    fi
}

# Function to reset everything
reset_all() {
    print_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Resetting everything..."
        check_docker
        
        docker-compose down -v --rmi all
        docker system prune -f
        
        print_success "Reset completed successfully!"
    else
        print_status "Reset cancelled."
    fi
}

# Function to create superuser
create_superuser() {
    print_status "Creating Django superuser..."
    check_docker
    
    docker-compose exec backend python manage.py createsuperuser
    
    print_success "Superuser created successfully!"
}

# Function to run migrations
run_migrations() {
    print_status "Running Django migrations..."
    check_docker
    
    docker-compose exec backend python manage.py migrate
    
    print_success "Migrations completed successfully!"
}

# Function to collect static files
collect_static() {
    print_status "Collecting static files..."
    check_docker
    
    docker-compose exec backend python manage.py collectstatic --noinput
    
    print_success "Static files collected successfully!"
}

# Function to show status
show_status() {
    print_status "Bee Management System Status:"
    echo ""
    docker-compose ps
    echo ""
    print_status "Service URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000/api"
    echo "  Django Admin: http://localhost:8000/admin"
    echo "  Database: localhost:5432"
}

# Function to show help
show_help() {
    echo "Bee Management System - Docker Helper Scripts"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start           Start the application"
    echo "  stop            Stop the application"
    echo "  restart         Restart the application"
    echo "  logs [service]  View logs (optionally for specific service)"
    echo "  status          Show application status"
    echo "  reset           Reset everything (removes all data)"
    echo "  superuser       Create Django superuser"
    echo "  migrate         Run Django migrations"
    echo "  static          Collect static files"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start the application"
    echo "  $0 logs backend            # View backend logs"
    echo "  $0 logs                    # View all logs"
    echo "  $0 reset                   # Reset everything"
}

# Main script logic
case "${1:-help}" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    logs)
        view_logs "$2"
        ;;
    status)
        show_status
        ;;
    reset)
        reset_all
        ;;
    superuser)
        create_superuser
        ;;
    migrate)
        run_migrations
        ;;
    static)
        collect_static
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
