#!/usr/bin/env python3
"""
Script to run the Infrastructure DSL Compiler

This script provides a convenient command-line interface for compiling
DSL files to JSON output.
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main as compiler_main
from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.code_generator import CodeGenerator
from src.error_handler import ErrorHandler


def run_full_compilation(source_file: str, output_file: str = None, verbose: bool = False):
    """Run the complete compilation pipeline."""
    
    # Read source file
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
        return False
    except Exception as e:
        print(f"Error reading source file: {e}")
        return False
    
    if verbose:
        print(f"Compiling: {source_file}")
        print(f"Source size: {len(source_code)} characters")
    
    # Initialize error handler
    error_handler = ErrorHandler()
    error_handler.set_source(source_code, source_file)
    
    try:
        # Step 1: Lexical Analysis
        if verbose:
            print("\n=== Lexical Analysis ===")
        
        lexer = Lexer(source_code, error_handler)
        tokens = lexer.tokenize()
        
        if verbose:
            print(f"Generated {len(tokens)} tokens")
            if error_handler.has_errors():
                print("Lexical errors detected:")
                for error in error_handler.get_errors():
                    print(f"  {error}")
        
        # Step 2: Parsing
        if verbose:
            print("\n=== Parsing ===")
        
        parser = Parser(tokens, error_handler)
        ast = parser.parse()
        
        if verbose:
            print("AST construction completed")
            if error_handler.has_errors():
                print("Syntax errors detected:")
                for error in error_handler.get_errors():
                    print(f"  {error}")
        
        # Step 3: Semantic Analysis
        if verbose:
            print("\n=== Semantic Analysis ===")
        
        semantic_analyzer = SemanticAnalyzer(error_handler)
        semantic_success = semantic_analyzer.analyze(ast)
        
        if verbose:
            print("Semantic analysis completed")
            if error_handler.has_errors():
                print("Semantic errors detected:")
                for error in error_handler.get_errors():
                    print(f"  {error}")
        
        # Step 4: Code Generation
        if verbose:
            print("\n=== Code Generation ===")
        
        code_generator = CodeGenerator(error_handler)
        json_output = code_generator.generate(ast)
        
        if verbose:
            print("JSON generation completed")
        
        # Determine output file path
        if output_file:
            output_path = Path(output_file)
        else:
            input_path = Path(source_file)
            output_path = input_path.with_suffix('.json')
        
        # Write output
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
            
            if verbose:
                print(f"Output written to: {output_path}")
        except Exception as e:
            print(f"Error writing output file: {e}")
            return False
        
        # Report compilation status
        if error_handler.has_errors():
            print(f"\nCompilation completed with {len(error_handler.get_errors())} errors")
            if verbose:
                error_handler.print_errors()
            return False
        elif error_handler.has_warnings():
            print(f"\nCompilation completed with {len(error_handler.get_warnings())} warnings")
            if verbose:
                error_handler.print_warnings()
            return True
        else:
            print("\nCompilation completed successfully")
            return True
            
    except Exception as e:
        print(f"Compilation error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False


def run_lexer_only(source_file: str, verbose: bool = False):
    """Run only the lexer and display tokens."""
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading source file: {e}")
        return False
    
    error_handler = ErrorHandler()
    lexer = Lexer(source_code, error_handler)
    tokens = lexer.tokenize()
    
    print(f"Tokens from {source_file}:")
    print("-" * 50)
    
    for i, token in enumerate(tokens):
        print(f"{i:3d}: {token}")
        
        if verbose and token.type.name == "UNKNOWN":
            print(f"     Unknown character at line {token.line}, column {token.column}")
    
    print(f"\nTotal tokens: {len(tokens)}")
    print(f"Errors: {len(error_handler.get_errors())}")
    print(f"Warnings: {len(error_handler.get_warnings())}")
    
    return len(error_handler.get_errors()) == 0


def run_ast_only(source_file: str, verbose: bool = False):
    """Run lexer and parser, display AST."""
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading source file: {e}")
        return False
    
    error_handler = ErrorHandler()
    error_handler.set_source(source_code, source_file)
    
    # Lexical analysis
    lexer = Lexer(source_code, error_handler)
    tokens = lexer.tokenize()
    
    if error_handler.has_errors():
        print("Lexical errors detected:")
        error_handler.print_errors()
        return False
    
    # Parsing
    parser = Parser(tokens, error_handler)
    ast = parser.parse()
    
    print(f"AST for {source_file}:")
    print("=" * 50)
    print(ast.to_string())
    
    if error_handler.has_errors():
        print("\nSyntax errors detected:")
        error_handler.print_errors()
        return False
    
    return True


def validate_json_output(json_file: str):
    """Validate generated JSON output."""
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"JSON validation for {json_file}:")
        print("-" * 40)
        
        # Basic structure validation
        required_sections = ["version", "metadata", "resources", "connections", "policies", "roles"]
        for section in required_sections:
            if section in data:
                if isinstance(data[section], dict):
                    print(f"✓ {section}: {len(data[section])} items")
                elif isinstance(data[section], list):
                    print(f"✓ {section}: {len(data[section])} items")
                else:
                    print(f"✓ {section}: present")
            else:
                print(f"✗ {section}: missing")
        
        # Resource validation
        if "resources" in data and isinstance(data["resources"], dict):
            print(f"\nResources found:")
            for name, resource in data["resources"].items():
                resource_type = resource.get("type", "unknown")
                print(f"  - {name} ({resource_type})")
        
        # Connection validation
        if "connections" in data and isinstance(data["connections"], list):
            print(f"\nConnections found: {len(data['connections'])}")
            for i, conn in enumerate(data["connections"]):
                conn_type = conn.get("type", "unknown")
                source = conn.get("source", {}).get("name", "unknown")
                target = conn.get("target", {}).get("name", "unknown")
                print(f"  {i+1}. {conn_type}: {source} -> {target}")
        
        print(f"\n✓ JSON file is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON validation failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error reading JSON file: {e}")
        return False


def benchmark_compiler(source_file: str, iterations: int = 10):
    """Benchmark compiler performance."""
    
    import time
    
    print(f"Benchmarking compiler with {iterations} iterations...")
    print(f"Source file: {source_file}")
    print("-" * 50)
    
    times = []
    success_count = 0
    
    for i in range(iterations):
        start_time = time.time()
        success = run_full_compilation(source_file, verbose=False)
        end_time = time.time()
        
        compilation_time = end_time - start_time
        times.append(compilation_time)
        
        if success:
            success_count += 1
        
        print(f"Iteration {i+1}: {compilation_time:.4f}s - {'Success' if success else 'Failed'}")
    
    # Calculate statistics
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\nBenchmark Results:")
    print(f"  Success rate: {success_count}/{iterations} ({100*success_count/iterations:.1f}%)")
    print(f"  Average time: {avg_time:.4f}s")
    print(f"  Min time: {min_time:.4f}s")
    print(f"  Max time: {max_time:.4f}s")
    print(f"  Total time: {sum(times):.4f}s")


def main():
    """Main entry point for the script."""
    
    parser = argparse.ArgumentParser(
        description="Infrastructure DSL Compiler Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s compile example.dsl                    # Compile to JSON
  %(prog)s compile example.dsl -o output.json    # Compile with custom output
  %(prog)s compile example.dsl -v                # Verbose compilation
  %(prog)s lexer example.dsl                      # Show tokens only
  %(prog)s ast example.dsl                        # Show AST only
  %(prog)s validate output.json                   # Validate JSON output
  %(prog)s benchmark example.dsl -i 5             # Benchmark performance
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile DSL to JSON')
    compile_parser.add_argument('input', help='Input DSL file')
    compile_parser.add_argument('-o', '--output', help='Output JSON file')
    compile_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # Lexer command
    lexer_parser = subparsers.add_parser('lexer', help='Run lexer only')
    lexer_parser.add_argument('input', help='Input DSL file')
    lexer_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # AST command
    ast_parser = subparsers.add_parser('ast', help='Show AST structure')
    ast_parser.add_argument('input', help='Input DSL file')
    ast_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON output')
    validate_parser.add_argument('input', help='Input JSON file')
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Benchmark compiler performance')
    benchmark_parser.add_argument('input', help='Input DSL file')
    benchmark_parser.add_argument('-i', '--iterations', type=int, default=10, help='Number of iterations')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == 'compile':
        success = run_full_compilation(args.input, args.output, args.verbose)
        return 0 if success else 1
    
    elif args.command == 'lexer':
        success = run_lexer_only(args.input, args.verbose)
        return 0 if success else 1
    
    elif args.command == 'ast':
        success = run_ast_only(args.input, args.verbose)
        return 0 if success else 1
    
    elif args.command == 'validate':
        success = validate_json_output(args.input)
        return 0 if success else 1
    
    elif args.command == 'benchmark':
        benchmark_compiler(args.input, args.iterations)
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
