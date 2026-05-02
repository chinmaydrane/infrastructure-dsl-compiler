"""
Symbol Table Implementation for Infrastructure DSL

This module implements the symbol table used during semantic analysis.
The symbol table tracks declarations, types, scopes, and references.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from abc import ABC, abstractmethod


class SymbolType(Enum):
    """Types of symbols in the symbol table."""
    
    # Resources
    SERVER = "server"
    NETWORK = "network"
    DATABASE = "database"
    NOSQL_DB = "nosql_db"
    SECURITY_GROUP = "security_group"
    LOAD_BALANCER = "load_balancer"
    CACHE = "cache"
    CONTAINER = "container"
    FUNCTION = "function"
    SUBNET = "subnet"
    
    # Declarations
    VARIABLE = "variable"
    CONSTANT = "constant"
    FUNCTION_DECLARATION = "function_declaration"
    MODULE = "module"
    ROLE = "role"
    POLICY = "policy"
    
    # Built-in
    BUILTIN_FUNCTION = "builtin_function"
    BUILTIN_CONSTANT = "builtin_constant"
    TYPE = "type"


class DataType(Enum):
    """Data types for expressions and attributes."""
    
    # Primitive types
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    SIZE = "size"
    NULL = "null"
    
    # Complex types
    ARRAY = "array"
    OBJECT = "object"
    
    # Special types
    RESOURCE_REFERENCE = "resource_reference"
    FUNCTION_TYPE = "function_type"
    UNKNOWN = "unknown"


@dataclass
class TypeInfo:
    """Type information for symbols and expressions."""
    
    data_type: DataType
    element_type: Optional[DataType] = None  # For arrays
    properties: Optional[Dict[str, 'TypeInfo']] = None  # For objects
    parameters: Optional[List['TypeInfo']] = None  # For functions
    return_type: Optional['TypeInfo'] = None  # For functions
    
    def __str__(self) -> str:
        if self.data_type == DataType.ARRAY and self.element_type:
            return f"Array<{self.element_type.value}>"
        elif self.data_type == DataType.OBJECT and self.properties:
            props = ", ".join(f"{k}: {v}" for k, v in self.properties.items())
            return f"Object{{{props}}}"
        elif self.data_type == DataType.FUNCTION_TYPE and self.parameters and self.return_type:
            params = ", ".join(str(p) for p in self.parameters)
            return f"({params}) -> {self.return_type}"
        else:
            return self.data_type.value


@dataclass
class Symbol:
    """Represents a symbol in the symbol table."""
    
    name: str
    symbol_type: SymbolType
    type_info: TypeInfo
    scope_level: int
    line: int
    column: int
    node: Any = None  # Reference to AST node
    is_defined: bool = True
    is_used: bool = False
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
    
    def mark_used(self):
        """Mark the symbol as used."""
        self.is_used = True
    
    def add_attribute(self, key: str, value: Any):
        """Add an attribute to the symbol."""
        self.attributes[key] = value
    
    def get_attribute(self, key: str) -> Any:
        """Get an attribute from the symbol."""
        return self.attributes.get(key)


class Scope:
    """Represents a lexical scope."""
    
    def __init__(self, scope_name: str, parent: Optional['Scope'] = None, level: int = 0):
        self.scope_name = scope_name
        self.parent = parent
        self.level = level
        self.symbols: Dict[str, Symbol] = {}
        self.children: List['Scope'] = []
        
        if parent:
            parent.add_child(self)
    
    def add_child(self, child: 'Scope'):
        """Add a child scope."""
        self.children.append(child)
    
    def define_symbol(self, symbol: Symbol) -> bool:
        """
        Define a symbol in this scope.
        
        Returns:
            True if symbol was defined successfully, False if already exists
        """
        if symbol.name in self.symbols:
            return False
        
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup_symbol(self, name: str, current_scope_only: bool = False) -> Optional[Symbol]:
        """
        Look up a symbol by name.
        
        Args:
            name: Symbol name to look up
            current_scope_only: If True, only search in current scope
            
        Returns:
            Symbol if found, None otherwise
        """
        # Check current scope
        if name in self.symbols:
            return self.symbols[name]
        
        # If not found and not current scope only, search parent
        if not current_scope_only and self.parent:
            return self.parent.lookup_symbol(name)
        
        return None
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols in this scope."""
        return list(self.symbols.values())
    
    def get_symbols_by_type(self, symbol_type: SymbolType) -> List[Symbol]:
        """Get all symbols of a specific type in this scope."""
        return [sym for sym in self.symbols.values() if sym.symbol_type == symbol_type]
    
    def __str__(self) -> str:
        return f"Scope({self.scope_name}, level={self.level}, symbols={len(self.symbols)})"


