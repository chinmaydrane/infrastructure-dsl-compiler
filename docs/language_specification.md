# Infrastructure DSL Language Specification

## Overview

The Infrastructure DSL is a domain-specific language designed for modeling cloud infrastructure resources, their relationships, policies, and configurations. The language provides a declarative syntax that is both human-readable and machine-processable.

## Language Design Philosophy

The DSL follows these design principles:

1. **Declarative**: Describe what infrastructure should exist, not how to create it
2. **Readable**: Syntax should be intuitive for infrastructure engineers
3. **Composable**: Support for modules and reusable components
4. **Type-safe**: Strong typing with validation
5. **Expressive**: Support for complex relationships and policies

## Language Constructs

### 1. Resource Definitions

Resources are the primary building blocks of the DSL. Each resource has a type, name, and attributes.

#### Syntax:
```
resource_type "resource_name" {
    attribute1 = value1
    attribute2 = value2
    ...
}
```

#### Supported Resource Types:

**Server Resources:**
- `server` - Virtual machines or physical servers
- `container` - Container instances
- `function` - Serverless functions

**Database Resources:**
- `database` - Relational databases
- `nosql_db` - NoSQL databases
- `cache` - In-memory caches

**Network Resources:**
- `network` - Virtual networks
- `subnet` - Network subnets
- `load_balancer` - Load balancing
- `firewall` - Network security

**Security Resources:**
- `security_group` - Security group rules
- `role` - IAM roles
- `policy` - Access policies

### 2. Attributes

Attributes define the properties of resources. The DSL supports various data types:

#### Primitive Types:
- **Integer**: `cpu = 4`
- **String**: `os = "ubuntu-20.04"`
- **Boolean**: `enabled = true`
- **Size**: `memory = 16GB` (supports KB, MB, GB, TB)
- **Array**: `tags = ["web", "production"]`
- **Object**: Nested attribute structures

#### Special Attributes:
- `id` - Unique identifier (auto-generated if not specified)
- `depends_on` - Explicit dependency declaration
- `count` - Resource count for scaling
- `provider` - Cloud provider specification

### 3. Relationships

Resources can be connected through various relationship types:

#### Connection Syntax:
```
connect source_resource -> target_resource {
    protocol = "tcp"
    port = 3306
}
```

#### Relationship Types:
- **connect**: Network connectivity between resources
- **attach**: Attach security groups, policies, etc.
- **bind**: Data binding relationships
- **reference**: Logical references

### 4. Policies

Policies define behavior rules and constraints:

#### Autoscaling Policy:
```
policy autoscale_web_servers {
    target = web_servers
    type = "autoscaling"
    min_instances = 2
    max_instances = 10
    metric = "cpu_utilization"
    threshold = 70
}
```

#### Security Policy:
```
policy restrict_database_access {
    target = database_security_group
    type = "security"
    rules = [
        {
            action = "allow"
            source = "web_servers"
            port = 3306
        }
    ]
}
```

### 5. Roles and Permissions

Define access control with roles:

```
role database_admin {
    permissions = [
        "database.read",
        "database.write",
        "database.delete"
    ]
    resources = ["production_db"]
}

assign database_admin to user "admin_user"
```

### 6. Control Flow

Conditional statements enable dynamic infrastructure:

```
if environment == "production" {
    server "web_server" {
        cpu = 8
        memory = 32GB
        os = "ubuntu-20.04"
    }
} else {
    server "web_server" {
        cpu = 2
        memory = 4GB
        os = "ubuntu-18.04"
    }
}
```

### 7. Modules

Modules enable reusable infrastructure patterns:

#### Module Definition:
```
module web_cluster {
    param server_count = 3
    param cpu_per_server = 4
    param memory_per_server = 8GB
    
    for i in range(server_count) {
        server "web_${i}" {
            cpu = cpu_per_server
            memory = memory_per_server
            os = "ubuntu-20.04"
            tags = ["web", "cluster"]
        }
    }
    
    load_balancer "web_lb" {
        target_servers = [web_0, web_1, web_2]
        algorithm = "round_robin"
    }
}
```

#### Module Usage:
```
use web_cluster with {
    server_count = 5
    cpu_per_server = 8
    memory_per_server = 16GB
}
```

### 8. Variables and Constants

#### Variable Declaration:
```
variable environment {
    type = "string"
    default = "development"
    description = "Deployment environment"
}

variable instance_types {
    type = "array"
    default = ["t2.micro", "t2.small", "t2.medium"]
}
```

