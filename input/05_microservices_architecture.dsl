# Microservices Architecture
# Multiple small services with databases

server "user_service" {
    cpu = 2
    memory = "4GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "auth_service" {
    cpu = 2
    memory = "4GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "payment_service" {
    cpu = 4
    memory = "8GB"
    os = "ubuntu-20.04"
    enabled = true
}

server "notification_service" {
    cpu = 1
    memory = "2GB"
    os = "ubuntu-20.04"
    enabled = true
}

database "user_db" {
    engine = "mysql"
    version = "8.0"
    storage = "100GB"
    instance_class = "db.t3.micro"
    backup_retention = 7
}

database "auth_db" {
    engine = "mysql"
    version = "8.0"
    storage = "50GB"
    instance_class = "db.t3.micro"
    backup_retention = 7
}

database "payment_db" {
    engine = "mysql"
    version = "8.0"
    storage = "200GB"
    instance_class = "db.t3.small"
    backup_retention = 14
}

database "redis_cache" {
    engine = "redis"
    version = "6.0"
    storage = "25GB"
    instance_class = "cache.t3.micro"
    backup_retention = 3
}

network "vpc_microservices" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
