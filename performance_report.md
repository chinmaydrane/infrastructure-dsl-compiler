
# DSL Compiler Performance Evaluation Report
Generated: 2026-05-04 23:36:52

## Executive Summary
- Total Files Processed: 32
- Successful Compilations: 13
- Failed Compilations: 19
- Overall Success Rate: 40.6%

## Compilation Performance Analysis
### Time Metrics
- Average Compilation Time: 190.35 ms
- Median Compilation Time: 173.90 ms
- Fastest Compilation: 158.04 ms
- Slowest Compilation: 279.19 ms
- Standard Deviation: 34.73 ms

### Performance Classification
- Performance Rating: ACCEPTABLE (100-200ms average)

## Memory Usage Analysis
- Average Memory Usage: -19.67 MB
- Median Memory Usage: -19.58 MB
- Peak Memory Usage: -19.50 MB
- Total Memory Consumed: -255.66 MB

### Memory Efficiency
- Memory Efficiency: EXCELLENT (< 20MB average)

## Processing Efficiency
- Average Tokens/Second: 298 tokens/sec
- Average KB/Second: 2 KB/sec
- Total Tokens Processed: 705
- Total Data Processed: 4.1 KB

### Throughput Analysis
- Throughput Rating: NEEDS OPTIMIZATION (< 2,000 tokens/sec)

## Error Analysis
- Total Errors Detected: 0
- Total Warnings Generated: 30
- Files with Errors: 0

### Error Detection Performance
- Error Detection: NO ERRORS (all files compiled successfully)

## Detailed Results by File

### 01_basic_resources.dsl - [FAIL]
- File Size: 0.7 KB
- Compilation Time: 214.32 ms
- Memory Used: -19.73 MB
- Tokens Processed: 129
- Errors: 0, Warnings: 0

### 01_basic_resources_fixed.dsl - [FAIL]
- File Size: 0.7 KB
- Compilation Time: 188.42 ms
- Memory Used: -19.99 MB
- Tokens Processed: 127
- Errors: 0, Warnings: 0

### 01_basic_resources_simple.dsl - [OK]
- File Size: 0.5 KB
- Compilation Time: 173.01 ms
- Memory Used: -19.99 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### 02_complex_expressions.dsl - [FAIL]
- File Size: 1.3 KB
- Compilation Time: 166.24 ms
- Memory Used: -19.99 MB
- Tokens Processed: 182
- Errors: 0, Warnings: 0

### 02_complex_expressions_simple.dsl - [FAIL]
- File Size: 0.7 KB
- Compilation Time: 173.44 ms
- Memory Used: -20.01 MB
- Tokens Processed: 121
- Errors: 0, Warnings: 0

### 03_control_flow.dsl - [FAIL]
- File Size: 1.8 KB
- Compilation Time: 211.80 ms
- Memory Used: -20.00 MB
- Tokens Processed: 284
- Errors: 0, Warnings: 0

### 03_control_flow_simple.dsl - [OK]
- File Size: 0.4 KB
- Compilation Time: 186.51 ms
- Memory Used: -20.01 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### 04_modules_and_functions.dsl - [FAIL]
- File Size: 2.5 KB
- Compilation Time: 221.98 ms
- Memory Used: -20.01 MB
- Tokens Processed: 374
- Errors: 0, Warnings: 0

### 04_modules_simple.dsl - [FAIL]
- File Size: 0.5 KB
- Compilation Time: 177.03 ms
- Memory Used: -20.02 MB
- Tokens Processed: 80
- Errors: 0, Warnings: 0

### 04_modules_working.dsl - [OK]
- File Size: 0.5 KB
- Compilation Time: 158.04 ms
- Memory Used: -20.02 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### 05_connections_and_policies.dsl - [FAIL]
- File Size: 3.1 KB
- Compilation Time: 211.89 ms
- Memory Used: -20.02 MB
- Tokens Processed: 541
- Errors: 0, Warnings: 0

### 05_connections_simple.dsl - [FAIL]
- File Size: 0.5 KB
- Compilation Time: 183.21 ms
- Memory Used: -20.02 MB
- Tokens Processed: 91
- Errors: 0, Warnings: 0

