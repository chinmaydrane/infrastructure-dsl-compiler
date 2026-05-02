# Working Example - Demonstrates Successful Compilation
# This file should compile successfully with minimal errors

server "web_server" {
    cpu = 4
    memory = 8GB
    os = "ubuntu-22.04"
    enabled = true
    tags = ["web", "production"]
}

database "app_database" {
    engine = "mysql"
    version = "8.0"
    storage = 200GB
    instance_class = "db.r5.large"
    backup_retention = 30
}

network "main_vpc" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
}

if (true) {
    server "backup_server" {
        cpu = 2
        memory = 4GB
        os = "ubuntu-20.04"
        tags = ["backup", "secondary"]
    }
}
