# Edge Cases and Error Scenarios
# Demonstrates various edge cases and potential error conditions

# Deeply nested structures
server "complex_server" {
    cpu = 4
    memory = 8GB
    os = "ubuntu-22.04"
    
    # Deeply nested object literals
    configuration = {
        "networking" = {
            "interfaces" = {
                "primary" = {
                    "ip" = "10.0.1.100"
                    "gateway" = "10.0.1.1"
                    "dns" = ["10.0.1.2", "10.0.1.3"]
                }
                "secondary" = {
                    "ip" = "10.0.2.100"
                    "gateway" = "10.0.2.1"
                    "dns" = ["10.0.2.2", "10.0.2.3"]
                }
            }
            "firewall" = {
                "rules" = [
                    {
                        "action" = "allow"
                        "protocol" = "tcp"
                        "ports" = [80, 443, 22]
                        "source" = "0.0.0.0/0"
                    },
                    {
                        "action" = "deny"
                        "protocol" = "all"
                        "ports" = "all"
                        "source" = "0.0.0.0/0"
                    }
                ]
            }
        }
        "storage" = {
            "volumes" = [
                {
                    "name" = "root"
                    "size" = 100GB
                    "type" = "ssd"
                    "encrypted" = true
                },
                {
                    "name" = "data"
                    "size" = 500GB
                    "type" = "hdd"
                    "encrypted" = true
                    "backup" = true
                }
            ]
        }
    }
}

# Complex conditional logic
variable "tier" {
    type = "string"
    default = "standard"
}

if (tier == "basic") {
    server "basic_server" {
        cpu = 1
        memory = 2GB
        os = "ubuntu-20.04"
    }
} else if (tier == "standard") {
    server "standard_server" {
        cpu = 2
        memory = 4GB
        os = "ubuntu-20.04"
    }
    
    database "standard_db" {
        engine = "mysql"
        storage = 100GB
    }
} else if (tier == "premium") {
    server "premium_server" {
        cpu = 4
        memory = 8GB
        os = "ubuntu-22.04"
    }
    
    database "premium_db" {
        engine = "mysql"
        storage = 500GB
        multi_az = true
    }
    
    load_balancer "premium_lb" {
        algorithm = "round_robin"
        listeners = [
            {"port": 80, "protocol": "http"},
            {"port": 443, "protocol": "https"}
        ]
    }
} else {
    server "custom_server" {
        cpu = 8
        memory = 16GB
        os = "ubuntu-22.04"
    }
}

# Complex function with multiple parameters
function create_infrastructure(name, cpu_count, memory_size, env_type, features) {
    base_config = {
        "cpu": cpu_count
        "memory": memory_size
        "os": "ubuntu-22.04"
    }
    
    if (env_type == "production") {
        base_config.cpu = base_config.cpu * 2
        base_config.memory = base_config.memory * 2
    }
    
    if (features.monitoring) {
        base_config.monitoring_enabled = true
    }
    
    if (features.backup) {
        base_config.backup_enabled = true
    }
    
    if (features.ssl) {
        base_config.ssl_enabled = true
    }
    
    return base_config
}

# Use the function with complex arguments
server "complex_app" {
    config = create_infrastructure("complex_app", 4, 8GB, "production", {
        "monitoring": true,
        "backup": true,
        "ssl": true,
        "high_availability": true,
        "auto_scaling": true
    })
    
    cpu = config.cpu
    memory = config.memory
    os = config.os
}

# Edge case: Empty and default values
server "minimal_server" {
    cpu = 1
    memory = 1GB
    os = "ubuntu-20.04"
    tags = []
    metadata = {}
}

# Edge case: Large arrays and objects
server "enterprise_server" {
    cpu = 16
    memory = 64GB
    os = "ubuntu-22.04"
    
    tags = [
        "enterprise", "production", "high-availability", "monitored", 
        "backed-up", "encrypted", "compliant", "audit-enabled",
        "auto-scaling", "load-balanced", "multi-az", "geo-redundant"
    ]
    
    environment_variables = {
        "APP_ENV" = "production"
        "LOG_LEVEL" = "INFO"
        "DB_HOST" = "primary-db.internal"
        "REDIS_HOST" = "redis.internal"
        "API_KEY" = "encrypted-api-key"
        "SECRET_KEY" = "encrypted-secret-key"
        "BACKUP_SCHEDULE" = "0 2 * * *"
        "MONITORING_ENABLED" = "true"
        "SSL_CERT_PATH" = "/etc/ssl/certs/app.crt"
        "SSL_KEY_PATH" = "/etc/ssl/private/app.key"
    }
}
