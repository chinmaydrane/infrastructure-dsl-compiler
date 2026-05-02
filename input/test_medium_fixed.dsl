# Test Medium - Fixed Version
# Simple working DSL example

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
