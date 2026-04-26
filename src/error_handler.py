"""
Error Handler for Infrastructure DSL Compiler

This module provides comprehensive error handling for all phases of compilation.
It defines error types, error reporting, and error management utilities.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


class ErrorSeverity(Enum):
    """Severity levels for compiler errors."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class ErrorPhase(Enum):
    """Compilation phases where errors can occur."""
    LEXICAL = "lexical"
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    CODE_GENERATION = "code_generation"
    GENERAL = "general"


@dataclass
class CompilerError(Exception, ABC):
    """Base class for all compiler errors."""
    
    message: str
    line: int
    column: int
    position: int
    severity: ErrorSeverity = ErrorSeverity.ERROR
    phase: ErrorPhase = ErrorPhase.GENERAL
    
    def __str__(self) -> str:
        location = f"Line {self.line}, Column {self.column}"
        if self.position >= 0:
            location += f" (Position {self.position})"
        return f"[{self.severity.value.upper()}] {location}: {self.message}"
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class LexerError(CompilerError):
    """Error during lexical analysis."""
    
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.LEXICAL)


@dataclass
class SyntaxError(CompilerError):
    """Error during parsing (syntax analysis)."""
    
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.SYNTAX)


@dataclass
class ParserError(CompilerError):
    """Error during parsing (alias for SyntaxError)."""
    
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.SYNTAX)


@dataclass
class SemanticError(CompilerError):
    """Error during semantic analysis."""
    
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.SEMANTIC)


@dataclass
class CodeGenerationError(CompilerError):
    """Error during code generation."""
    
    def __init__(self, message: str, line: int, column: int, position: int):
        super().__init__(message, line, column, position, ErrorSeverity.ERROR, ErrorPhase.CODE_GENERATION)


@dataclass
class CompilerWarning(CompilerError):
    """Compiler warning."""
    
    def __init__(self, message: str, line: int, column: int, position: int, phase: ErrorPhase = ErrorPhase.GENERAL):
        super().__init__(message, line, column, position, ErrorSeverity.WARNING, phase)


@dataclass
class CompilerInfo(CompilerError):
    """Informational message."""
    
    def __init__(self, message: str, line: int, column: int, position: int, phase: ErrorPhase = ErrorPhase.GENERAL):
        super().__init__(message, line, column, position, ErrorSeverity.INFO, phase)


