# 🎓 DSL Compiler Demonstration Guide

This guide provides step-by-step commands for testing every DSL file and shows exactly where to find inputs and outputs.

## 🚀 Quick Start

```bash
# Navigate to project directory
cd infrastructure-dsl-compiler

# Run any DSL file
python main.py input/<filename>.dsl --verbose

# Generate AST only (no JSON output)
python main.py input/<filename>.dsl --ast-only

# Validate only (no JSON output)
python main.py input/<filename>.dsl --validate-only
```

## 📁 File Structure

```
infrastructure-dsl-compiler/
├── input/           # 📂 All DSL source files
├── output/          # ✅ Successful compilations (JSON)
├── error/           # ❌ Error reports (JSON)
└── error/README.md  # 📖 Detailed error explanations
```

---

## � **AST DEMONSTRATION COMMANDS**

### **Generate AST Only**
```bash
# Generate AST for successful file
python main.py input/test_simple.dsl --ast-only

# Generate AST for error file (shows parsing structure despite errors)
python main.py input/demo_syntax_errors_clean.dsl --ast-only
```

### **AST Output Examples**

#### **Successful AST** (`test_simple.dsl`)
```bash
python main.py input/test_simple.dsl --ast-only
```
**📍 Input**: `input/test_simple.dsl`  
**🌳 Output**: AST printed directly in terminal  
**📊 Result**: ✅ Clean AST structure

#### **Error AST** (`demo_syntax_errors_clean.dsl`)
```bash
python main.py input/demo_syntax_errors_clean.dsl --ast-only
```
**📍 Input**: `input/demo_syntax_errors_clean.dsl`  
**🌳 Output**: AST with error recovery nodes  
**📊 Result**: ⚠️ AST shows parsing structure despite errors

---

## �🎯 DEMONSTRATION FILES

### ✅ **SUCCESSFUL COMPILATIONS**

#### 1. **Simple Success Case**
```bash
# Full compilation
python main.py input/test_simple.dsl --verbose

# AST only
python main.py input/test_simple.dsl --ast-only

# Validate only
python main.py input/test_simple.dsl --validate-only
```
**📍 Input**: `input/test_simple.dsl`  
**✅ Output**: `output/test_simple.json`  
**🌳 AST**: Printed in terminal with `--ast-only`  
**📊 Result**: ✅ Success (0 errors, 1 warning)

---

#### 2. **Basic Resources**
```bash
# Original with errors
python main.py input/01_basic_resources.dsl --verbose

# Corrected version
python main.py input/01_basic_resources_simple.dsl --verbose
```
**📍 Input**: `input/01_basic_resources.dsl` / `input/01_basic_resources_simple.dsl`  
**❌ Original**: `error/01_basic_resources_errors.json`  
**✅ Corrected**: `output/01_basic_resources_simple.json`  
**📊 Result**: ❌ Original (15 errors) / ✅ Corrected (success)

---

#### 3. **Complex Expressions**
```bash
# Original with errors
python main.py input/02_complex_expressions.dsl --verbose

# Corrected version
python main.py input/02_complex_expressions_simple.dsl --verbose
```
**📍 Input**: `input/02_complex_expressions.dsl` / `input/02_complex_expressions_simple.dsl`  
**❌ Original**: `error/02_complex_expressions_errors.json`  
**✅ Corrected**: `error/02_complex_expressions_simple_errors.json`  
**📊 Result**: ❌ Original (35 errors) / ⚠️ Corrected (1 error)

---

#### 4. **Control Flow**
```bash
# Original with errors
python main.py input/03_control_flow.dsl --verbose

# Corrected version
python main.py input/03_control_flow_simple.dsl --verbose
```
**📍 Input**: `input/03_control_flow.dsl` / `input/03_control_flow_simple.dsl`  
**❌ Original**: `error/03_control_flow_errors.json`  
**✅ Corrected**: `output/03_control_flow_simple.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

#### 5. **Modules and Functions**
```bash
# Original with errors
python main.py input/04_modules_and_functions.dsl --verbose

