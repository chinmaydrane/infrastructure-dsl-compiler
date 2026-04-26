# Semantic Analysis Documentation

## Overview

Semantic analysis is the third phase of the compilation pipeline, following lexical analysis and parsing. While lexical analysis ensures the source code follows lexical rules and parsing ensures it follows syntactic rules, semantic analysis ensures the program follows the semantic rules of the language.

## Purpose of Semantic Analysis

### 1. Type Checking
- Verify that operations are performed on compatible types
- Ensure function calls have correct parameter types
- Validate attribute assignments match expected types
- Check array indices are integers

### 2. Reference Validation
- Ensure all identifiers are declared before use
- Validate resource references exist
- Check function calls reference defined functions
- Verify module references are valid

### 3. Constraint Validation
- Enforce business rules and limits
- Validate autoscaling constraints (min ≤ max)
- Check required attributes are present
- Verify relationship constraints

### 4. Scope Management
- Handle variable and parameter scoping
- Manage nested scopes in blocks and functions
- Ensure proper symbol visibility
- Detect shadowing and conflicts

### 5. Duplicate Detection
- Identify duplicate resource definitions
- Check for conflicting declarations
- Detect multiple definitions of the same symbol
- Validate unique names within scopes

## Implementation Architecture

### Symbol Table Design

The symbol table is the core data structure for semantic analysis:

```python
class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global", level=0)
        self.current_scope = self.global_scope
        self.all_scopes: List[Scope] = [self.global_scope]
    
    def enter_scope(self, scope_name: str) -> Scope:
        """Enter a new nested scope."""
        new_scope = Scope(
            scope_name=scope_name,
            parent=self.current_scope,
            level=self.current_scope.level + 1
        )
        self.current_scope = new_scope
        self.all_scopes.append(new_scope)
        return new_scope
    
    def define_symbol(self, name: str, symbol_type: SymbolType, 
                     type_info: TypeInfo, line: int, column: int) -> bool:
        """Define a symbol in the current scope."""
        symbol = Symbol(name, symbol_type, type_info, line, column)
        return self.current_scope.define_symbol(symbol)
    
    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in the current and parent scopes."""
        return self.current_scope.lookup_symbol(name)
```

### Type System

The type system provides a framework for type checking:

```python
class DataType(Enum):
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    SIZE = "size"
    NULL = "null"
    ARRAY = "array"
    OBJECT = "object"
    RESOURCE_REFERENCE = "resource_reference"
    FUNCTION_TYPE = "function_type"
    UNKNOWN = "unknown"

@dataclass
class TypeInfo:
    data_type: DataType
    element_type: Optional[DataType] = None  # For arrays
    properties: Optional[Dict[str, 'TypeInfo']] = None  # For objects
    parameters: Optional[List['TypeInfo']] = None  # For functions
    return_type: Optional['TypeInfo'] = None  # For functions
```

### Two-Pass Analysis

The semantic analyzer uses a two-pass approach:

#### Pass 1: Symbol Collection
- Traverse the AST and collect all symbol declarations
- Build the symbol table with scopes and type information
- No validation performed in this pass

#### Pass 2: Validation
- Traverse the AST again and perform all validations
- Use the populated symbol table for reference resolution
- Generate comprehensive error reports

## Detailed Analysis Algorithms

### 1. Resource Declaration Analysis

```python
def analyze_resource_declaration(self, node: ResourceDeclarationNode):
    """Analyze a resource declaration."""
    
    # Check for duplicate resources
    if node.identifier in self.defined_resources:
        self.error_handler.add_error(
            SemanticError(f"Duplicate resource declaration: {node.identifier}", 
                         node.line, node.column, -1)
        )
        return
    
    # Create resource type info
    resource_type = TypeInfo(DataType.OBJECT)
    
    # Define resource symbol
    if not self.symbol_table.define_symbol(
        node.identifier, SymbolType.SERVER, resource_type, node.line, node.column
    ):
        self.error_handler.add_error(
            SemanticError(f"Resource already defined: {node.identifier}", 
                         node.line, node.column, -1)
        )
        return
    
    self.defined_resources[node.identifier] = node
    
    # Validate attributes
    for attr in node.attributes:
        self.analyze_attribute(attr, node.resource_type)
```

### 2. Attribute Type Checking

