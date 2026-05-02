# Demo file with corrected syntax errors for demonstration

# Fixed Error 1: Added assignment operator
server "web_server" {
    cpu = 4                   # FIXED: Added = operator
    memory = "8GB"
}

# Fixed Error 2: Valid resource type
database "test" {             # FIXED: Changed to valid resource type
    cpu = 2
    memory = "4GB"
}

# Fixed Error 3: Added closing brace
database "db" {              # FIXED: Added closing }
    engine = "mysql"
    storage = "100GB"
}