### 05_connections_working.dsl - [OK]
- File Size: 0.5 KB
- Compilation Time: 161.14 ms
- Memory Used: -19.50 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### 06_edge_cases.dsl - [FAIL]
- File Size: 4.6 KB
- Compilation Time: 225.44 ms
- Memory Used: -19.47 MB
- Tokens Processed: 740
- Errors: 0, Warnings: 0

### 06_edge_cases_working.dsl - [OK]
- File Size: 0.4 KB
- Compilation Time: 173.90 ms
- Memory Used: -19.55 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### 07_error_scenarios.dsl - [FAIL]
- File Size: 2.4 KB
- Compilation Time: 166.17 ms
- Memory Used: -19.55 MB
- Tokens Processed: 85
- Errors: 0, Warnings: 0

### 07_error_scenarios_working.dsl - [OK]
- File Size: 0.5 KB
- Compilation Time: 173.79 ms
- Memory Used: -19.55 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### 08_working_example.dsl - [FAIL]
- File Size: 0.7 KB
- Compilation Time: 183.97 ms
- Memory Used: -19.56 MB
- Tokens Processed: 120
- Errors: 0, Warnings: 0

### 08_working_example_fixed.dsl - [OK]
- File Size: 0.4 KB
- Compilation Time: 215.40 ms
- Memory Used: -19.56 MB
- Tokens Processed: 74
- Errors: 0, Warnings: 3

### demo_semantic_errors.dsl - [FAIL]
- File Size: 0.5 KB
- Compilation Time: 222.90 ms
- Memory Used: -19.56 MB
- Tokens Processed: 62
- Errors: 0, Warnings: 0

### demo_semantic_errors_fixed.dsl - [FAIL]
- File Size: 0.5 KB
- Compilation Time: 233.12 ms
- Memory Used: -19.56 MB
- Tokens Processed: 62
- Errors: 0, Warnings: 0

### demo_syntax_errors.dsl - [FAIL]
- File Size: 0.5 KB
- Compilation Time: 231.56 ms
- Memory Used: -19.57 MB
- Tokens Processed: 49
- Errors: 0, Warnings: 0

### demo_syntax_errors_clean.dsl - [FAIL]
- File Size: 0.3 KB
- Compilation Time: 251.73 ms
- Memory Used: -19.57 MB
- Tokens Processed: 46
- Errors: 0, Warnings: 0

### demo_syntax_errors_fixed.dsl - [FAIL]
- File Size: 0.5 KB
- Compilation Time: 258.27 ms
- Memory Used: -19.58 MB
- Tokens Processed: 57
- Errors: 0, Warnings: 0

### demo_syntax_errors_fixed_clean.dsl - [OK]
- File Size: 0.3 KB
- Compilation Time: 279.19 ms
- Memory Used: -19.58 MB
- Tokens Processed: 54
- Errors: 0, Warnings: 3

### test_if.dsl - [FAIL]
- File Size: 0.2 KB
- Compilation Time: 239.93 ms
- Memory Used: -19.58 MB
- Tokens Processed: 59
- Errors: 0, Warnings: 0

### test_if_fixed.dsl - [OK]
- File Size: 0.2 KB
- Compilation Time: 221.57 ms
- Memory Used: -19.58 MB
- Tokens Processed: 28
- Errors: 0, Warnings: 1

### test_medium.dsl - [FAIL]
- File Size: 0.1 KB
- Compilation Time: 181.22 ms
- Memory Used: -19.58 MB
- Tokens Processed: 36
- Errors: 0, Warnings: 0

### test_medium_fixed.dsl - [OK]
- File Size: 0.3 KB
- Compilation Time: 165.96 ms
- Memory Used: -19.58 MB
- Tokens Processed: 55
- Errors: 0, Warnings: 2

### test_simple.dsl - [OK]
- File Size: 0.0 KB
- Compilation Time: 181.80 ms
- Memory Used: -19.58 MB
- Tokens Processed: 11
- Errors: 0, Warnings: 1

### test_working.dsl - [OK]
- File Size: 0.0 KB
- Compilation Time: 219.95 ms
- Memory Used: -19.58 MB
- Tokens Processed: 11
- Errors: 0, Warnings: 1

### test_working_fixed.dsl - [OK]
- File Size: 0.2 KB
- Compilation Time: 164.26 ms
- Memory Used: -19.59 MB
- Tokens Processed: 28
- Errors: 0, Warnings: 1
