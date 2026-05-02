#!/usr/bin/env python3
"""
Infrastructure DSL Compiler - Web IDE Backend

Flask backend for the web-based IDE that compiles DSL code to JSON.
"""

import sys
import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Add the parent directory to Python path to import compiler modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.code_generator import CodeGenerator
from src.error_handler import ErrorHandler, ErrorPhase

app = Flask(__name__)
CORS(app)

def compile_dsl_to_json(dsl_code: str) -> dict:
    """
    Compile DSL code to JSON using the existing compiler pipeline.
    
    Args:
        dsl_code: DSL source code as string
        
    Returns:
        Dictionary with compilation result and output
    """
    try:
        # Initialize error handler
        error_handler = ErrorHandler()
        
        # Step 1: Lexical Analysis
        lexer = Lexer(dsl_code, error_handler)
        tokens = lexer.tokenize()
        
        # Check for lexical errors
        if error_handler.has_critical_errors():
            lexical_errors = [str(error) for error in error_handler.get_errors() 
                             if hasattr(error, 'phase') and error.phase == ErrorPhase.LEXICAL]
            return {
                "success": False,
                "error": "Lexical analysis failed",
                "details": lexical_errors,
                "phase": "lexical"
            }
        
        # Step 2: Parsing
        parser = Parser(tokens, error_handler)
        ast = parser.parse()
        
        # Check for syntax errors
        if error_handler.has_errors():
            syntax_errors = [str(error) for error in error_handler.get_errors() 
                           if hasattr(error, 'phase') and error.phase == ErrorPhase.SYNTAX]
            return {
                "success": False,
                "error": "Syntax analysis failed",
                "details": syntax_errors,
                "phase": "syntax"
            }
        
        # Step 3: Semantic Analysis
        semantic_analyzer = SemanticAnalyzer(error_handler)
        semantic_analyzer.analyze(ast)
        
        # Check for semantic errors
        if error_handler.has_errors():
            semantic_errors = [str(error) for error in error_handler.get_errors() 
                             if hasattr(error, 'phase') and error.phase == ErrorPhase.SEMANTIC]
            return {
                "success": False,
                "error": "Semantic analysis failed",
                "details": semantic_errors,
                "phase": "semantic"
            }
        
        # Step 4: Code Generation
        code_generator = CodeGenerator()
        json_output = code_generator.generate(ast)
        
        return {
            "success": True,
            "output": json_output,
            "message": "Compilation successful"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": "Internal compiler error",
            "details": [str(e)],
            "phase": "internal"
        }

@app.route('/')
def index():
    """Serve the main IDE page."""
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_dsl():
    """
    Compile DSL code endpoint.
    
    Expects JSON: { "code": "<DSL_CODE>" }
    Returns: { "success": bool, "output": str, "error": str, "details": list }
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'code' parameter in request",
                "details": []
            }), 400
        
        dsl_code = data['code']
        
        if not dsl_code.strip():
            return jsonify({
                "success": False,
                "error": "Empty DSL code",
                "details": ["Please provide some DSL code to compile"]
            }), 400
        
        # Compile the DSL code
        result = compile_dsl_to_json(dsl_code)
        
        # Return appropriate HTTP status based on success
        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server error",
            "details": [str(e)]
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Infrastructure DSL Compiler Web IDE",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    print("Starting Infrastructure DSL Compiler Web IDE...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
