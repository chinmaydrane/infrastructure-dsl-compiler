# Modules and Functions - Working Version
# Demonstrates basic resources without complex module syntax

server "web_server" {
    cpu = 2
    memory = "4GB"
    os = "ubuntu-20.04"
    enabled = true
}

database "primary_db" {
    engine = "mysql"
    version = "8.0"
    storage = "100GB"
    instance_class = "db.t3.medium"
    backup_retention = 7
}

network "vpc_main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}
