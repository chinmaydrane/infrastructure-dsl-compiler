# Error Examples for Infrastructure DSL
# This file contains various types of errors to test error handling

# 1. Syntax Error - Missing closing brace
server "broken_server" {
    cpu = 4
    memory = 8GB
    # Missing closing brace

# 2. Semantic Error - Undefined resource reference
connect nonexistent_server -> database {
    protocol = "tcp"
    port = 3306
}

# 3. Type Error - Invalid attribute type
server "type_error_server" {
    cpu = "not_a_number"  # Should be integer
    memory = true          # Should be size
}

# 4. Duplicate Resource Definition
server "duplicate_server" {
    cpu = 2
    memory = 4GB
}

server "duplicate_server" {
    cpu = 4
    memory = 8GB
}

# 5. Invalid Resource Type
invalid_resource "bad_resource" {
    attribute = "value"
}

# 6. Undefined Variable
server "var_error_server" {
    cpu = undefined_var
    memory = 4GB
}

# 7. Invalid Function Call
server "func_error_server" {
    cpu = nonexistent_function(5)
    memory = 4GB
}

# 8. Invalid Array Access
server "array_error_server" {
    cpu = [1, 2, 3]["invalid_index"]
    memory = 4GB
}

# 9. Invalid Member Access
server "member_error_server" {
    cpu = 5.invalid_member
    memory = 4GB
}

# 10. Invalid Assignment
nonexistent_identifier = "value"

# 11. Invalid Role Assignment
assign nonexistent_role to user "test_user"

# 12. Invalid Module Usage
use nonexistent_module with {
    param = "value"
}

# 13. Invalid Policy Target
policy invalid_policy {
    type = "autoscaling"
    target = nonexistent_resource
    min_instances = 1
    max_instances = 10
}

# 14. Invalid Conditional Expression
if 5 + 3 {  # Condition should be boolean
    server "cond_error_server" {
        cpu = 2
        memory = 4GB
    }
}

# 15. Invalid Loop Variable
for invalid_loop_var in [1, 2, 3] {
    server "loop_server" {
        cpu = loop_var
        memory = 4GB
    }
}

# 16. Invalid Attribute Name
server "attr_error_server" {
    invalid_attribute = "value"  # Not a valid server attribute
    cpu = 2
    memory = 4GB
}

# 17. Invalid Connection Attributes
connect server "conn_error_server" -> database "test_db" {
    invalid_protocol = "udp"  # Should be 'protocol'
    port = "not_a_number"     # Should be integer
}

# 18. Invalid Security Group Rule
security_group "invalid_sg" {
    description = "Invalid security group"
    ingress = [
        {
            from_port = "invalid"  # Should be integer
            to_port = 80
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }
    ]
}

# 19. Invalid Database Configuration
database "invalid_db" {
    engine = 12345        # Should be string
    version = true        # Should be string
    storage = "not_size"  # Should be size
}

# 20. Invalid Network Configuration
network "invalid_network" {
    cidr_block = 12345    # Should be string
    enable_dns_hostnames = "yes"  # Should be boolean
}

# 21. Invalid Variable Declaration
variable invalid_var {
    type = "invalid_type"
    default = "value"
}

# 22. Invalid Constant Declaration
constant invalid_const = undefined_var

# 23. Invalid Role Declaration
role "invalid_role" {
    permissions = [
        "invalid_permission_format"
    ]
    resources = [
        nonexistent_resource
    ]
}

# 24. Invalid Policy Declaration
policy "invalid_policy_2" {
    type = "invalid_policy_type"
    target = server "test_server"
    invalid_attribute = "value"
}

# 25. Invalid Module Declaration
module invalid_module {
    param invalid_param = undefined_var
    
    server "module_server" {
        cpu = invalid_param
        memory = 4GB
    }
}

# 26. Invalid Function Declaration
function invalid_func(undefined_param) {
    return undefined_param + "string";  # Type mismatch
}

# 27. Invalid Use Statement with Invalid Arguments
use web_cluster with {
    server_count = "not_a_number"
    cpu_per_server = undefined_var
}

# 28. Invalid Array Element Type
server "array_type_error" {
    tags = [1, 2, 3]  # Should be array of strings
    cpu = 2
    memory = 4GB
}

# 29. Invalid Object Property Type
server "object_type_error" {
    tags = {
        key1 = 123,      # Should be string
        key2 = true      # Should be string
    }
    cpu = 2
    memory = 4GB
}

# 30. Invalid Size Unit
server "size_error_server" {
    cpu = 2
    memory = 4XB  # Invalid size unit
}

# 31. Invalid String Escape
server "string_error_server" {
    name = "Invalid \x escape sequence"
    cpu = 2
    memory = 4GB
}

# 32. Invalid Comment
# This comment is fine
/* This comment is also fine */
server "comment_error_server" {
    cpu = 2
    memory = 4GB
}
/* Unterminated multi-line comment