class ErrorHandler:
    """
    Centralized error handling for the compiler.
    
    This class collects, manages, and reports errors and warnings
    throughout the compilation process.
    """
    
    def __init__(self, max_errors: int = 100, max_warnings: int = 50):
        self.max_errors = max_errors
        self.max_warnings = max_warnings
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerWarning] = []
        self.info_messages: List[CompilerInfo] = []
        self.error_counts: Dict[ErrorPhase, int] = {phase: 0 for phase in ErrorPhase}
        self.warning_counts: Dict[ErrorPhase, int] = {phase: 0 for phase in ErrorPhase}
        self.source_lines: List[str] = []
        self.source_file: Optional[str] = None
    
    def set_source(self, source_code: str, filename: Optional[str] = None):
        """Set the source code for context in error messages."""
        self.source_lines = source_code.splitlines()
        self.source_file = filename
    
    def add_error(self, error: CompilerError):
        """Add an error to the error list."""
        if len(self.errors) >= self.max_errors:
            return
        
        self.errors.append(error)
        self.error_counts[error.phase] += 1
    
    def add_warning(self, warning: CompilerWarning):
        """Add a warning to the warning list."""
        if len(self.warnings) >= self.max_warnings:
            return
        
        self.warnings.append(warning)
        self.warning_counts[warning.phase] += 1
    
    def add_info(self, info: CompilerInfo):
        """Add an info message."""
        self.info_messages.append(info)
    
    def add_lexical_error(self, message: str, line: int, column: int, position: int):
        """Add a lexical error."""
        self.add_error(LexerError(message, line, column, position))
    
    def add_syntax_error(self, message: str, line: int, column: int, position: int):
        """Add a syntax error."""
        self.add_error(SyntaxError(message, line, column, position))
    
    def add_semantic_error(self, message: str, line: int, column: int, position: int):
        """Add a semantic error."""
        self.add_error(SemanticError(message, line, column, position))
    
    def add_code_generation_error(self, message: str, line: int, column: int, position: int):
        """Add a code generation error."""
        self.add_error(CodeGenerationError(message, line, column, position))
    
    def add_warning_message(self, message: str, line: int, column: int, position: int, phase: ErrorPhase = ErrorPhase.GENERAL):
        """Add a warning message."""
        self.add_warning(CompilerWarning(message, line, column, position, phase))
    
    def add_info_message(self, message: str, line: int, column: int, position: int, phase: ErrorPhase = ErrorPhase.GENERAL):
        """Add an info message."""
        self.add_info(CompilerInfo(message, line, column, position, phase))
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def has_semantic_errors(self) -> bool:
        """Check if there are semantic errors."""
        return self.error_counts[ErrorPhase.SEMANTIC] > 0
    
    def has_critical_errors(self) -> bool:
        """Check if there are critical errors (lexical only)."""
        return self.error_counts[ErrorPhase.LEXICAL] > 0
    
    def has_syntax_errors(self) -> bool:
        """Check if there are syntax errors."""
        return self.error_counts[ErrorPhase.SYNTAX] > 0
    
    def get_errors(self) -> List[CompilerError]:
        """Get all errors."""
        return self.errors.copy()
    
    def get_warnings(self) -> List[CompilerWarning]:
        """Get all warnings."""
        return self.warnings.copy()
    
    def get_info_messages(self) -> List[CompilerInfo]:
        """Get all info messages."""
        return self.info_messages.copy()
    
    def get_error_count(self) -> int:
        """Get total error count."""
        return len(self.errors)
    
    def get_warning_count(self) -> int:
        """Get total warning count."""
        return len(self.warnings)
    
    def get_errors_by_phase(self, phase: ErrorPhase) -> List[CompilerError]:
        """Get errors by phase."""
        return [error for error in self.errors if error.phase == phase]
    
    def get_warnings_by_phase(self, phase: ErrorPhase) -> List[CompilerWarning]:
        """Get warnings by phase."""
        return [warning for warning in self.warnings if warning.phase == phase]
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get error summary by phase."""
        return self.error_counts.copy()
    
    def get_warning_summary(self) -> Dict[str, int]:
        """Get warning summary by phase."""
        return self.warning_counts.copy()
    
    def clear_errors(self):
        """Clear all errors."""
        self.errors.clear()
        self.error_counts = {phase: 0 for phase in ErrorPhase}
    
    def clear_warnings(self):
        """Clear all warnings."""
        self.warnings.clear()
        self.warning_counts = {phase: 0 for phase in ErrorPhase}
    
    def clear_all(self):
        """Clear all messages."""
        self.clear_errors()
        self.clear_warnings()
        self.info_messages.clear()
    
    def format_error(self, error: CompilerError, include_context: bool = True) -> str:
        """
        Format an error message with optional context.
        
        Args:
            error: The error to format
            include_context: Whether to include source context
            
        Returns:
            Formatted error message
        """
        formatted = str(error)
        
        if include_context and self.source_lines and 0 <= error.line < len(self.source_lines):
            source_line = self.source_lines[error.line]
            formatted += f"\n  {source_line}"
            
            # Add pointer to error location
            if error.column > 0:
                pointer = " " * (error.column - 1) + "^"
                formatted += f"\n  {pointer}"
        
        return formatted
    
    def format_all_errors(self, include_context: bool = True) -> str:
        """Format all errors into a string."""
        if not self.errors:
            return "No errors found."
        
        messages = [f"Found {len(self.errors)} error(s):"]
        for error in self.errors:
            messages.append(self.format_error(error, include_context))
        
        return "\n".join(messages)
    
    def format_all_warnings(self, include_context: bool = True) -> str:
        """Format all warnings into a string."""
        if not self.warnings:
            return "No warnings."
        
        messages = [f"Found {len(self.warnings)} warning(s):"]
        for warning in self.warnings:
            messages.append(self.format_error(warning, include_context))
        
        return "\n".join(messages)
    
    def format_all_messages(self, include_context: bool = True) -> str:
        """Format all messages (errors, warnings, info) into a string."""
        messages = []
        
        if self.source_file:
            messages.append(f"Compilation report for: {self.source_file}")
        
        if self.errors:
            messages.append(self.format_all_errors(include_context))
        
        if self.warnings:
            messages.append(self.format_all_warnings(include_context))
        
        if self.info_messages:
            messages.append(f"Information ({len(self.info_messages)} message(s)):")
            for info in self.info_messages:
                messages.append(f"  {info}")
        
        if not self.errors and not self.warnings:
            messages.append("Compilation completed successfully with no errors or warnings.")
        
        return "\n\n".join(messages)
    
    def print_errors(self, include_context: bool = True):
        """Print all errors to stdout."""
        print(self.format_all_errors(include_context))
    
    def print_warnings(self, include_context: bool = True):
        """Print all warnings to stdout."""
        print(self.format_all_warnings(include_context))
    
    def print_all(self, include_context: bool = True):
        """Print all messages to stdout."""
        print(self.format_all_messages(include_context))
    
    def export_to_json(self) -> Dict[str, Any]:
        """Export error information to JSON format."""
        return {
            "summary": {
                "total_errors": len(self.errors),
                "total_warnings": len(self.warnings),
                "total_info": len(self.info_messages),
                "error_counts": {phase.value: count for phase, count in self.error_counts.items()},
                "warning_counts": {phase.value: count for phase, count in self.warning_counts.items()}
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
            ],
            "warnings": [
                {
                    "message": warning.message,
                    "line": warning.line,
                    "column": warning.column,
                    "position": warning.position,
                    "severity": warning.severity.value,
                    "phase": warning.phase.value
                }
                for warning in self.warnings
            ],
            "info": [
                {
                    "message": info.message,
                    "line": info.line,
                    "column": info.column,
                    "position": info.position,
                    "severity": info.severity.value,
                    "phase": info.phase.value
                }
                for info in self.info_messages
            ]
        }
    
    def get_most_common_errors(self, limit: int = 10) -> List[tuple]:
        """Get the most common error messages."""
        from collections import Counter
        error_messages = [error.message for error in self.errors]
        return Counter(error_messages).most_common(limit)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get detailed error statistics."""
        return {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "total_info": len(self.info_messages),
            "error_by_phase": {phase.value: count for phase, count in self.error_counts.items()},
            "warning_by_phase": {phase.value: count for phase, count in self.warning_counts.items()},
            "most_common_errors": self.get_most_common_errors(5),
            "error_density": len(self.errors) / max(len(self.source_lines), 1) if self.source_lines else 0
        }


