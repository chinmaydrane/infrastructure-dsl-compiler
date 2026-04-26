"""
AST Node Definitions for Infrastructure DSL

This module defines all Abstract Syntax Tree (AST) node classes used in the compiler.
Each node represents a specific construct in the DSL language.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Enumeration of all AST node types."""
    
    # Program structure
    PROGRAM = "program"
    COMPILATION_UNIT = "compilation_unit"
    
    # Statements
    RESOURCE_DECLARATION = "resource_declaration"
    NETWORK_DECLARATION = "network_declaration"
    DATABASE_DECLARATION = "database_declaration"
    SECURITY_GROUP_DECLARATION = "security_group_declaration"
    LOAD_BALANCER_DECLARATION = "load_balancer_declaration"
    CACHE_DECLARATION = "cache_declaration"
    CONTAINER_DECLARATION = "container_declaration"
    FUNCTION_RESOURCE_DECLARATION = "function_resource_declaration"
    SUBNET_DECLARATION = "subnet_declaration"
    
    # Control flow
    IF_STATEMENT = "if_statement"
    FOR_STATEMENT = "for_statement"
    
    # Declarations
    FUNCTION_DECLARATION = "function_declaration"
    MODULE_DECLARATION = "module_declaration"
    VARIABLE_DECLARATION = "variable_declaration"
    CONSTANT_DECLARATION = "constant_declaration"
    ROLE_DECLARATION = "role_declaration"
    POLICY_DECLARATION = "policy_declaration"
    
    # Statements
    ASSIGNMENT = "assignment"
    USE_STATEMENT = "use_statement"
    CONNECT_STATEMENT = "connect_statement"
    ATTACH_STATEMENT = "attach_statement"
    ASSIGN_ROLE_STATEMENT = "assign_role_statement"
    
    # Expressions
    BINARY_EXPRESSION = "binary_expression"
    UNARY_EXPRESSION = "unary_expression"
    CONDITIONAL_EXPRESSION = "conditional_expression"
    FUNCTION_CALL = "function_call"
    MEMBER_ACCESS = "member_access"
    ARRAY_ACCESS = "array_access"
    
    # Literals
    LITERAL = "literal"
    IDENTIFIER = "identifier"
    OBJECT_LITERAL = "object_literal"
    ARRAY_LITERAL = "array_literal"
    
    # Components
    ATTRIBUTE = "attribute"
    PARAMETER = "parameter"
    OBJECT_PROPERTY = "object_property"
    CONNECTION_ATTRIBUTE = "connection_attribute"
    
    # Special
    BLOCK = "block"
    COMMENT = "comment"


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    def __init__(self, node_type: NodeType, line: int = -1, column: int = -1):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.children: List['ASTNode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Accept a visitor for double dispatch pattern."""
        pass
    
    def add_child(self, child: 'ASTNode'):
        """Add a child node."""
        if child:
            self.children.append(child)
    
    def get_children(self) -> List['ASTNode']:
        """Get all child nodes."""
        return self.children
    
    def to_string(self, indent: int = 0) -> str:
        """Convert node to string representation."""
        indent_str = "  " * indent
        result = f"{indent_str}{self.node_type.value}"
        
        if hasattr(self, 'value'):
            result += f": {self.value}"
        elif hasattr(self, 'name'):
            result += f": {self.name}"
        elif hasattr(self, 'identifier'):
            result += f": {self.identifier}"
        
        result += f" (line: {self.line}, col: {self.column})"
        
        for child in self.children:
            result += "\n" + child.to_string(indent + 1)
        
        return result


class ProgramNode(ASTNode):
    """Root node of the AST."""
    
    def __init__(self, line: int = -1, column: int = -1):
        super().__init__(NodeType.PROGRAM, line, column)
        self.compilation_units: List[CompilationUnitNode] = []
    
    def add_compilation_unit(self, unit: 'CompilationUnitNode'):
        """Add a compilation unit."""
        self.compilation_units.append(unit)
        self.add_child(unit)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_program(self)


class CompilationUnitNode(ASTNode):
    """Represents a compilation unit (top-level statement)."""
    
    def __init__(self, statement: ASTNode, line: int = -1, column: int = -1):
        super().__init__(NodeType.COMPILATION_UNIT, line, column)
        self.statement = statement
        self.add_child(statement)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_compilation_unit(self)


# Resource Declaration Nodes

class ResourceDeclarationNode(ASTNode):
    """Base class for resource declarations."""
    
    def __init__(self, resource_type: str, identifier: str, 
                 attributes: List['AttributeNode'], line: int = -1, column: int = -1):
        super().__init__(NodeType.RESOURCE_DECLARATION, line, column)
        self.resource_type = resource_type
        self.identifier = identifier
        self.attributes = attributes
        
        for attr in attributes:
            self.add_child(attr)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_resource_declaration(self)


class ServerNode(ResourceDeclarationNode):
    """Server resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("server", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_server(self)


class NetworkNode(ResourceDeclarationNode):
    """Network resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("network", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_network(self)


class DatabaseNode(ResourceDeclarationNode):
    """Database resource declaration."""
    
    def __init__(self, database_type: str, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__(database_type, identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_database(self)


class SecurityGroupNode(ResourceDeclarationNode):
    """Security group resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("security_group", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_security_group(self)


class LoadBalancerNode(ResourceDeclarationNode):
    """Load balancer resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("load_balancer", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_load_balancer(self)


class CacheNode(ResourceDeclarationNode):
    """Cache resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("cache", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_cache(self)


class ContainerNode(ResourceDeclarationNode):
    """Container resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("container", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_container(self)


class FunctionResourceNode(ResourceDeclarationNode):
    """Function resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("function", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_resource(self)


class SubnetNode(ResourceDeclarationNode):
    """Subnet resource declaration."""
    
    def __init__(self, identifier: str, attributes: List['AttributeNode'], 
                 line: int = -1, column: int = -1):
        super().__init__("subnet", identifier, attributes, line, column)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_subnet(self)


# Control Flow Nodes

class IfStatementNode(ASTNode):
    """If statement node."""
    
    def __init__(self, condition: 'ExpressionNode', then_block: 'BlockNode', 
                 else_block: Optional['BlockNode'] = None, line: int = -1, column: int = -1):
        super().__init__(NodeType.IF_STATEMENT, line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
        
        self.add_child(condition)
        self.add_child(then_block)
        if else_block:
            self.add_child(else_block)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_if_statement(self)


class ForStatementNode(ASTNode):
    """For statement node."""
    
    def __init__(self, variable: str, iterable: 'ExpressionNode', body: 'BlockNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.FOR_STATEMENT, line, column)
        self.variable = variable
        self.iterable = iterable
        self.body = body
        
        self.add_child(iterable)
        self.add_child(body)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_for_statement(self)


class BlockNode(ASTNode):
    """Block node containing statements."""
    
    def __init__(self, statements: List[ASTNode], line: int = -1, column: int = -1):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements
        
        for stmt in statements:
            self.add_child(stmt)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_block(self)


# Declaration Nodes

class FunctionDeclarationNode(ASTNode):
    """Function declaration node."""
    
    def __init__(self, name: str, parameters: List['ParameterNode'], 
                 body: 'BlockNode', return_expression: 'ExpressionNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.FUNCTION_DECLARATION, line, column)
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_expression = return_expression
        
        for param in parameters:
            self.add_child(param)
        self.add_child(body)
        self.add_child(return_expression)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_declaration(self)


class ModuleDeclarationNode(ASTNode):
    """Module declaration node."""
    
    def __init__(self, name: str, parameters: List['ParameterNode'], 
                 statements: List[ASTNode], line: int = -1, column: int = -1):
        super().__init__(NodeType.MODULE_DECLARATION, line, column)
        self.name = name
        self.parameters = parameters
        self.statements = statements
        
        for param in parameters:
            self.add_child(param)
        for stmt in statements:
            self.add_child(stmt)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_module_declaration(self)


class VariableDeclarationNode(ASTNode):
    """Variable declaration node."""
    
    def __init__(self, name: str, var_type: str, default_value: Optional['ExpressionNode'] = None, 
                 description: Optional[str] = None, line: int = -1, column: int = -1):
        super().__init__(NodeType.VARIABLE_DECLARATION, line, column)
        self.name = name
        self.var_type = var_type
        self.default_value = default_value
        self.description = description
        
        if default_value:
            self.add_child(default_value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_variable_declaration(self)


class ConstantDeclarationNode(ASTNode):
    """Constant declaration node."""
    
    def __init__(self, name: str, value: 'ExpressionNode', line: int = -1, column: int = -1):
        super().__init__(NodeType.CONSTANT_DECLARATION, line, column)
        self.name = name
        self.value = value
        self.add_child(value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_constant_declaration(self)


class RoleDeclarationNode(ASTNode):
    """Role declaration node."""
    
    def __init__(self, name: str, permissions: List['ExpressionNode'], 
                 resources: List['ExpressionNode'], conditions: Optional['ObjectLiteralNode'] = None, 
                 description: Optional[str] = None, line: int = -1, column: int = -1):
        super().__init__(NodeType.ROLE_DECLARATION, line, column)
        self.name = name
        self.permissions = permissions
        self.resources = resources
        self.conditions = conditions
        self.description = description
        
        for perm in permissions:
            self.add_child(perm)
        for res in resources:
            self.add_child(res)
        if conditions:
            self.add_child(conditions)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_role_declaration(self)


class PolicyDeclarationNode(ASTNode):
    """Policy declaration node."""
    
    def __init__(self, name: str, policy_type: str, target: 'ExpressionNode', 
                 attributes: Dict[str, 'ExpressionNode'], line: int = -1, column: int = -1):
        super().__init__(NodeType.POLICY_DECLARATION, line, column)
        self.name = name
        self.policy_type = policy_type
        self.target = target
        self.attributes = attributes
        
        self.add_child(target)
        for attr_value in attributes.values():
            self.add_child(attr_value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_policy_declaration(self)


# Statement Nodes

class AssignmentNode(ASTNode):
    """Assignment statement node."""
    
    def __init__(self, identifier: str, value: 'ExpressionNode', line: int = -1, column: int = -1):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.identifier = identifier
        self.value = value
        self.add_child(value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_assignment(self)


class UseStatementNode(ASTNode):
    """Use statement node."""
    
    def __init__(self, module_name: str, arguments: 'ObjectLiteralNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.USE_STATEMENT, line, column)
        self.module_name = module_name
        self.arguments = arguments
        self.add_child(arguments)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_use_statement(self)


class ConnectStatementNode(ASTNode):
    """Connect statement node."""
    
    def __init__(self, source: 'ExpressionNode', target: 'ExpressionNode', 
                 attributes: List['ConnectionAttributeNode'], line: int = -1, column: int = -1):
        super().__init__(NodeType.CONNECT_STATEMENT, line, column)
        self.source = source
        self.target = target
        self.attributes = attributes
        
        self.add_child(source)
        self.add_child(target)
        for attr in attributes:
            self.add_child(attr)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_connect_statement(self)


class AttachStatementNode(ASTNode):
    """Attach statement node."""
    
    def __init__(self, source: 'ExpressionNode', target: 'ExpressionNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.ATTACH_STATEMENT, line, column)
        self.source = source
        self.target = target
        
        self.add_child(source)
        self.add_child(target)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_attach_statement(self)


class AssignRoleStatementNode(ASTNode):
    """Assign role statement node."""
    
    def __init__(self, role_name: str, user_type: str, user_identifier: str, 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.ASSIGN_ROLE_STATEMENT, line, column)
        self.role_name = role_name
        self.user_type = user_type  # 'user', 'group', or 'role'
        self.user_identifier = user_identifier
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_assign_role_statement(self)


# Expression Nodes

class BinaryExpressionNode(ASTNode):
    """Binary expression node."""
    
    def __init__(self, left: 'ExpressionNode', operator: str, right: 'ExpressionNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.BINARY_EXPRESSION, line, column)
        self.left = left
        self.operator = operator
        self.right = right
        
        self.add_child(left)
        self.add_child(right)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_binary_expression(self)


class UnaryExpressionNode(ASTNode):
    """Unary expression node."""
    
    def __init__(self, operator: str, operand: 'ExpressionNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.UNARY_EXPRESSION, line, column)
        self.operator = operator
        self.operand = operand
        self.add_child(operand)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_unary_expression(self)


class ConditionalExpressionNode(ASTNode):
    """Conditional expression node."""
    
    def __init__(self, condition: 'ExpressionNode', then_expr: 'ExpressionNode', 
                 else_expr: Optional['ExpressionNode'] = None, line: int = -1, column: int = -1):
        super().__init__(NodeType.CONDITIONAL_EXPRESSION, line, column)
        self.condition = condition
        self.then_expression = then_expr
        self.else_expression = else_expr
        
        self.add_child(condition)
        self.add_child(then_expr)
        if else_expr:
            self.add_child(else_expr)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_conditional_expression(self)


class FunctionCallNode(ASTNode):
    """Function call node."""
    
    def __init__(self, function_name: str, arguments: List['ExpressionNode'], 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.FUNCTION_CALL, line, column)
        self.function_name = function_name
        self.arguments = arguments
        
        for arg in arguments:
            self.add_child(arg)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_call(self)


class MemberAccessNode(ASTNode):
    """Member access node (dot notation)."""
    
    def __init__(self, object_expr: 'ExpressionNode', member: str, 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.MEMBER_ACCESS, line, column)
        self.object_expr = object_expr
        self.member = member
        self.add_child(object_expr)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_member_access(self)


class ArrayAccessNode(ASTNode):
    """Array access node (bracket notation)."""
    
    def __init__(self, array_expr: 'ExpressionNode', index: 'ExpressionNode', 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.ARRAY_ACCESS, line, column)
        self.array_expr = array_expr
        self.index = index
        self.add_child(array_expr)
        self.add_child(index)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_array_access(self)


# Literal Nodes

class LiteralNode(ASTNode):
    """Literal value node."""
    
    def __init__(self, value: Any, literal_type: str, line: int = -1, column: int = -1):
        super().__init__(NodeType.LITERAL, line, column)
        self.value = value
        self.literal_type = literal_type  # 'integer', 'float', 'string', 'boolean', 'size', 'null'
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_literal(self)


class IdentifierNode(ASTNode):
    """Identifier node."""
    
    def __init__(self, name: str, line: int = -1, column: int = -1):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier(self)


class ObjectLiteralNode(ASTNode):
    """Object literal node."""
    
    def __init__(self, properties: List['ObjectPropertyNode'], line: int = -1, column: int = -1):
        super().__init__(NodeType.OBJECT_LITERAL, line, column)
        self.properties = properties
        
        for prop in properties:
            self.add_child(prop)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_object_literal(self)


class ArrayLiteralNode(ASTNode):
    """Array literal node."""
    
    def __init__(self, elements: List['ExpressionNode'], line: int = -1, column: int = -1):
        super().__init__(NodeType.ARRAY_LITERAL, line, column)
        self.elements = elements
        
        for element in elements:
            self.add_child(element)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_array_literal(self)


# Component Nodes

class AttributeNode(ASTNode):
    """Attribute node."""
    
    def __init__(self, name: str, value: 'ExpressionNode', line: int = -1, column: int = -1):
        super().__init__(NodeType.ATTRIBUTE, line, column)
        self.name = name
        self.value = value
        self.add_child(value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_attribute(self)


class ParameterNode(ASTNode):
    """Parameter node."""
    
    def __init__(self, name: str, default_value: Optional['ExpressionNode'] = None, 
                 line: int = -1, column: int = -1):
        super().__init__(NodeType.PARAMETER, line, column)
        self.name = name
        self.default_value = default_value
        
        if default_value:
            self.add_child(default_value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_parameter(self)


class ObjectPropertyNode(ASTNode):
    """Object property node."""
    
    def __init__(self, key: str, value: 'ExpressionNode', line: int = -1, column: int = -1):
        super().__init__(NodeType.OBJECT_PROPERTY, line, column)
        self.key = key
        self.value = value
        self.add_child(value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_object_property(self)


class ConnectionAttributeNode(ASTNode):
    """Connection attribute node."""
    
    def __init__(self, name: str, value: 'ExpressionNode', line: int = -1, column: int = -1):
        super().__init__(NodeType.CONNECTION_ATTRIBUTE, line, column)
        self.name = name
        self.value = value
        self.add_child(value)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_connection_attribute(self)


class CommentNode(ASTNode):
    """Comment node."""
    
    def __init__(self, text: str, comment_type: str, line: int = -1, column: int = -1):
        super().__init__(NodeType.COMMENT, line, column)
        self.text = text
        self.comment_type = comment_type  # 'single_line' or 'multi_line'
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_comment(self)


# Visitor Pattern Interface

class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""
    
    @abstractmethod
    def visit_program(self, node: ProgramNode) -> Any:
        pass
    
    @abstractmethod
    def visit_compilation_unit(self, node: CompilationUnitNode) -> Any:
        pass
    
    # Resource declarations
    @abstractmethod
    def visit_resource_declaration(self, node: ResourceDeclarationNode) -> Any:
        pass
    
    @abstractmethod
    def visit_server(self, node: ServerNode) -> Any:
        pass
    
    @abstractmethod
    def visit_network(self, node: NetworkNode) -> Any:
        pass
    
    @abstractmethod
    def visit_database(self, node: DatabaseNode) -> Any:
        pass
    
    @abstractmethod
    def visit_security_group(self, node: SecurityGroupNode) -> Any:
        pass
    
    @abstractmethod
    def visit_load_balancer(self, node: LoadBalancerNode) -> Any:
        pass
    
    @abstractmethod
    def visit_cache(self, node: CacheNode) -> Any:
        pass
    
    @abstractmethod
    def visit_container(self, node: ContainerNode) -> Any:
        pass
    
    @abstractmethod
    def visit_function_resource(self, node: FunctionResourceNode) -> Any:
        pass
    
    @abstractmethod
    def visit_subnet(self, node: SubnetNode) -> Any:
        pass
    
    # Control flow
    @abstractmethod
    def visit_if_statement(self, node: IfStatementNode) -> Any:
        pass
    
    @abstractmethod
    def visit_for_statement(self, node: ForStatementNode) -> Any:
        pass
    
    @abstractmethod
    def visit_block(self, node: BlockNode) -> Any:
        pass
    
    # Declarations
    @abstractmethod
    def visit_function_declaration(self, node: FunctionDeclarationNode) -> Any:
        pass
    
    @abstractmethod
    def visit_module_declaration(self, node: ModuleDeclarationNode) -> Any:
        pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        pass
    
    @abstractmethod
    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> Any:
        pass
    
    @abstractmethod
    def visit_role_declaration(self, node: RoleDeclarationNode) -> Any:
        pass
    
    @abstractmethod
    def visit_policy_declaration(self, node: PolicyDeclarationNode) -> Any:
        pass
    
    # Statements
    @abstractmethod
    def visit_assignment(self, node: AssignmentNode) -> Any:
        pass
    
    @abstractmethod
    def visit_use_statement(self, node: UseStatementNode) -> Any:
        pass
    
    @abstractmethod
    def visit_connect_statement(self, node: ConnectStatementNode) -> Any:
        pass
    
    @abstractmethod
    def visit_attach_statement(self, node: AttachStatementNode) -> Any:
        pass
    
    @abstractmethod
    def visit_assign_role_statement(self, node: AssignRoleStatementNode) -> Any:
        pass
    
    # Expressions
    @abstractmethod
    def visit_binary_expression(self, node: BinaryExpressionNode) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_expression(self, node: UnaryExpressionNode) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional_expression(self, node: ConditionalExpressionNode) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCallNode) -> Any:
        pass
    
    @abstractmethod
    def visit_member_access(self, node: MemberAccessNode) -> Any:
        pass
    
    @abstractmethod
    def visit_array_access(self, node: ArrayAccessNode) -> Any:
        pass
    
    # Literals
    @abstractmethod
    def visit_literal(self, node: LiteralNode) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: IdentifierNode) -> Any:
        pass
    
    @abstractmethod
    def visit_object_literal(self, node: ObjectLiteralNode) -> Any:
        pass
    
    @abstractmethod
    def visit_array_literal(self, node: ArrayLiteralNode) -> Any:
        pass
    
    # Components
    @abstractmethod
    def visit_attribute(self, node: AttributeNode) -> Any:
        pass
    
    @abstractmethod
    def visit_parameter(self, node: ParameterNode) -> Any:
        pass
    
    @abstractmethod
    def visit_object_property(self, node: ObjectPropertyNode) -> Any:
        pass
    
    @abstractmethod
    def visit_connection_attribute(self, node: ConnectionAttributeNode) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: CommentNode) -> Any:
        pass


# Type Aliases for Expressions
ExpressionNode = Union[
    BinaryExpressionNode,
    UnaryExpressionNode,
    ConditionalExpressionNode,
    FunctionCallNode,
    MemberAccessNode,
    ArrayAccessNode,
    LiteralNode,
    IdentifierNode,
    ObjectLiteralNode,
    ArrayLiteralNode
]
