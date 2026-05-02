# Modules and Functions
# Demonstrates modular design and function definitions

# Function to calculate instance size based on requirements
function calculate_instance_size(cpu, memory, environment) {
    if (environment == "production") {
        return {
            "cpu": cpu * 2,
            "memory": memory * 2,
            "instance_class": "m5.large"
        }
    } else {
        return {
            "cpu": cpu,
            "memory": memory,
            "instance_class": "t3.medium"
        }
    }
}

# Module for web server infrastructure
module "web_infrastructure" {
    param server_count
    param base_cpu
    param base_memory
    param environment
    
    # Create multiple servers using function
    for i in range(0, server_count) {
        server_name = "web_" + i
        instance_config = calculate_instance_size(base_cpu, base_memory, environment)
        
        server server_name {
            cpu = instance_config.cpu
            memory = instance_config.memory
            os = "ubuntu-22.04"
            instance_class = instance_config.instance_class
            tags = ["web", environment, "auto-generated"]
        }
    }
    
    # Create load balancer for the web servers
    load_balancer "web_lb" {
        algorithm = "round_robin"
        target_servers = ["web_" + i for i in range(0, server_count)]
        listeners = [
            {
                "port": 80
                "protocol": "http"
            },
            {
                "port": 443
                "protocol": "https"
            }
        ]
    }
}

# Module for database infrastructure
module "database_infrastructure" {
    param db_engine
    param storage_size
    param environment
    
    database "primary_db" {
        engine = db_engine
        storage = storage_size
        if (environment == "production") {
            version = "8.0"
            instance_class = "db.r5.large"
            multi_az = true
            backup_retention = 30
        } else {
            version = "8.0"
            instance_class = "db.t3.micro"
            multi_az = false
            backup_retention = 7
        }
    }
    
    if (environment == "production") {
        # Read replica for production
        database "read_replica" {
            engine = db_engine
            storage = storage_size
            version = "8.0"
            instance_class = "db.r5.large"
            read_replica_count = 1
        }
    }
}

# Use the modules
web_infrastructure(3, 2, 4GB, "production")
database_infrastructure("mysql", 200GB, "production")
