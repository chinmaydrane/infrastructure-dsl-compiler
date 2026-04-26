# Complex Expressions and Data Types
# Demonstrates various expression types and literals

server "app_server" {
    cpu = 4
    memory = 8GB
    os = "ubuntu-22.04"
    tags = ["web", "production", "frontend"]
    
    # Complex object literal
    metadata = {
        "environment": "production"
        "owner": "devops-team"
        "cost_center": "engineering"
        "backup_required": true
    }
    
    # Array literals with different types
    security_groups = ["sg-web", "sg-ssh", "sg-rds"]
    subnets = ["subnet-private-1", "subnet-private-2"]
    
    # Numeric expressions
    disk_size = 500GB
    max_connections = 1000
    timeout = 30
}

# Complex resource with nested structures
load_balancer "main_lb" {
    algorithm = "round_robin"
    listeners = [
        {
            "port": 443
            "protocol": "https"
            "certificate_arn": "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012"
        },
        {
            "port": 80
            "protocol": "http"
            "redirect_to_https": true
        }
    ]
    
    target_servers = ["app_server"]
    health_check = {
        "path": "/health"
        "interval": 30
        "timeout": 5
        "healthy_threshold": 2
        "unhealthy_threshold": 3
    }
}