class SymbolTable:
    """
    Main symbol table implementation.
    
    Manages scopes, symbols, and provides lookup services for semantic analysis.
    """
    
    def __init__(self):
        self.global_scope = Scope("global", level=0)
        self.current_scope = self.global_scope
        self.all_scopes: List[Scope] = [self.global_scope]
        self.undefined_references: List[str] = []
        self.unused_symbols: List[Symbol] = []
        
        # Initialize built-in symbols
        self._init_builtin_symbols()
    
    def _init_builtin_symbols(self):
        """Initialize built-in functions and constants."""
        
        # Built-in functions
        builtin_functions = {
            "range": TypeInfo(DataType.FUNCTION_TYPE, 
                            parameters=[TypeInfo(DataType.INTEGER)], 
                            return_type=TypeInfo(DataType.ARRAY, element_type=DataType.INTEGER)),
            "concat": TypeInfo(DataType.FUNCTION_TYPE,
                             parameters=[TypeInfo(DataType.ARRAY), TypeInfo(DataType.ARRAY)],
                             return_type=TypeInfo(DataType.ARRAY)),
            "length": TypeInfo(DataType.FUNCTION_TYPE,
                             parameters=[TypeInfo(DataType.ARRAY)],
                             return_type=TypeInfo(DataType.INTEGER)),
            "substring": TypeInfo(DataType.FUNCTION_TYPE,
                                parameters=[TypeInfo(DataType.STRING), TypeInfo(DataType.INTEGER), TypeInfo(DataType.INTEGER)],
                                return_type=TypeInfo(DataType.STRING)),
            "timestamp": TypeInfo(DataType.FUNCTION_TYPE,
                                parameters=[],
                                return_type=TypeInfo(DataType.STRING)),
            "index": TypeInfo(DataType.FUNCTION_TYPE,
                            parameters=[TypeInfo(DataType.ARRAY), TypeInfo(DataType.STRING)],
                            return_type=TypeInfo(DataType.INTEGER)),
        }
        
        for func_name, type_info in builtin_functions.items():
            symbol = Symbol(
                name=func_name,
                symbol_type=SymbolType.BUILTIN_FUNCTION,
                type_info=type_info,
                scope_level=0,
                line=-1,
                column=-1,
                is_defined=True
            )
            self.global_scope.define_symbol(symbol)
        
        # Built-in constants
        builtin_constants = {
            "true": TypeInfo(DataType.BOOLEAN),
            "false": TypeInfo(DataType.BOOLEAN),
            "null": TypeInfo(DataType.NULL),
        }
        
        for const_name, type_info in builtin_constants.items():
            symbol = Symbol(
                name=const_name,
                symbol_type=SymbolType.BUILTIN_CONSTANT,
                type_info=type_info,
                scope_level=0,
                line=-1,
                column=-1,
                is_defined=True
            )
            self.global_scope.define_symbol(symbol)
    
    def enter_scope(self, scope_name: str) -> Scope:
        """
        Enter a new scope.
        
        Args:
            scope_name: Name of the new scope
            
        Returns:
            The new scope
        """
        new_scope = Scope(
            scope_name=scope_name,
            parent=self.current_scope,
            level=self.current_scope.level + 1
        )
        self.current_scope = new_scope
        self.all_scopes.append(new_scope)
        return new_scope
    
    def exit_scope(self) -> Scope:
        """
        Exit the current scope.
        
        Returns:
            The parent scope
        """
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        return self.current_scope
    
    def define_symbol(self, name: str, symbol_type: SymbolType, type_info: TypeInfo,
                      line: int, column: int, node: Any = None) -> bool:
        """
        Define a new symbol in the current scope.
        
        Args:
            name: Symbol name
            symbol_type: Type of symbol
            type_info: Type information
            line: Line number
            column: Column number
            node: AST node reference
            
        Returns:
            True if defined successfully, False if already exists
        """
        symbol = Symbol(
            name=name,
            symbol_type=symbol_type,
            type_info=type_info,
            scope_level=self.current_scope.level,
            line=line,
            column=column,
            node=node
        )
        
        return self.current_scope.define_symbol(symbol)
    
    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol by name.
        
        Args:
            name: Symbol name to look up
            
        Returns:
            Symbol if found, None otherwise
        """
        symbol = self.current_scope.lookup_symbol(name)
        if symbol:
            symbol.mark_used()
        return symbol
    
    def lookup_in_current_scope(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in the current scope only.
        
        Args:
            name: Symbol name to look up
            
        Returns:
            Symbol if found, None otherwise
        """
        return self.current_scope.lookup_symbol(name, current_scope_only=True)
    
    def get_current_scope(self) -> Scope:
        """Get the current scope."""
        return self.current_scope
    
    def get_global_scope(self) -> Scope:
        """Get the global scope."""
        return self.global_scope
    
    def get_all_scopes(self) -> List[Scope]:
        """Get all scopes."""
        return self.all_scopes
    
    def find_symbols_by_type(self, symbol_type: SymbolType) -> List[Symbol]:
        """
        Find all symbols of a specific type across all scopes.
        
        Args:
            symbol_type: Type of symbols to find
            
        Returns:
            List of symbols of the specified type
        """
        symbols = []
        for scope in self.all_scopes:
            symbols.extend(scope.get_symbols_by_type(symbol_type))
        return symbols
    
    def get_resource_symbols(self) -> List[Symbol]:
        """Get all resource symbols."""
        resource_types = [
            SymbolType.SERVER, SymbolType.NETWORK, SymbolType.DATABASE,
            SymbolType.NOSQL_DB, SymbolType.SECURITY_GROUP, SymbolType.LOAD_BALANCER,
            SymbolType.CACHE, SymbolType.CONTAINER, SymbolType.FUNCTION, SymbolType.SUBNET
        ]
        symbols = []
        for resource_type in resource_types:
            symbols.extend(self.find_symbols_by_type(resource_type))
        return symbols
    
    def validate_references(self) -> List[str]:
        """
        Validate all symbol references.
        
        Returns:
            List of undefined references
        """
        undefined_refs = []
        
        # Check for undefined references by looking at all identifier expressions
        # This would be called after AST traversal
        
        return undefined_refs
    
    def find_unused_symbols(self) -> List[Symbol]:
        """
        Find all unused symbols.
        
        Returns:
            List of unused symbols
        """
        unused = []
        for scope in self.all_scopes:
            for symbol in scope.get_all_symbols():
                if not symbol.is_used and symbol.symbol_type not in [
                    SymbolType.BUILTIN_FUNCTION, SymbolType.BUILTIN_CONSTANT
                ]:
                    unused.append(symbol)
        return unused
    
    def check_duplicate_definitions(self) -> List[str]:
        """
        Check for duplicate symbol definitions.
        
        Returns:
            List of duplicate definition errors
        """
        duplicates = []
        global_symbols = set()
        
        for scope in self.all_scopes:
            scope_symbols = set()
            
            for symbol in scope.get_all_symbols():
                symbol_key = f"{symbol.name}@{symbol.scope_level}"
                
                if scope_level == 0:
                    if symbol.name in global_symbols:
                        duplicates.append(f"Duplicate global symbol: {symbol.name}")
                    else:
                        global_symbols.add(symbol.name)
                else:
                    if symbol.name in scope_symbols:
                        duplicates.append(f"Duplicate symbol in scope {scope.scope_name}: {symbol.name}")
                    else:
                        scope_symbols.add(symbol.name)
        
        return duplicates
    
    def get_type_info(self, symbol_name: str) -> Optional[TypeInfo]:
        """
        Get type information for a symbol.
        
        Args:
            symbol_name: Name of the symbol
            
        Returns:
            Type information if found, None otherwise
        """
        symbol = self.lookup_symbol(symbol_name)
        return symbol.type_info if symbol else None
    
    def is_compatible_type(self, source_type: TypeInfo, target_type: TypeInfo) -> bool:
        """
        Check if two types are compatible for assignment.
        
        Args:
            source_type: Source type
            target_type: Target type
            
        Returns:
            True if types are compatible
        """
        # Exact match
        if source_type.data_type == target_type.data_type:
            # For arrays, check element types
            if source_type.data_type == DataType.ARRAY:
                return (source_type.element_type == target_type.element_type or
                        target_type.element_type == DataType.UNKNOWN)
            return True
        
        # Integer can be promoted to float
        if source_type.data_type == DataType.INTEGER and target_type.data_type == DataType.FLOAT:
            return True
        
        # Any type can be assigned to unknown
        if target_type.data_type == DataType.UNKNOWN:
            return True
        
        # Null can be assigned to any reference type
        if source_type.data_type == DataType.NULL:
            return target_type.data_type in [DataType.STRING, DataType.ARRAY, DataType.OBJECT]
        
        return False
    
    def infer_expression_type(self, expression) -> TypeInfo:
        """
        Infer the type of an expression.
        
        Args:
            expression: AST expression node
            
        Returns:
            Inferred type information
        """
        # This would be implemented based on expression node types
        # For now, return unknown type
        return TypeInfo(DataType.UNKNOWN)
    
    def dump_symbols(self) -> str:
        """
        Dump all symbols for debugging.
        
        Returns:
            String representation of all symbols
        """
        output = []
        output.append("=== Symbol Table Dump ===")
        
        for scope in self.all_scopes:
            output.append(f"\n{scope}")
            for symbol in scope.get_all_symbols():
                used_status = "USED" if symbol.is_used else "UNUSED"
                output.append(f"  {symbol.name}: {symbol.symbol_type.value} - {symbol.type_info} ({used_status})")
        
        return "\n".join(output)
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the symbol table.
        
        Returns:
            Dictionary with various statistics
        """
        stats = {
            "total_scopes": len(self.all_scopes),
            "total_symbols": sum(len(scope.get_all_symbols()) for scope in self.all_scopes),
            "global_symbols": len(self.global_scope.get_all_symbols()),
            "resource_symbols": len(self.get_resource_symbols()),
            "unused_symbols": len(self.find_unused_symbols()),
        }
        
        # Count symbols by type
        for symbol_type in SymbolType:
            stats[f"{symbol_type.value}_count"] = len(self.find_symbols_by_type(symbol_type))
        
        return stats


class TypeChecker:
    """
    Type checking utilities for the semantic analyzer.
    """
    
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.errors: List[str] = []
    
    def check_type_compatibility(self, source_type: TypeInfo, target_type: TypeInfo, 
                               context: str = "") -> bool:
        """
        Check if two types are compatible.
        
        Args:
            source_type: Source type
            target_type: Target type
            context: Context for error messages
            
        Returns:
            True if compatible
        """
        if self.symbol_table.is_compatible_type(source_type, target_type):
            return True
        
        error_msg = f"Type mismatch"
        if context:
            error_msg += f" in {context}"
        error_msg += f": cannot assign {source_type} to {target_type}"
        # Create a proper error object instead of appending string
        from src.error_handler import SemanticError
        semantic_error = SemanticError(error_msg, -1, -1, -1)
        self.errors.append(semantic_error)
        return False
    
    def check_attribute_type(self, resource_type: str, attribute_name: str, 
                           attribute_type: TypeInfo) -> bool:
        """
        Check if attribute type is valid for resource type.
        
        Args:
            resource_type: Type of resource
            attribute_name: Name of attribute
            attribute_type: Type of attribute value
            
        Returns:
            True if valid
        """
        # Define valid attributes for each resource type
        valid_attributes = self._get_valid_attributes()
        
        if resource_type not in valid_attributes:
            # Create a proper error object instead of appending string
            from src.error_handler import SemanticError
            semantic_error = SemanticError(f"Unknown resource type: {resource_type}", -1, -1, -1)
            self.errors.append(semantic_error)
            return False
        
        if attribute_name not in valid_attributes[resource_type]:
            # Create a proper error object instead of appending string
            from src.error_handler import SemanticError
            semantic_error = SemanticError(f"Invalid attribute '{attribute_name}' for resource type '{resource_type}'", -1, -1, -1)
            self.errors.append(semantic_error)
            return False
        
        expected_type = valid_attributes[resource_type][attribute_name]
        return self.check_type_compatibility(attribute_type, expected_type, 
                                         f"attribute '{attribute_name}' of {resource_type}")
    
    def _get_valid_attributes(self) -> Dict[str, Dict[str, TypeInfo]]:
        """Get valid attributes for each resource type."""
        return {
            "server": {
                "cpu": TypeInfo(DataType.INTEGER),
                "memory": TypeInfo(DataType.SIZE),
                "os": TypeInfo(DataType.STRING),
                "enabled": TypeInfo(DataType.BOOLEAN),
                "tags": TypeInfo(DataType.ARRAY, element_type=DataType.STRING),
                "security_groups": TypeInfo(DataType.ARRAY, element_type=DataType.RESOURCE_REFERENCE),
                "subnet": TypeInfo(DataType.RESOURCE_REFERENCE),
            },
            "database": {
                "engine": TypeInfo(DataType.STRING),
                "version": TypeInfo(DataType.STRING),
                "storage": TypeInfo(DataType.SIZE),
                "instance_class": TypeInfo(DataType.STRING),
                "backup_retention": TypeInfo(DataType.INTEGER),
                "multi_az": TypeInfo(DataType.BOOLEAN),
                "storage_encrypted": TypeInfo(DataType.BOOLEAN),
            },
            "network": {
                "cidr_block": TypeInfo(DataType.STRING),
                "enable_dns_hostnames": TypeInfo(DataType.BOOLEAN),
                "enable_dns_support": TypeInfo(DataType.BOOLEAN),
                "tags": TypeInfo(DataType.OBJECT),
            },
            "security_group": {
                "description": TypeInfo(DataType.STRING),
                "ingress": TypeInfo(DataType.ARRAY),
                "egress": TypeInfo(DataType.ARRAY),
                "vpc": TypeInfo(DataType.RESOURCE_REFERENCE),
            },
            # Add more resource types as needed
        }
    
    def get_errors(self) -> List[str]:
        """Get all type checking errors."""
        return self.errors
    
    def clear_errors(self):
        """Clear all errors."""
        self.errors.clear()