# Corrected version
python main.py input/04_modules_working.dsl --verbose
```
**📍 Input**: `input/04_modules_and_functions.dsl` / `input/04_modules_working.dsl`  
**❌ Original**: `error/04_modules_and_functions_errors.json`  
**✅ Corrected**: `output/04_modules_working.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

#### 6. **Connections and Policies**
```bash
# Original with errors
python main.py input/05_connections_and_policies.dsl --verbose

# Corrected version
python main.py input/05_connections_working.dsl --verbose
```
**📍 Input**: `input/05_connections_and_policies.dsl` / `input/05_connections_working.dsl`  
**❌ Original**: `error/05_connections_and_policies_errors.json`  
**✅ Corrected**: `output/05_connections_working.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

#### 7. **Edge Cases**
```bash
# Original with errors
python main.py input/06_edge_cases.dsl --verbose

# Corrected version
python main.py input/06_edge_cases_working.dsl --verbose
```
**📍 Input**: `input/06_edge_cases.dsl` / `input/06_edge_cases_working.dsl`  
**❌ Original**: `error/06_edge_cases_errors.json`  
**✅ Corrected**: `output/06_edge_cases_working.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

#### 8. **Error Scenarios**
```bash
# Original with errors
python main.py input/07_error_scenarios.dsl --verbose

# Corrected version
python main.py input/07_error_scenarios_working.dsl --verbose
```
**📍 Input**: `input/07_error_scenarios.dsl` / `input/07_error_scenarios_working.dsl`  
**❌ Original**: `error/07_error_scenarios_errors.json`  
**✅ Corrected**: `output/07_error_scenarios_working.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

#### 9. **Working Example**
```bash
# Original with errors
python main.py input/08_working_example.dsl --verbose

# Corrected version
python main.py input/08_working_example_fixed.dsl --verbose
```
**📍 Input**: `input/08_working_example.dsl` / `input/08_working_example_fixed.dsl`  
**❌ Original**: `error/08_working_example_errors.json`  
**✅ Corrected**: `output/08_working_example_fixed.json`  
**📊 Result**: ❌ Original (18 errors) / ✅ Corrected (success)

---

#### 10. **Test Medium**
```bash
# Original with errors
python main.py input/test_medium.dsl --verbose

# Corrected version
python main.py input/test_medium_fixed.dsl --verbose
```
**📍 Input**: `input/test_medium.dsl` / `input/test_medium_fixed.dsl`  
**❌ Original**: `error/test_medium_errors.json`  
**✅ Corrected**: `output/test_medium_fixed.json`  
**📊 Result**: ❌ Original (11 errors) / ✅ Corrected (success)

---

#### 11. **Test Working**
```bash
# Original with errors
python main.py input/test_working.dsl --verbose

# Corrected version
python main.py input/test_working_fixed.dsl --verbose
```
**📍 Input**: `input/test_working.dsl` / `input/test_working_fixed.dsl`  
**❌ Original**: `error/test_working_errors.json`  
**✅ Corrected**: `output/test_working_fixed.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

#### 12. **Test IF**
```bash
# Original with errors
python main.py input/test_if.dsl --verbose

# Corrected version
python main.py input/test_if_fixed.dsl --verbose
```
**📍 Input**: `input/test_if.dsl` / `input/test_if_fixed.dsl`  
**❌ Original**: `error/test_if_errors.json`  
**✅ Corrected**: `output/test_if_fixed.json`  
**📊 Result**: ❌ Original (syntax errors) / ✅ Corrected (success)

---

## 🎭 **DEMONSTRATION SCENARIOS**

### **Scenario 1: Syntax Error Demonstration**

#### **Step 1: Show Error Case**
```bash
# Full compilation with errors
python main.py input/demo_syntax_errors_clean.dsl --verbose

# AST despite errors (shows parsing structure)
python main.py input/demo_syntax_errors_clean.dsl --ast-only

# Validate only
python main.py input/demo_syntax_errors_clean.dsl --validate-only
```
**📍 Input**: `input/demo_syntax_errors_clean.dsl`  
**❌ Output**: `error/demo_syntax_errors_clean_errors.json`  
**🌳 AST**: Printed in terminal (shows error recovery)  
**📊 Result**: ❌ 12 syntax errors  
**🔍 Errors**: Missing `=` operators, unclosed braces