class ErrorRecovery:
    """
    Error recovery utilities for the parser.
    
    Provides strategies for recovering from parsing errors
    and continuing compilation.
    """
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.synchronization_tokens = {
            TokenType.SERVER, TokenType.NETWORK, TokenType.DATABASE, TokenType.NOSQL_DB,
            TokenType.SECURITY_GROUP, TokenType.LOAD_BALANCER, TokenType.CACHE,
            TokenType.CONTAINER, TokenType.FUNCTION, TokenType.SUBNET, TokenType.MODULE,
            TokenType.VARIABLE, TokenType.CONSTANT, TokenType.ROLE, TokenType.POLICY,
            TokenType.IF, TokenType.FOR, TokenType.USE, TokenType.CONNECT, TokenType.ATTACH,
            TokenType.ASSIGN, TokenType.RBRACE, TokenType.RBRACKET, TokenType.EOF
        }
    
    def synchronize_to_statement(self, current_token):
        """
        Synchronize parser to the next statement boundary.
        
        Args:
            current_token: Current token position
        """
        # Skip tokens until we find a synchronization point
        while current_token and current_token.type not in self.synchronization_tokens:
            current_token = self._advance_token()
        
        return current_token
    
    def recover_from_mismatched_token(self, expected: str, found: str, line: int, column: int, position: int):
        """
        Recover from a mismatched token error.
        
        Args:
            expected: Expected token
            found: Found token
            line: Line number
            column: Column number
            position: Character position
        """
        self.error_handler.add_syntax_error(
            f"Expected '{expected}', found '{found}'", line, column, position
        )
    
    def recover_from_unexpected_token(self, unexpected: str, line: int, column: int, position: int):
        """
        Recover from an unexpected token error.
        
        Args:
            unexpected: Unexpected token
            line: Line number
            column: Column number
            position: Character position
        """
        self.error_handler.add_syntax_error(
            f"Unexpected token: '{unexpected}'", line, column, position
        )
    
    def _advance_token(self):
        """Advance to the next token (placeholder for actual implementation)."""
        # This would be implemented in the parser class
        return None


# Import TokenType for error recovery
try:
    from src.lexer import TokenType
except ImportError:
    # Define a placeholder if lexer is not available
    class TokenType:
        pass
