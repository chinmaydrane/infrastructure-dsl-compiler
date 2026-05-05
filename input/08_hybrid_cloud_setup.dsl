# Hybrid Cloud Setup
# Mixed workloads with different requirements

server "web_frontend" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "api_gateway" {
    cpu = 8
    memory = "16GB"
    os = "ubuntu-22.04"
    enabled = true
}

server "batch_processor" {
    cpu = 16
    memory = "32GB"
    os = "ubuntu-22.04"
    enabled = true
}

database "transactional_db" {
    engine = "mysql"
    version = "8.0"
    storage = "500GB"
    instance_class = "db.r5.large"
    backup_retention = 30
}

database "analytics_db" {
    engine = "postgres"
    version = "14.0"
    storage = "2000GB"
    instance_class = "db.r5.xlarge"
    backup_retention = 14
}

database "session_cache" {
    engine = "redis"
    version = "6.0"
    storage = "50GB"
    instance_class = "cache.r5.medium"
    backup_retention = 7
}

database "analytics_cache" {
    engine = "redis"
    version = "6.0"
    storage = "200GB"
    instance_class = "cache.r5.large"
    backup_retention = 14
}

network "vpc_hybrid" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