#### **Step 2: Show Fixed Case**
```bash
# Full compilation success
python main.py input/demo_syntax_errors_fixed_clean.dsl --verbose

# Clean AST structure
python main.py input/demo_syntax_errors_fixed_clean.dsl --ast-only

# Validation success
python main.py input/demo_syntax_errors_fixed_clean.dsl --validate-only
```
**📍 Input**: `input/demo_syntax_errors_fixed_clean.dsl`  
**✅ Output**: `output/demo_syntax_errors_fixed_clean.json`  
**🌳 AST**: Clean structure printed in terminal  
**📊 Result**: ✅ Success (3 warnings)

#### **Step 3: Compare Results**
- **Error Report**: `error/demo_syntax_errors_clean_errors.json`
- **Success Output**: `output/demo_syntax_errors_fixed_clean.json`
- **Error Details**: See `error/README.md`
- **AST Comparison**: Error AST vs Clean AST

---

### **Scenario 2: Semantic Error Demonstration**

#### **Step 1: Show Error Case**
```bash
# Full compilation with errors
python main.py input/demo_semantic_errors.dsl --verbose

# AST despite semantic errors
python main.py input/demo_semantic_errors.dsl --ast-only

# Validation only
python main.py input/demo_semantic_errors.dsl --validate-only
```
**📍 Input**: `input/demo_semantic_errors.dsl`  
**❌ Output**: `error/demo_semantic_errors_errors.json`  
**🌳 AST**: Printed in terminal (shows parsing structure)  
**📊 Result**: ❌ 3 syntax errors  
**🔍 Errors**: Invalid connect syntax, comment issues

#### **Step 2: Show Fixed Case**
```bash
# Full compilation success
python main.py input/demo_semantic_errors_fixed.dsl --verbose

# Clean AST structure
python main.py input/demo_semantic_errors_fixed.dsl --ast-only

# Validation success
python main.py input/demo_semantic_errors_fixed.dsl --validate-only
```
**📍 Input**: `input/demo_semantic_errors_fixed.dsl`  
**✅ Output**: `output/demo_semantic_errors_fixed.json`  
**🌳 AST**: Clean structure printed in terminal  
**📊 Result**: ✅ Success

---

## 📊 **OUTPUT LOCATIONS SUMMARY**

| Original File | Corrected File | Success Location | Error Location | AST Location |
|---------------|----------------|------------------|-----------------|--------------|
| `test_simple.dsl` | - | `output/test_simple.json` | - | Terminal (`--ast-only`) |
| `demo_syntax_errors_clean.dsl` | `demo_syntax_errors_fixed_clean.dsl` | `output/demo_syntax_errors_fixed_clean.json` | `error/demo_syntax_errors_clean_errors.json` | Terminal (`--ast-only`) |
| `demo_semantic_errors.dsl` | `demo_semantic_errors_fixed.dsl` | `output/demo_semantic_errors_fixed.json` | `error/demo_semantic_errors_errors.json` | Terminal (`--ast-only`) |
| `01_basic_resources.dsl` | `01_basic_resources_simple.dsl` | `output/01_basic_resources_simple.json` | `error/01_basic_resources_errors.json` | Terminal (`--ast-only`) |
| `02_complex_expressions.dsl` | `02_complex_expressions_simple.dsl` | `error/02_complex_expressions_simple_errors.json` | `error/02_complex_expressions_errors.json` | Terminal (`--ast-only`) |
| `03_control_flow.dsl` | `03_control_flow_simple.dsl` | `output/03_control_flow_simple.json` | `error/03_control_flow_errors.json` | Terminal (`--ast-only`) |
| `04_modules_and_functions.dsl` | `04_modules_working.dsl` | `output/04_modules_working.json` | `error/04_modules_and_functions_errors.json` | Terminal (`--ast-only`) |
| `05_connections_and_policies.dsl` | `05_connections_working.dsl` | `output/05_connections_working.json` | `error/05_connections_and_policies_errors.json` | Terminal (`--ast-only`) |
| `06_edge_cases.dsl` | `06_edge_cases_working.dsl` | `output/06_edge_cases_working.json` | `error/06_edge_cases_errors.json` | Terminal (`--ast-only`) |
| `07_error_scenarios.dsl` | `07_error_scenarios_working.dsl` | `output/07_error_scenarios_working.json` | `error/07_error_scenarios_errors.json` | Terminal (`--ast-only`) |
| `08_working_example.dsl` | `08_working_example_fixed.dsl` | `output/08_working_example_fixed.json` | `error/08_working_example_errors.json` | Terminal (`--ast-only`) |
| `test_medium.dsl` | `test_medium_fixed.dsl` | `output/test_medium_fixed.json` | `error/test_medium_errors.json` | Terminal (`--ast-only`) |
| `test_working.dsl` | `test_working_fixed.dsl` | `output/test_working_fixed.json` | `error/test_working_errors.json` | Terminal (`--ast-only`) |
| `test_if.dsl` | `test_if_fixed.dsl` | `output/test_if_fixed.json` | `error/test_if_errors.json` | Terminal (`--ast-only`) |

