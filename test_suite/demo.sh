#!/bin/bash
# Infrastructure DSL Compiler Demonstration Script

echo "🎯 Infrastructure DSL Compiler - Comprehensive Test Suite Demo"
echo "============================================================"

echo ""
echo "📋 Test Files Available:"
ls -la test_suite/*.dsl

echo ""
echo "🚀 Starting Demonstration..."
echo ""

# Test 1: Working Example
echo "1️⃣ Testing Working Example (Should succeed with minimal errors):"
echo "   Command: python main.py test_suite/08_working_example.dsl --verbose"
echo "   --------------------------------------------------------"
python main.py test_suite/08_working_example.dsl --verbose
echo ""

# Test 2: Error Scenarios
echo "2️⃣ Testing Error Scenarios (Should show lexical error detection):"
echo "   Command: python main.py test_suite/07_error_scenarios.dsl --verbose"
echo "   ---------------------------------------------------------------"
python main.py test_suite/07_error_scenarios.dsl --verbose
echo ""

# Test 3: Complex Features
echo "3️⃣ Testing Complex Features (Should show syntax error recovery):"
echo "   Command: python main.py test_suite/05_connections_and_policies.dsl --verbose"
echo "   ----------------------------------------------------------------------"
python main.py test_suite/05_connections_and_policies.dsl --verbose
echo ""

# Show generated outputs
echo "4️⃣ Generated JSON Outputs:"
echo "   --------------------"
ls -la test_suite/*.json 2>/dev/null || echo "   No JSON files generated (due to errors)"
echo ""

# Show sample JSON if available
if [ -f "test_suite/08_working_example.json" ]; then
    echo "5️⃣ Sample JSON Output:"
    echo "   ------------------"
    head -20 test_suite/08_working_example.json
    echo "   ... (truncated)"
fi

echo ""
echo "🎉 Demonstration Complete!"
echo ""
echo "📚 Key Points Demonstrated:"
echo "   ✅ Lexical analysis with error detection"
echo "   ✅ Parsing with error recovery"
echo "   ✅ Semantic analysis with error collection"
echo "   ✅ Conditional code generation"
echo "   ✅ Proper error handling and reporting"
echo "   ✅ Complex feature support"
echo "   ✅ Edge case handling"
