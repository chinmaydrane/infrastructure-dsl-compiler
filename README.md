# Infrastructure DSL Compiler

A comprehensive college-level compiler project that translates a Domain-Specific Language (DSL) for infrastructure modeling into structured JSON.

## Project Overview

This project implements a complete compiler pipeline for an Infrastructure Modeling DSL that allows developers to define:

- **Resources**: servers, databases, networks
- **Attributes**: CPU, memory, OS, engine versions
- **Relationships**: connections between resources
- **Policies**: autoscaling rules and security policies
- **Control Flow**: conditional statements
- **Modules**: reusable templates

## Team Contribution

This project is developed by a 4-member team with clearly defined individual contributions:

- **Member 1**: Lexical analysis and error handling system
- **Member 2**: Parser implementation and AST node definitions  
- **Member 3**: Semantic analysis and symbol table implementation
- **Member 4**: Integration coordination and main orchestration

For detailed file-by-file contribution mapping, see `TEAM_CONTRIBUTION_DISTRIBUTION.md` and `COMPLETE_FILE_CONTRIBUTION_MAPPING.md`.

## Project Structure

```
infrastructure-dsl-compiler/
├── README.md                    # This file
├── requirements.txt             # Python dependencies   
├── main.py                      # Main compiler entry point
├── TEAM_CONTRIBUTION_DISTRIBUTION.md # Team contribution mapping
├── COMPLETE_FILE_CONTRIBUTION_MAPPING.md # Complete file ownership
├── docs/
│   ├── language_specification.md
│   ├── grammar.md
│   ├── ast_design.md
│   ├── semantic_analysis.md
│   ├── code_generation.md
│   ├── error_handling.md
│   ├── project_explanation.md
│   └── viva_preparation.md
├── src/
│   ├── __init__.py
│   ├── lexer.py                 # Lexical analysis
│   ├── parser.py                # Parsing and AST construction
│   ├── ast_nodes.py             # AST node definitions
│   ├── semantic_analyzer.py     # Semantic analysis
│   ├── code_generator.py        # JSON code generation
│   ├── symbol_table.py          # Symbol table implementation
│   └── error_handler.py         # Error handling
├── grammar/
│   ├── InfrastructureDSL.g4     # ANTLR grammar file
│   └── cfg_grammar.md           # Context-free grammar
├── examples/
│   ├── basic.dsl                # Simple DSL example
│   ├── advanced.dsl             # Complex DSL example
│   ├── error_examples.dsl       # Examples with errors
│   └── outputs/                 # Generated JSON outputs
│       ├── basic.json
│       ├── advanced.json
│       └── error_outputs.json
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic_analyzer.py
│   ├── test_code_generator.py
│   └── test_integration.py
└── scripts/
    ├── run_compiler.py          # Script to run the compiler
    └── validate_examples.py     # Validate all examples
```

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the compiler on a DSL file:
   ```bash
   python main.py examples/basic.dsl
   ```

3. Run tests:
   ```bash
   python -m pytest tests/
   ```

## Compiler Pipeline

1. **Lexical Analysis**: Tokenizes the input DSL code
2. **Parsing**: Builds parse tree using ANTLR grammar
3. **AST Construction**: Creates abstract syntax tree
4. **Semantic Analysis**: Type checking, symbol resolution, validation
5. **Code Generation**: Translates AST to JSON output

## Features

- **Rich DSL Syntax**: Support for complex infrastructure definitions
- **Comprehensive Grammar**: 60+ production rules
- **Strong Type System**: Type checking and validation
- **Error Recovery**: Meaningful error messages with line numbers
- **Modular Design**: Clean separation of concerns
- **Extensible Architecture**: Easy to add new language features

## Documentation

Detailed documentation is available in the `docs/` directory:

- `language_specification.md` - Complete DSL language reference
- `grammar.md` - Grammar specifications and explanations
- `ast_design.md` - AST node design and examples
- `semantic_analysis.md` - Semantic analysis algorithms
- `code_generation.md` - JSON generation strategies
- `error_handling.md` - Error handling mechanisms
- `project_explanation.md` - Project rationale and objectives
- `viva_preparation.md` - Viva questions and answers

### Team Contribution Documentation
- `TEAM_CONTRIBUTION_DISTRIBUTION.md` - Individual team member responsibilities
- `COMPLETE_FILE_CONTRIBUTION_MAPPING.md` - Complete file-by-file ownership mapping

## Examples

The `examples/` directory contains various DSL examples ranging from basic to complex, along with their corresponding JSON outputs.

## Requirements

- Python 3.8+
- ANTLR4 runtime
- See `requirements.txt` for complete dependency list
