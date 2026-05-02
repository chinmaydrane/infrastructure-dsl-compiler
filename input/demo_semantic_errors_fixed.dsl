# Demo file with corrected semantic errors for demonstration

# Error 1: Undefined resource reference - FIXED
server "web_server" {
    cpu = 4
    memory = "8GB"
}

database "db" {
    engine = "mysql"
    storage = "100GB"
}

# FIXED: Referencing defined resource "web_server"
connect "web_server" to "db"    # FIXED: db is defined above

# Error 2: Invalid attribute value type - FIXED
server "another_server" {
    cpu = 8                   # FIXED: cpu is now integer
    memory = "8GB"
}
