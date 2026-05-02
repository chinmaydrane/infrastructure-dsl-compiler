# Control Flow and Conditional Logic
# Demonstrates if-else statements and conditional compilation

variable "environment" {
    type = "string"
    default = "production"
}

variable "enable_monitoring" {
    type = "boolean"
    default = true
}

# Conditional resource creation based on environment
if (environment == "production") {
    server "production_web" {
        cpu = 8
        memory = 16GB
        os = "ubuntu-22.04"
        enabled = true
        tags = ["production", "high-availability"]
    }
    
    database "production_db" {
        engine = "mysql"
        version = "8.0"
        storage = 500GB
        instance_class = "db.r5.large"
        multi_az = true
        backup_retention = 30
    }
    
    load_balancer "production_lb" {
        algorithm = "least_connections"
        listeners = [
            {
                "port": 443
                "protocol": "https"
            }
        ]
    }
} else {
    server "dev_web" {
        cpu = 2
        memory = 4GB
        os = "ubuntu-20.04"
        enabled = false
        tags = ["development", "test"]
    }
    
    database "dev_db" {
        engine = "mysql"
        version = "8.0"
        storage = 50GB
        instance_class = "db.t3.micro"
        multi_az = false
        backup_retention = 7
    }
}

# Conditional monitoring setup
if (enable_monitoring) {
    server "monitoring_server" {
        cpu = 2
        memory = 4GB
        os = "ubuntu-20.04"
        tags = ["monitoring", "prometheus"]
    }
    
    # Monitoring configuration
    policy "monitoring_policy" {
        policy_type = "monitoring"
        target = "all_servers"
        rules = {
            "cpu_threshold": 80
            "memory_threshold": 85
            "disk_threshold": 90
            "alert_interval": 300
        }
    }
}