#### Constant Declaration:
```
constant AWS_REGION = "us-west-2"
constant MAX_RETRIES = 3
```

### 9. Functions

Built-in and user-defined functions:

#### Built-in Functions:
- `range(n)` - Generate sequence 0 to n-1
- `concat(array1, array2)` - Array concatenation
- `length(array)` - Array length
- `substring(string, start, end)` - String substring
- `timestamp()` - Current timestamp

#### User-defined Functions:
```
function calculate_instance_count(cpu_requirement, memory_requirement) {
    if cpu_requirement > 8 and memory_requirement > 16GB {
        return 5
    } else {
        return 3
    }
}
```

### 10. Comments

Comments are ignored by the compiler:

```
# Single line comment
// Another single line comment

/*
   Multi-line comment
   that spans multiple lines
*/
```

## Language Examples

### Basic Example:
```
# Define a simple web server
server "web_server" {
    cpu = 2
    memory = 4GB
    os = "ubuntu-20.04"
    tags = ["web", "frontend"]
}

# Define a database
database "app_db" {
    engine = "mysql"
    version = "8.0"
    storage = 100GB
    instance_class = "db.t3.medium"
}

# Connect server to database
connect web_server -> app_db {
    protocol = "tcp"
    port = 3306
}
```

### Advanced Example:
```
# Variables
variable environment {
    type = "string"
    default = "production"
}

variable cluster_size {
    type = "integer"
    default = 3
}

# Security group
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
}

# Web server cluster using module
use web_cluster with {
    server_count = cluster_size
    cpu_per_server = 4
    memory_per_server = 8GB
    security_group = web_sg
}

# Database with conditional configuration
database "primary_db" {
    engine = "postgresql"
    version = "13.4"
    
    if environment == "production" {
        instance_class = "db.r5.large"
        storage = 500GB
        backup_retention = 30
    } else {
        instance_class = "db.t3.medium"
        storage = 100GB
        backup_retention = 7
    }
    
    tags = {
        Environment = environment
        Application = "web_app"
    }
}

# Autoscaling policy
policy web_autoscaling {
    target = web_cluster
    type = "autoscaling"
    min_instances = 2
    max_instances = 10
    scale_up_cooldown = 300
    scale_down_cooldown = 600
    
    rules = [
        {
            metric = "CPUUtilization"
            threshold = 70
            comparison = "GreaterThanThreshold"
            adjustment = 1
        },
        {
            metric = "CPUUtilization"
            threshold = 20
            comparison = "LessThanThreshold"
            adjustment = -1
        }
    ]
}

# Role for database access
role db_admin_role {
    description = "Database administrator role"
    permissions = [
        "rds:*",
        "ec2:DescribeInstances"
    ]
}

assign db_admin_role to user "db_admin"
```

## Type System

The DSL implements a strong type system with the following types:

### Primitive Types:
- `integer` - Whole numbers
- `float` - Decimal numbers
- `string` - Text values
- `boolean` - true/false values
- `size` - Memory/storage sizes with units

### Complex Types:
- `array<T>` - Arrays of type T
- `object` - Key-value structures
- `resource_type` - Specific resource types
- `policy_type` - Policy definitions

### Type Coercion:
- `integer` → `float` (automatic)
- `size` → `integer` (bytes value)
- `string` → `resource_type` (reference resolution)

## Validation Rules

### Resource Validation:
- Required attributes must be present
- Attribute values must be of correct type
- Resource names must be unique within scope
- References must resolve to existing resources

### Relationship Validation:
- Connection sources and targets must exist
- Connection protocols and ports must be valid
- Circular dependencies are not allowed

### Policy Validation:
- Policy targets must exist
- Policy rules must be syntactically correct
- Permission strings must follow naming conventions

## Error Handling

The DSL compiler provides comprehensive error handling:

### Syntax Errors:
- Missing brackets, semicolons, etc.
- Invalid token sequences
- Malformed expressions

### Semantic Errors:
- Type mismatches
- Undefined references
- Duplicate definitions
- Constraint violations

### Runtime Errors:
- Division by zero
- Array index out of bounds
- Invalid function arguments

## Compiler Directives

Special instructions to the compiler:

```
#compiler_version = "1.0.0"
#strict_mode = true
#warn_unused = true
#output_format = "json"
```
