# AST Design Documentation

## Overview

The Abstract Syntax Tree (AST) is a hierarchical representation of the DSL source code that abstracts away syntactic details and focuses on the semantic structure. This document describes the design and implementation of the AST for the Infrastructure DSL.

## AST Design Principles

### 1. Hierarchical Structure
The AST follows a tree structure where each node represents a language construct. Parent-child relationships represent containment and scope.

### 2. Type Safety
Each node type is strongly typed to ensure semantic correctness during compilation phases.

### 3. Visitor Pattern
The AST implements the Visitor pattern to enable operations to be performed on the tree structure without modifying the node classes.

### 4. Extensibility
The design allows for easy addition of new node types and operations.

## AST Node Hierarchy

```
ASTNode (Abstract Base Class)
├── ProgramNode
├── CompilationUnitNode
├── ResourceDeclarationNode
│   ├── ServerNode
│   ├── NetworkNode
│   ├── DatabaseNode
│   ├── SecurityGroupNode
│   ├── LoadBalancerNode
│   ├── CacheNode
│   ├── ContainerNode
│   ├── FunctionResourceNode
│   └── SubnetNode
├── ControlFlowNode
│   ├── IfStatementNode
│   └── ForStatementNode
├── DeclarationNode
│   ├── FunctionDeclarationNode
│   ├── ModuleDeclarationNode
│   ├── VariableDeclarationNode
│   ├── ConstantDeclarationNode
│   ├── RoleDeclarationNode
│   └── PolicyDeclarationNode
├── StatementNode
│   ├── AssignmentNode
│   ├── UseStatementNode
│   ├── ConnectStatementNode
│   ├── AttachStatementNode
│   └── AssignRoleStatementNode
├── ExpressionNode
│   ├── BinaryExpressionNode
│   ├── UnaryExpressionNode
│   ├── ConditionalExpressionNode
│   ├── FunctionCallNode
│   ├── MemberAccessNode
│   ├── ArrayAccessNode
│   ├── LiteralNode
│   ├── IdentifierNode
│   ├── ObjectLiteralNode
│   └── ArrayLiteralNode
├── ComponentNode
│   ├── AttributeNode
│   ├── ParameterNode
│   ├── ObjectPropertyNode
│   ├── ConnectionAttributeNode
│   └── CommentNode
└── BlockNode
```

## Node Categories

### 1. Structural Nodes

#### ProgramNode
- **Purpose**: Root node representing the entire program
- **Children**: List of CompilationUnitNode
- **Properties**: compilation_units

#### CompilationUnitNode
- **Purpose**: Represents a top-level statement
- **Children**: Single statement node
- **Properties**: statement

#### BlockNode
- **Purpose**: Represents a block of statements
- **Children**: List of statement nodes
- **Properties**: statements

### 2. Resource Declaration Nodes

#### ResourceDeclarationNode (Abstract)
- **Purpose**: Base class for all resource declarations
- **Properties**: resource_type, identifier, attributes
- **Children**: AttributeNode list

#### ServerNode
- **Purpose**: Server resource declaration
- **Resource Type**: "server"
- **Common Attributes**: cpu, memory, os, tags, enabled

#### NetworkNode
- **Purpose**: Network resource declaration
- **Resource Type**: "network"
- **Common Attributes**: cidr_block, enable_dns_hostnames, tags

#### DatabaseNode
- **Purpose**: Database resource declaration
- **Resource Type**: "database" or "nosql_db"
- **Common Attributes**: engine, version, storage, instance_class

### 3. Control Flow Nodes

#### IfStatementNode
- **Purpose**: Conditional statement
- **Properties**: condition, then_block, else_block (optional)
- **Children**: Condition expression, then block, optional else block

#### ForStatementNode
- **Purpose**: Loop statement
- **Properties**: variable, iterable, body
- **Children**: Iterable expression, body block

### 4. Expression Nodes

#### BinaryExpressionNode
- **Purpose**: Binary operations
- **Properties**: left, operator, right
- **Operators**: +, -, *, /, %, **, ==, !=, <, <=, >, >=, and, or

#### UnaryExpressionNode
- **Purpose**: Unary operations
- **Properties**: operator, operand
- **Operators: -, +, not

#### FunctionCallNode
- **Purpose**: Function invocation
- **Properties**: function_name, arguments
- **Children**: Argument expressions

#### MemberAccessNode
- **Purpose**: Object property access
- **Properties**: object_expr, member
- **Example**: server.cpu

#### ArrayAccessNode
- **Purpose**: Array element access
- **Properties**: array_expr, index
- **Example**: servers[0]

### 5. Literal Nodes

#### LiteralNode
- **Purpose**: Literal values
- **Properties**: value, literal_type
- **Types**: integer, float, string, boolean, size, null

#### IdentifierNode
- **Purpose**: Variable/resource names
- **Properties**: name

#### ObjectLiteralNode
- **Purpose**: Object literals
- **Properties**: properties
- **Children**: ObjectPropertyNode list

#### ArrayLiteralNode
- **Purpose**: Array literals
- **Properties**: elements
- **Children**: ExpressionNode list

## Example Parse Trees

### Example 1: Simple Resource Declaration

**DSL Code:**
```
server "web_server" {
    cpu = 4
    memory = 8GB
}
```

**Parse Tree:**
```
ProgramNode
└── CompilationUnitNode
    └── ServerNode
        ├── Identifier: "web_server"
        └── AttributeNode List
            ├── AttributeNode
            │   ├── Name: "cpu"
            │   └── LiteralNode: 4
            └── AttributeNode
                ├── Name: "memory"
                └── LiteralNode: 8GB
```

