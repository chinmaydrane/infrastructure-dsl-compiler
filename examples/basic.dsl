# Basic Infrastructure DSL Example
# This example demonstrates fundamental language constructs

# Define a simple web server
server "web_server" {
    cpu = 2
    memory = 4GB
    os = "ubuntu-20.04"
    tags = ["web", "frontend"]
    enabled = true
}

# Define a database server
database "app_database" {
    engine = "mysql"
    version = "8.0"
    storage = 100GB
    instance_class = "db.t3.medium"
    backup_retention = 7
}

# Define network resources
network "vpc" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
}

subnet "public_subnet" {
    network = vpc
    cidr_block = "10.0.1.0/24"
    availability_zone = "us-west-2a"
    public = true
}

subnet "private_subnet" {
    network = vpc
    cidr_block = "10.0.2.0/24"
    availability_zone = "us-west-2b"
    public = false
}

# Define security group
security_group "web_sg" {
    description = "Security group for web servers"
    ingress = [
        {
            from_port = 80
            to_port = 80
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        },
        {
            from_port = 443
            to_port = 443
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }
    ]
    egress = [
        {
            from_port = 0
            to_port = 0
            protocol = "-1"
            cidr_blocks = ["0.0.0.0/0"]
        }
    ]
}

# Connect resources
connect web_server -> app_database {
    protocol = "tcp"
    port = 3306
}

attach web_sg to web_server

# Define a simple role
role "web_admin" {
    description = "Web server administrator"
    permissions = [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:RebootInstances"
    ]
    resources = ["web_server"]
}

# Assign role to user
assign web_admin to user "admin_user"
