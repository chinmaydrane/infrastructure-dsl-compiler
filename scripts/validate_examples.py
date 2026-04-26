#!/usr/bin/env python3
"""
Script to validate all example DSL files

This script compiles all example DSL files and validates the output.
It's used to ensure all examples work correctly with the compiler.
"""

import sys
import os
import json
from pathlib import Path
import traceback

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main as compiler_main
from src.error_handler import ErrorHandler


def validate_dsl_file(dsl_path: Path, verbose: bool = False) -> bool:
    """Validate a single DSL file."""
    
    print(f"\n{'='*60}")
    print(f"Validating: {dsl_path.name}")
    print(f"{'='*60}")
    
    try:
        # Read the DSL file
        with open(dsl_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        if verbose:
            print(f"File size: {len(source_code)} characters")
            print(f"Lines: {len(source_code.splitlines())}")
        
        # Initialize error handler
        error_handler = ErrorHandler()
        error_handler.set_source(source_code, str(dsl_path))
        
        # Run compilation
        from src.lexer import Lexer
        from src.parser import Parser
        from src.semantic_analyzer import SemanticAnalyzer
        from src.code_generator import CodeGenerator
        
        # Step 1: Lexical Analysis
        lexer = Lexer(source_code, error_handler)
        tokens = lexer.tokenize()
        
        if verbose:
            print(f"Tokens generated: {len(tokens)}")
        
        # Step 2: Parsing
        parser = Parser(tokens, error_handler)
        ast = parser.parse()
        
        # Step 3: Semantic Analysis
        semantic_analyzer = SemanticAnalyzer(error_handler)
        semantic_success = semantic_analyzer.analyze(ast)
        
        # Step 4: Code Generation
        code_generator = CodeGenerator(error_handler)
        json_output = code_generator.generate(ast)
        
        # Validate JSON output
        try:
            json_data = json.loads(json_output)
            json_valid = True
        except json.JSONDecodeError as e:
            print(f"❌ JSON validation failed: {e}")
            json_valid = False
        
        # Report results
        has_errors = error_handler.has_errors()
        has_warnings = error_handler.has_warnings()
        
        if has_errors:
            print(f"❌ Compilation failed with {len(error_handler.get_errors())} errors")
            if verbose:
                print("\nErrors:")
                for error in error_handler.get_errors():
                    print(f"  {error}")
        elif has_warnings:
            print(f"⚠️  Compilation completed with {len(error_handler.get_warnings())} warnings")
            if verbose:
                print("\nWarnings:")
                for warning in error_handler.get_warnings():
                    print(f"  {warning}")
        else:
            print("✅ Compilation completed successfully")
        
        if json_valid:
            print("✅ JSON output is valid")
            
            # Show basic statistics
            if isinstance(json_data, dict):
                resources = json_data.get('resources', {})
                connections = json_data.get('connections', [])
                policies = json_data.get('policies', {})
                roles = json_data.get('roles', {})
                
                print(f"📊 Statistics:")
                print(f"   Resources: {len(resources)}")
                print(f"   Connections: {len(connections)}")
                print(f"   Policies: {len(policies)}")
                print(f"   Roles: {len(roles)}")
        else:
            print("❌ JSON output is invalid")
        
        # Write output file for comparison
        output_path = dsl_path.with_suffix('.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        print(f"📝 Output written to: {output_path}")
        
        return not has_errors and json_valid
        
    except Exception as e:
        print(f"❌ Validation failed with exception: {e}")
        if verbose:
            traceback.print_exc()
        return False


def validate_all_examples(verbose: bool = False) -> bool:
    """Validate all example DSL files."""
    
    examples_dir = Path(__file__).parent.parent / 'examples'
    
    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        return False
    
    # Find all .dsl files
    dsl_files = list(examples_dir.glob('*.dsl'))
    
    if not dsl_files:
        print(f"❌ No DSL files found in {examples_dir}")
        return False
    
    print(f"Found {len(dsl_files)} DSL files to validate")
    
    results = {}
    overall_success = True
    
    for dsl_file in sorted(dsl_files):
        success = validate_dsl_file(dsl_file, verbose)
        results[dsl_file.name] = success
        overall_success = overall_success and success
    
    # Print summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"Total files: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    
    if not overall_success:
        print("\n❌ Failed files:")
        for filename, success in results.items():
            if not success:
                print(f"  - {filename}")
    else:
        print("\n✅ All files validated successfully!")
    
    return overall_success


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate Infrastructure DSL example files"
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('file', nargs='?', help='Specific DSL file to validate')
    
    args = parser.parse_args()
    
    if args.file:
        # Validate specific file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return 1
        
        success = validate_dsl_file(file_path, args.verbose)
        return 0 if success else 1
    else:
        # Validate all examples
        success = validate_all_examples(args.verbose)
        return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
