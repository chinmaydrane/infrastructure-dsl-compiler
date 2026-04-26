# Error Handling Documentation

## Overview

Error handling is a critical aspect of the Infrastructure DSL compiler. It provides comprehensive error detection, reporting, and recovery mechanisms throughout all compilation phases. This document describes the error handling architecture, strategies, and implementation details.

## Error Classification

### 1. Error Types by Phase

#### Lexical Errors
- **Invalid Characters**: Characters not recognized by the lexer
- **Unterminated Strings**: Missing closing quotes
- **Invalid Numbers**: Malformed numeric literals
- **Invalid Identifiers**: Reserved words used as identifiers

#### Syntax Errors
- **Unexpected Tokens**: Token sequence doesn't match grammar
- **Missing Tokens**: Required tokens not present
- **Mismatched Delimiters**: Unbalanced brackets, braces, parentheses
- **Invalid Structure**: Grammar rule violations

#### Semantic Errors
- **Type Mismatches**: Incompatible types in operations
- **Undefined References**: Use of undeclared identifiers
- **Duplicate Definitions**: Multiple definitions of same symbol
- **Scope Violations**: Variables used outside their scope

#### Code Generation Errors
- **Output Generation Failures**: JSON serialization errors
- **Memory Issues**: Insufficient memory for large ASTs
- **File I/O Errors**: Output file write failures
- **Internal Errors**: Unexpected conditions in generator

### 2. Error Severity Levels

```python
class ErrorSeverity(Enum):
    ERROR = "error"      # Compilation cannot continue
    WARNING = "warning"  # Compilation can continue with issues
    INFO = "info"        # Informational messages
    DEBUG = "debug"      # Debugging information
```

## Error Handler Architecture

### Core Components

```python
class ErrorHandler:
    """Centralized error handling for the compiler."""
    
    def __init__(self, max_errors: int = 100, max_warnings: int = 50):
        self.max_errors = max_errors
        self.max_warnings = max_warnings
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerWarning] = []
        self.info_messages: List[CompilerInfo] = []
        self.error_counts: Dict[ErrorPhase, int] = {phase: 0 for phase in ErrorPhase}
        self.source_lines: List[str] = []
        self.source_file: Optional[str] = None
```

### Error Types

```python
@dataclass
class CompilerError(ABC):
    """Base class for all compiler errors."""
    message: str
    line: int
    column: int
    position: int
    severity: ErrorSeverity = ErrorSeverity.ERROR
    phase: ErrorPhase = ErrorPhase.GENERAL

class LexerError(CompilerError):
    """Error during lexical analysis."""
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.LEXICAL)

class SyntaxError(CompilerError):
    """Error during parsing (syntax analysis)."""
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.SYNTAX)

class SemanticError(CompilerError):
    """Error during semantic analysis."""
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.SEMANTIC)

class CodeGenerationError(CompilerError):
    """Error during code generation."""
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.CODE_GENERATION)
```

## Error Reporting

### 1. Basic Error Format

```
[ERROR] Line 15, Column 10: Undefined identifier: 'undefined_var'
   server "web_server" {
       cpu = undefined_var
              ^^^^^^^^^^^^
```

### 2. Enhanced Error Context

```python
def format_error(self, error: CompilerError, include_context: bool = True) -> str:
    """Format an error message with optional context."""
    formatted = str(error)
    
    if include_context and self.source_lines and 0 <= error.line < len(self.source_lines):
        source_line = self.source_lines[error.line]
        formatted += f"\n  {source_line}"
        
        # Add pointer to error location
        if error.column > 0:
            pointer = " " * (error.column - 1) + "^"
            formatted += f"\n  {pointer}"
    
    return formatted
```

### 3. Error Summary

```python
def format_all_errors(self, include_context: bool = True) -> str:
    """Format all errors into a string."""
    if not self.errors:
        return "No errors found."
    
    messages = [f"Found {len(self.errors)} error(s):"]
    for error in self.errors:
        messages.append(self.format_error(error, include_context))
    
    return "\n".join(messages)
```

## Error Recovery Strategies

### 1. Lexical Error Recovery

```python
def _next_token(self) -> Token:
    """Get the next token from the source code."""
    if self.position >= len(self.source_code):
        return Token(TokenType.EOF, '', self.line, self.column, self.position)
    
    # Try each pattern
    for token_type, pattern in self.token_patterns:
        regex = re.compile(pattern)
        match = regex.match(self.source_code, self.position)
        
        if match:
            value = match.group(0)
            token = Token(token_type, value, self.line, self.column, self.position)
            self._update_position(value)
            return token
    
    # If no pattern matched, create unknown token and continue
    char = self.source_code[self.position]
    self.error_handler.add_error(
        LexerError(f"Unknown character: '{char}'", self.line, self.column, self.position)
    )
    
    token = Token(TokenType.UNKNOWN, char, self.line, self.column, self.position)
    self._update_position(char)
    return token
```

### 2. Parsing Error Recovery

