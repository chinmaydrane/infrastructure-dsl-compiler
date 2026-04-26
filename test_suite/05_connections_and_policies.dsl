# Resource Connections and Policies
# Demonstrates resource relationships and policy enforcement

# Define resources
server "web_server" {
    cpu = 4
    memory = 8GB
    os = "ubuntu-22.04"
    tags = ["web", "frontend"]
}

server "app_server" {
    cpu = 8
    memory = 16GB
    os = "ubuntu-22.04"
    tags = ["app", "backend"]
}

database "primary_db" {
    engine = "mysql"
    version = "8.0"
    storage = 200GB
    instance_class = "db.r5.large"
    tags = ["database", "production"]
}

cache "redis_cache" {
    node_type = "cache.r5.large"
    num_cache_nodes = 3
    port = 6379
    automatic_failover = true
    multi_az_enabled = true
}

network "vpc_main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}

subnet "public_subnet" {
    cidr_block = "10.0.1.0/24"
    vpc = "vpc_main"
    public = true
    map_public_ip_on_launch = true
}

subnet "private_subnet" {
    cidr_block = "10.0.2.0/24"
    vpc = "vpc_main"
    public = false
    map_public_ip_on_launch = false
}

# Define connections between resources
connect "web_to_app" {
    web_server to app_server
    attributes = {
        "protocol": "http"
        "port": 8080
        "timeout": 30
    }
}

connect "app_to_db" {
    app_server to primary_db
    attributes = {
        "protocol": "mysql"
        "port": 3306
        "timeout": 10
        "ssl_enabled": true
    }
}

connect "app_to_cache" {
    app_server to redis_cache
    attributes = {
        "protocol": "redis"
        "port": 6379
        "timeout": 5
    }
}

connect "web_to_lb" {
    web_server to "internet"
    attributes = {
        "protocol": "https"
        "port": 443
    }
}

# Define security policies
policy "security_baseline" {
    policy_type = "security"
    target = "all_servers"
    rules = {
        "encryption_required": true
        "patch_management": true
        "access_logging": true
        "firewall_enabled": true
    }
}

policy "database_security" {
    policy_type = "security"
    target = "primary_db"
    rules = {
        "encryption_at_rest": true
        "encryption_in_transit": true
        "backup_encryption": true
        "audit_logging": true
        "min_password_length": 16
        "require_ssl": true
    }
}

policy "performance_monitoring" {
    policy_type = "monitoring"
    target = "all_resources"
    rules = {
        "cpu_threshold": 80
        "memory_threshold": 85
        "disk_threshold": 90
        "network_threshold": 75
        "alert_interval": 300
        "retention_days": 30
    }
}

# Define roles and permissions
role "web_admin" {
    description = "Administrators for web servers"
    permissions = ["read", "write", "execute"]
    resources = ["web_server"]
    conditions = {
        "ip_whitelist": ["10.0.0.0/8", "192.168.0.0/16"]
        "time_restrictions": "business_hours"
    }
}

role "database_admin" {
    description = "Database administrators"
    permissions = ["read", "write", "backup", "restore"]
    resources = ["primary_db"]
    conditions = {
        "require_mfa": true
        "audit_all_actions": true
    }
}

# Assign roles to users
assign role "web_admin" to user "alice"
assign role "database_admin" to user "bob"
