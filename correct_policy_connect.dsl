# CORRECT Policy and Connect Examples
# Using the right syntax that actually works in your DSL

# =================================================================
# BASIC RESOURCES (Required for connections and policies)
# =================================================================

server "web_server" {
    cpu = 2
    memory = "4GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "app_server" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu-20.04"
    enabled = true
}

database "primary_db" {
    engine = "mysql"
    version = "8.0"
    storage = "100GB"
    instance_class = "db.t3.medium"
    backup_retention = 7
}

cache "redis_cache" {
    engine = "redis"
    version = "6.0"
    node_type = "cache.t3.micro"
    num_cache_nodes = 1
}

network "vpc_main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}

# =================================================================
# CORRECT CONNECT STATEMENTS (Using -> syntax)
# =================================================================

# Connection between web and app server
connect web_server -> app_server {
    protocol = "http"
    port = 8080
}

# Connection between app and database
connect app_server -> primary_db {
    protocol = "mysql"
    port = 3306
}

# Connection between app and cache
connect app_server -> redis_cache {
    protocol = "redis"
    port = 6379
}

# =================================================================
# CORRECT POLICY STATEMENTS
# =================================================================

# Security policy for all servers
policy "security_baseline" {
    policy_type = "security"
    target = "all_servers"
    rules = {
        encryption_required = true
        firewall_enabled = true
        monitoring_enabled = true
    }
}

# Database security policy
policy "database_security" {
    policy_type = "security"
    target = "primary_db"
    rules = {
        encryption_at_rest = true
        encryption_in_transit = true
        backup_enabled = true
        audit_logging = true
    }
}

# Performance monitoring policy
policy "performance_monitoring" {
    policy_type = "monitoring"
    target = "all_resources"
    rules = {
        cpu_threshold = 80
        memory_threshold = 85
        disk_threshold = 90
        alert_enabled = true
    }
}

# =================================================================
# CORRECT ROLE STATEMENTS
# =================================================================

role "web_admin" {
    permissions = {
        read = ["web_server"]
        write = ["web_server"]
        restart = ["web_server"]
    }
}

role "db_admin" {
    permissions = {
        read = ["primary_db"]
        write = ["primary_db"]
        backup = ["primary_db"]
        restore = ["primary_db"]
    }
}

# =================================================================
# CORRECT ASSIGN STATEMENTS
# =================================================================

assign "web_admin" -> "web_server"
assign "db_admin" -> "primary_db"
