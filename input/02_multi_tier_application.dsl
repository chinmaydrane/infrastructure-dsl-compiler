# Multi-Tier Application Setup
# Web, application, and database servers

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
    storage = "200GB"
    instance_class = "db.t3.medium"
    backup_retention = 14
}

database "cache_db" {
    engine = "redis"
    version = "6.0"
    storage = "50GB"
    instance_class = "cache.t3.micro"
    backup_retention = 3
}

network "vpc_main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