---

## 🔍 **ERROR ANALYSIS**

### **View Error Reports**
```bash
# View any error report
cat error/demo_syntax_errors_clean_errors.json

# View detailed error explanations
cat error/README.md
```

### **View Successful Outputs**
```bash
# View any successful JSON output
cat output/test_simple.json
cat output/demo_syntax_errors_fixed_clean.json
```

### **View AST in Terminal**
```bash
# Generate AST for successful file
python main.py input/test_simple.dsl --ast-only

# Generate AST for error file (shows error recovery)
python main.py input/demo_syntax_errors_clean.dsl --ast-only

# Compare AST structures
python main.py input/demo_syntax_errors_clean.dsl --ast-only
python main.py input/demo_syntax_errors_fixed_clean.dsl --ast-only
```

---

## 🎯 **VIVA DEMONSTRATION CHECKLIST**

### ✅ **Show Compiler Features**
1. **Error Detection**: Run any error file to show error categorization
2. **Error Reporting**: Show JSON error reports with line numbers
3. **Success Cases**: Show successful compilation to JSON
4. **File Organization**: Show input/output/error folder structure
5. **AST Generation**: Show AST structure with `--ast-only` flag
6. **Error Recovery**: Show AST despite syntax errors

### 🎪 **Recommended Demonstration Order**
1. **Start with success**: `python main.py input/test_simple.dsl --verbose`
2. **Show AST generation**: `python main.py input/test_simple.dsl --ast-only`
3. **Show syntax errors**: `python main.py input/demo_syntax_errors_clean.dsl --verbose`
4. **Show AST despite errors**: `python main.py input/demo_syntax_errors_clean.dsl --ast-only`
5. **Show fixed version**: `python main.py input/demo_syntax_errors_fixed_clean.dsl --verbose`
6. **Show clean AST**: `python main.py input/demo_syntax_errors_fixed_clean.dsl --ast-only`
7. **Show semantic errors**: `python main.py input/demo_semantic_errors.dsl --verbose`
8. **Show real test case**: `python main.py input/08_working_example.dsl --verbose`
9. **Show error analysis**: `cat error/README.md`

---

## 🚨 **COMMON ERROR TYPES**

| Emoji | Type | Example Command |
|-------|------|-----------------|
| 🔤 | Lexical | `python main.py input/07_error_scenarios.dsl --verbose` |
| 📝 | Syntax | `python main.py input/demo_syntax_errors_clean.dsl --verbose` |
| 🧠 | Semantic | `python main.py input/demo_semantic_errors.dsl --verbose` |

---

## 🎓 **LEARNING OUTCOMES**

After this demonstration, students will understand:
- ✅ **Compiler Pipeline**: Lexical → Parsing → Semantic → Code Generation
- ✅ **Error Handling**: Categorization and reporting
- ✅ **File Organization**: Input/Output/Error separation
- ✅ **Error Recovery**: Parser continues despite errors
- ✅ **JSON Generation**: Successful compilation produces structured output

**Ready for your viva demonstration!** 🎉
