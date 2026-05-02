server "web_server" {
    cpu = 2
    memory = 4GB
}

if (true) {
    server "backup_server" {
        cpu = 1
        memory = 2GB
    }
} else {
    server "test_server" {
        cpu = 4
        memory = 8GB
    }
}
