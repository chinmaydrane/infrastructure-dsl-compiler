# Complex Expressions - Simple Fixed Version
# Demonstrates working expressions without complex syntax

server "web_server" {
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
    backup_retention = 7
}

network "vpc_main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}

load_balancer "app_lb" {
    algorithm = "round_robin"
    target_servers = ["web_server"]
    listeners {
        port = 80
        protocol = "http"
    }
    health_check {
        path = "/health"
        interval = 30
        timeout = 5
    }
}
