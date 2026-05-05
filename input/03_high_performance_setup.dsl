# High Performance Setup
# Large servers for production workloads

server "web_server_1" {
    cpu = 8
    memory = "16GB"
    os = "ubuntu-22.04"
    enabled = true
}

server "web_server_2" {
    cpu = 8
    memory = "16GB"
    os = "ubuntu-22.04"
    enabled = true
}

server "app_server_1" {
    cpu = 16
    memory = "32GB"
    os = "ubuntu-22.04"
    enabled = true
}

database "primary_db" {
    engine = "mysql"
    version = "8.0"
    storage = "500GB"
    instance_class = "db.r5.large"
    backup_retention = 30
}

database "read_replica" {
    engine = "mysql"
    version = "8.0"
    storage = "500GB"
    instance_class = "db.r5.large"
    backup_retention = 7
}

database "redis_cluster" {
    engine = "redis"
    version = "6.0"
    storage = "100GB"
    instance_class = "cache.r5.large"
    backup_retention = 7
}

network "vpc_production" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
