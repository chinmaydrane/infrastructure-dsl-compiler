# Error Reports Folder

This folder contains detailed error reports for DSL files that failed compilation. Each error report is generated automatically when a DSL file fails to compile.

## 📁 Error Report Files

### Syntax Error Demonstrations

#### `demo_syntax_errors_clean_errors.json`
**File**: `input/demo_syntax_errors_clean.dsl`

**🔍 Errors Found:**
- **Line 5, Column 9**: `Expected ASSIGN_OP, got INTEGER`
  - **Issue**: Missing `=` operator in `cpu 4` (should be `cpu = 4`)
- **Line 6, Column 12**: `Expected ASSIGN_OP, got STRING`
  - **Issue**: Missing `=` operator in `memory "8GB"` (should be `memory = "8GB"`)
- **Line 10, Column 18**: `Expected ASSIGN_OP, got STRING`
  - **Issue**: Missing `=` operator in `memory "4GB"` (should be `memory = "4GB"`)
- **Line 17, Column 12**: `Expected ASSIGN_OP, got STRING`
  - **Issue**: Missing `=` operator in `engine "mysql"` (should be `engine = "mysql"`)
- **Line 18, Column 13**: `Expected ASSIGN_OP, got STRING`
  - **Issue**: Missing `=` operator in `storage "100GB"` (should be `storage = "100GB"`)
- **Line 19, Column 1**: `Expected IDENTIFIER, got EOF`
  - **Issue**: Missing closing `}` for the database block
- **Line -1, Column -1**: `Expected RBRACE, got EOF`
  - **Issue**: Same as above - missing closing brace

**🎯 How to Fix:**
1. Add `=` operators after attribute names: `cpu = 4`, `memory = "8GB"`
2. Add missing closing `}` brace for the database block
3. **Fixed file**: `input/demo_syntax_errors_fixed_clean.dsl` ✅

---

### Semantic Error Demonstrations

#### `demo_semantic_errors_errors.json`
**File**: `input/demo_semantic_errors.dsl`

**🔍 Errors Found:**
- **Line 15, Column 22**: `Expected ARROW, got TO`
  - **Issue**: Invalid connect statement syntax - should use `->` instead of `to`
- **Line 19, Column 30**: `Expected IDENTIFIER, got COMMENT`
  - **Issue**: Comment inside attribute block not properly handled

**🎯 How to Fix:**
1. Use proper connect syntax: `connect "web_server" -> "db"`
2. Remove inline comments from attribute blocks
3. **Fixed file**: `input/demo_semantic_errors_fixed.dsl` ✅

---

### Real Test Case Errors

#### `08_working_example_errors.json`
**File**: `input/08_working_example.dsl`

**🔍 Errors Found:** 18 Syntax Errors
- **Multiple "Expected ASSIGN_OP, got IDENTIFIER" errors**
  - **Issue**: Missing `=` operators in attribute assignments
- **Multiple "Expected IDENTIFIER, got STRING" errors**
  - **Issue**: Parser expecting identifiers but finding string literals

**🎯 How to Fix:**
1. Add `=` operators after all attribute names
2. Ensure proper syntax for string literals
3. Check resource declaration syntax

---

## 🎓 Learning Objectives

These error reports demonstrate:

### 🔤 **Lexical Errors**
- Invalid tokens or characters
- Malformed literals

### 📝 **Syntax Errors**
- Missing operators (`=`)
- Invalid resource types
- Unclosed blocks (`}`)
- Invalid statement syntax

### 🧠 **Semantic Errors**
- Undefined resource references
- Type mismatches
- Invalid attribute values

## 🚀 Demonstration Workflow

### Step 1: Show Error Case
```bash
python main.py input/demo_syntax_errors_clean.dsl --verbose
```
**Result**: ❌ Compilation fails with detailed error report

### Step 2: Show Fixed Case
```bash
python main.py input/demo_syntax_errors_fixed_clean.dsl --verbose
```
**Result**: ✅ Compilation succeeds, generates JSON output

### Step 3: Compare Results
- **Error folder**: Contains detailed error analysis
- **Output folder**: Contains successful JSON generation
- **Terminal**: Shows categorized error types with emojis

## 📊 Error Categories

| Emoji | Type | Description |
|-------|------|-------------|
| 🔤 | Lexical | Tokenization issues |
| 📝 | Syntax | Grammar/structure issues |
| 🧠 | Semantic | Meaning/type issues |

## 🔧 Error Report Format

Each error report contains:
- **status**: "FAILED"
- **input_file**: Path to the problematic DSL file
- **error_summary**: Counts by error type
- **errors**: Detailed list with line numbers, columns, and messages

**Use these reports to understand and fix DSL compilation errors!** 🎯
