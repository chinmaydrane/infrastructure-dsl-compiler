# Code Generation Documentation

## Overview

Code generation is the final phase of the compilation pipeline. It transforms the validated Abstract Syntax Tree (AST) into the target output format - structured JSON representing the infrastructure configuration.

## Purpose of Code Generation

### 1. Target Representation
- Convert AST nodes to JSON structures
- Preserve semantic information from earlier phases
- Maintain relationships between resources
- Include metadata for debugging and tracing

### 2. Output Optimization
- Generate clean, readable JSON
- Remove unnecessary intermediate structures
- Optimize for human readability and machine processing
- Include optional debugging information

### 3. Integration Support
- Produce output compatible with deployment tools
- Include metadata for tool integration
- Support multiple output formats
- Enable post-processing pipelines

## Architecture Overview

### Visitor Pattern Implementation

The code generator uses the Visitor pattern to traverse the AST:

```python
class CodeGenerator(ASTVisitor):
    def __init__(self, error_handler: Optional[ErrorHandler] = None):
        self.error_handler = error_handler or ErrorHandler()
        self.output: Dict[str, Any] = {}
        self.generated_resources: Dict[str, Any] = {}
        self.generated_connections: List[Dict[str, Any]] = []
        self.generated_policies: Dict[str, Any] = {}
        # ... other collections
    
    def generate(self, ast: ProgramNode) -> str:
        """Generate JSON output from the AST."""
        self._initialize_output()
        ast.accept(self)
        self._finalize_output()
        return json.dumps(self.output, indent=2, ensure_ascii=False)
```

### Output Structure

The generated JSON follows a structured format:

```json
{
  "version": "1.0",
  "metadata": {
    "generated_at": "2024-01-15T10:30:00.000000",
    "compiler_version": "1.0.0",
    "dsl_version": "1.0.0",
    "resource_count": 5,
    "connection_count": 2,
    "policy_count": 1,
    "role_count": 1
  },
  "resources": {
    "web_server": {
      "type": "server",
      "name": "web_server",
      "attributes": { ... },
      "metadata": { ... }
    }
  },
  "connections": [ ... ],
  "policies": { ... },
  "roles": { ... },
  "modules": { ... },
  "variables": { ... },
  "constants": { ... }
}
```

## Detailed Generation Process

### 1. Resource Generation

Each resource declaration generates a structured JSON object:

```python
def visit_server(self, node: ServerNode) -> Any:
    """Generate JSON for server declaration."""
    resource_data = {
        "type": "server",
        "name": node.identifier,
        "attributes": self._generate_attributes(node.attributes),
        "metadata": {
            "line": node.line,
            "column": node.column
        }
    }
    
    self.generated_resources[node.identifier] = resource_data
    return resource_data

def _generate_attributes(self, attributes: List[AttributeNode]) -> Dict[str, Any]:
    """Generate attributes dictionary."""
    return {attr.name: self._generate_expression(attr.value) for attr in attributes}
```

### 2. Expression Generation

Expressions are recursively converted to JSON representations:

```python
def visit_literal(self, node: LiteralNode) -> Any:
    """Generate JSON for literal value."""
    return {
        "type": "literal",
        "value": node.value,
        "literal_type": node.literal_type,
        "metadata": {
            "line": node.line,
            "column": node.column
        }
    }

def visit_identifier(self, node: IdentifierNode) -> Any:
    """Generate JSON for identifier."""
    return {
        "type": "identifier",
        "name": node.name,
        "metadata": {
            "line": node.line,
            "column": node.column
        }
    }

def visit_binary_expression(self, node: BinaryExpressionNode) -> Any:
    """Generate JSON for binary expression."""
    return {
        "type": "binary_expression",
        "operator": node.operator,
        "left": self._generate_expression(node.left),
        "right": self._generate_expression(node.right),
        "metadata": {
            "line": node.line,
            "column": node.column
        }
    }
```

### 3. Connection Generation

Connections between resources are generated as separate objects:

```python
def visit_connect_statement(self, node: ConnectStatementNode) -> Any:
    """Generate JSON for connect statement."""
    connection_data = {
        "type": "connection",
        "source": self._generate_expression(node.source),
        "target": self._generate_expression(node.target),
        "attributes": self._generate_connection_attributes(node.attributes),
        "metadata": {
            "line": node.line,
            "column": node.column
        }
    }
    
    self.generated_connections.append(connection_data)
    return connection_data
```