```python
def analyze_attribute(self, attr: AttributeNode, resource_type: str):
    """Analyze and validate an attribute."""
    
    # Infer the type of the attribute value
    value_type = self.infer_expression_type(attr.value)
    
    # Check if the attribute is valid for this resource type
    if not self.type_checker.check_attribute_type(resource_type, attr.name, value_type):
        self.error_handler.add_error(
            SemanticError(f"Invalid attribute '{attr.name}' for {resource_type}", 
                         attr.line, attr.column, -1)
        )
    
    # Analyze the attribute value expression
    attr.value.accept(self._Validator(self))
```

### 3. Expression Type Inference

```python
def infer_expression_type(self, expression: ExpressionNode) -> TypeInfo:
    """Infer the type of an expression."""
    
    if isinstance(expression, LiteralNode):
        return TypeInfo(self._literal_to_data_type(expression.literal_type))
    
    elif isinstance(expression, IdentifierNode):
        symbol = self.symbol_table.lookup_symbol(expression.name)
        return symbol.type_info if symbol else TypeInfo(DataType.UNKNOWN)
    
    elif isinstance(expression, BinaryExpressionNode):
        return self.infer_binary_expression_type(expression)
    
    elif isinstance(expression, FunctionCallNode):
        symbol = self.symbol_table.lookup_symbol(expression.function_name)
        return symbol.type_info.return_type if symbol else TypeInfo(DataType.UNKNOWN)
    
    elif isinstance(expression, ArrayLiteralNode):
        if expression.elements:
            element_type = self.infer_expression_type(expression.elements[0])
            return TypeInfo(DataType.ARRAY, element_type=element_type)
        else:
            return TypeInfo(DataType.ARRAY, element_type=DataType.UNKNOWN)
    
    else:
        return TypeInfo(DataType.UNKNOWN)
```

### 4. Binary Expression Type Inference

```python
def infer_binary_expression_type(self, expr: BinaryExpressionNode) -> TypeInfo:
    """Infer the type of a binary expression."""
    
    left_type = self.infer_expression_type(expr.left)
    right_type = self.infer_expression_type(expr.right)
    
    if expr.operator in ['+', '-', '*', '/', '%']:
        # Arithmetic operations
        if left_type.data_type == DataType.FLOAT or right_type.data_type == DataType.FLOAT:
            return TypeInfo(DataType.FLOAT)
        elif left_type.data_type == DataType.INTEGER and right_type.data_type == DataType.INTEGER:
            return TypeInfo(DataType.INTEGER)
        else:
            return TypeInfo(DataType.UNKNOWN)
    
    elif expr.operator in ['==', '!=', '<', '<=', '>', '>=']:
        # Comparison operations
        return TypeInfo(DataType.BOOLEAN)
    
    elif expr.operator in ['and', 'or']:
        # Logical operations
        return TypeInfo(DataType.BOOLEAN)
    
    else:
        return TypeInfo(DataType.UNKNOWN)
```

### 5. Reference Validation

```python
def validate_resource_reference(self, identifier: str, line: int, column: int):
    """Validate that a resource reference exists."""
    
    if identifier not in self.defined_resources:
        self.error_handler.add_error(
            SemanticError(f"Undefined resource reference: {identifier}", 
                         line, column, -1)
        )
        return False
    return True
```

### 6. Scope Management

```python
def analyze_if_statement(self, node: IfStatementNode):
    """Analyze an if statement with proper scope handling."""
    
    # Enter new scope for if statement
    old_scope = self.current_scope
    self.current_scope = self.symbol_table.enter_scope("if")
    
    # Validate condition type
    condition_type = self.infer_expression_type(node.condition)
    if condition_type.data_type != DataType.BOOLEAN:
        self.error_handler.add_error(
            SemanticError("If condition must be boolean", 
                         node.condition.line, node.condition.column, -1)
        )
    
    # Visit condition
    node.condition.accept(self._Validator(self))
    
    # Visit then block
    node.then_block.accept(self._Validator(self))
    
    # Exit if scope for then block
    self.symbol_table.exit_scope()
    
    # Visit else block if present
    if node.else_block:
        self.current_scope = self.symbol_table.enter_scope("else")
        node.else_block.accept(self._Validator(self))
        self.symbol_table.exit_scope()
    
    self.current_scope = old_scope
```

## Error Handling

### Error Classification

1. **Type Errors**: Mismatched types, invalid operations
2. **Reference Errors**: Undefined identifiers, invalid references
3. **Scope Errors**: Variable not in scope, duplicate declarations
4. **Constraint Errors**: Business rule violations
5. **Semantic Errors**: General semantic rule violations

