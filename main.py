#!/usr/bin/env python3
"""
Infrastructure DSL Compiler - Main Entry Point

This is the main entry point for the Infrastructure DSL compiler.
It orchestrates the complete compilation pipeline from DSL source to JSON output.
"""

import sys
import argparse
import json
from pathlib import Path

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.code_generator import CodeGenerator
from src.error_handler import ErrorHandler, ErrorPhase, CompilerError


def main():
    """Main compiler entry point."""
    parser = argparse.ArgumentParser(
        description="Infrastructure DSL Compiler - Translate DSL to JSON"
    )
    parser.add_argument(
        "input_file",
        help="Path to the DSL source file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file path (default: input_file.json)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--ast-only",
        action="store_true",
        help="Only generate AST, skip semantic analysis and code generation"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only perform semantic analysis, skip code generation"
    )
    
    args = parser.parse_args()
    
    # Initialize error handler
    error_handler = ErrorHandler()
    
    try:
        # Read input file
        input_path = Path(args.input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.input_file}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        if args.verbose:
            print(f"Compiling: {args.input_file}")
            print(f"Source size: {len(source_code)} characters")
        
        # Step 1: Lexical Analysis
        if args.verbose:
            print("\n=== Lexical Analysis ===")
        
        lexer = Lexer(source_code, error_handler)
        tokens = lexer.tokenize()
        
        if args.verbose:
            print(f"Generated {len(tokens)} tokens")
            if error_handler.has_errors():
                print("Lexical errors detected:")
                for error in error_handler.get_errors():
                    print(f"  {error}")
        
        # If critical lexical errors, stop compilation
        if error_handler.has_critical_errors():
            print("Compilation stopped due to lexical errors")
            return 1
        
        # Step 2: Parsing
        if args.verbose:
            print("\n=== Parsing ===")
        
        parser_instance = Parser(tokens, error_handler)
        ast = parser_instance.parse()
        
        if args.verbose:
            print("AST construction completed")
            if error_handler.has_syntax_errors():
                syntax_count = error_handler.error_counts[ErrorPhase.SYNTAX]
                print(f"{syntax_count} syntax errors detected (recovered)")
                for error in error_handler.get_errors():
                    if error.phase == ErrorPhase.SYNTAX:
                        print(f"  {error}")
        
        # If any errors exist, stop compilation
        if error_handler.has_errors():
            print("❌ COMPILATION FAILED DUE TO ERRORS")
            if args.verbose:
                # Categorize errors by type
                lexical_errors = [e for e in error_handler.get_errors() if hasattr(e, 'phase') and e.phase.name == 'LEXICAL']
                syntax_errors = [e for e in error_handler.get_errors() if hasattr(e, 'phase') and e.phase.name == 'SYNTAX']
                semantic_errors = [e for e in error_handler.get_errors() if hasattr(e, 'phase') and e.phase.name == 'SEMANTIC']
                
                total_errors = len(error_handler.get_errors())
                print(f"\n📊 ERROR SUMMARY:")
                print(f"   Total Errors: {total_errors}")
                if lexical_errors:
                    print(f"   🔤 Lexical Errors: {len(lexical_errors)}")
                if syntax_errors:
                    print(f"   📝 Syntax Errors: {len(syntax_errors)}")
                if semantic_errors:
                    print(f"   🧠 Semantic Errors: {len(semantic_errors)}")
                
                print(f"\n🔍 DETAILED ERRORS:")
                for error in error_handler.get_errors():
                    error_type = getattr(error, 'phase', 'UNKNOWN').name if hasattr(error, 'phase') else 'UNKNOWN'
                    type_emoji = {'LEXICAL': '🔤', 'SYNTAX': '📝', 'SEMANTIC': '🧠', 'UNKNOWN': '❓'}.get(error_type, '❓')
                    print(f"   {type_emoji} {error}")
                
                # Generate error report file
                error_filename = input_path.stem + '_errors.json'
                error_path = Path('error') / error_filename
                error_report = {
                    "status": "FAILED",
                    "input_file": str(input_path),
                    "error_summary": {
                        "total_errors": total_errors,
                        "lexical_errors": len(lexical_errors),
                        "syntax_errors": len(syntax_errors),
                        "semantic_errors": len(semantic_errors)
                    },
                    "errors": [
                        {
                            "type": getattr(e, 'phase', 'UNKNOWN').name if hasattr(e, 'phase') else 'UNKNOWN',
                            "message": str(e),
                            "line": getattr(e, 'line', -1),
                            "column": getattr(e, 'column', -1)
                        }
                        for e in error_handler.get_errors()
                    ]
                }
                
                with open(error_path, 'w', encoding='utf-8') as f:
                    json.dump(error_report, f, indent=2)
                
                print(f"\n📄 Error report written to: {error_path}")
            return 1
        
        # If AST-only mode, print AST and exit
        if args.ast_only:
            print("\n=== Abstract Syntax Tree ===")
            print(ast.to_string())
            return 0
        
        # Step 3: Semantic Analysis
        if args.verbose:
            print("\n=== Semantic Analysis ===")
        
        semantic_analyzer = SemanticAnalyzer(error_handler)
        semantic_analyzer.analyze(ast)
        
        if args.verbose:
            print("Semantic analysis completed")
            if error_handler.has_semantic_errors():
                semantic_count = error_handler.error_counts[ErrorPhase.SEMANTIC]
                print(f"{semantic_count} semantic errors detected")
                for error in error_handler.get_errors():
                    if error.phase == ErrorPhase.SEMANTIC:
                        print(f"  {error}")
        
        # If any errors exist after semantic analysis, stop compilation
        if error_handler.has_errors():
            print("Compilation failed due to semantic errors")
            if args.verbose:
                error_count = len(error_handler.get_errors())
                print(f"Total errors: {error_count}")
                for error in error_handler.get_errors():
                    print(f"  {error}")
            return 1
        
        # If validate-only mode, exit after semantic analysis
        if args.validate_only:
            print("Validation passed successfully")
            return 0
        
        # Step 4: Code Generation
        if args.verbose:
            print("\n=== Code Generation ===")
        
        code_generator = CodeGenerator()
        json_output = code_generator.generate(ast)
        
        if args.verbose:
            print("JSON generation completed")
        
        # Determine output file path
        if args.output:
            output_path = Path(args.output)
        else:
            # Use output/ folder for successful compilations
            output_filename = input_path.stem + '.json'
            output_path = Path('output') / output_filename
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        if args.verbose:
            print(f"Output written to: {output_path}")
        
        # Report compilation status
        if error_handler.has_errors():
            print(f"\nCompilation completed with {len(error_handler.get_errors())} errors")
            return 1
        elif error_handler.has_warnings():
            print(f"\nCompilation completed with {len(error_handler.get_warnings())} warnings")
            return 0
        else:
            print("\nCompilation completed successfully")
            return 0
            
    except CompilerError as e:
        print(f"Compiler Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