### 4. Policy and Role Generation

Policies and roles are generated with their specific structures:

```python
def visit_policy_declaration(self, node: PolicyDeclarationNode) -> Any:
    """Generate JSON for policy declaration."""
    policy_data = {
        "type": "policy",
        "name": node.name,
        "policy_type": node.policy_type,
        "target": self._generate_expression(node.target),
        "attributes": {k: self._generate_expression(v) for k, v in node.attributes.items()},
        "metadata": {
            "line": node.line,
            "column": node.column
        }
    }
    
    self.generated_policies[node.name] = policy_data
    return policy_data
```

## Optimization Strategies

### 1. Literal Simplification

Direct values are output without wrapper objects when possible:

```python
def _simplify_literal(self, literal_data: Dict[str, Any]) -> Any:
    """Simplify literal data for cleaner JSON output."""
    if literal_data.get("type") == "literal":
        return literal_data.get("value")
    return literal_data
```

### 2. Structure Optimization

Unnecessary nesting is removed for cleaner output:

```python
class OptimizedCodeGenerator(CodeGenerator):
    def _optimize_resources(self, resources: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resources for cleaner output."""
        optimized = {}
        for name, resource in resources.items():
            optimized[name] = {
                "type": resource["type"],
                "attributes": self._simplify_attributes(resource["attributes"])
            }
        return optimized
```

### 3. Metadata Filtering

Debugging metadata can be optionally included:

```python
def _finalize_output(self):
    """Finalize output structure."""
    if not self.include_metadata:
        # Remove metadata from resources
        for resource in self.generated_resources.values():
            resource.pop("metadata", None)
        # Remove metadata from other structures
        for connection in self.generated_connections:
            connection.pop("metadata", None)
```

## Expression Mapping

### 1. Literal Mapping

| DSL Literal | JSON Representation |
|-------------|-------------------|
| `42` | `{"type": "literal", "value": 42, "literal_type": "integer"}` |
| `"hello"` | `{"type": "literal", "value": "hello", "literal_type": "string"}` |
| `true` | `{"type": "literal", "value": true, "literal_type": "boolean"}` |
| `4GB` | `{"type": "literal", "value": "4GB", "literal_type": "size"}` |

### 2. Expression Mapping

| DSL Expression | JSON Representation |
|---------------|-------------------|
| `cpu + memory` | `{"type": "binary_expression", "operator": "+", "left": {...}, "right": {...}}` |
| `web_server.cpu` | `{"type": "member_access", "object": {...}, "member": "cpu"}` |
| `servers[0]` | `{"type": "array_access", "array": {...}, "index": {...}}` |
| `range(5)` | `{"type": "function_call", "function": "range", "arguments": [...]}` |

### 3. Complex Structure Mapping

```dsl
# DSL Input
server "web_server" {
    cpu = 4
    memory = 8GB
    tags = ["web", "production"]
}
```

```json
// JSON Output
{
  "type": "server",
  "name": "web_server",
  "attributes": {
    "cpu": {
      "type": "literal",
      "value": 4,
      "literal_type": "integer"
    },
    "memory": {
      "type": "literal", 
      "value": "8GB",
      "literal_type": "size"
    },
    "tags": {
      "type": "array_literal",
      "elements": [
        {
          "type": "literal",
          "value": "web",
          "literal_type": "string"
        },
        {
          "type": "literal",
          "value": "production", 
          "literal_type": "string"
        }
      ]
    }
  }
}
```

## Error Handling

### 1. Error Propagation

Errors from earlier phases are preserved and included in output:

```python
def generate(self, ast: ProgramNode) -> str:
    """Generate JSON output from the AST."""
    try:
        self._initialize_output()
        ast.accept(self)
        self._finalize_output()
        
        # Include error information if present
        if self.error_handler.has_errors():
            self.output["compilation_errors"] = self.error_handler.export_to_json()["errors"]
        
        return json.dumps(self.output, indent=2, ensure_ascii=False)
        
    except Exception as e:
        self.error_handler.add_error(
            CodeGenerationError(f"Code generation failed: {str(e)}", -1, -1, -1)
        )
        raise
```

### 2. Partial Output Generation

Even with errors, attempt to generate partial output:

