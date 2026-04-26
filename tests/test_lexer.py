"""
Test cases for the Lexer module
"""

import unittest
from src.lexer import Lexer, TokenType, Token
from src.error_handler import ErrorHandler


class TestLexer(unittest.TestCase):
    """Test cases for the Lexer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.error_handler = ErrorHandler()
    
    def test_simple_tokens(self):
        """Test simple token recognition."""
        source = "server web_server { cpu = 4 }"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.SERVER,
            TokenType.IDENTIFIER,
            TokenType.LBRACE,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN_OP,
            TokenType.INTEGER,
            TokenType.RBRACE,
            TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_keywords(self):
        """Test keyword recognition."""
        source = "server network database security_group if else for in use with connect attach to assign"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_keywords = [
            TokenType.SERVER, TokenType.NETWORK, TokenType.DATABASE, TokenType.SECURITY_GROUP,
            TokenType.IF, TokenType.ELSE, TokenType.FOR, TokenType.IN, TokenType.USE,
            TokenType.WITH, TokenType.CONNECT, TokenType.ATTACH, TokenType.TO, TokenType.ASSIGN
        ]
        
        for i, expected_keyword in enumerate(expected_keywords):
            self.assertEqual(tokens[i].type, expected_keyword)
    
    def test_literals(self):
        """Test literal token recognition."""
        source = '42 3.14 "hello" true false null 4GB'
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_values = [
            ("42", TokenType.INTEGER),
            ("3.14", TokenType.FLOAT),
            ("\"hello\"", TokenType.STRING),
            ("true", TokenType.TRUE),
            ("false", TokenType.FALSE),
            ("null", TokenType.NULL_KW),
            ("4GB", TokenType.SIZE)
        ]
        
        for i, (expected_value, expected_type) in enumerate(expected_values):
            self.assertEqual(tokens[i].value, expected_value)
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_operators(self):
        """Test operator recognition."""
        source = "+ - * / % ** == != < <= > >="
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_operators = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.MODULO, TokenType.POWER, TokenType.EQUALS, TokenType.NOT_EQUALS,
            TokenType.LESS_THAN, TokenType.LESS_THAN_OR_EQUAL, TokenType.GREATER_THAN,
            TokenType.GREATER_THAN_OR_EQUAL
        ]
        
        for i, expected_operator in enumerate(expected_operators):
            self.assertEqual(tokens[i].type, expected_operator)
    
    def test_punctuation(self):
        """Test punctuation recognition."""
        source = ". , ; : ( ) { } [ ] -> ="
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_punctuation = [
            TokenType.DOT, TokenType.COMMA, TokenType.SEMICOLON, TokenType.COLON,
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
            TokenType.LBRACKET, TokenType.RBRACKET, TokenType.ARROW, TokenType.ASSIGN_OP
        ]
        
        for i, expected_punct in enumerate(expected_punctuation):
            self.assertEqual(tokens[i].type, expected_punct)
    
    def test_identifiers(self):
        """Test identifier recognition."""
        source = "web_server app_database vpc_sg1 _private_var camelCase"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_identifiers = [
            "web_server", "app_database", "vpc_sg1", "_private_var", "camelCase"
        ]
        
        for i, expected_id in enumerate(expected_identifiers):
            self.assertEqual(tokens[i].type, TokenType.IDENTIFIER)
            self.assertEqual(tokens[i].value, expected_id)
    
    def test_comments(self):
        """Test comment recognition."""
        source = """
        # This is a single line comment
        server "test" { cpu = 4 }
        /* This is a
           multi-line comment */
        """
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # Comments should be filtered out in the main token stream
        non_comment_tokens = [t for t in tokens if t.type != TokenType.COMMENT]
        
        # Should have: server, identifier, lbrace, identifier, assign, integer, rbrace, eof
        self.assertEqual(len(non_comment_tokens), 8)
        self.assertEqual(non_comment_tokens[0].type, TokenType.SERVER)
    
    def test_whitespace_handling(self):
        """Test whitespace handling."""
        source = "server   \t\n  web_server \t { cpu = 4 }"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # Whitespace should be skipped
        non_ws_tokens = [t for t in tokens if t.type != TokenType.WHITESPACE]
        
        expected_types = [
            TokenType.SERVER, TokenType.IDENTIFIER, TokenType.LBRACE,
            TokenType.IDENTIFIER, TokenType.ASSIGN_OP, TokenType.INTEGER,
            TokenType.RBRACE, TokenType.EOF
        ]
        
        self.assertEqual(len(non_ws_tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(non_ws_tokens[i].type, expected_type)
    
    def test_line_column_tracking(self):
        """Test line and column tracking."""
        source = """server "web_server" {
    cpu = 4
    memory = 8GB
}"""
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # Check positions of key tokens
        server_token = tokens[0]
        self.assertEqual(server_token.line, 1)
        self.assertEqual(server_token.column, 1)
        
        cpu_token = None
        for token in tokens:
            if token.value == "cpu":
                cpu_token = token
                break
        
        self.assertIsNotNone(cpu_token)
        self.assertEqual(cpu_token.line, 2)
        self.assertEqual(cpu_token.column, 5)
    
    def test_unknown_character(self):
        """Test handling of unknown characters."""
        source = "server @#$ web_server"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # Should generate errors for unknown characters
        self.assertTrue(self.error_handler.has_errors())
        
        # Should still produce valid tokens where possible
        self.assertEqual(tokens[0].type, TokenType.SERVER)
        self.assertEqual(tokens[1].type, TokenType.UNKNOWN)
        self.assertEqual(tokens[1].value, "@")
    
    def test_string_literals(self):
        """Test string literal parsing."""
        source = '"simple string" "string with \\"quotes\\"" "string with \n newline"'
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        self.assertEqual(len(tokens), 4)  # 3 strings + EOF
        self.assertEqual(tokens[0].value, '"simple string"')
        self.assertEqual(tokens[1].value, '"string with \\"quotes\\""')
        self.assertEqual(tokens[2].value, '"string with \\n newline"')
    
    def test_size_literals(self):
        """Test size literal parsing."""
        source = "1KB 2MB 4GB 8TB"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        expected_sizes = ["1KB", "2MB", "4GB", "8TB"]
        
        for i, expected_size in enumerate(expected_sizes):
            self.assertEqual(tokens[i].type, TokenType.SIZE)
            self.assertEqual(tokens[i].value, expected_size)
    
    def test_complex_source(self):
        """Test parsing a complex source file."""
        source = """
        # Define a web server
        server "web_server" {
            cpu = 4
            memory = 8GB
            os = "ubuntu-20.04"
            tags = ["web", "production"]
        }
        
        # Define a database
        database "app_db" {
            engine = "mysql"
            version = "8.0"
            storage = 100GB
        }
        
        # Connect them
        connect web_server -> app_db {
            protocol = "tcp"
            port = 3306
        }
        """
        
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # Should have many tokens but no errors
        self.assertFalse(self.error_handler.has_errors())
        self.assertGreater(len(tokens), 50)  # Should have substantial number of tokens
        
        # Check for expected key tokens
        token_values = [t.value for t in tokens]
        self.assertIn("server", token_values)
        self.assertIn("web_server", token_values)
        self.assertIn("database", token_values)
        self.assertIn("connect", token_values)
        self.assertIn("->", token_values)
    
    def test_empty_source(self):
        """Test parsing empty source."""
        lexer = Lexer("", self.error_handler)
        tokens = lexer.tokenize()
        
        # Should only have EOF token
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
    
    def test_only_whitespace(self):
        """Test parsing source with only whitespace."""
        source = "   \t\n   \t  "
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # Should only have EOF token after filtering whitespace
        non_ws_tokens = [t for t in tokens if t.type != TokenType.WHITESPACE]
        self.assertEqual(len(non_ws_tokens), 1)
        self.assertEqual(non_ws_tokens[0].type, TokenType.EOF)
    
    def test_keyword_vs_identifier(self):
        """Test that keywords are not treated as identifiers."""
        source = "server server_name"
        lexer = Lexer(source, self.error_handler)
        tokens = lexer.tokenize()
        
        # First should be SERVER keyword, second should be identifier
        self.assertEqual(tokens[0].type, TokenType.SERVER)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "server_name")


class TestTokenStream(unittest.TestCase):
    """Test cases for the TokenStream class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.error_handler = ErrorHandler()
        source = "server web { cpu = 4 }"
        lexer = Lexer(source, self.error_handler)
        self.tokens = lexer.tokenize()
        from src.lexer import TokenStream
        self.stream = TokenStream(self.tokens)
    
    def test_current_and_advance(self):
        """Test current() and advance() methods."""
        # Current should be first token
        self.assertEqual(self.stream.current().type, TokenType.SERVER)
        
        # Advance should move to next token
        self.stream.advance()
        self.assertEqual(self.stream.current().type, TokenType.IDENTIFIER)
        self.assertEqual(self.stream.current().value, "web")
    
    def test_peek(self):
        """Test peek() method."""
        # Peek should look ahead without advancing
        peeked = self.stream.peek()
        self.assertEqual(peeked.type, TokenType.IDENTIFIER)
        self.assertEqual(peeked.value, "web")
        
        # Current should still be SERVER
        self.assertEqual(self.stream.current().type, TokenType.SERVER)
    
    def test_expect(self):
        """Test expect() method."""
        # Should succeed for expected token
        token = self.stream.expect(TokenType.SERVER)
        self.assertEqual(token.type, TokenType.SERVER)
        
        # Should fail for unexpected token
        with self.assertRaises(Exception):
            self.stream.expect(TokenType.DATABASE)
    
    def test_match(self):
        """Test match() method."""
        # Should match current token
        self.assertTrue(self.stream.match(TokenType.SERVER))
        self.assertFalse(self.stream.match(TokenType.DATABASE))
        
        # Should match multiple token types
        self.assertTrue(self.stream.match(TokenType.SERVER, TokenType.IDENTIFIER))
    
    def test_is_at_end(self):
        """Test is_at_end() method."""
        # Should not be at end initially
        self.assertFalse(self.stream.is_at_end())
        
        # Advance to EOF
        while not self.stream.is_at_end():
            self.stream.advance()
        
        # Should be at end now
        self.assertTrue(self.stream.is_at_end())


if __name__ == '__main__':
    unittest.main()
