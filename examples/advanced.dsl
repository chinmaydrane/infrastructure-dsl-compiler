# Advanced Infrastructure DSL Example
# This example demonstrates complex language features

# Variable declarations
variable environment {
    type = "string"
    default = "production"
    description = "Deployment environment"
}

variable cluster_size {
    type = "integer"
    default = 3
    description = "Number of servers in cluster"
}

variable enable_monitoring {
    type = "boolean"
    default = true
    description = "Enable monitoring services"
}

# Constants
constant AWS_REGION = "us-west-2"
constant MAX_RETRIES = 3
constant BACKUP_RETENTION_DAYS = 30

# User-defined function
function calculate_instance_count(cpu_requirement, memory_requirement) {
    if cpu_requirement > 8 and memory_requirement > 16GB {
        return 5
    } else if cpu_requirement > 4 and memory_requirement > 8GB {
        return 3
    } else {
        return 2
    }
}

# Module definition for web cluster
module web_cluster {
    param server_count = 3
    param cpu_per_server = 4
    param memory_per_server = 8GB
    param security_group = null
    param subnet = null
    
    # Create servers in a loop
    for i in range(server_count) {
        server "web_${i}" {
            cpu = cpu_per_server
            memory = memory_per_server
            os = "ubuntu-20.04"
            tags = ["web", "cluster", "server_${i}"]
            
            if security_group != null {
                security_groups = [security_group]
            }
            
            if subnet != null {
                subnet = subnet
            }
            
            # Conditional monitoring
            if enable_monitoring {
                monitoring = {
                    enabled = true
                    metrics = ["cpu", "memory", "disk"]
                    alarm_threshold = 80
                }
            }
        }
    }
    
    # Load balancer
    load_balancer "web_lb" {
        type = "application"
        algorithm = "round_robin"
        
        # Target servers
        target_servers = [for i in range(server_count) -> "web_${i}"]
        
        listeners = [
            {
                port = 80
                protocol = "HTTP"
                default_action = "forward"
            },
            {
                port = 443
                protocol = "HTTPS"
                certificate_arn = "arn:aws:acm:us-west-2:123456789012:certificate/12345678-1234-1234-1234-123456789012"
                default_action = "forward"
            }
        ]
        
        health_check = {
            path = "/health"
            interval = 30
            timeout = 5
            healthy_threshold = 2
            unhealthy_threshold = 3
        }
    }
}

# Network infrastructure
network "main_vpc" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
    tags = {
        Name = "Main VPC"
        Environment = environment
    }
}

# Public subnets
for az in ["us-west-2a", "us-west-2b"] {
    subnet "public_${az}" {
        network = main_vpc
        cidr_block = "10.0.${index(az) + 1}.0/24"
        availability_zone = az
        public = true
        map_public_ip_on_launch = true
        tags = {
            Type = "Public"
            AZ = az
        }
    }
}

# Private subnets
for az in ["us-west-2a", "us-west-2b"] {
    subnet "private_${az}" {
        network = main_vpc
        cidr_block = "10.0.${index(az) + 3}.0/24"
        availability_zone = az
        public = false
        tags = {
            Type = "Private"
            AZ = az
        }
    }
}

# Security groups
security_group "web_sg" {
    description = "Security group for web servers"
    vpc = main_vpc
    
    ingress = [
        {
            from_port = 80
            to_port = 80
            protocol = "tcp"
            security_groups = []
            cidr_blocks = ["0.0.0.0/0"]
            description = "HTTP access"
        },
        {
            from_port = 443
            to_port = 443
            protocol = "tcp"
            security_groups = []
            cidr_blocks = ["0.0.0.0/0"]
            description = "HTTPS access"
        }
    ]
    
    egress = [
        {
            from_port = 0
            to_port = 0
            protocol = "-1"
            security_groups = []
            cidr_blocks = ["0.0.0.0/0"]
            description = "All outbound traffic"
        }
    ]
}

security_group "db_sg" {
    description = "Security group for databases"
    vpc = main_vpc
    
    ingress = [
        {
            from_port = 3306
            to_port = 3306
            protocol = "tcp"
            security_groups = [web_sg]
            cidr_blocks = []
            description = "MySQL access from web servers"
        }
    ]
    
    egress = [
        {
            from_port = 0
            to_port = 0
            protocol = "-1"
            security_groups = []
            cidr_blocks = ["0.0.0.0/0"]
            description = "All outbound traffic"
        }
    ]
}

# Database configuration
database "primary_db" {
    engine = "postgresql"
    version = "13.4"
    instance_class = if environment == "production" then "db.r5.large" else "db.t3.medium"
    
    storage = if environment == "production" then 500GB else 100GB
    storage_type = "gp2"
    storage_encrypted = true
    
    backup_retention = if environment == "production" then BACKUP_RETENTION_DAYS else 7
    backup_window = "03:00-04:00"
    maintenance_window = "sun:04:00-sun:05:00"
    
    # Multi-AZ configuration for production
    if environment == "production" {
        multi_az = true
        read_replica_count = 2
    }
    
    subnet_group = "default"
    vpc_security_group_ids = [db_sg]
    
    tags = {
        Environment = environment
        Application = "web_app"
        Backup = "enabled"
    }
    
    # Database parameters
    parameters = {
        "shared_preload_libraries" = "pg_stat_statements"
        "log_statement" = "all"
        "log_min_duration_statement" = "1000"
    }
}