```python
def _finalize_output(self):
    """Finalize output structure, even with errors."""
    self.output["resources"] = self.generated_resources
    self.output["connections"] = self.generated_connections
    # ... other components
    
    # Add compilation status
    self.output["compilation_status"] = {
        "success": not self.error_handler.has_errors(),
        "error_count": len(self.error_handler.get_errors()),
        "warning_count": len(self.error_handler.get_warnings())
    }
```

## Output Formats

### 1. Standard Format

Complete, verbose output with all metadata:

```json
{
  "version": "1.0",
  "metadata": { ... },
  "resources": { ... },
  "connections": [ ... ],
  "policies": { ... },
  "roles": { ... },
  "modules": { ... },
  "variables": { ... },
  "constants": { ... }
}
```

### 2. Optimized Format

Clean, production-ready output:

```json
{
  "infrastructure": {
    "resources": { ... },
    "connections": [ ... ],
    "policies": { ... },
    "roles": { ... }
  },
  "configuration": { ... },
  "metadata": { ... }
}
```

### 3. Compact Format

Minimal output for machine processing:

```json
{
  "resources": { ... },
  "connections": [ ... ],
  "policies": { ... },
  "roles": { ... }
}
```

## Performance Considerations

### 1. Memory Efficiency

- **Streaming Generation**: Generate output incrementally for large ASTs
- **Node Reuse**: Share common sub-expressions
- **Garbage Collection**: Clean up intermediate structures

### 2. Generation Speed

- **Visitor Pattern**: Efficient tree traversal
- **Lazy Evaluation**: Generate JSON only when needed
- **Batch Operations**: Process similar nodes together

### 3. Output Size

- **Compression**: Optional JSON compression
- **Filtering**: Remove unnecessary metadata
- **Optimization**: Eliminate redundant information

## Testing Strategy

### 1. Unit Tests

- Individual node generation testing
- Expression mapping validation
- Error handling verification
- Output format compliance

### 2. Integration Tests

- Complete AST traversal
- Complex structure generation
- Multi-resource scenarios
- Error case handling

### 3. Output Validation

- JSON schema validation
- Format compliance checking
- Content accuracy verification
- Performance benchmarking

## Future Extensions

### 1. Multiple Output Formats

- **YAML Output**: For YAML-based tools
- **XML Output**: For enterprise integration
- **Terraform HCL**: For Terraform compatibility
- **CloudFormation**: For AWS integration

### 2. Advanced Optimization

- **Constant Folding**: Evaluate expressions at generation time
- **Dead Code Elimination**: Remove unused resources
- **Resource Merging**: Combine compatible resources
- **Dependency Optimization**: Reorder for efficiency

### 3. Tool Integration

- **Direct Deployment**: Generate deployment-ready configurations
- **Validation Integration**: Include deployment-time validation
- **Monitoring Integration**: Add monitoring configurations
- **Cost Analysis**: Include cost estimation data

## Example Transformations

### Simple Resource

```dsl
// DSL Input
server "web" {
    cpu = 4
    memory = 8GB
}
```

```json
// JSON Output
{
  "type": "server",
  "name": "web",
  "attributes": {
    "cpu": {"type": "literal", "value": 4, "literal_type": "integer"},
    "memory": {"type": "literal", "value": "8GB", "literal_type": "size"}
  },
  "metadata": {"line": 2, "column": 1}
}
```

### Complex Module

```dsl
// DSL Input
module web_cluster {
    param server_count = 3
    
    for i in range(server_count) {
        server "web_${i}" {
            cpu = 4
            memory = 8GB
        }
    }
}
```

```json
// JSON Output
{
  "type": "module_definition",
  "name": "web_cluster",
  "parameters": [
    {
      "name": "server_count",
      "default_value": {"type": "literal", "value": 3, "literal_type": "integer"}
    }
  ],
  "statements": [
    {
      "type": "loop",
      "variable": "i",
      "iterable": {
        "type": "function_call",
        "function": "range",
        "arguments": [{"type": "identifier", "name": "server_count"}]
      },
      "body": {
        "type": "block",
        "statements": [/* server declarations */]
      }
    }
  ]
}
```

The code generation phase transforms the validated AST into a structured, machine-readable JSON representation that preserves all semantic information while optimizing for readability and integration with deployment tools.
