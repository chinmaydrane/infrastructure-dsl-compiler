# Infrastructure DSL Compiler - Test Suite

This test suite demonstrates the compiler's capabilities across various scenarios and edge cases.

## Test Files Overview

### 1. `01_basic_resources.dsl`
**Purpose**: Demonstrates fundamental resource types
- Server, Database, Network, Security Group declarations
- Basic attribute assignments
- Simple data types (strings, numbers, booleans)

**Expected Output**: Multiple resources with basic configurations

### 2. `02_complex_expressions.dsl`
**Purpose**: Complex expressions and nested data structures
- Object literals with nested objects
- Array literals with mixed types
- Complex resource configurations
- Multi-level data structures

**Expected Output**: Resources with complex nested configurations

### 3. `03_control_flow.dsl`
**Purpose**: Control flow and conditional logic
- If-else statements
- Variable declarations
- Conditional resource creation
- Environment-based configurations

**Expected Output**: Different resources based on conditions

### 4. `04_modules_and_functions.dsl`
**Purpose**: Modular design and function definitions
- Function definitions with parameters
- Module declarations and usage
- Complex parameter passing
- Code reusability patterns

**Expected Output**: Infrastructure created through modules and functions

### 5. `05_connections_and_policies.dsl`
**Purpose**: Resource relationships and policy enforcement
- Resource connections
- Security policies
- Role definitions and assignments
- Complex infrastructure relationships

**Expected Output**: Connected resources with policies and roles

### 6. `06_edge_cases.dsl`
**Purpose**: Edge cases and complex scenarios
- Deeply nested structures
- Complex conditional logic
- Large data structures
- Function complexity
- Empty and default values

**Expected Output**: Complex infrastructure with edge case handling

### 7. `07_error_scenarios.dsl`
**Purpose**: Error scenarios and invalid syntax
- Syntax errors (missing brackets, quotes)
- Semantic errors (undefined references, type mismatches)
- Duplicate resource names
- Invalid policy targets
- Circular dependencies

**Expected Output**: Compilation stopped with detailed error messages

### 8. `08_working_example.dsl`
**Purpose**: Working example for successful compilation
- Clean syntax
- Proper resource definitions
- Simple control flow
- Should compile with minimal errors

**Expected Output**: Successful JSON generation

## Compiler Behavior Demonstration

### Error Handling Flow
```
=== Lexical Analysis ===
Generated tokens
[ERRORS] - Stop compilation if critical lexical errors

=== Parsing ===
AST construction completed
[X syntax errors detected (recovered)] - Continue with error recovery

=== Semantic Analysis ===
Semantic analysis completed
[X semantic errors detected] - Collect all errors

=== Code Generation ===
[Skipped due to semantic errors] - Skip if semantic errors exist
```

### Test Commands

```bash
# Test each scenario
python main.py test_suite/01_basic_resources.dsl --verbose
python main.py test_suite/02_complex_expressions.dsl --verbose
python main.py test_suite/03_control_flow.dsl --verbose
python main.py test_suite/04_modules_and_functions.dsl --verbose
python main.py test_suite/05_connections_and_policies.dsl --verbose
python main.py test_suite/06_edge_cases.dsl --verbose
python main.py test_suite/07_error_scenarios.dsl --verbose
python main.py test_suite/08_working_example.dsl --verbose

# Check generated JSON outputs
ls test_suite/*.json
```

## Expected Demonstration Points

### 1. Lexical Analysis
- Token generation for valid syntax
- Error detection for invalid characters
- Critical error handling

### 2. Parsing with Error Recovery
- AST construction despite syntax errors
- Error recovery mechanisms
- Syntax error reporting

### 3. Semantic Analysis
- Type checking
- Reference validation
- Duplicate detection
- Semantic error collection

### 4. Code Generation Control
- Conditional JSON generation
- Skip on semantic errors
- Proper output formatting

### 5. Edge Case Handling
- Complex data structures
- Nested expressions
- Large input files
- Memory management

### 6. Error Reporting
- Detailed error messages
- Line/column information
- Error categorization
- Multiple error reporting

## Viva Demonstration Script

1. **Start with working example**:
   ```bash
   python main.py test_suite/08_working_example.dsl --verbose
   ```

2. **Show error handling**:
   ```bash
   python main.py test_suite/07_error_scenarios.dsl --verbose
   ```

3. **Demonstrate complex features**:
   ```bash
   python main.py test_suite/05_connections_and_policies.dsl --verbose
   ```

4. **Show edge cases**:
   ```bash
   python main.py test_suite/06_edge_cases.dsl --verbose
   ```

5. **Display generated JSON**:
   ```bash
   cat test_suite/08_working_example.json
   ```

This comprehensive test suite demonstrates all aspects of the compiler's functionality and error handling capabilities.
