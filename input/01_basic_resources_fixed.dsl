# Basic Resource Declarations - Fixed Version
# Demonstrates fundamental resource types

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

security_group "web_sg" {
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
