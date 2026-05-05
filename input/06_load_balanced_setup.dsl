# Load Balanced Setup
# Multiple web servers behind load balancer

server "web_server_1" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "web_server_2" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "web_server_3" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "app_server_1" {
    cpu = 8
    memory = "16GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "app_server_2" {
    cpu = 8
    memory = "16GB"
    os = "ubuntu-20.04"
    enabled = true
}

database "primary_db" {
    engine = "mysql"
    version = "8.0"
    storage = "300GB"
    instance_class = "db.t3.medium"
    backup_retention = 14
}

database "read_replica_1" {
    engine = "mysql"
    version = "8.0"
    storage = "300GB"
    instance_class = "db.t3.medium"
    backup_retention = 7
}

database "redis_cluster" {
    engine = "redis"
    version = "6.0"
    storage = "50GB"
    instance_class = "cache.t3.medium"
    backup_retention = 7
}

network "vpc_load_balanced" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
