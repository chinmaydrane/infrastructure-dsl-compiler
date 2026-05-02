# Demo file with intentional semantic errors for demonstration

# Error 1: Undefined resource reference
server "web_server" {
    cpu = 4
    memory = "8GB"
}

database "db" {
    engine = "mysql"
    storage = "100GB"
}

# ERROR: Referencing undefined resource "nonexistent_server"
connect "web_server" to "nonexistent_server"    # ERROR: nonexistent_server not defined

# Error 2: Invalid attribute value type
server "another_server" {
    cpu = "invalid"          # ERROR: cpu should be integer, not string
    memory = "8GB"
}
