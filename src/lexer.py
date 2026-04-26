"""
Lexical Analyzer for Infrastructure DSL

This module implements the lexical analysis phase of the compiler.
It converts the input DSL source code into a stream of tokens for the parser.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterator
from src.error_handler import ErrorHandler, LexerError


class TokenType(Enum):
    """Token types for the Infrastructure DSL."""
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    SIZE = auto()
    NULL = auto()
    IDENTIFIER = auto()
    
    # Keywords
    SERVER = auto()
    NETWORK = auto()
    DATABASE = auto()
    NOSQL_DB = auto()
    SECURITY_GROUP = auto()
    LOAD_BALANCER = auto()
    CACHE = auto()
    CONTAINER = auto()
    FUNCTION = auto()
    SUBNET = auto()
    MODULE = auto()
    VARIABLE = auto()
    CONSTANT = auto()
    ROLE = auto()
    POLICY = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()
    USE = auto()
    WITH = auto()
    CONNECT = auto()
    ATTACH = auto()
    TO = auto()
    ASSIGN = auto()
    USER = auto()
    GROUP = auto()
    PARAM = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL_KW = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Attribute names (treated as keywords)
    TYPE = auto()
    DEFAULT = auto()
    DESCRIPTION = auto()
    PERMISSIONS = auto()
    RESOURCES = auto()
    CONDITIONS = auto()
    TARGET = auto()
    RULES = auto()
    METRICS = auto()
    ALARMS = auto()
    SCHEDULE = auto()
    RETENTION_DAYS = auto()
    BACKUP_RETENTION = auto()
    SCALE_UP_COOLDOWN = auto()
    SCALE_DOWN_COOLDOWN = auto()
    LOG_GROUPS = auto()
    LOG_STREAMS = auto()
    MIN_INSTANCES = auto()
    MAX_INSTANCES = auto()
    DESIRED_CAPACITY = auto()
    
    # Resource attributes
    CPU = auto()
    MEMORY = auto()
    OS = auto()
    ENGINE = auto()
    VERSION = auto()
    STORAGE = auto()
    INSTANCE_CLASS = auto()
    CIDR_BLOCK = auto()
    ENABLE_DNS_HOSTNAMES = auto()
    ENABLE_DNS_SUPPORT = auto()
    AVAILABILITY_ZONE = auto()
    PUBLIC = auto()
    MAP_PUBLIC_IP_ON_LAUNCH = auto()
    INGRESS = auto()
    EGRESS = auto()
    FROM_PORT = auto()
    TO_PORT = auto()
    PROTOCOL = auto()
    SECURITY_GROUPS = auto()
    CIDR_BLOCKS = auto()
    VPC = auto()
    SUBNET_GROUP = auto()
    VPC_SECURITY_GROUP_IDS = auto()
    NODE_TYPE = auto()
    NUM_CACHE_NODES = auto()
    PORT = auto()
    SUBNET_GROUP_NAME = auto()
    AUTOMATIC_FAILOVER = auto()
    MULTI_AZ_ENABLED = auto()
    READ_REPLICA_COUNT = auto()
    MULTI_AZ = auto()
    BACKUP_WINDOW = auto()
    MAINTENANCE_WINDOW = auto()
    STORAGE_TYPE = auto()
    STORAGE_ENCRYPTED = auto()
    PARAMETERS = auto()
    TAGS = auto()
    ENABLED = auto()
    MONITORING = auto()
    ALGORITHM = auto()
    TARGET_SERVERS = auto()
    LISTENERS = auto()
    CERTIFICATE_ARN = auto()
    DEFAULT_ACTION = auto()
    HEALTH_CHECK = auto()
    PATH = auto()
    INTERVAL = auto()
    TIMEOUT = auto()
    HEALTHY_THRESHOLD = auto()
    UNHEALTHY_THRESHOLD = auto()
    METRIC = auto()
    THRESHOLD = auto()
    COMPARISON = auto()
    STATISTIC = auto()
    PERIOD = auto()
    EVALUATION_PERIODS = auto()
    ADJUSTMENT_TYPE = auto()
    SCALING_ADJUSTMENT = auto()
    COLD_STORAGE_AFTER_DAYS = auto()
    DELETE_AFTER_DAYS = auto()
    LIFECYCLE = auto()
    TRANSITION_TO_IA = auto()
    TRANSITION_TO_GLACIER = auto()
    TRANSITION_TO_DEEP_ARCHIVE = auto()
    NAME = auto()
    FILTER_PATTERN = auto()
    SOURCE_IP = auto()
    SOFTWARE = auto()
    ALARM_ACTIONS = auto()
    TRANSITION = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    LESS_THAN_OR_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_THAN_OR_EQUAL = auto()
    ASSIGN_OP = auto()
    ARROW = auto()
    
    # Punctuation
    DOT = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    
    # Special
    NEWLINE = auto()
    WHITESPACE = auto()
    COMMENT = auto()
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    """Represents a token in the DSL."""
    type: TokenType
    value: str
    line: int
    column: int
    position: int
    
    def __str__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"
    
    def __repr__(self) -> str:
        return self.__str__()


class Lexer:
    """
    Lexical analyzer for Infrastructure DSL.
    
    This class converts source code into a stream of tokens using regular expressions
    and state machine patterns.
    """
    
    def __init__(self, source_code: str, error_handler: ErrorHandler):
        self.source_code = source_code
        self.error_handler = error_handler
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Define token patterns
        self.token_patterns = self._init_token_patterns()
        
        # Define keywords
        self.keywords = self._init_keywords()
    
    def _init_token_patterns(self) -> List[Tuple[TokenType, str]]:
        """Initialize regular expression patterns for tokens."""
        return [
            # Whitespace and comments
            (TokenType.WHITESPACE, r'[ \t]+'),
            (TokenType.NEWLINE, r'\r?\n'),
            (TokenType.COMMENT, r'#.*'),
            (TokenType.COMMENT, r'/\*.*?\*/'),
            
            # Literals
            (TokenType.INTEGER, r'\d+'),
            (TokenType.FLOAT, r'\d+\.\d+'),
            (TokenType.STRING, r'"(?:\\.|[^"\\])*"'),
            (TokenType.SIZE, r'\d+(?:KB|MB|GB|TB)'),
            
            # Operators and punctuation
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.MODULO, r'%'),
            (TokenType.POWER, r'\*\*'),
            (TokenType.EQUALS, r'=='),
            (TokenType.NOT_EQUALS, r'!='),
            (TokenType.LESS_THAN, r'<'),
            (TokenType.LESS_THAN_OR_EQUAL, r'<='),
            (TokenType.GREATER_THAN, r'>'),
            (TokenType.GREATER_THAN_OR_EQUAL, r'>='),
            (TokenType.ASSIGN_OP, r'='),
            (TokenType.ARROW, r'->'),
            (TokenType.DOT, r'\.'),
            (TokenType.COMMA, r','),
            (TokenType.SEMICOLON, r';'),
            (TokenType.COLON, r':'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.LBRACE, r'\{'),
            (TokenType.RBRACE, r'\}'),
            (TokenType.LBRACKET, r'\['),
            (TokenType.RBRACKET, r'\]'),
            
            # Identifiers
            (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ]
    
    def _init_keywords(self) -> dict:
        """Initialize keyword mappings."""
        return {
            # Resource types
            'server': TokenType.SERVER,
            'network': TokenType.NETWORK,
            'database': TokenType.DATABASE,
            'nosql_db': TokenType.NOSQL_DB,
            'security_group': TokenType.SECURITY_GROUP,
            'load_balancer': TokenType.LOAD_BALANCER,
            'cache': TokenType.CACHE,
            'container': TokenType.CONTAINER,
            'function': TokenType.FUNCTION,
            'subnet': TokenType.SUBNET,
            
            # Control structures
            'module': TokenType.MODULE,
            'variable': TokenType.VARIABLE,
            'constant': TokenType.CONSTANT,
            'role': TokenType.ROLE,
            'policy': TokenType.POLICY,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'use': TokenType.USE,
            'with': TokenType.WITH,
            'connect': TokenType.CONNECT,
            'attach': TokenType.ATTACH,
            'to': TokenType.TO,
            'assign': TokenType.ASSIGN,
            'user': TokenType.USER,
            'group': TokenType.GROUP,
            'param': TokenType.PARAM,
            'return': TokenType.RETURN,
            
            # Literals
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL_KW,
            
            # Logical operators
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            
            # Attribute names
            'type': TokenType.TYPE,
            'default': TokenType.DEFAULT,
            'description': TokenType.DESCRIPTION,
            'permissions': TokenType.PERMISSIONS,
            'resources': TokenType.RESOURCES,
            'conditions': TokenType.CONDITIONS,
            'target': TokenType.TARGET,
            'rules': TokenType.RULES,
            'metrics': TokenType.METRICS,
            'alarms': TokenType.ALARMS,
            'schedule': TokenType.SCHEDULE,
            'retention_days': TokenType.RETENTION_DAYS,
            'backup_retention': TokenType.BACKUP_RETENTION,
            'scale_up_cooldown': TokenType.SCALE_UP_COOLDOWN,
            'scale_down_cooldown': TokenType.SCALE_DOWN_COOLDOWN,
            'log_groups': TokenType.LOG_GROUPS,
            'log_streams': TokenType.LOG_STREAMS,
            'min_instances': TokenType.MIN_INSTANCES,
            'max_instances': TokenType.MAX_INSTANCES,
            'desired_capacity': TokenType.DESIRED_CAPACITY,
            
            # Resource attributes
            'cpu': TokenType.CPU,
            'memory': TokenType.MEMORY,
            'os': TokenType.OS,
            'engine': TokenType.ENGINE,
            'version': TokenType.VERSION,
            'storage': TokenType.STORAGE,
            'instance_class': TokenType.INSTANCE_CLASS,
            'cidr_block': TokenType.CIDR_BLOCK,
            'enable_dns_hostnames': TokenType.ENABLE_DNS_HOSTNAMES,
            'enable_dns_support': TokenType.ENABLE_DNS_SUPPORT,
            'availability_zone': TokenType.AVAILABILITY_ZONE,
            'public': TokenType.PUBLIC,
            'map_public_ip_on_launch': TokenType.MAP_PUBLIC_IP_ON_LAUNCH,
            'ingress': TokenType.INGRESS,
            'egress': TokenType.EGRESS,
            'from_port': TokenType.FROM_PORT,
            'to_port': TokenType.TO_PORT,
            'protocol': TokenType.PROTOCOL,
            'security_groups': TokenType.SECURITY_GROUPS,
            'cidr_blocks': TokenType.CIDR_BLOCKS,
            'vpc': TokenType.VPC,
            'subnet_group': TokenType.SUBNET_GROUP,
            'vpc_security_group_ids': TokenType.VPC_SECURITY_GROUP_IDS,
            'node_type': TokenType.NODE_TYPE,
            'num_cache_nodes': TokenType.NUM_CACHE_NODES,
            'port': TokenType.PORT,
            'subnet_group_name': TokenType.SUBNET_GROUP_NAME,
            'automatic_failover': TokenType.AUTOMATIC_FAILOVER,
            'multi_az_enabled': TokenType.MULTI_AZ_ENABLED,
            'read_replica_count': TokenType.READ_REPLICA_COUNT,
            'multi_az': TokenType.MULTI_AZ,
            'backup_window': TokenType.BACKUP_WINDOW,
            'maintenance_window': TokenType.MAINTENANCE_WINDOW,
            'storage_type': TokenType.STORAGE_TYPE,
            'storage_encrypted': TokenType.STORAGE_ENCRYPTED,
            'parameters': TokenType.PARAMETERS,
            'tags': TokenType.TAGS,
            'enabled': TokenType.ENABLED,
            'monitoring': TokenType.MONITORING,
            'algorithm': TokenType.ALGORITHM,
            'target_servers': TokenType.TARGET_SERVERS,
            'listeners': TokenType.LISTENERS,
            'certificate_arn': TokenType.CERTIFICATE_ARN,
            'default_action': TokenType.DEFAULT_ACTION,
            'health_check': TokenType.HEALTH_CHECK,
            'path': TokenType.PATH,
            'interval': TokenType.INTERVAL,
            'timeout': TokenType.TIMEOUT,
            'healthy_threshold': TokenType.HEALTHY_THRESHOLD,
            'unhealthy_threshold': TokenType.UNHEALTHY_THRESHOLD,
            'metric': TokenType.METRIC,
            'threshold': TokenType.THRESHOLD,
            'comparison': TokenType.COMPARISON,
            'statistic': TokenType.STATISTIC,
            'period': TokenType.PERIOD,
            'evaluation_periods': TokenType.EVALUATION_PERIODS,
            'adjustment_type': TokenType.ADJUSTMENT_TYPE,
            'scaling_adjustment': TokenType.SCALING_ADJUSTMENT,
            'cold_storage_after_days': TokenType.COLD_STORAGE_AFTER_DAYS,
            'delete_after_days': TokenType.DELETE_AFTER_DAYS,
            'lifecycle': TokenType.LIFECYCLE,
            'transition_to_ia': TokenType.TRANSITION_TO_IA,
            'transition_to_glacier': TokenType.TRANSITION_TO_GLACIER,
            'transition_to_deep_archive': TokenType.TRANSITION_TO_DEEP_ARCHIVE,
            'name': TokenType.NAME,
            'filter_pattern': TokenType.FILTER_PATTERN,
            'source_ip': TokenType.SOURCE_IP,
            'software': TokenType.SOFTWARE,
            'alarm_actions': TokenType.ALARM_ACTIONS,
            'transition': TokenType.TRANSITION,
        }
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of tokens
            
        Raises:
            LexerError: If an invalid token is encountered
        """
        self.tokens = []
        self.position = 0
        self.line = 1
        self.column = 1
        
        while self.position < len(self.source_code):
            token = self._next_token()
            if token.type != TokenType.WHITESPACE:
                self.tokens.append(token)
        
        # Add EOF token
        self.tokens.append(Token(
            TokenType.EOF,
            '',
            self.line,
            self.column,
            self.position
        ))
        
        return self.tokens
    
    def _next_token(self) -> Token:
        """
        Get the next token from the source code.
        
        Returns:
            The next token
        """
        if self.position >= len(self.source_code):
            return Token(TokenType.EOF, '', self.line, self.column, self.position)
        
        # Try each pattern
        for token_type, pattern in self.token_patterns:
            regex = re.compile(pattern)
            match = regex.match(self.source_code, self.position)
            
            if match:
                value = match.group(0)
                token = Token(token_type, value, self.line, self.column, self.position)
                
                # Update position tracking
                self._update_position(value)
                
                # Handle special cases
                if token_type == TokenType.IDENTIFIER:
                    # Check if it's a keyword
                    if value in self.keywords:
                        token.type = self.keywords[value]
                
                return token
        
        # If no pattern matched, it's an unknown token
        char = self.source_code[self.position]
        self.error_handler.add_error(
            LexerError(
                f"Unknown character: '{char}'",
                self.line,
                self.column,
                self.position
            )
        )
        
        # Create unknown token and advance
        token = Token(TokenType.UNKNOWN, char, self.line, self.column, self.position)
        self._update_position(char)
        return token
    
    def _update_position(self, text: str):
        """
        Update line, column, and position based on consumed text.
        
        Args:
            text: The text that was consumed
        """
        for char in text:
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        
        self.position += len(text)
    
    def get_tokens_iterator(self) -> Iterator[Token]:
        """
        Get an iterator over tokens.
        
        Returns:
            Iterator over the token stream
        """
        return iter(self.tokens)
    
    def peek_token(self, offset: int = 0) -> Optional[Token]:
        """
        Peek at a token without consuming it.
        
        Args:
            offset: Number of tokens to look ahead
            
        Returns:
            The token at the given offset, or None if out of bounds
        """
        index = self.current_token_index + offset
        if 0 <= index < len(self.tokens):
            return self.tokens[index]
        return None
    
    def consume_token(self) -> Optional[Token]:
        """
        Consume and return the current token.
        
        Returns:
            The current token, or None if no more tokens
        """
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            return token
        return None
    
    def reset(self):
        """Reset the lexer to the beginning of the token stream."""
        self.current_token_index = 0
    
    @property
    def current_token_index(self) -> int:
        """Get the current token index."""
        if not hasattr(self, '_current_token_index'):
            self._current_token_index = 0
        return self._current_token_index
    
    @current_token_index.setter
    def current_token_index(self, value: int):
        """Set the current token index."""
        self._current_token_index = value