**AST Structure:**
```
ProgramNode
└── CompilationUnitNode
    └── ServerNode
        ├── resource_type: "server"
        ├── identifier: "web_server"
        └── attributes: [
            AttributeNode(name="cpu", value=LiteralNode(4)),
            AttributeNode(name="memory", value=LiteralNode("8GB"))
        ]
```

### Example 2: Conditional Statement

**DSL Code:**
```
if environment == "production" {
    server "web_server" {
        cpu = 8
        memory = 16GB
    }
} else {
    server "web_server" {
        cpu = 2
        memory = 4GB
    }
}
```

**AST Structure:**
```
IfStatementNode
├── condition: BinaryExpressionNode
│   ├── left: IdentifierNode("environment")
│   ├── operator: "=="
│   └── right: LiteralNode("production")
├── then_block: BlockNode
│   └── statements: [
│       ServerNode(resource_type="server", identifier="web_server", attributes=[
│           AttributeNode(name="cpu", value=LiteralNode(8)),
│           AttributeNode(name="memory", value=LiteralNode("16GB"))
│       ])
│   ]
└── else_block: BlockNode
    └── statements: [
        ServerNode(resource_type="server", identifier="web_server", attributes=[
            AttributeNode(name="cpu", value=LiteralNode(2)),
            AttributeNode(name="memory", value=LiteralNode("4GB"))
        ])
    ]
```

### Example 3: Complex Expression

**DSL Code:**
```
connect web_server -> database {
    protocol = "tcp"
    port = 3306
}
```

**AST Structure:**
```
ConnectStatementNode
├── source: IdentifierNode("web_server")
├── target: IdentifierNode("database")
└── attributes: [
    ConnectionAttributeNode(name="protocol", value=LiteralNode("tcp")),
    ConnectionAttributeNode(name="port", value=LiteralNode(3306))
]
```

### Example 4: Function Call

**DSL Code:**
```
use web_cluster with {
    server_count = 5
    cpu_per_server = 8
}
```

**AST Structure:**
```
UseStatementNode
├── module_name: "web_cluster"
└── arguments: ObjectLiteralNode
    └── properties: [
        ObjectPropertyNode(key="server_count", value=LiteralNode(5)),
        ObjectPropertyNode(key="cpu_per_server", value=LiteralNode(8))
    ]
```

## AST Construction Process

### 1. Token Recognition
The lexer identifies tokens and their types with position information.

### 2. Parse Tree Generation
The parser builds a parse tree following the grammar rules.

### 3. AST Transformation
The parse tree is transformed into an AST by:
- Removing syntactic noise (parentheses, commas, etc.)
- Grouping related constructs
- Creating semantic nodes
- Preserving essential information

### 4. Node Creation
Each language construct maps to a specific node type:
- Resource declarations → ResourceDeclarationNode subclasses
- Expressions → ExpressionNode subclasses
- Statements → StatementNode subclasses
- Control flow → ControlFlowNode subclasses

## AST Properties

### 1. Position Information
Each node maintains:
- Line number in source code
- Column number
- Character position

### 2. Type Information
Nodes carry semantic type information:
- Expression types
- Resource types
- Attribute types

### 3. Scope Information
Nodes maintain scope relationships:
- Parent-child scope
- Symbol table references
- Visibility rules

## Visitor Pattern Implementation

### 1. Visitor Interface
The ASTVisitor interface defines visit methods for each node type.

### 2. Double Dispatch
Each node implements an accept() method that calls the appropriate visitor method.

### 3. Operations
Common operations implemented via visitors:
- Semantic analysis
- Type checking
- Code generation
- Optimization
- Pretty printing

## AST Optimization Opportunities

### 1. Constant Folding
Evaluate constant expressions at compile time:
```
cpu = 2 + 4  →  cpu = 6
```

### 2. Dead Code Elimination
Remove unreachable code:
```
if false { ... }  →  (removed)
```

### 3. Expression Simplification
Simplify complex expressions:
```
not (x == y)  →  x != y
```

## AST Validation

### 1. Structural Validation
- Node relationships are correct
- Required children are present
- No circular references

### 2. Type Validation
- Expression types are compatible
- Attribute types match resource definitions
- Function signatures are correct

### 3. Semantic Validation
- References are resolved
- Scopes are properly nested
- Constraints are satisfied

## AST Serialization

### 1. JSON Format
The AST can be serialized to JSON for:
- Debugging
- Visualization
- Interoperability

### 2. Custom Format
Custom serialization formats for:
- Compact storage
- Fast loading
- Tool integration

## AST Visualization

### 1. Tree Diagrams
Visual representation of AST structure:
- Graphviz DOT format
- ASCII art
- Interactive viewers

### 2. Debug Output
Human-readable AST representation:
- Indented text format
- Pretty printing
- Syntax highlighting

## Performance Considerations

### 1. Memory Usage
- Node object overhead
- Child list management
- Reference handling

### 2. Construction Time
- Node creation overhead
- Tree building algorithms
- Memory allocation patterns

### 3. Traversal Performance
- Visitor pattern overhead
- Recursive vs. iterative traversal
- Cache-friendly data structures

## Future Extensions

### 1. New Node Types
- Additional resource types
- New language constructs
- Extended expression types

### 2. Enhanced Visitors
- Advanced optimization passes
- Additional analysis phases
- Code generation for multiple targets

### 3. Tool Integration
- IDE support
- Debuggers
- Profilers

This AST design provides a solid foundation for the compiler's semantic analysis and code generation phases while maintaining flexibility for future extensions and optimizations.
