# Demo file with intentional syntax errors for demonstration

# Error 1: Missing assignment operator
server "web_server" {
    cpu 4
    memory "8GB"
}

# Error 2: Invalid resource type
invalid_resource "test" {
    cpu 2
    memory "4GB"
}

# Error 3: Missing closing brace
database "db" {
    engine "mysql"
    storage "100GB"