```python
def _skip_to_next_statement(self):
    """Skip tokens until we reach the next likely statement start."""
    while not self.token_stream.is_at_end():
        if self._match(
            TokenType.SERVER, TokenType.NETWORK, TokenType.DATABASE,
            TokenType.IF, TokenType.FOR, TokenType.USE, TokenType.CONNECT,
            TokenType.RBRACE, TokenType.EOF
        ):
            break
        self._advance()
```

### 3. Semantic Error Recovery

```python
def analyze_resource_declaration(self, node: ResourceDeclarationNode):
    """Analyze a resource declaration with error recovery."""
    try:
        # Check for duplicate resources
        if node.identifier in self.defined_resources:
            self.error_handler.add_error(
                SemanticError(f"Duplicate resource declaration: {node.identifier}", 
                             node.line, node.column, -1)
            )
            return  # Skip processing this resource
        
        # Continue with normal processing
        self._process_resource(node)
        
    except Exception as e:
        # Log error and continue with next resource
        self.error_handler.add_error(
            SemanticError(f"Error analyzing resource {node.identifier}: {str(e)}", 
                         node.line, node.column, -1)
        )
```

## Phase-Specific Error Handling

### 1. Lexical Analysis Errors

#### Invalid Character Detection

```python
# Input contains invalid characters
server "test" {
    cpu = 4@  # Invalid character '@'
}
```

```
[ERROR] Line 3, Column 12: Unknown character: '@'
   cpu = 4@
            ^
```

#### Unterminated String

```python
# Input has unterminated string
server "test" {
    name = "unterminated string
}
```

```
[ERROR] Line 3, Column 11: Unterminated string literal
   name = "unterminated string
          ^^^^^^^^^^^^^^^^^^^^^^^^
```

### 2. Syntax Errors

#### Missing Closing Brace

```python
# Input missing closing brace
server "test" {
    cpu = 4
    memory = 8GB
# Missing }
```

```
[ERROR] Line 5, Column 1: Expected '}', found EOF
   ^
```

#### Unexpected Token

```python
# Input has unexpected token
server "test" {
    cpu = 4
    invalid_token = true
}
```

```
[ERROR] Line 4, Column 5: Unexpected token: 'invalid_token'
   invalid_token = true
   ^^^^^^^^^^^^^
```

### 3. Semantic Errors

#### Type Mismatch

```python
# Type mismatch in assignment
server "test" {
    cpu = "not_a_number"  # Should be integer
}
```

```
[ERROR] Line 3, Column 11: Type mismatch in assignment
   cpu = "not_a_number"
         ^^^^^^^^^^^^^^^
Expected: integer, got: string
```

#### Undefined Reference

```python
# Reference to undefined resource
connect nonexistent_server -> database {
    protocol = "tcp"
}
```

```
[ERROR] Line 1, Column 10: Undefined resource reference: 'nonexistent_server'
   connect nonexistent_server -> database {
           ^^^^^^^^^^^^^^^^^^^^
```

#### Duplicate Definition

```python
# Duplicate resource definition
server "duplicate" {
    cpu = 2
}

server "duplicate" {
    cpu = 4
}
```

```
[ERROR] Line 6, Column 1: Duplicate resource declaration: 'duplicate'
   server "duplicate" {
   ^^^^^^^^^^^^^^^^^^^
Previously defined at line 2, column 1
```

### 4. Code Generation Errors

#### JSON Serialization Error

```python
# Error during JSON generation
[ERROR] Line 15, Column 10: Code generation failed: Object of type 'ComplexObject' is not JSON serializable
```

## Error Statistics and Analysis

### 1. Error Collection

```python
def get_error_statistics(self) -> Dict[str, Any]:
    """Get detailed error statistics."""
    return {
        "total_errors": len(self.errors),
        "total_warnings": len(self.warnings),
        "error_by_phase": {phase.value: count for phase, count in self.error_counts.items()},
        "most_common_errors": self.get_most_common_errors(5),
        "error_density": len(self.errors) / max(len(self.source_lines), 1) if self.source_lines else 0
    }
```

### 2. Error Pattern Analysis

```python
def get_most_common_errors(self, limit: int = 10) -> List[tuple]:
    """Get the most common error messages."""
    from collections import Counter
    error_messages = [error.message for error in self.errors]
    return Counter(error_messages).most_common(limit)
```

### 3. Error Export

```python
def export_to_json(self) -> Dict[str, Any]:
    """Export error information to JSON format."""
    return {
        "summary": {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "error_counts": {phase.value: count for phase, count in self.error_counts.items()}
        },
        "errors": [
            {
                "message": error.message,
                "line": error.line,
                "column": error.column,
                "position": error.position,
                "severity": error.severity.value,
                "phase": error.phase.value
            }
            for error in self.errors
        ]
    }
```

## Warning System

### 1. Warning Categories

#### Unused Symbols

```python
# Warning for unused variable
variable "unused_var" {
    type = "string"
    default = "value"
}
```

```
[WARNING] Line 1, Column 1: Unused variable: 'unused_var'
   variable "unused_var" {
   ^^^^^^^^^^^^^^^^^^^^
```

#### Deprecated Features

```python
# Warning for deprecated syntax
old_syntax_resource "test" {
    # This syntax is deprecated
}
```