class TokenStream:
    """
    Wrapper class for token stream operations.
    
    Provides convenient methods for working with the token stream
    during parsing.
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current(self) -> Optional[Token]:
        """Get the current token."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at tokens."""
        peek_position = self.position + offset
        if peek_position < len(self.tokens):
            return self.tokens[peek_position]
        return None
    
    def advance(self) -> Optional[Token]:
        """Consume the current token and advance."""
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        """
        Expect a specific token type.
        
        Args:
            token_type: The expected token type
            
        Returns:
            The token if it matches
            
        Raises:
            LexerError: If the token doesn't match
        """
        token = self.current()
        if token and token.type == token_type:
            return self.advance()
        
        raise LexerError(
            f"Expected {token_type.name}, got {token.type.name if token else 'EOF'}",
            token.line if token else -1,
            token.column if token else -1,
            token.position if token else -1
        )
    
    def match(self, *token_types: TokenType) -> bool:
        """
        Check if current token matches any of the given types.
        
        Args:
            token_types: Token types to match against
            
        Returns:
            True if current token matches any type
        """
        token = self.current()
        return token and token.type in token_types
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of the token stream."""
        return self.position >= len(self.tokens) or \
               (self.current() and self.current().type == TokenType.EOF)
    
    def reset(self):
        """Reset to the beginning of the token stream."""
        self.position = 0
    
    def get_tokens_since(self, start_position: int) -> List[Token]:
        """
        Get all tokens since a specific position.
        
        Args:
            start_position: Starting position
            
        Returns:
            List of tokens from start_position to current position
        """
        return self.tokens[start_position:self.position]
