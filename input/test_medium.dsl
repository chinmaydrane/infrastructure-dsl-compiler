server "web_server" {
    cpu = 2
    memory = 4GB
    os = "ubuntu-20.04"
}

database "app_db" {
    engine = "mysql"
    storage = 100GB
}