```
[WARNING] Line 1, Column 1: Deprecated syntax: 'old_syntax_resource'
   old_syntax_resource "test" {
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use 'server' instead
```

#### Performance Issues

```python
# Warning for potential performance issue
for i in range(10000) {
    server "server_${i}" {
        cpu = 2
        memory = 4GB
    }
}
```

```
[WARNING] Line 1, Column 5: Large loop iteration count may impact performance
   for i in range(10000) {
       ^^^^^^^^^^^^^^^^^^^^
Consider using modules or templates instead
```

## Error Prevention and User Guidance

### 1. Suggestive Error Messages

```python
def suggest_fix(self, error: CompilerError) -> str:
    """Suggest fixes for common errors."""
    suggestions = {
        "Undefined identifier": "Check if the identifier is spelled correctly and defined before use",
        "Type mismatch": "Check the expected type and ensure the value is compatible",
        "Duplicate declaration": "Use a different name or remove the duplicate declaration",
        "Missing closing brace": "Add the missing closing brace '}'",
        "Unexpected token": "Check the syntax and remove or replace the unexpected token"
    }
    
    for pattern, suggestion in suggestions.items():
        if pattern in error.message:
            return f"Suggestion: {suggestion}"
    
    return ""
```

### 2. Context-Aware Help

```python
def get_help_context(self, error: CompilerError) -> Dict[str, Any]:
    """Get help context for the error."""
    return {
        "error_type": type(error).__name__,
        "documentation_link": f"https://dsl-docs.com/errors/{type(error).__name__.lower()}",
        "related_examples": self.get_related_examples(error),
        "common_fixes": self.get_common_fixes(error)
    }
```

## Testing Error Handling

### 1. Error Case Testing

```python
class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling."""
    
    def test_lexical_errors(self):
        """Test lexical error detection and reporting."""
        source = 'server "test" { cpu = 4@ }'
        error_handler = ErrorHandler()
        lexer = Lexer(source, error_handler)
        tokens = lexer.tokenize()
        
        self.assertTrue(error_handler.has_errors())
        self.assertEqual(len(error_handler.get_errors()), 1)
        self.assertIn("Unknown character", error_handler.get_errors()[0].message)
    
    def test_syntax_errors(self):
        """Test syntax error detection and reporting."""
        source = 'server "test" cpu = 4'  # Missing braces
        error_handler = ErrorHandler()
        # ... run compilation
        self.assertTrue(error_handler.has_errors())
    
    def test_semantic_errors(self):
        """Test semantic error detection and reporting."""
        source = '''
        server "test" {
            cpu = "not_a_number"  # Type error
        }
        '''
        error_handler = ErrorHandler()
        # ... run compilation
        self.assertTrue(error_handler.has_errors())
        self.assertIn("Type mismatch", error_handler.get_errors()[0].message)
```

### 2. Error Recovery Testing

```python
def test_error_recovery(self):
    """Test that compilation continues after errors."""
    source = '''
    server "bad1" { cpu = @ }  # Lexical error
    server "good" { cpu = 4 }    # Should still be processed
    server "bad2" { cpu = "x" } # Semantic error
    '''
    
    error_handler = ErrorHandler()
    # ... run compilation
    
    # Should detect multiple errors
    self.assertGreaterEqual(len(error_handler.get_errors()), 2)
    
    # Should still process the good resource
    # ... verify good resource was processed
```

## Best Practices

### 1. Error Message Design

- **Be Specific**: Clearly identify what went wrong
- **Provide Context**: Show where the error occurred
- **Suggest Solutions**: Help users fix the problem
- **Be Consistent**: Use consistent formatting and terminology

### 2. Error Recovery Strategy

- **Continue When Possible**: Don't stop at the first error
- **Maintain State**: Keep compiler in valid state after errors
- **Limit Cascading Errors**: Prevent one error from causing many others
- **Provide Partial Results**: Generate output even with errors

### 3. User Experience

- **Group Related Errors**: Show related errors together
- **Prioritize Errors**: Show most important errors first
- **Progress Indication**: Show compilation progress
- **Recovery Options**: Allow users to fix errors incrementally

## Future Enhancements

### 1. Advanced Error Recovery

- **Intelligent Repair**: Automatically fix common errors
- **Partial Compilation**: Compile valid portions only
- **Incremental Compilation**: Re-compile only changed parts
- **Error Suppression**: Allow users to ignore certain errors

### 2. Enhanced User Experience

- **IDE Integration**: Real-time error highlighting
- **Fix Suggestions**: Automated fix recommendations
- **Error Templates**: Common error patterns and solutions
- **Interactive Debugging**: Step-by-step error investigation

### 3. Analytics and Learning

- **Error Pattern Analysis**: Identify common user mistakes
- **Documentation Improvement**: Update docs based on errors
- **Language Evolution**: Improve language based on usage patterns
- **User Feedback**: Collect and analyze user error reports

This comprehensive error handling system ensures that the Infrastructure DSL compiler provides clear, actionable feedback to users while maintaining robust operation even in the presence of errors.
