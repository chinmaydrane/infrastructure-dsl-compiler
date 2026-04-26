"""
Semantic Analyzer for Infrastructure DSL

This module implements semantic analysis including type checking, symbol resolution,
and validation of language constructs.
"""

from typing import List, Dict, Any, Optional, Set
from src.ast_nodes import *
from src.symbol_table import SymbolTable, SymbolType, DataType, TypeInfo, Symbol, TypeChecker
from src.error_handler import ErrorHandler, SemanticError


class SemanticAnalyzer(ASTVisitor):
    """
    Semantic analyzer for the Infrastructure DSL.
    
    Performs:
    - Symbol table construction
    - Type checking
    - Reference resolution
    - Constraint validation
    - Duplicate detection
    """
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.symbol_table = SymbolTable()
        self.type_checker = TypeChecker(self.symbol_table)
        self.current_scope = self.symbol_table.get_global_scope()
        self.loop_depth = 0
        self.function_depth = 0
        self.module_depth = 0
        
        # Track defined resources for validation
        self.defined_resources: Dict[str, ResourceDeclarationNode] = {}
        self.defined_modules: Dict[str, ModuleDeclarationNode] = {}
        self.defined_functions: Dict[str, FunctionDeclarationNode] = {}
        self.defined_roles: Dict[str, RoleDeclarationNode] = {}
        self.defined_policies: Dict[str, PolicyDeclarationNode] = {}
        
        # Track references for validation
        self.resource_references: List[str] = []
        self.module_references: List[str] = []
        self.function_references: List[str] = []
        self.role_references: List[str] = []
    
    def analyze(self, ast: ProgramNode) -> bool:
        """
        Perform semantic analysis on the AST.
        
        Args:
            ast: Abstract syntax tree
            
        Returns:
            True if analysis passed without errors
        """
        try:
            # First pass: collect symbols
            self._collect_symbols(ast)
            
            # Second pass: validate references and types
            self._validate_ast(ast)
            
            # Check for unused symbols
            self._check_unused_symbols()
            
            # Check for undefined references
            self._check_undefined_references()
            
            # Return True if no semantic errors
            return not self.error_handler.has_semantic_errors()
            
        except Exception as e:
            error_msg = f"Semantic analysis failed: {str(e)}"
            self.error_handler.add_error(
                SemanticError(error_msg, -1, -1, -1)
            )
            return False
    
    def _collect_symbols(self, node: ASTNode):
        """First pass: collect all symbols in the symbol table."""
        node.accept(self._SymbolCollector(self))
    
    def _validate_ast(self, node: ASTNode):
        """Second pass: validate the AST."""
        node.accept(self._Validator(self))
    
    def _check_unused_symbols(self):
        """Check for unused symbols and report warnings."""
        unused_symbols = self.symbol_table.find_unused_symbols()
        for symbol in unused_symbols:
            self.error_handler.add_warning(
                f"Unused symbol: {symbol.name} (defined at line {symbol.line})"
            )
    
    def _check_undefined_references(self):
        """Check for undefined references."""
        # Check resource references
        for ref in self.resource_references:
            if ref not in self.defined_resources:
                self.error_handler.add_error(
                    SemanticError(f"Undefined resource reference: {ref}", -1, -1, -1)
                )
        
        # Check module references
        for ref in self.module_references:
            if ref not in self.defined_modules:
                self.error_handler.add_error(
                    SemanticError(f"Undefined module reference: {ref}", -1, -1, -1)
                )
        
        # Check function references
        for ref in self.function_references:
            if ref not in self.defined_functions:
                builtin_symbol = self.symbol_table.lookup_symbol(ref)
                if not builtin_symbol or builtin_symbol.symbol_type != SymbolType.BUILTIN_FUNCTION:
                    self.error_handler.add_error(
                        SemanticError(f"Undefined function reference: {ref}", -1, -1, -1)
                    )
        
        # Check role references
        for ref in self.role_references:
            if ref not in self.defined_roles:
                self.error_handler.add_error(
                    SemanticError(f"Undefined role reference: {ref}", -1, -1, -1)
                )
    
    # Visitor methods for symbol collection
    
    def visit_program(self, node: ProgramNode):
        """Visit program node."""
        for unit in node.compilation_units:
            unit.accept(self)
    
    def visit_compilation_unit(self, node: CompilationUnitNode):
        """Visit compilation unit."""
        node.statement.accept(self)
    
    def visit_server(self, node: ServerNode):
        """Visit server declaration."""
        self._declare_resource(node, SymbolType.SERVER)
    
    def visit_network(self, node: NetworkNode):
        """Visit network declaration."""
        self._declare_resource(node, SymbolType.NETWORK)
    
    def visit_database(self, node: DatabaseNode):
        """Visit database declaration."""
        self._declare_resource(node, SymbolType.DATABASE)
    
    def visit_security_group(self, node: SecurityGroupNode):
        """Visit security group declaration."""
        self._declare_resource(node, SymbolType.SECURITY_GROUP)
    
    def visit_load_balancer(self, node: LoadBalancerNode):
        """Visit load balancer declaration."""
        self._declare_resource(node, SymbolType.LOAD_BALANCER)
    
    def visit_cache(self, node: CacheNode):
        """Visit cache declaration."""
        self._declare_resource(node, SymbolType.CACHE)
    
    def visit_container(self, node: ContainerNode):
        """Visit container declaration."""
        self._declare_resource(node, SymbolType.CONTAINER)
    
    def visit_function_resource(self, node: FunctionResourceNode):
        """Visit function resource declaration."""
        self._declare_resource(node, SymbolType.FUNCTION)
    
    def visit_subnet(self, node: SubnetNode):
        """Visit subnet declaration."""
        self._declare_resource(node, SymbolType.SUBNET)
    
    def visit_module_declaration(self, node: ModuleDeclarationNode):
        """Visit module declaration."""
        # Check for duplicate module
        if node.name in self.defined_modules:
            self.error_handler.add_error(
                SemanticError(f"Duplicate module declaration: {node.name}", node.line, node.column, -1)
            )
            return
        
        # Create module type info
        module_type = TypeInfo(DataType.OBJECT)
        
        # Define module symbol
        if not self.symbol_table.define_symbol(
            node.name, SymbolType.MODULE, module_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Module already defined: {node.name}", node.line, node.column, -1)
            )
            return
        
        self.defined_modules[node.name] = node
        
        # Enter module scope
        old_scope = self.current_scope
        self.current_scope = self.symbol_table.enter_scope(f"module_{node.name}")
        self.module_depth += 1
        
        # Define parameters
        for param in node.parameters:
            param_type = self._infer_expression_type(param.default_value) if param.default_value else TypeInfo(DataType.UNKNOWN)
            if not self.symbol_table.define_symbol(
                param.name, SymbolType.VARIABLE, param_type, param.line, param.column, param
            ):
                self.error_handler.add_error(
                    SemanticError(f"Parameter already defined: {param.name}", param.line, param.column, -1)
                )
        
        # Visit module body
        for stmt in node.statements:
            stmt.accept(self)
        
        # Exit module scope
        self.symbol_table.exit_scope()
        self.current_scope = old_scope
        self.module_depth -= 1
    
    def visit_function_declaration(self, node: FunctionDeclarationNode):
        """Visit function declaration."""
        # Check for duplicate function
        if node.name in self.defined_functions:
            self.error_handler.add_error(
                SemanticError(f"Duplicate function declaration: {node.name}", node.line, node.column, -1)
            )
            return
        
        # Create function type info
        param_types = []
        for param in node.parameters:
            param_type = self._infer_expression_type(param.default_value) if param.default_value else TypeInfo(DataType.UNKNOWN)
            param_types.append(param_type)
        
        return_type = self._infer_expression_type(node.return_expression)
        function_type = TypeInfo(DataType.FUNCTION_TYPE, parameters=param_types, return_type=return_type)
        
        # Define function symbol
        if not self.symbol_table.define_symbol(
            node.name, SymbolType.FUNCTION_DECLARATION, function_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Function already defined: {node.name}", node.line, node.column, -1)
            )
            return
        
        self.defined_functions[node.name] = node
        
        # Enter function scope
        old_scope = self.current_scope
        self.current_scope = self.symbol_table.enter_scope(f"function_{node.name}")
        self.function_depth += 1
        
        # Define parameters
        for param in node.parameters:
            param_type = self._infer_expression_type(param.default_value) if param.default_value else TypeInfo(DataType.UNKNOWN)
            if not self.symbol_table.define_symbol(
                param.name, SymbolType.VARIABLE, param_type, param.line, param.column, param
            ):
                self.error_handler.add_error(
                    SemanticError(f"Parameter already defined: {param.name}", param.line, param.column, -1)
                )
        
        # Visit function body
        node.body.accept(self)
        
        # Exit function scope
        self.symbol_table.exit_scope()
        self.current_scope = old_scope
        self.function_depth -= 1
    
    def visit_variable_declaration(self, node: VariableDeclarationNode):
        """Visit variable declaration."""
        var_type = self._string_to_data_type(node.var_type)
        
        if not self.symbol_table.define_symbol(
            node.name, SymbolType.VARIABLE, var_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Variable already defined: {node.name}", node.line, node.column, -1)
            )
    
    def visit_constant_declaration(self, node: ConstantDeclarationNode):
        """Visit constant declaration."""
        const_type = self._infer_expression_type(node.value)
        
        if not self.symbol_table.define_symbol(
            node.name, SymbolType.CONSTANT, const_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Constant already defined: {node.name}", node.line, node.column, -1)
            )
    
    def visit_role_declaration(self, node: RoleDeclarationNode):
        """Visit role declaration."""
        # Check for duplicate role
        if node.name in self.defined_roles:
            self.error_handler.add_error(
                SemanticError(f"Duplicate role declaration: {node.name}", node.line, node.column, -1)
            )
            return
        
        # Create role type info
        role_type = TypeInfo(DataType.OBJECT)
        
        # Define role symbol
        if not self.symbol_table.define_symbol(
            node.name, SymbolType.ROLE, role_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Role already defined: {node.name}", node.line, node.column, -1)
            )
            return
        
        self.defined_roles[node.name] = node
    
    def visit_policy_declaration(self, node: PolicyDeclarationNode):
        """Visit policy declaration."""
        # Check for duplicate policy
        if node.name in self.defined_policies:
            self.error_handler.add_error(
                SemanticError(f"Duplicate policy declaration: {node.name}", node.line, node.column, -1)
            )
            return
        
        # Create policy type info
        policy_type = TypeInfo(DataType.OBJECT)
        
        # Define policy symbol
        if not self.symbol_table.define_symbol(
            node.name, SymbolType.POLICY, policy_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Policy already defined: {node.name}", node.line, node.column, -1)
            )
            return
        
        self.defined_policies[node.name] = node
    
    def visit_if_statement(self, node: IfStatementNode):
        """Visit if statement."""
        # Enter new scope for if statement
        old_scope = self.current_scope
        self.current_scope = self.symbol_table.enter_scope("if")
        
        # Visit condition
        node.condition.accept(self)
        
        # Visit then block
        node.then_block.accept(self)
        
        # Exit if scope for then block
        self.symbol_table.exit_scope()
        
        # Visit else block if present
        if node.else_block:
            self.current_scope = self.symbol_table.enter_scope("else")
            node.else_block.accept(self)
            self.symbol_table.exit_scope()
        
        self.current_scope = old_scope
    
    def visit_for_statement(self, node: ForStatementNode):
        """Visit for statement."""
        # Enter new scope for for loop
        old_scope = self.current_scope
        self.current_scope = self.symbol_table.enter_scope("for")
        self.loop_depth += 1
        
        # Define loop variable
        iterable_type = self._infer_expression_type(node.iterable)
        element_type = TypeInfo(DataType.UNKNOWN)
        if iterable_type.data_type == DataType.ARRAY and iterable_type.element_type:
            element_type = iterable_type.element_type
        
        if not self.symbol_table.define_symbol(
            node.variable, SymbolType.VARIABLE, element_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Loop variable already defined: {node.variable}", node.line, node.column, -1)
            )
        
        # Visit iterable and body
        node.iterable.accept(self)
        node.body.accept(self)
        
        # Exit for scope
        self.symbol_table.exit_scope()
        self.current_scope = old_scope
        self.loop_depth -= 1
    
    def visit_identifier(self, node: IdentifierNode):
        """Visit identifier."""
        # Check if identifier is defined
        symbol = self.symbol_table.lookup_symbol(node.name)
        if not symbol:
            # Could be a resource reference
            if node.name in self.defined_resources:
                self.resource_references.append(node.name)
            else:
                self.error_handler.add_error(
                    SemanticError(f"Undefined identifier: {node.name}", node.line, node.column, -1)
                )
    
    def visit_function_call(self, node: FunctionCallNode):
        """Visit function call."""
        # Check if function is defined
        symbol = self.symbol_table.lookup_symbol(node.function_name)
        if not symbol:
            self.function_references.append(node.function_name)
        else:
            # Validate function call
            if symbol.symbol_type not in [SymbolType.FUNCTION_DECLARATION, SymbolType.BUILTIN_FUNCTION]:
                self.error_handler.add_error(
                    SemanticError(f"'{node.function_name}' is not a function", node.line, node.column, -1)
                )
        
        # Visit arguments
        for arg in node.arguments:
            arg.accept(self)
    
    def visit_use_statement(self, node: UseStatementNode):
        """Visit use statement."""
        # Check if module is defined
        if node.module_name not in self.defined_modules:
            self.module_references.append(node.module_name)
        
        # Visit arguments
        node.arguments.accept(self)
    
    def visit_connect_statement(self, node: ConnectStatementNode):
        """Visit connect statement."""
        # Visit source and target
        node.source.accept(self)
        node.target.accept(self)
        
        # Visit attributes
        for attr in node.attributes:
            attr.accept(self)
    
    def visit_attach_statement(self, node: AttachStatementNode):
        """Visit attach statement."""
        # Visit source and target
        node.source.accept(self)
        node.target.accept(self)
    
    def visit_assign_role_statement(self, node: AssignRoleStatementNode):
        """Visit assign role statement."""
        # Check if role is defined
        if node.role_name not in self.defined_roles:
            self.role_references.append(node.role_name)
    
    # Helper methods
    
    def _declare_resource(self, node: ResourceDeclarationNode, symbol_type: SymbolType):
        """Declare a resource symbol."""
        # Check for duplicate resource
        if node.identifier in self.defined_resources:
            self.error_handler.add_error(
                SemanticError(f"Duplicate resource declaration: {node.identifier}", node.line, node.column, -1)
            )
            return
        
        # Create resource type info
        resource_type = TypeInfo(DataType.OBJECT)
        
        # Define resource symbol
        if not self.symbol_table.define_symbol(
            node.identifier, symbol_type, resource_type, node.line, node.column, node
        ):
            self.error_handler.add_error(
                SemanticError(f"Resource already defined: {node.identifier}", node.line, node.column, -1)
            )
            return
        
        self.defined_resources[node.identifier] = node
        
        # Validate attributes
        for attr in node.attributes:
            attr.accept(self)
    
    def _infer_expression_type(self, expression: ExpressionNode) -> TypeInfo:
        """Infer the type of an expression."""
        if isinstance(expression, LiteralNode):
            return TypeInfo(self._literal_to_data_type(expression.literal_type))
        elif isinstance(expression, IdentifierNode):
            symbol = self.symbol_table.lookup_symbol(expression.name)
            return symbol.type_info if symbol else TypeInfo(DataType.UNKNOWN)
        elif isinstance(expression, BinaryExpressionNode):
            return self._infer_binary_expression_type(expression)
        elif isinstance(expression, UnaryExpressionNode):
            return self._infer_unary_expression_type(expression)
        elif isinstance(expression, FunctionCallNode):
            symbol = self.symbol_table.lookup_symbol(expression.function_name)
            return symbol.type_info.return_type if symbol and symbol.type_info.return_type else TypeInfo(DataType.UNKNOWN)
        elif isinstance(expression, ArrayLiteralNode):
            if expression.elements:
                element_type = self._infer_expression_type(expression.elements[0])
                return TypeInfo(DataType.ARRAY, element_type=element_type)
            else:
                return TypeInfo(DataType.ARRAY, element_type=DataType.UNKNOWN)
        elif isinstance(expression, ObjectLiteralNode):
            return TypeInfo(DataType.OBJECT)
        else:
            return TypeInfo(DataType.UNKNOWN)
    
    def _infer_binary_expression_type(self, expr: BinaryExpressionNode) -> TypeInfo:
        """Infer type of binary expression."""
        left_type = self._infer_expression_type(expr.left)
        right_type = self._infer_expression_type(expr.right)
        
        if expr.operator in ['+', '-', '*', '/', '%']:
            # Arithmetic operations
            if left_type.data_type == DataType.FLOAT or right_type.data_type == DataType.FLOAT:
                return TypeInfo(DataType.FLOAT)
            elif left_type.data_type == DataType.INTEGER and right_type.data_type == DataType.INTEGER:
                return TypeInfo(DataType.INTEGER)
        elif expr.operator in ['==', '!=', '<', '<=', '>', '>=']:
            # Comparison operations
            return TypeInfo(DataType.BOOLEAN)
        elif expr.operator in ['and', 'or']:
            # Logical operations
            return TypeInfo(DataType.BOOLEAN)
        
        return TypeInfo(DataType.UNKNOWN)
    
    def _infer_unary_expression_type(self, expr: UnaryExpressionNode) -> TypeInfo:
        """Infer type of unary expression."""
        operand_type = self._infer_expression_type(expr.operand)
        
        if expr.operator in ['-', '+']:
            return operand_type
        elif expr.operator == 'not':
            return TypeInfo(DataType.BOOLEAN)
        
        return TypeInfo(DataType.UNKNOWN)
    
    def _literal_to_data_type(self, literal_type: str) -> DataType:
        """Convert literal type string to DataType enum."""
        mapping = {
            'integer': DataType.INTEGER,
            'float': DataType.FLOAT,
            'string': DataType.STRING,
            'boolean': DataType.BOOLEAN,
            'size': DataType.SIZE,
            'null': DataType.NULL,
        }
        return mapping.get(literal_type, DataType.UNKNOWN)
    
    def _string_to_data_type(self, type_string: str) -> TypeInfo:
        """Convert type string to TypeInfo."""
        mapping = {
            'integer': TypeInfo(DataType.INTEGER),
            'float': TypeInfo(DataType.FLOAT),
            'string': TypeInfo(DataType.STRING),
            'boolean': TypeInfo(DataType.BOOLEAN),
            'size': TypeInfo(DataType.SIZE),
            'null': TypeInfo(DataType.NULL),
            'array': TypeInfo(DataType.ARRAY),
            'object': TypeInfo(DataType.OBJECT),
        }
        return mapping.get(type_string, TypeInfo(DataType.UNKNOWN))
    
    # Inner classes for different analysis phases
    
    class _SymbolCollector(ASTVisitor):
        """Visitor for collecting symbols in the first pass."""
        
        def __init__(self, analyzer):
            self.analyzer = analyzer
        
        def visit_program(self, node: ProgramNode):
            for unit in node.compilation_units:
                unit.accept(self)
        
        def visit_compilation_unit(self, node: CompilationUnitNode):
            node.statement.accept(self)
        
        def visit_resource_declaration(self, node):
            """Handle generic resource declaration."""
            pass
        
        def visit_server(self, node: ServerNode):
            self.analyzer.visit_server(node)
        
        def visit_network(self, node: NetworkNode):
            self.analyzer.visit_network(node)
        
        def visit_database(self, node: DatabaseNode):
            self.analyzer.visit_database(node)
        
        def visit_security_group(self, node: SecurityGroupNode):
            self.analyzer.visit_security_group(node)
        
        def visit_load_balancer(self, node: LoadBalancerNode):
            self.analyzer.visit_load_balancer(node)
        
        def visit_cache(self, node: CacheNode):
            self.analyzer.visit_cache(node)
        
        def visit_container(self, node: ContainerNode):
            self.analyzer.visit_container(node)
        
        def visit_function_resource(self, node: FunctionResourceNode):
            self.analyzer.visit_function_resource(node)
        
        def visit_subnet(self, node: SubnetNode):
            self.analyzer.visit_subnet(node)
        
        def visit_module_declaration(self, node: ModuleDeclarationNode):
            self.analyzer.visit_module_declaration(node)
        
        def visit_function_declaration(self, node: FunctionDeclarationNode):
            self.analyzer.visit_function_declaration(node)
        
        def visit_variable_declaration(self, node: VariableDeclarationNode):
            self.analyzer.visit_variable_declaration(node)
        
        def visit_constant_declaration(self, node: ConstantDeclarationNode):
            self.analyzer.visit_constant_declaration(node)
        
        def visit_role_declaration(self, node: RoleDeclarationNode):
            self.analyzer.visit_role_declaration(node)
        
        def visit_policy_declaration(self, node: PolicyDeclarationNode):
            self.analyzer.visit_policy_declaration(node)
        
        def visit_if_statement(self, node: IfStatementNode):
            self.analyzer.visit_if_statement(node)
        
        def visit_for_statement(self, node: ForStatementNode):
            self.analyzer.visit_for_statement(node)
        
        def visit_identifier(self, node: IdentifierNode):
            self.analyzer.visit_identifier(node)
        
        def visit_function_call(self, node: FunctionCallNode):
            self.analyzer.visit_function_call(node)
        
        def visit_use_statement(self, node: UseStatementNode):
            self.analyzer.visit_use_statement(node)
        
        def visit_connect_statement(self, node: ConnectStatementNode):
            self.analyzer.visit_connect_statement(node)
        
        def visit_attach_statement(self, node: AttachStatementNode):
            self.analyzer.visit_attach_statement(node)
        
        def visit_assign_role_statement(self, node: AssignRoleStatementNode):
            self.analyzer.visit_assign_role_statement(node)
        
        # Default implementations for other nodes
        def visit_block(self, node: BlockNode):
            for stmt in node.statements:
                stmt.accept(self)
        
        def visit_assignment(self, node: AssignmentNode):
            node.value.accept(self)
        
        def visit_binary_expression(self, node: BinaryExpressionNode):
            node.left.accept(self)
            node.right.accept(self)
        
        def visit_unary_expression(self, node: UnaryExpressionNode):
            node.operand.accept(self)
        
        def visit_conditional_expression(self, node: ConditionalExpressionNode):
            node.condition.accept(self)
            node.then_expression.accept(self)
            if node.else_expression:
                node.else_expression.accept(self)
        
        def visit_member_access(self, node: MemberAccessNode):
            node.object_expr.accept(self)
        
        def visit_array_access(self, node: ArrayAccessNode):
            node.array_expr.accept(self)
            node.index.accept(self)
        
        def visit_literal(self, node: LiteralNode):
            pass
        
        def visit_object_literal(self, node: ObjectLiteralNode):
            for prop in node.properties:
                prop.accept(self)
        
        def visit_array_literal(self, node: ArrayLiteralNode):
            for element in node.elements:
                element.accept(self)
        
        def visit_attribute(self, node: AttributeNode):
            node.value.accept(self)
        
        def visit_parameter(self, node: ParameterNode):
            if node.default_value:
                node.default_value.accept(self)
        
        def visit_object_property(self, node: ObjectPropertyNode):
            node.value.accept(self)
        
        def visit_connection_attribute(self, node: ConnectionAttributeNode):
            node.value.accept(self)
        
        def visit_comment(self, node: CommentNode):
            pass
    
    class _Validator(ASTVisitor):
        """Visitor for validating the AST in the second pass."""
        
        def __init__(self, analyzer):
            self.analyzer = analyzer
        
        def visit_program(self, node: ProgramNode):
            for unit in node.compilation_units:
                unit.accept(self)
        
        def visit_compilation_unit(self, node: CompilationUnitNode):
            node.statement.accept(self)
        
        def visit_resource_declaration(self, node):
            """Handle generic resource declaration."""
            pass
        
        def visit_server(self, node: ServerNode):
            # Validate attributes
            for attr in node.attributes:
                attr.accept(self)
                self.analyzer.type_checker.check_attribute_type(
                    "server", attr.name, self.analyzer._infer_expression_type(attr.value)
                )
        
        def visit_network(self, node: NetworkNode):
            for attr in node.attributes:
                attr.accept(self)
                self.analyzer.type_checker.check_attribute_type(
                    "network", attr.name, self.analyzer._infer_expression_type(attr.value)
                )
        
        def visit_database(self, node: DatabaseNode):
            for attr in node.attributes:
                attr.accept(self)
                self.analyzer.type_checker.check_attribute_type(
                    node.resource_type, attr.name, self.analyzer._infer_expression_type(attr.value)
                )
        
        def visit_security_group(self, node: SecurityGroupNode):
            for attr in node.attributes:
                attr.accept(self)
        
        def visit_load_balancer(self, node: LoadBalancerNode):
            for attr in node.attributes:
                attr.accept(self)
        
        def visit_cache(self, node: CacheNode):
            for attr in node.attributes:
                attr.accept(self)
        
        def visit_container(self, node: ContainerNode):
            for attr in node.attributes:
                attr.accept(self)
        
        def visit_function_resource(self, node: FunctionResourceNode):
            for attr in node.attributes:
                attr.accept(self)
        
        def visit_subnet(self, node: SubnetNode):
            for attr in node.attributes:
                attr.accept(self)
        
        def visit_connect_statement(self, node: ConnectStatementNode):
            # Validate connection attributes
            for attr in node.attributes:
                attr.accept(self)
                
                # Check required attributes
                if attr.name == "protocol":
                    attr_type = self.analyzer._infer_expression_type(attr.value)
                    if attr_type.data_type != DataType.STRING:
                        self.analyzer.error_handler.add_error(
                            SemanticError("Protocol must be a string", attr.line, attr.column, -1)
                        )
                elif attr.name == "port":
                    attr_type = self.analyzer._infer_expression_type(attr.value)
                    if attr_type.data_type not in [DataType.INTEGER, DataType.STRING]:
                        self.analyzer.error_handler.add_error(
                            SemanticError("Port must be an integer or string", attr.line, attr.column, -1)
                        )
        
        def visit_attach_statement(self, node: AttachStatementNode):
            node.source.accept(self)
            node.target.accept(self)
        
        def visit_use_statement(self, node: UseStatementNode):
            node.arguments.accept(self)
        
        def visit_assign_role_statement(self, node: AssignRoleStatementNode):
            pass  # Already validated in symbol collection
        
        def visit_if_statement(self, node: IfStatementNode):
            # Validate condition type
            condition_type = self.analyzer._infer_expression_type(node.condition)
            if condition_type.data_type != DataType.BOOLEAN:
                self.analyzer.error_handler.add_error(
                    SemanticError("If condition must be boolean", node.condition.line, node.condition.column, -1)
                )
            
            node.condition.accept(self)
            node.then_block.accept(self)
            if node.else_block:
                node.else_block.accept(self)
        
        def visit_for_statement(self, node: ForStatementNode):
            # Validate iterable type
            iterable_type = self.analyzer._infer_expression_type(node.iterable)
            if iterable_type.data_type != DataType.ARRAY:
                self.analyzer.error_handler.add_error(
                    SemanticError("For loop iterable must be an array", node.iterable.line, node.iterable.column, -1)
                )
            
            node.iterable.accept(self)
            node.body.accept(self)
        
        def visit_assignment(self, node: AssignmentNode):
            # Check if variable is defined
            symbol = self.analyzer.symbol_table.lookup_symbol(node.identifier)
            if not symbol:
                self.analyzer.error_handler.add_error(
                    SemanticError(f"Undefined variable: {node.identifier}", node.line, node.column, -1)
                )
            
            node.value.accept(self)
        
        def visit_binary_expression(self, node: BinaryExpressionNode):
            node.left.accept(self)
            node.right.accept(self)
            
            # Validate operator compatibility
            left_type = self.analyzer._infer_expression_type(node.left)
            right_type = self.analyzer._infer_expression_type(node.right)
            
            if node.operator in ['+', '-', '*', '/', '%']:
                if left_type.data_type not in [DataType.INTEGER, DataType.FLOAT, DataType.SIZE]:
                    self.analyzer.error_handler.add_error(
                        SemanticError(f"Cannot perform arithmetic on {left_type.data_type}", node.line, node.column, -1)
                    )
                if right_type.data_type not in [DataType.INTEGER, DataType.FLOAT, DataType.SIZE]:
                    self.analyzer.error_handler.add_error(
                        SemanticError(f"Cannot perform arithmetic on {right_type.data_type}", node.line, node.column, -1)
                    )
            elif node.operator in ['and', 'or']:
                if left_type.data_type != DataType.BOOLEAN:
                    self.analyzer.error_handler.add_error(
                        SemanticError(f"Left operand of '{node.operator}' must be boolean", node.line, node.column, -1)
                    )
                if right_type.data_type != DataType.BOOLEAN:
                    self.analyzer.error_handler.add_error(
                        SemanticError(f"Right operand of '{node.operator}' must be boolean", node.line, node.column, -1)
                    )
        
        def visit_function_call(self, node: FunctionCallNode):
            # Validate arguments count
            symbol = self.analyzer.symbol_table.lookup_symbol(node.function_name)
            if symbol and symbol.type_info.parameters:
                expected_args = len(symbol.type_info.parameters)
                actual_args = len(node.arguments)
                if expected_args != actual_args:
                    self.analyzer.error_handler.add_error(
                        SemanticError(f"Function '{node.function_name}' expects {expected_args} arguments, got {actual_args}", 
                                    node.line, node.column, -1)
                    )
            
            for arg in node.arguments:
                arg.accept(self)
        
        def visit_member_access(self, node: MemberAccessNode):
            node.object_expr.accept(self)
        
        def visit_array_access(self, node: ArrayAccessNode):
            node.array_expr.accept(self)
            node.index.accept(self)
            
            # Validate index type
            index_type = self.analyzer._infer_expression_type(node.index)
            if index_type.data_type != DataType.INTEGER:
                self.analyzer.error_handler.add_error(
                    SemanticError("Array index must be integer", node.index.line, node.index.column, -1)
                )
        
        def visit_literal(self, node: LiteralNode):
            pass
        
        def visit_identifier(self, node: IdentifierNode):
            pass  # Already validated in symbol collection
        
        def visit_object_literal(self, node: ObjectLiteralNode):
            for prop in node.properties:
                prop.accept(self)
        
        def visit_array_literal(self, node: ArrayLiteralNode):
            for element in node.elements:
                element.accept(self)
        
        def visit_attribute(self, node: AttributeNode):
            node.value.accept(self)
        
        def visit_parameter(self, node: ParameterNode):
            if node.default_value:
                node.default_value.accept(self)
        
        def visit_object_property(self, node: ObjectPropertyNode):
            node.value.accept(self)
        
        def visit_connection_attribute(self, node: ConnectionAttributeNode):
            node.value.accept(self)
        
        def visit_block(self, node: BlockNode):
            for stmt in node.statements:
                stmt.accept(self)
        
        def visit_unary_expression(self, node: UnaryExpressionNode):
            node.operand.accept(self)
        
        def visit_conditional_expression(self, node: ConditionalExpressionNode):
            node.condition.accept(self)
            node.then_expression.accept(self)
            if node.else_expression:
                node.else_expression.accept(self)
        
        def visit_comment(self, node: CommentNode):
            pass
        
        def visit_variable_declaration(self, node: VariableDeclarationNode):
            if node.default_value:
                node.default_value.accept(self)
        
        def visit_constant_declaration(self, node: ConstantDeclarationNode):
            node.value.accept(self)
        
        def visit_role_declaration(self, node: RoleDeclarationNode):
            for perm in node.permissions:
                perm.accept(self)
            for res in node.resources:
                res.accept(self)
            if node.conditions:
                node.conditions.accept(self)
        
        def visit_policy_declaration(self, node: PolicyDeclarationNode):
            node.target.accept(self)
            for attr_value in node.attributes.values():
                attr_value.accept(self)
        
        def visit_module_declaration(self, node: ModuleDeclarationNode):
            for param in node.parameters:
                param.accept(self)
            for stmt in node.statements:
                stmt.accept(self)
        
        def visit_function_declaration(self, node: FunctionDeclarationNode):
            for param in node.parameters:
                param.accept(self)
            node.body.accept(self)
            node.return_expression.accept(self)
    
    # Missing abstract methods that need to be implemented
    def visit_array_access(self, node: ArrayAccessNode):
        node.array_expr.accept(self)
        node.index.accept(self)
    
    def visit_array_literal(self, node: ArrayLiteralNode):
        for element in node.elements:
            element.accept(self)
    
    def visit_assignment(self, node: AssignmentNode):
        node.value.accept(self)
    
    def visit_attribute(self, node: AttributeNode):
        node.value.accept(self)
    
    def visit_binary_expression(self, node: BinaryExpressionNode):
        node.left.accept(self)
        node.right.accept(self)
    
    def visit_block(self, node: BlockNode):
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_comment(self, node: CommentNode):
        pass
    
    def visit_conditional_expression(self, node: ConditionalExpressionNode):
        node.condition.accept(self)
        node.then_expression.accept(self)
        if node.else_expression:
            node.else_expression.accept(self)
    
    def visit_connection_attribute(self, node: ConnectionAttributeNode):
        node.value.accept(self)
    
    def visit_literal(self, node: LiteralNode):
        pass
    
    def visit_member_access(self, node: MemberAccessNode):
        node.object_expr.accept(self)
    
    def visit_object_literal(self, node: ObjectLiteralNode):
        for prop in node.properties:
            prop.value.accept(self)
    
    def visit_object_property(self, node: ObjectPropertyNode):
        node.value.accept(self)
    
    def visit_parameter(self, node: ParameterNode):
        if node.default_value:
            node.default_value.accept(self)
    
    def visit_resource_declaration(self, node):
        # Generic resource declaration handler
        pass
    
    def visit_unary_expression(self, node: UnaryExpressionNode):
        node.operand.accept(self)
