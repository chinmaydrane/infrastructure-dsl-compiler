"""
JSON Code Generator for Infrastructure DSL

This module implements the code generation phase of the compiler.
It converts the AST into structured JSON output representing the infrastructure configuration.
"""

import json
from typing import Dict, List, Any, Optional
from src.ast_nodes import *
from src.error_handler import ErrorHandler, CodeGenerationError


class CodeGenerator(ASTVisitor):
    """
    Code generator that converts AST to JSON.
    
    The generator follows the visitor pattern to traverse the AST and
    generate appropriate JSON representations for each node type.
    """
    
    def __init__(self, error_handler: Optional[ErrorHandler] = None):
        self.error_handler = error_handler or ErrorHandler()
        self.output: Dict[str, Any] = {}
        self.current_context: List[str] = []
        self.generated_resources: Dict[str, Any] = {}
        self.generated_connections: List[Dict[str, Any]] = []
        self.generated_policies: Dict[str, Any] = {}
        self.generated_roles: Dict[str, Any] = {}
        self.generated_modules: Dict[str, Any] = {}
        self.generated_variables: Dict[str, Any] = {}
        self.generated_constants: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        
    def generate(self, ast: ProgramNode) -> str:
        """
        Generate JSON output from the AST.
        
        Args:
            ast: Abstract syntax tree
            
        Returns:
            JSON string representation
            
        Raises:
            CodeGenerationError: If code generation fails
        """
        try:
            # Initialize output structure
            self._initialize_output()
            
            # Visit the AST
            ast.accept(self)
            
            # Finalize output
            self._finalize_output()
            
            # Convert to JSON string
            return json.dumps(self.output, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.error_handler.add_error(
                CodeGenerationError(f"Code generation failed: {str(e)}", -1, -1, -1)
            )
            raise
    
    def _initialize_output(self):
        """Initialize the output structure."""
        self.output = {
            "version": "1.0",
            "metadata": {
                "generated_at": "",
                "compiler_version": "1.0.0",
                "dsl_version": "1.0.0"
            },
            "resources": {},
            "connections": [],
            "policies": {},
            "roles": {},
            "modules": {},
            "variables": {},
            "constants": {}
        }
    
    def _finalize_output(self):
        """Finalize the output structure."""
        # Add generated components to output
        self.output["resources"] = self.generated_resources
        self.output["connections"] = self.generated_connections
        self.output["policies"] = self.generated_policies
        self.output["roles"] = self.generated_roles
        self.output["modules"] = self.generated_modules
        self.output["variables"] = self.generated_variables
        self.output["constants"] = self.generated_constants
        
        # Update metadata
        from datetime import datetime
        self.output["metadata"]["generated_at"] = datetime.now().isoformat()
        self.output["metadata"]["resource_count"] = len(self.generated_resources)
        self.output["metadata"]["connection_count"] = len(self.generated_connections)
        self.output["metadata"]["policy_count"] = len(self.generated_policies)
        self.output["metadata"]["role_count"] = len(self.generated_roles)
    
    # Visitor methods
    
    def visit_program(self, node: ProgramNode) -> Any:
        """Visit program node."""
        for unit in node.compilation_units:
            unit.accept(self)
        return self.output
    
    def visit_compilation_unit(self, node: CompilationUnitNode) -> Any:
        """Visit compilation unit."""
        return node.statement.accept(self)
    
    def visit_server(self, node: ServerNode) -> Any:
        """Visit server declaration."""
        resource_data = {
            "type": "server",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_network(self, node: NetworkNode) -> Any:
        """Visit network declaration."""
        resource_data = {
            "type": "network",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_database(self, node: DatabaseNode) -> Any:
        """Visit database declaration."""
        resource_data = {
            "type": node.resource_type,
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_security_group(self, node: SecurityGroupNode) -> Any:
        """Visit security group declaration."""
        resource_data = {
            "type": "security_group",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_load_balancer(self, node: LoadBalancerNode) -> Any:
        """Visit load balancer declaration."""
        resource_data = {
            "type": "load_balancer",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_cache(self, node: CacheNode) -> Any:
        """Visit cache declaration."""
        resource_data = {
            "type": "cache",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_container(self, node: ContainerNode) -> Any:
        """Visit container declaration."""
        resource_data = {
            "type": "container",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_function_resource(self, node: FunctionResourceNode) -> Any:
        """Visit function resource declaration."""
        resource_data = {
            "type": "function",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_subnet(self, node: SubnetNode) -> Any:
        """Visit subnet declaration."""
        resource_data = {
            "type": "subnet",
            "name": self._get_identifier_string(node.identifier),
            "attributes": self._generate_attributes(node.attributes),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self._add_resource(self._get_identifier_string(node.identifier), resource_data)
        return resource_data
    
    def visit_connect_statement(self, node: ConnectStatementNode) -> Any:
        """Visit connect statement."""
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
    
    def visit_attach_statement(self, node: AttachStatementNode) -> Any:
        """Visit attach statement."""
        connection_data = {
            "type": "attachment",
            "source": self._generate_expression(node.source),
            "target": self._generate_expression(node.target),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self.generated_connections.append(connection_data)
        return connection_data
    
    def visit_use_statement(self, node: UseStatementNode) -> Any:
        """Visit use statement."""
        module_data = {
            "type": "module_instantiation",
            "module_name": node.module_name,
            "arguments": self._generate_expression(node.arguments),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        # Add to modules section
        module_id = f"{node.module_name}_instance_{len(self.generated_modules)}"
        self.generated_modules[module_id] = module_data
        return module_data
    
    def visit_assign_role_statement(self, node: AssignRoleStatementNode) -> Any:
        """Visit assign role statement."""
        assignment_data = {
            "type": "role_assignment",
            "role": node.role_name,
            "user_type": node.user_type,
            "user_identifier": node.user_identifier,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        # Add to roles section
        assignment_id = f"{node.role_name}_assignment_{len(self.generated_roles)}"
        self.generated_roles[assignment_id] = assignment_data
        return assignment_data
    
    def visit_role_declaration(self, node: RoleDeclarationNode) -> Any:
        """Visit role declaration."""
        role_data = {
            "type": "role",
            "name": self._get_identifier_string(node.name),
            "description": node.description,
            "permissions": [self._generate_expression(perm) for perm in node.permissions],
            "resources": [self._generate_expression(res) for res in node.resources],
            "conditions": self._generate_expression(node.conditions) if node.conditions else None,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self.generated_roles[node.name] = role_data
        return role_data
    
    def visit_policy_declaration(self, node: PolicyDeclarationNode) -> Any:
        """Visit policy declaration."""
        policy_data = {
            "type": "policy",
            "name": self._get_identifier_string(node.name),
            "policy_type": node.policy_type,
            "target": self._generate_expression(node.target),
            "attributes": {k: self._generate_expression(v) for k, v in node.attributes.items()},
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self.generated_policies[self._get_identifier_string(node.name)] = policy_data
        return policy_data
    
    def visit_module_declaration(self, node: ModuleDeclarationNode) -> Any:
        """Visit module declaration."""
        module_data = {
            "type": "module_definition",
            "name": self._get_identifier_string(node.name),
            "parameters": self._generate_parameters(node.parameters),
            "statements": [self._generate_statement(stmt) for stmt in node.statements],
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self.generated_modules[self._get_identifier_string(node.name)] = module_data
        return module_data
    
    def visit_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        """Visit variable declaration."""
        variable_data = {
            "type": "variable",
            "name": self._get_identifier_string(node.name),
            "var_type": node.var_type,
            "default_value": self._generate_expression(node.default_value) if node.default_value else None,
            "description": node.description,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self.generated_variables[self._get_identifier_string(node.name)] = variable_data
        return variable_data
    
    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> Any:
        """Visit constant declaration."""
        constant_data = {
            "type": "constant",
            "name": self._get_identifier_string(node.name),
            "value": self._generate_expression(node.value),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        
        self.generated_constants[self._get_identifier_string(node.name)] = constant_data
        return constant_data
    
    def visit_if_statement(self, node: IfStatementNode) -> Any:
        """Visit if statement."""
        if_data = {
            "type": "conditional",
            "condition": self._generate_expression(node.condition),
            "then_branch": self._generate_block(node.then_block),
            "else_branch": self._generate_block(node.else_block) if node.else_block else None,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        return if_data
    
    def visit_for_statement(self, node: ForStatementNode) -> Any:
        """Visit for statement."""
        for_data = {
            "type": "loop",
            "variable": node.variable,
            "iterable": self._generate_expression(node.iterable),
            "body": self._generate_block(node.body),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        return for_data
    
    def visit_assignment(self, node: AssignmentNode) -> Any:
        """Visit assignment."""
        assignment_data = {
            "type": "assignment",
            "identifier": self._get_identifier_string(node.identifier),
            "value": self._generate_expression(node.value),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        return assignment_data
    
    def visit_block(self, node: BlockNode) -> Any:
        """Visit block."""
        return self._generate_block(node)
    
    # Expression generation methods
    
    def visit_binary_expression(self, node: BinaryExpressionNode) -> Any:
        """Visit binary expression."""
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
    
    def visit_unary_expression(self, node: UnaryExpressionNode) -> Any:
        """Visit unary expression."""
        return {
            "type": "unary_expression",
            "operator": node.operator,
            "operand": self._generate_expression(node.operand),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_conditional_expression(self, node: ConditionalExpressionNode) -> Any:
        """Visit conditional expression."""
        return {
            "type": "conditional_expression",
            "condition": self._generate_expression(node.condition),
            "then_expression": self._generate_expression(node.then_expression),
            "else_expression": self._generate_expression(node.else_expression) if node.else_expression else None,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_function_call(self, node: FunctionCallNode) -> Any:
        """Visit function call."""
        return {
            "type": "function_call",
            "function": node.function_name,
            "arguments": [self._generate_expression(arg) for arg in node.arguments],
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_member_access(self, node: MemberAccessNode) -> Any:
        """Visit member access."""
        return {
            "type": "member_access",
            "object": self._generate_expression(node.object_expr),
            "member": node.member,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_array_access(self, node: ArrayAccessNode) -> Any:
        """Visit array access."""
        return {
            "type": "array_access",
            "array": self._generate_expression(node.array_expr),
            "index": self._generate_expression(node.index),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_literal(self, node: LiteralNode) -> Any:
        """Visit literal."""
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
        """Visit identifier."""
        return {
            "type": "identifier",
            "name": node.name,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_object_literal(self, node: ObjectLiteralNode) -> Any:
        """Visit object literal."""
        return {
            "type": "object_literal",
            "properties": {prop.key: self._generate_expression(prop.value) for prop in node.properties},
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_array_literal(self, node: ArrayLiteralNode) -> Any:
        """Visit array literal."""
        return {
            "type": "array_literal",
            "elements": [self._generate_expression(element) for element in node.elements],
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_attribute(self, node: AttributeNode) -> Any:
        """Visit attribute."""
        return {
            "name": self._get_identifier_string(node.name),
            "value": self._generate_expression(node.value),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_parameter(self, node: ParameterNode) -> Any:
        """Visit parameter."""
        return {
            "name": self._get_identifier_string(node.name),
            "default_value": self._generate_expression(node.default_value) if node.default_value else None,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_object_property(self, node: ObjectPropertyNode) -> Any:
        """Visit object property."""
        return {
            "key": self._get_identifier_string(node.key),
            "value": self._generate_expression(node.value),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_connection_attribute(self, node: ConnectionAttributeNode) -> Any:
        """Visit connection attribute."""
        return {
            "name": self._get_identifier_string(node.name),
            "value": self._generate_expression(node.value),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    def visit_comment(self, node: CommentNode) -> Any:
        """Visit comment."""
        return {
            "type": "comment",
            "text": node.text,
            "comment_type": node.comment_type,
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
    
    # Helper methods
    
    def _get_identifier_string(self, identifier) -> str:
        """Extract string value from identifier node."""
        return identifier.name if hasattr(identifier, 'name') else str(identifier)
    
    def _add_resource(self, name: str, resource_data: Dict[str, Any]):
        """Add resource to generated resources."""
        self.generated_resources[name] = resource_data
    
    def _generate_attributes(self, attributes: List[AttributeNode]) -> Dict[str, Any]:
        """Generate attributes dictionary."""
        return {attr.name.name: self._generate_expression(attr.value) for attr in attributes}
    
    def _generate_connection_attributes(self, attributes: List[ConnectionAttributeNode]) -> Dict[str, Any]:
        """Generate connection attributes dictionary."""
        return {attr.name.name: self._generate_expression(attr.value) for attr in attributes}
    
    def _generate_parameters(self, parameters: List[ParameterNode]) -> List[Dict[str, Any]]:
        """Generate parameters list."""
        return [self._generate_parameter(param) for param in parameters]
    
    def _generate_parameter(self, param: ParameterNode) -> Dict[str, Any]:
        """Generate single parameter."""
        return param.accept(self)
    
    def _generate_block(self, block: BlockNode) -> Dict[str, Any]:
        """Generate block."""
        return {
            "type": "block",
            "statements": [self._generate_statement(stmt) for stmt in block.statements],
            "metadata": {
                "line": block.line,
                "column": block.column
            }
        }
    
    def _generate_statement(self, stmt: ASTNode) -> Any:
        """Generate statement."""
        return stmt.accept(self)
    
    def _generate_expression(self, expr: ExpressionNode) -> Any:
        """Generate expression."""
        if expr is None:
            return None
        return expr.accept(self)
    
    def _simplify_literal(self, literal_data: Dict[str, Any]) -> Any:
        """
        Simplify literal data for cleaner JSON output.
        
        Args:
            literal_data: Literal data from visitor
            
        Returns:
            Simplified value
        """
        if literal_data.get("type") == "literal":
            return literal_data.get("value")
        return literal_data
    
    def _optimize_output(self) -> None:
        """Optimize the output for cleaner JSON."""
        # This method can be used to optimize the output structure
        # For example, removing unnecessary metadata in production mode
        pass
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get generation statistics.
        
        Returns:
            Dictionary with generation statistics
        """
        return {
            "resources": len(self.generated_resources),
            "connections": len(self.generated_connections),
            "policies": len(self.generated_policies),
            "roles": len(self.generated_roles),
            "modules": len(self.generated_modules),
            "variables": len(self.generated_variables),
            "constants": len(self.generated_constants),
        }
    
    # Missing abstract methods
    def visit_function_declaration(self, node):
        """Generate JSON for function declaration."""
        function_data = {
            "type": "function_declaration",
            "name": getattr(node, 'name', 'unknown'),
            "parameters": [self._generate_parameter(param) for param in getattr(node, 'parameters', [])],
            "body": self._generate_block(getattr(node, 'body', None)),
            "return_expression": self._generate_expression(getattr(node, 'return_expression', None)),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        return function_data
    
    def visit_resource_declaration(self, node):
        """Generate JSON for generic resource declaration."""
        resource_data = {
            "type": "resource_declaration",
            "name": getattr(node, 'identifier', 'unknown'),
            "attributes": self._generate_attributes(getattr(node, 'attributes', [])),
            "metadata": {
                "line": node.line,
                "column": node.column
            }
        }
        return resource_data


class OptimizedCodeGenerator(CodeGenerator):
    """
    Optimized code generator that produces cleaner JSON output.
    """
    
    def _initialize_output(self):
        """Initialize optimized output structure."""
        self.output = {
            "version": "1.0",
            "infrastructure": {
                "resources": {},
                "connections": [],
                "policies": {},
                "roles": {}
            },
            "configuration": {
                "variables": {},
                "constants": {},
                "modules": {}
            },
            "metadata": {
                "generated_at": "",
                "compiler_version": "1.0.0"
            }
        }
    
    def _finalize_output(self):
        """Finalize optimized output structure."""
        # Add generated components
        self.output["infrastructure"]["resources"] = self._optimize_resources(self.generated_resources)
        self.output["infrastructure"]["connections"] = self._optimize_connections(self.generated_connections)
        self.output["infrastructure"]["policies"] = self._optimize_policies(self.generated_policies)
        self.output["infrastructure"]["roles"] = self._optimize_roles(self.generated_roles)
        self.output["configuration"]["variables"] = self._optimize_variables(self.generated_variables)
        self.output["configuration"]["constants"] = self._optimize_constants(self.generated_constants)
        self.output["configuration"]["modules"] = self._optimize_modules(self.generated_modules)
        
        # Update metadata
        from datetime import datetime
        self.output["metadata"]["generated_at"] = datetime.now().isoformat()
        self.output["metadata"]["summary"] = {
            "total_resources": len(self.generated_resources),
            "total_connections": len(self.generated_connections),
            "total_policies": len(self.generated_policies),
            "total_roles": len(self.generated_roles)
        }
    
    def _optimize_resources(self, resources: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resources for cleaner output."""
        optimized = {}
        for name, resource in resources.items():
            optimized[name] = {
                "type": resource["type"],
                "attributes": self._simplify_attributes(resource["attributes"])
            }
        return optimized
    
    def _optimize_connections(self, connections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize connections for cleaner output."""
        optimized = []
        for conn in connections:
            optimized.append({
                "type": conn["type"],
                "source": self._simplify_expression(conn["source"]),
                "target": self._simplify_expression(conn["target"]),
                "attributes": self._simplify_attributes(conn.get("attributes", {}))
            })
        return optimized
    
    def _optimize_policies(self, policies: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize policies for cleaner output."""
        optimized = {}
        for name, policy in policies.items():
            optimized[name] = {
                "type": policy["policy_type"],
                "target": self._simplify_expression(policy["target"]),
                "rules": self._simplify_attributes(policy["attributes"])
            }
        return optimized
    
    def _optimize_roles(self, roles: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize roles for cleaner output."""
        optimized = {}
        for name, role in roles.items():
            optimized[name] = {
                "permissions": [self._simplify_expression(perm) for perm in role["permissions"]],
                "resources": [self._simplify_expression(res) for res in role["resources"]]
            }
            if role.get("conditions"):
                optimized[name]["conditions"] = self._simplify_expression(role["conditions"])
        return optimized
    
    def _optimize_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize variables for cleaner output."""
        optimized = {}
        for name, var in variables.items():
            optimized[name] = {
                "type": var["var_type"],
                "default": self._simplify_expression(var["default_value"]) if var["default_value"] else None
            }
            if var.get("description"):
                optimized[name]["description"] = var["description"]
        return optimized
    
    def _optimize_constants(self, constants: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize constants for cleaner output."""
        optimized = {}
        for name, const in constants.items():
            optimized[name] = self._simplify_expression(const["value"])
        return optimized
    
    def _optimize_modules(self, modules: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize modules for cleaner output."""
        optimized = {}
        for name, module in modules.items():
            if module["type"] == "module_definition":
                optimized[name] = {
                    "parameters": {p["name"]: self._simplify_expression(p["default_value"]) if p["default_value"] else None 
                                 for p in module["parameters"]},
                    "resources": self._extract_module_resources(module["statements"])
                }
            else:  # module_instantiation
                optimized[name] = {
                    "module": module["module_name"],
                    "arguments": self._simplify_attributes(module["arguments"])
                }
        return optimized
    
    def _simplify_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Simplify attributes dictionary."""
        simplified = {}
        for key, value in attributes.items():
            simplified[key] = self._simplify_expression(value)
        return simplified
    
    def _simplify_expression(self, expr: Any) -> Any:
        """Simplify expression for cleaner output."""
        if isinstance(expr, dict):
            if expr.get("type") == "literal":
                return expr.get("value")
            elif expr.get("type") == "identifier":
                return expr.get("name")
            elif expr.get("type") == "object_literal":
                return {k: self._simplify_expression(v) for k, v in expr.get("properties", {}).items()}
            elif expr.get("type") == "array_literal":
                return [self._simplify_expression(e) for e in expr.get("elements", [])]
            # Add more simplification rules as needed
        return expr
    
    def _extract_module_resources(self, statements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract resources from module statements."""
        resources = {}
        for stmt in statements:
            if stmt.get("type") in ["server", "network", "database", "security_group", "load_balancer", "cache", "container", "function", "subnet"]:
                resource_name = stmt.get("name", f"resource_{len(resources)}")
                resources[resource_name] = {
                    "type": stmt.get("type"),
                    "attributes": self._simplify_attributes(stmt.get("attributes", {}))
                }
        return resources