# Cache configuration
cache "redis_cache" {
    engine = "redis"
    version = "6.2"
    node_type = "cache.t3.micro"
    num_cache_nodes = 1
    port = 6379
    
    subnet_group_name = "default"
    security_group_ids = [web_sg]
    
    if environment == "production" {
        automatic_failover = true
        multi_az_enabled = true
        num_cache_nodes = 3
    }
    
    tags = {
        Environment = environment
        Application = "web_app"
    }
}

# Use the web cluster module
use web_cluster with {
    server_count = calculate_instance_count(4, 8GB)
    cpu_per_server = 4
    memory_per_server = 8GB
    security_group = web_sg
    subnet = public_us-west-2a
}

# Autoscaling policy
policy web_autoscaling {
    target = web_cluster
    type = "autoscaling"
    min_instances = 2
    max_instances = 10
    desired_capacity = cluster_size
    
    scale_up_cooldown = 300
    scale_down_cooldown = 600
    
    metrics = [
        {
            metric = "CPUUtilization"
            threshold = 70
            comparison = "GreaterThanThreshold"
            statistic = "Average"
            period = 300
            evaluation_periods = 2
            adjustment_type = "ChangeInCapacity"
            scaling_adjustment = 1
        },
        {
            metric = "CPUUtilization"
            threshold = 20
            comparison = "LessThanThreshold"
            statistic = "Average"
            period = 300
            evaluation_periods = 2
            adjustment_type = "ChangeInCapacity"
            scaling_adjustment = -1
        }
    ]
}

# Monitoring policy
policy monitoring_policy {
    target = [web_cluster, primary_db, redis_cache]
    type = "monitoring"
    
    alarms = [
        {
            name = "HighCPUUtilization"
            metric = "CPUUtilization"
            threshold = 80
            comparison = "GreaterThanThreshold"
            statistic = "Average"
            period = 300
            evaluation_periods = 2
            alarm_actions = ["arn:aws:sns:us-west-2:123456789012:alerts"]
        },
        {
            name = "HighMemoryUtilization"
            metric = "MemoryUtilization"
            threshold = 85
            comparison = "GreaterThanThreshold"
            statistic = "Average"
            period = 300
            evaluation_periods = 2
            alarm_actions = ["arn:aws:sns:us-west-2:123456789012:alerts"]
        }
    ]
}

# Backup policy
policy backup_policy {
    target = primary_db
    type = "backup"
    
    schedule = "cron(0 2 * * ? *)"
    retention_days = BACKUP_RETENTION_DAYS
    cold_storage_after_days = 30
    delete_after_days = 365
    
    lifecycle = {
        transition_to_ia = 30
        transition_to_glacier = 60
        transition_to_deep_archive = 180
    }
}

# Role definitions
role "database_admin" {
    description = "Database administrator role"
    permissions = [
        "rds:*",
        "ec2:DescribeInstances",
        "ec2:DescribeSecurityGroups"
    ]
    resources = ["primary_db"]
    
    conditions = {
        "aws:SourceIp" = ["203.0.113.0/24", "198.51.100.0/24"]
    }
}

role "web_developer" {
    description = "Web developer role"
    permissions = [
        "ec2:DescribeInstances",
        "ec2:RebootInstances",
        "elasticloadbalancing:*"
    ]
    resources = ["web_cluster", "web_lb"]
}

role "system_admin" {
    description = "System administrator role"
    permissions = [
        "*"
    ]
    resources = ["*"]
}

# Role assignments
assign database_admin to user "db_admin"
assign web_developer to user "web_dev"
assign system_admin to user "sys_admin"

# Conditional resource creation
if environment == "production" {
    # Additional monitoring for production
    server "monitoring_server" {
        cpu = 2
        memory = 4GB
        os = "ubuntu-20.04"
        subnet = private_us-west-2a
        security_groups = [web_sg]
        
        software = {
            "prometheus" = "latest"
            "grafana" = "latest"
            "node_exporter" = "latest"
        }
    }
    
    # Connect monitoring to web cluster
    connect monitoring_server -> web_cluster {
        protocol = "http"
        port = 9100
    }
    
    # Enhanced logging
    policy enhanced_logging {
        target = [web_cluster, primary_db]
        type = "logging"
        
        log_groups = [
            {
                name = "/aws/ec2/web-cluster"
                retention_days = 30
            },
            {
                name = "/aws/rds/primary-db"
                retention_days = 30
            }
        ]
        
        log_streams = [
            {
                name = "application-logs"
                filter_pattern = "[timestamp, request_id, level, message]"
            },
            {
                name = "error-logs"
                filter_pattern = "ERROR"
            }
        ]
    }
}

# Network connections
connect web_cluster -> primary_db {
    protocol = "tcp"
    port = 5432
    security_group = db_sg
}

connect web_cluster -> redis_cache {
    protocol = "tcp"
    port = 6379
    security_group = web_sg
}

# Final configuration summary
constant CONFIG_SUMMARY = {
    environment = environment
    cluster_size = cluster_size
    monitoring_enabled = enable_monitoring
    region = AWS_REGION
    created_at = timestamp()
}
