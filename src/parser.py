"""
Parser for Infrastructure DSL

This module implements the parser that converts tokens into an Abstract Syntax Tree (AST).
It uses a recursive descent parsing approach based on the grammar rules.
"""

from typing import List, Optional, Union
from src.lexer import Token, TokenType, TokenStream
from src.ast_nodes import *
from src.error_handler import ErrorHandler, ParserError


class Parser:
    """
    Recursive descent parser for Infrastructure DSL.
    
    This parser implements the grammar defined in InfrastructureDSL.g4 and
    builds an Abstract Syntax Tree (AST) from the token stream.
    """
    
    def __init__(self, tokens: List[Token], error_handler: ErrorHandler):
        self.token_stream = TokenStream(tokens)
        self.error_handler = error_handler
        self.current_token = self.token_stream.current()
        
    def parse(self) -> ProgramNode:
        """
        Parse the token stream into an AST.
        
        Returns:
            Root AST node (ProgramNode)
            
        Raises:
            ParserError: If parsing fails
        """
        try:
            program = ProgramNode()
            
            # Parse compilation units until EOF
            while not self.token_stream.is_at_end():
                unit = self._parse_compilation_unit()
                if unit:
                    program.add_compilation_unit(unit)
            
            return program
            
        except Exception as e:
            self.error_handler.add_error(
                ParserError(f"Parser error: {str(e)}", 
                           self.current_token.line if self.current_token else -1,
                           self.current_token.column if self.current_token else -1,
                           self.current_token.position if self.current_token else -1)
            )
            raise
    
    def _advance(self) -> Token:
        """Advance to the next token and return it."""
        self.current_token = self.token_stream.advance()
        return self.current_token
    
    def _match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.token_stream.match(*token_types)
    
    def _expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type and consume it."""
        try:
            return self.token_stream.expect(token_type)
        except Exception as e:
            self.error_handler.add_error(
                ParserError(str(e), 
                           self.current_token.line if self.current_token else -1,
                           self.current_token.column if self.current_token else -1,
                           self.current_token.position if self.current_token else -1)
            )
            raise
    
    def _parse_compilation_unit(self) -> Optional[CompilationUnitNode]:
        """Parse a compilation unit."""
        try:
            # Try to parse different statement types
            if self._match(TokenType.SERVER):
                return CompilationUnitNode(self._parse_server_declaration())
            elif self._match(TokenType.NETWORK):
                return CompilationUnitNode(self._parse_network_declaration())
            elif self._match(TokenType.DATABASE):
                return CompilationUnitNode(self._parse_database_declaration())
            elif self._match(TokenType.NOSQL_DB):
                return CompilationUnitNode(self._parse_database_declaration("nosql_db"))
            elif self._match(TokenType.SECURITY_GROUP):
                return CompilationUnitNode(self._parse_security_group_declaration())
            elif self._match(TokenType.LOAD_BALANCER):
                return CompilationUnitNode(self._parse_load_balancer_declaration())
            elif self._match(TokenType.CACHE):
                return CompilationUnitNode(self._parse_cache_declaration())
            elif self._match(TokenType.CONTAINER):
                return CompilationUnitNode(self._parse_container_declaration())
            elif self._match(TokenType.FUNCTION):
                return CompilationUnitNode(self._parse_function_resource_declaration())
            elif self._match(TokenType.SUBNET):
                return CompilationUnitNode(self._parse_subnet_declaration())
            elif self._match(TokenType.MODULE):
                return CompilationUnitNode(self._parse_module_declaration())
            elif self._match(TokenType.VARIABLE):
                return CompilationUnitNode(self._parse_variable_declaration())
            elif self._match(TokenType.CONSTANT):
                return CompilationUnitNode(self._parse_constant_declaration())
            elif self._match(TokenType.ROLE):
                return CompilationUnitNode(self._parse_role_declaration())
            elif self._match(TokenType.POLICY):
                return CompilationUnitNode(self._parse_policy_declaration())
            elif self._match(TokenType.IF):
                return CompilationUnitNode(self._parse_if_statement())
            elif self._match(TokenType.FOR):
                return CompilationUnitNode(self._parse_for_statement())
            elif self._match(TokenType.USE):
                return CompilationUnitNode(self._parse_use_statement())
            elif self._match(TokenType.CONNECT):
                return CompilationUnitNode(self._parse_connect_statement())
            elif self._match(TokenType.ATTACH):
                return CompilationUnitNode(self._parse_attach_statement())
            elif self._match(TokenType.ASSIGN):
                return CompilationUnitNode(self._parse_assign_role_statement())
            elif self._match(TokenType.IDENTIFIER):
                return CompilationUnitNode(self._parse_assignment())
            elif self._match(TokenType.COMMENT):
                # Skip comments for now
                self._advance()
                return None
            else:
                # Skip unknown tokens
                if not self.token_stream.is_at_end():
                    self._advance()
                return None
                
        except Exception as e:
            # Skip to next statement on error
            self._skip_to_next_statement()
            return None
    
    def _skip_to_next_statement(self):
        """Skip tokens until we reach the next likely statement start."""
        while not self.token_stream.is_at_end():
            if self._match(
                TokenType.SERVER, TokenType.NETWORK, TokenType.DATABASE, TokenType.NOSQL_DB,
                TokenType.SECURITY_GROUP, TokenType.LOAD_BALANCER, TokenType.CACHE,
                TokenType.CONTAINER, TokenType.FUNCTION, TokenType.SUBNET, TokenType.MODULE,
                TokenType.VARIABLE, TokenType.CONSTANT, TokenType.ROLE, TokenType.POLICY,
                TokenType.IF, TokenType.FOR, TokenType.USE, TokenType.CONNECT, TokenType.ATTACH,
                TokenType.ASSIGN, TokenType.EOF
            ):
                break
            self._advance()
    
    # Resource Declarations
    
    def _parse_server_declaration(self) -> ServerNode:
        """Parse server declaration."""
        token = self._expect(TokenType.SERVER)
        # Resource names can be quoted strings or identifiers
        if self._match(TokenType.STRING):
            name_token = self.token_stream.current()
            self._advance()
            identifier = name_token.value.strip('"')
        else:
            identifier_node = self._parse_identifier()
            identifier = identifier_node.name
        attributes = self._parse_resource_block()
        return ServerNode(identifier, attributes, token.line, token.column)
    
    def _parse_network_declaration(self) -> NetworkNode:
        """Parse network declaration."""
        token = self._expect(TokenType.NETWORK)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return NetworkNode(identifier, attributes, token.line, token.column)
    
    def _parse_database_declaration(self, db_type: str = "database") -> DatabaseNode:
        """Parse database declaration."""
        token = self._expect(TokenType.DATABASE if db_type == "database" else TokenType.NOSQL_DB)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return DatabaseNode(db_type, identifier, attributes, token.line, token.column)
    
    def _parse_security_group_declaration(self) -> SecurityGroupNode:
        """Parse security group declaration."""
        token = self._expect(TokenType.SECURITY_GROUP)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return SecurityGroupNode(identifier, attributes, token.line, token.column)
    
    def _parse_load_balancer_declaration(self) -> LoadBalancerNode:
        """Parse load balancer declaration."""
        token = self._expect(TokenType.LOAD_BALANCER)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return LoadBalancerNode(identifier, attributes, token.line, token.column)
    
    def _parse_cache_declaration(self) -> CacheNode:
        """Parse cache declaration."""
        token = self._expect(TokenType.CACHE)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return CacheNode(identifier, attributes, token.line, token.column)
    
    def _parse_container_declaration(self) -> ContainerNode:
        """Parse container declaration."""
        token = self._expect(TokenType.CONTAINER)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return ContainerNode(identifier, attributes, token.line, token.column)
    
    def _parse_function_resource_declaration(self) -> FunctionResourceNode:
        """Parse function resource declaration."""
        token = self._expect(TokenType.FUNCTION)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return FunctionResourceNode(identifier, attributes, token.line, token.column)
    
    def _parse_subnet_declaration(self) -> SubnetNode:
        """Parse subnet declaration."""
        token = self._expect(TokenType.SUBNET)
        identifier = self._parse_identifier()
        attributes = self._parse_resource_block()
        return SubnetNode(identifier, attributes, token.line, token.column)
    
    def _parse_resource_block(self) -> List[AttributeNode]:
        """Parse resource block with attributes."""
        self._expect(TokenType.LBRACE)
        attributes = []
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            attr = self._parse_attribute()
            if attr:
                attributes.append(attr)
            else:
                # Skip to next token after failed attribute parse
                self._advance()
            
            # Skip comma if present
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACE)
        return attributes
    
    def _parse_attribute(self) -> Optional[AttributeNode]:
        """Parse attribute assignment."""
        try:
            name = self._parse_identifier()
            self._expect(TokenType.ASSIGN_OP)
            value = self._parse_expression()
            return AttributeNode(name, value, name.line, name.column)
        except Exception as e:
            self.error_handler.add_error(
                ParserError(f"Failed to parse attribute: {str(e)}", 
                           self.token_stream.current().line if self.token_stream.current() else -1,
                           self.token_stream.current().column if self.token_stream.current() else -1,
                           -1)
            )
            return None
    
    # Control Flow
    
    def _parse_if_statement(self) -> IfStatementNode:
        """Parse if statement."""
        token = self._expect(TokenType.IF)
        condition = self._parse_expression()
        then_block = self._parse_block()
        
        else_block = None
        if self._match(TokenType.ELSE):
            self._advance()
            else_block = self._parse_block()
        
        return IfStatementNode(condition, then_block, else_block, token.line, token.column)
    
    def _parse_for_statement(self) -> ForStatementNode:
        """Parse for statement."""
        token = self._expect(TokenType.FOR)
        variable = self._parse_identifier()
        self._expect(TokenType.IN)
        iterable = self._parse_expression()
        body = self._parse_block()
        return ForStatementNode(variable, iterable, body, token.line, token.column)
    
    def _parse_block(self) -> BlockNode:
        """Parse block of statements."""
        self._expect(TokenType.LBRACE)
        statements = []
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            unit = self._parse_compilation_unit()
            if unit and unit.statement:
                statements.append(unit.statement)
        
        self._expect(TokenType.RBRACE)
        return BlockNode(statements, self.current_token.line, self.current_token.column)
    
    # Declarations
    
    def _parse_module_declaration(self) -> ModuleDeclarationNode:
        """Parse module declaration."""
        token = self._expect(TokenType.MODULE)
        name = self._parse_identifier()
        
        self._expect(TokenType.LBRACE)
        
        # Parse parameters
        parameters = []
        while self._match(TokenType.PARAM):
            param = self._parse_parameter()
            if param:
                parameters.append(param)
            if self._match(TokenType.COMMA):
                self._advance()
        
        # Parse statements
        statements = []
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            unit = self._parse_compilation_unit()
            if unit and unit.statement:
                statements.append(unit.statement)
        
        self._expect(TokenType.RBRACE)
        return ModuleDeclarationNode(name, parameters, statements, token.line, token.column)
    
    def _parse_parameter(self) -> Optional[ParameterNode]:
        """Parse parameter."""
        try:
            self._expect(TokenType.PARAM)
            name = self._parse_identifier()
            self._expect(TokenType.ASSIGN_OP)
            default_value = self._parse_expression()
            return ParameterNode(name, default_value, name.line, name.column)
        except Exception:
            return None
    
    def _parse_variable_declaration(self) -> VariableDeclarationNode:
        """Parse variable declaration."""
        token = self._expect(TokenType.VARIABLE)
        name = self._parse_identifier()
        
        self._expect(TokenType.LBRACE)
        
        var_type = None
        default_value = None
        description = None
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            if self._match(TokenType.TYPE):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                type_token = self._expect(TokenType.STRING)
                var_type = type_token.value.strip('"')
            elif self._match(TokenType.DEFAULT):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                default_value = self._parse_expression()
            elif self._match(TokenType.DESCRIPTION):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                desc_token = self._expect(TokenType.STRING)
                description = desc_token.value.strip('"')
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACE)
        return VariableDeclarationNode(name, var_type, default_value, description, token.line, token.column)
    
    def _parse_constant_declaration(self) -> ConstantDeclarationNode:
        """Parse constant declaration."""
        token = self._expect(TokenType.CONSTANT)
        name = self._parse_identifier()
        self._expect(TokenType.ASSIGN_OP)
        value = self._parse_expression()
        return ConstantDeclarationNode(name, value, token.line, token.column)
    
    def _parse_role_declaration(self) -> RoleDeclarationNode:
        """Parse role declaration."""
        token = self._expect(TokenType.ROLE)
        name = self._parse_identifier()
        
        self._expect(TokenType.LBRACE)
        
        permissions = []
        resources = []
        conditions = None
        description = None
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            if self._match(TokenType.DESCRIPTION):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                desc_token = self._expect(TokenType.STRING)
                description = desc_token.value.strip('"')
            elif self._match(TokenType.PERMISSIONS):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                permissions = self._parse_array_literal().elements
            elif self._match(TokenType.RESOURCES):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                resources = self._parse_array_literal().elements
            elif self._match(TokenType.CONDITIONS):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                conditions = self._parse_object_literal()
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACE)
        return RoleDeclarationNode(name, permissions, resources, conditions, description, token.line, token.column)
    
    def _parse_policy_declaration(self) -> PolicyDeclarationNode:
        """Parse policy declaration."""
        token = self._expect(TokenType.POLICY)
        name = self._parse_identifier()
        
        self._expect(TokenType.LBRACE)
        
        target = None
        policy_type = None
        attributes = {}
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            if self._match(TokenType.TARGET):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                target = self._parse_expression()
            elif self._match(TokenType.TYPE):
                self._advance()
                self._expect(TokenType.ASSIGN_OP)
                type_token = self._expect(TokenType.STRING)
                policy_type = type_token.value.strip('"')
            else:
                # Parse other attributes
                attr_name = self._parse_identifier()
                self._expect(TokenType.ASSIGN_OP)
                attr_value = self._parse_expression()
                attributes[attr_name.name] = attr_value
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACE)
        return PolicyDeclarationNode(name, policy_type, target, attributes, token.line, token.column)
    
    # Statements
    
    def _parse_use_statement(self) -> UseStatementNode:
        """Parse use statement."""
        token = self._expect(TokenType.USE)
        module_name = self._parse_identifier()
        self._expect(TokenType.WITH)
        arguments = self._parse_object_literal()
        return UseStatementNode(module_name, arguments, token.line, token.column)
    
    def _parse_connect_statement(self) -> ConnectStatementNode:
        """Parse connect statement."""
        token = self._expect(TokenType.CONNECT)
        source = self._parse_expression()
        self._expect(TokenType.ARROW)
        target = self._parse_expression()
        attributes = self._parse_connection_block()
        return ConnectStatementNode(source, target, attributes, token.line, token.column)
    
    def _parse_connection_block(self) -> List[ConnectionAttributeNode]:
        """Parse connection block."""
        self._expect(TokenType.LBRACE)
        attributes = []
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            attr = self._parse_connection_attribute()
            if attr:
                attributes.append(attr)
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACE)
        return attributes
    
    def _parse_connection_attribute(self) -> Optional[ConnectionAttributeNode]:
        """Parse connection attribute."""
        try:
            name = self._parse_identifier()
            self._expect(TokenType.ASSIGN_OP)
            value = self._parse_expression()
            return ConnectionAttributeNode(name, value, name.line, name.column)
        except Exception:
            return None
    
    def _parse_attach_statement(self) -> AttachStatementNode:
        """Parse attach statement."""
        token = self._expect(TokenType.ATTACH)
        source = self._parse_expression()
        self._expect(TokenType.TO)
        target = self._parse_expression()
        return AttachStatementNode(source, target, token.line, token.column)
    
    def _parse_assign_role_statement(self) -> AssignRoleStatementNode:
        """Parse assign role statement."""
        token = self._expect(TokenType.ASSIGN)
        role_name = self._parse_identifier()
        self._expect(TokenType.TO)
        
        if self._match(TokenType.USER):
            user_type = "user"
            self._advance()
        elif self._match(TokenType.GROUP):
            user_type = "group"
            self._advance()
        elif self._match(TokenType.ROLE):
            user_type = "role"
            self._advance()
        else:
            # Default to user
            user_type = "user"
        
        user_token = self._expect(TokenType.STRING)
        user_identifier = user_token.value.strip('"')
        
        return AssignRoleStatementNode(role_name, user_type, user_identifier, token.line, token.column)
    
    def _parse_assignment(self) -> AssignmentNode:
        """Parse assignment statement."""
        identifier = self._parse_identifier()
        self._expect(TokenType.ASSIGN_OP)
        value = self._parse_expression()
        return AssignmentNode(identifier.name, value, identifier.line, identifier.column)
    
    # Expressions
    
    def _parse_expression(self) -> ExpressionNode:
        """Parse expression with precedence."""
        return self._parse_or_expression()
    
    def _parse_or_expression(self) -> ExpressionNode:
        """Parse logical OR expression."""
        left = self._parse_and_expression()
        
        while self._match(TokenType.OR):
            operator = self._advance().value
            right = self._parse_and_expression()
            left = BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_and_expression(self) -> ExpressionNode:
        """Parse logical AND expression."""
        left = self._parse_equality_expression()
        
        while self._match(TokenType.AND):
            operator = self._advance().value
            right = self._parse_equality_expression()
            left = BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_equality_expression(self) -> ExpressionNode:
        """Parse equality expression."""
        left = self._parse_relational_expression()
        
        while self._match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self._advance().value
            right = self._parse_relational_expression()
            left = BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_relational_expression(self) -> ExpressionNode:
        """Parse relational expression."""
        left = self._parse_additive_expression()
        
        while self._match(TokenType.LESS_THAN, TokenType.LESS_THAN_OR_EQUAL,
                          TokenType.GREATER_THAN, TokenType.GREATER_THAN_OR_EQUAL):
            operator = self._advance().value
            right = self._parse_additive_expression()
            left = BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_additive_expression(self) -> ExpressionNode:
        """Parse additive expression."""
        left = self._parse_multiplicative_expression()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._advance().value
            right = self._parse_multiplicative_expression()
            left = BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_multiplicative_expression(self) -> ExpressionNode:
        """Parse multiplicative expression."""
        left = self._parse_power_expression()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self._advance().value
            right = self._parse_power_expression()
            left = BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_power_expression(self) -> ExpressionNode:
        """Parse power expression."""
        left = self._parse_unary_expression()
        
        if self._match(TokenType.POWER):
            operator = self._advance().value
            right = self._parse_power_expression()
            return BinaryExpressionNode(left, operator, right, left.line, left.column)
        
        return left
    
    def _parse_unary_expression(self) -> ExpressionNode:
        """Parse unary expression."""
        if self._match(TokenType.MINUS, TokenType.PLUS, TokenType.NOT):
            operator = self._advance().value
            operand = self._parse_unary_expression()
            return UnaryExpressionNode(operator, operand, self.current_token.line, self.current_token.column)
        
        return self._parse_primary_expression()
    
    def _parse_primary_expression(self) -> ExpressionNode:
        """Parse primary expression."""
        if self._match(TokenType.INTEGER):
            token = self._advance()
            return LiteralNode(int(token.value), "integer", token.line, token.column)
        elif self._match(TokenType.FLOAT):
            token = self._advance()
            return LiteralNode(float(token.value), "float", token.line, token.column)
        elif self._match(TokenType.STRING):
            token = self._advance()
            return LiteralNode(token.value.strip('"'), "string", token.line, token.column)
        elif self._match(TokenType.TRUE):
            token = self._advance()
            return LiteralNode(True, "boolean", token.line, token.column)
        elif self._match(TokenType.FALSE):
            token = self._advance()
            return LiteralNode(False, "boolean", token.line, token.column)
        elif self._match(TokenType.NULL_KW):
            token = self._advance()
            return LiteralNode(None, "null", token.line, token.column)
        elif self._match(TokenType.SIZE):
            token = self._advance()
            return LiteralNode(token.value, "size", token.line, token.column)
        elif self._match(TokenType.IDENTIFIER):
            return self._parse_identifier_or_function_call()
        elif self._match(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return expr
        elif self._match(TokenType.LBRACKET):
            return self._parse_array_literal()
        elif self._match(TokenType.LBRACE):
            return self._parse_object_literal()
        else:
            raise ParserError(f"Unexpected token: {self.current_token.value}", 
                           self.current_token.line, self.current_token.column, self.current_token.position)
    
    def _parse_identifier_or_function_call(self) -> ExpressionNode:
        """Parse identifier or function call."""
        identifier = self._parse_identifier()
        
        if self._match(TokenType.LPAREN):
            # Function call
            self._advance()
            arguments = []
            
            while not self._match(TokenType.RPAREN) and not self.token_stream.is_at_end():
                arg = self._parse_expression()
                arguments.append(arg)
                
                if self._match(TokenType.COMMA):
                    self._advance()
            
            self._expect(TokenType.RPAREN)
            return FunctionCallNode(identifier.name, arguments, identifier.line, identifier.column)
        else:
            # Simple identifier
            return identifier
    
    def _parse_identifier(self) -> IdentifierNode:
        """Parse identifier."""
        token = self._expect(TokenType.IDENTIFIER)
        return IdentifierNode(token.value, token.line, token.column)
    
    def _parse_array_literal(self) -> ArrayLiteralNode:
        """Parse array literal."""
        token = self._expect(TokenType.LBRACKET)
        elements = []
        
        while not self._match(TokenType.RBRACKET) and not self.token_stream.is_at_end():
            element = self._parse_expression()
            elements.append(element)
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACKET)
        return ArrayLiteralNode(elements, token.line, token.column)
    
    def _parse_object_literal(self) -> ObjectLiteralNode:
        """Parse object literal."""
        token = self._expect(TokenType.LBRACE)
        properties = []
        
        while not self._match(TokenType.RBRACE) and not self.token_stream.is_at_end():
            # Parse key (can be identifier or string)
            if self._match(TokenType.IDENTIFIER):
                key_token = self._advance()
                key = key_token.value
            elif self._match(TokenType.STRING):
                key_token = self._advance()
                key = key_token.value.strip('"')
            else:
                raise ParserError(f"Expected object key, got {self.current_token.value}", 
                               self.current_token.line, self.current_token.column, self.current_token.position)
            
            self._expect(TokenType.COLON)
            value = self._parse_expression()
            properties.append(ObjectPropertyNode(key, value, key_token.line, key_token.column))
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._expect(TokenType.RBRACE)
        return ObjectLiteralNode(properties, token.line, token.column)
    
    def _parse_member_access(self, object_expr: ExpressionNode) -> MemberAccessNode:
        """Parse member access (dot notation)."""
        self._expect(TokenType.DOT)
        member_token = self._expect(TokenType.IDENTIFIER)
        return MemberAccessNode(object_expr, member_token.value, object_expr.line, object_expr.column)
    
    def _parse_array_access(self, array_expr: ExpressionNode) -> ArrayAccessNode:
        """Parse array access (bracket notation)."""
        self._expect(TokenType.LBRACKET)
        index = self._parse_expression()
        self._expect(TokenType.RBRACKET)
        return ArrayAccessNode(array_expr, index, array_expr.line, array_expr.column)
    
    def _parse_identifier(self) -> IdentifierNode:
        """Parse identifier (including attribute names like 'cpu', 'memory', etc.)."""
        # Handle special attribute name tokens
        special_tokens = [
            TokenType.CPU, TokenType.MEMORY, TokenType.OS, TokenType.ENGINE,
            TokenType.VERSION, TokenType.STORAGE, TokenType.INSTANCE_CLASS
        ]
        
        if self._match(*special_tokens):
            token = self.token_stream.current()
            self._advance()
            return IdentifierNode(token.type.name.lower(), token.line, token.column)
        else:
            token = self._expect(TokenType.IDENTIFIER)
            return IdentifierNode(token.value, token.line, token.column)
