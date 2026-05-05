# Development Environment Setup
# Smaller servers for development and testing

server "dev_web_server" {
    cpu = 1
    memory = "2GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "dev_app_server" {
    cpu = 2
    memory = "4GB"
    os = "ubuntu-20.04"
    enabled = true
}

database "dev_db" {
    engine = "mysql"
    version = "8.0"
    storage = "50GB"
    instance_class = "db.t3.micro"
    backup_retention = 3
}

database "dev_cache" {
    engine = "redis"
    version = "6.0"
    storage = "10GB"
    instance_class = "cache.t3.micro"
    backup_retention = 1
}

network "vpc_dev" {
    cidr_block = "192.168.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
