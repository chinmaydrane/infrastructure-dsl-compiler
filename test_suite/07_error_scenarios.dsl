# Error Scenarios and Invalid Syntax
# Demonstrates various error conditions that the compiler should catch

# Syntax errors: Missing brackets and quotes
server "error_server1 {
    cpu = 2
    memory = 4GB
    # Missing closing quote above

# Syntax errors: Invalid attribute assignments
database "error_db" {
    engine = "mysql"
    storage = 100GB
    invalid_attr = ???  # Invalid value
    missing_value =     # Missing value
}

# Semantic errors: Undefined references
connect "invalid_connection" {
    undefined_server to another_undefined_server
    attributes = {
        "protocol": "http"
    }
}

# Semantic errors: Type mismatches
server "type_error_server" {
    cpu = "not_a_number"  # Should be numeric
    memory = "4GB"       # This is correct
    os = 12345           # Should be string
}

# Semantic errors: Duplicate resource names
server "duplicate_name" {
    cpu = 2
    memory = 4GB
}

server "duplicate_name" {
    cpu = 4
    memory = 8GB
}

# Semantic errors: Invalid policy targets
policy "invalid_policy" {
    policy_type = "security"
    target = "nonexistent_resource"
    rules = {
        "encryption_required": true
    }
}

# Semantic errors: Circular dependencies
connect "circular1" {
    server_a to server_b
}

connect "circular2" {
    server_b to server_a
}

# Syntax errors: Malformed expressions
server "expression_errors" {
    cpu = 2 + * 4  # Invalid expression
    memory = 4GB / 0  # Division by zero (if caught)
    os = "ubuntu" + 20.04  # Invalid string concatenation
}

# Semantic errors: Invalid role assignments
role "invalid_role" {
    description = "Invalid role"
    permissions = ["invalid_permission"]
    resources = ["nonexistent_resource"]
}

assign role "invalid_role" to user "nonexistent_user"

# Syntax errors: Unclosed blocks and structures
server "incomplete_server" {
    cpu = 2
    memory = 4GB
    # Missing closing brace

if (true) {
    server "nested_incomplete" {
        cpu = 1
        # Missing closing brace for nested block
# Missing closing brace for if statement

# Syntax errors: Invalid function calls
function "invalid_function" {
    param missing_type
    # No return type
}

# Call with wrong number of arguments
result = calculate_instance_size(2)  # Missing memory and environment

# Syntax errors: Invalid module usage
module "invalid_module" {
    param undefined_param
    # No module body
}

# Use module with wrong arguments
invalid_module()  # Missing required parameters