### Error Recovery Strategies

1. **Continue Compilation**: Don't stop at first error
2. **Skip to Next Statement**: Recover from local errors
3. **Assume Unknown Type**: Continue with placeholder types
4. **Record Multiple Errors**: Report all issues at once

### Error Message Format

```
[ERROR] Line 15, Column 10: Type mismatch in assignment
   server "web_server" {
       cpu = "not_a_number"
              ^^^^^^^^^^^^^^^
   Expected: integer, got: string
```

## Type Checking Rules

### 1. Primitive Type Compatibility

| Source Type | Target Type | Compatible |
|-------------|-------------|-------------|
| integer     | integer     | Yes |
| integer     | float       | Yes (promotion) |
| float       | float       | Yes |
| float       | integer     | No |
| string      | string      | Yes |
| boolean     | boolean     | Yes |
| size        | size        | Yes |
| null        | any reference | Yes |

### 2. Array Type Rules

- Array elements must have compatible types
- Array access must use integer index
- Array concatenation requires same element types

### 3. Object Type Rules

- Object property access must use valid property names
- Property types must match expected types
- Objects can be extended with additional properties

### 4. Function Type Rules

- Function calls must match parameter count
- Argument types must be compatible with parameter types
- Return type must match expected context

## Validation Rules

### 1. Resource Validation

```python
RESOURCE_ATTRIBUTES = {
    "server": {
        "cpu": TypeInfo(DataType.INTEGER),
        "memory": TypeInfo(DataType.SIZE),
        "os": TypeInfo(DataType.STRING),
        "enabled": TypeInfo(DataType.BOOLEAN),
        "tags": TypeInfo(DataType.ARRAY, element_type=DataType.STRING),
    },
    "database": {
        "engine": TypeInfo(DataType.STRING),
        "version": TypeInfo(DataType.STRING),
        "storage": TypeInfo(DataType.SIZE),
        "instance_class": TypeInfo(DataType.STRING),
        "multi_az": TypeInfo(DataType.BOOLEAN),
    },
    # ... more resource types
}
```

### 2. Policy Validation

- Autoscaling policies must have min_instances ≤ max_instances
- Security policies must reference valid resources
- Backup policies must have valid retention periods

### 3. Role Validation

- Role permissions must follow naming conventions
- Role resources must exist or be wildcards
- Role assignments must reference valid roles

### 4. Connection Validation

- Connection sources and targets must exist
- Connection protocols must be valid strings
- Connection ports must be valid integers or strings

## Performance Considerations

### 1. Symbol Table Optimization

- **Hash-based Lookup**: O(1) average case for symbol lookup
- **Scope Chaining**: Efficient parent scope traversal
- **Lazy Evaluation**: Compute information only when needed

### 2. Type Inference Caching

- **Memoization**: Cache inferred types for expressions
- **Shared Subexpressions**: Reuse type information for duplicate expressions
- **Incremental Updates**: Update types only when dependencies change

### 3. Memory Management

- **Scope Cleanup**: Remove symbols when scopes are exited
- **Reference Counting**: Manage AST node lifetimes
- **Garbage Collection**: Clean up unused type information

## Testing Strategy

### 1. Unit Tests

- Individual component testing
- Type inference algorithm testing
- Symbol table operation testing
- Error condition testing

### 2. Integration Tests

- Complete semantic analysis pipeline
- Complex expression type checking
- Multi-scope validation
- Error recovery testing

### 3. Regression Tests

- Known error cases
- Edge case validation
- Performance regression
- Memory leak detection

## Future Extensions

### 1. Advanced Type Features

- **Generic Types**: Parameterized types for templates
- **Type Aliases**: Named type definitions
- **Union Types**: Values of multiple possible types
- **Type Constraints**: User-defined type rules

### 2. Enhanced Validation

- **Custom Validators**: User-defined validation rules
- **Policy Engines**: Complex policy validation
- **Dependency Analysis**: Automatic dependency detection
- **Impact Analysis**: Change impact validation

### 3. Optimization Opportunities

- **Constant Folding**: Evaluate constant expressions
- **Dead Code Elimination**: Remove unreachable code
- **Type Specialization**: Optimize based on known types
- **Inline Expansion**: Replace function calls with bodies

This semantic analysis system provides comprehensive validation of DSL programs, ensuring type safety, reference correctness, and constraint satisfaction before code generation.
