# DSL Compiler Performance Evaluation Guide

## 🚀 Quick Start

### **Step 1: Install Dependencies**
```bash
pip install -r performance_requirements.txt
```

### **Step 2: Run Complete Performance Evaluation**
```bash
# Step 2a: Basic performance profiling
python performance_profiler.py

# Step 2b: Comprehensive benchmark testing
python benchmark_suite.py

# Step 2c: Advanced statistical analysis
python performance_analyzer.py

# Step 2d: Generate comprehensive report
python generate_performance_report.py
```

### **Step 3: View Results**
- **Main Report**: `comprehensive_performance_report.md`
- **Basic Results**: `performance_results.json`
- **Benchmark Data**: `benchmark_results.json`
- **Statistical Analysis**: `performance_analysis.json`

---

## 📊 Evaluation Tools Overview

### **1. Performance Profiler (`performance_profiler.py`)**
**Purpose**: Basic performance measurement and analysis

**Features**:
- Compilation time measurement
- Memory usage tracking
- Token processing efficiency
- Error detection accuracy
- Success rate analysis

**Usage**:
```bash
python performance_profiler.py
```

**Outputs**:
- `performance_results.json` - Raw performance data
- `performance_report.md` - Basic analysis report

### **2. Benchmark Suite (`benchmark_suite.py`)**
**Purpose**: Comprehensive benchmark testing with multiple iterations

**Features**:
- Multi-iteration testing (5 runs per file)
- Stress testing (continuous compilation)
- Scalability testing (increasing file sizes)
- Performance categorization
- Reliability assessment

**Usage**:
```bash
python benchmark_suite.py
```

**Outputs**:
- `benchmark_results.json` - Detailed benchmark data
- `benchmark_report.md` - Benchmark analysis report

### **3. Performance Analyzer (`performance_analyzer.py`)**
**Purpose**: Advanced statistical analysis and insights

**Features**:
- Comprehensive statistical metrics
- Distribution analysis (normality, skewness, kurtosis)
- Outlier detection (IQR and Z-score methods)
- Correlation and regression analysis
- Performance classification and rating

**Usage**:
```bash
python performance_analyzer.py
```

**Outputs**:
- `performance_analysis.json` - Statistical analysis results
- `performance_analysis_report.md` - Advanced analysis report

### **4. Report Generator (`generate_performance_report.py`)**
**Purpose**: Consolidates all data into comprehensive evaluation report

**Features**:
- Executive summary generation
- Detailed metrics compilation
- Performance recommendations
- Technical appendix
- Complete documentation

**Usage**:
```bash
python generate_performance_report.py
```

**Outputs**:
- `comprehensive_performance_report.md` - Complete evaluation report

---

## 📈 Performance Metrics Explained

### **Time Metrics**
- **Compilation Time**: Total time from start to finish (milliseconds)
- **Average Time**: Mean compilation time across all runs
- **Median Time**: Middle value (less affected by outliers)
- **Standard Deviation**: Measure of consistency
- **Percentiles**: Performance distribution (5th, 95th, 99th)

### **Memory Metrics**
- **Peak Memory**: Maximum memory used during compilation
- **Memory Used**: Additional memory consumed
- **Memory Efficiency**: Tokens processed per MB

### **Throughput Metrics**
- **Tokens/Second**: Processing speed for lexical tokens
- **KB/Second**: Data processing speed
- **Files/Second**: Compilation throughput

### **Reliability Metrics**
- **Success Rate**: Percentage of successful compilations
- **Error Detection**: Accuracy of error reporting
- **Recovery Rate**: Ability to continue after errors

---

## 🎯 Performance Ratings

### **Compilation Performance**
- **🟢 EXCELLENT**: < 50ms average, CV < 0.3
- **🟡 GOOD**: 50-100ms average, CV < 0.5
- **🟠 ACCEPTABLE**: 100-200ms average
- **🔴 NEEDS OPTIMIZATION**: > 200ms average

### **Memory Efficiency**
- **🟢 EXCELLENT**: < 20MB average
- **🟡 GOOD**: 20-50MB average
- **🟠 ACCEPTABLE**: 50-100MB average
- **🔴 NEEDS OPTIMIZATION**: > 100MB average

### **Reliability**
- **🟢 EXCELLENT**: > 95% success rate
- **🟡 GOOD**: 85-95% success rate
- **🟠 ACCEPTABLE**: 70-85% success rate
- **🔴 NEEDS IMPROVEMENT**: < 70% success rate

---

## 📋 Individual Tool Usage

### **Quick Performance Check**
```bash
# Run single file with performance tracking
python main.py input/test_simple.dsl --verbose

# View performance metrics in output
```

### **Basic Profiling**
```bash
python performance_profiler.py

# View:
# - Average compilation time
# - Memory usage statistics
# - Success/failure rates
# - Processing efficiency
```

### **Comprehensive Benchmarking**
```bash
python benchmark_suite.py

# View:
# - Multi-iteration consistency
# - Stress test results
# - Scalability analysis
# - Category-wise performance
```

### **Statistical Analysis**
```bash
python performance_analyzer.py

# View:
# - Advanced statistical metrics
# - Distribution analysis
# - Outlier detection
# - Performance correlations
```

### **Complete Evaluation**
```bash
# Run all evaluation tools in sequence
python performance_profiler.py
python benchmark_suite.py
python performance_analyzer.py
python generate_performance_report.py

# View comprehensive report
```

---

## 🔍 Understanding Results

### **Executive Summary**
- Overall performance assessment
- Key metrics at a glance
- Performance ratings with color coding
- Critical issues identification

### **Detailed Metrics**
- Individual file performance
- Statistical distributions
- Performance trends and patterns
- Comparative analysis

### **Recommendations**
- Prioritized improvement suggestions
- Performance targets and benchmarks
- Monitoring recommendations
- Optimization strategies

### **Technical Appendix**
- Test environment details
- Evaluation methodology
- Statistical methods used
- Data file descriptions

---

## 🚨 Troubleshooting

### **Common Issues**

**ModuleNotFoundError: No module named 'psutil'**
```bash
pip install psutil
```

**No performance data found**
```bash
# Ensure you run performance_profiler.py first
python performance_profiler.py
```

**Memory tracking not working**
```bash
# Check if tracemalloc is available
python -c "import tracemalloc; print('OK')"
```

**Statistical analysis errors**
```bash
# Install scientific computing packages
pip install numpy scipy pandas
```

### **Performance Issues**

**Slow evaluation**
- Reduce number of iterations in benchmark suite
- Exclude large files from initial testing
- Run evaluation on smaller subset

**Memory errors during evaluation**
- Close other applications
- Increase system virtual memory
- Run evaluation tools individually

**Inconsistent results**
- Ensure system is not under load
- Run multiple evaluations
- Check for background processes

---

## 📊 Customization Options

### **Modify Evaluation Parameters**

**Change iterations in benchmark suite:**
```python
# In benchmark_suite.py, line ~67
iterations = 3  # Default is 5
```

**Adjust stress test duration:**
```python
# In benchmark_suite.py, line ~120
duration_seconds = 30  # Default is 60
```

**Customize file size categories:**
```python
# In benchmark_suite.py, line ~25
if size_kb < 1:
    size_category = 'tiny_files'  # Custom category
```

### **Add Custom Metrics**

**Add new performance metric:**
```python
# In performance_profiler.py, add to measure_compilation method
custom_metric = calculate_custom_metric()
result['custom_metric'] = custom_metric
```

**Modify rating thresholds:**
```python
# In performance_analyzer.py, adjust rating functions
if avg_time < 75:  # Custom threshold
    return "EXCELLENT"
```

---

## 📈 Continuous Monitoring

### **Automated Testing**
```bash
# Create a script for automated evaluation
#!/bin/bash
python performance_profiler.py
python benchmark_suite.py
python generate_performance_report.py

# Add to CI/CD pipeline
```

### **Performance Tracking**
```bash
# Create performance history directory
mkdir -p performance_history/$(date +%Y%m%d)

# Archive results
cp *.json performance_history/$(date +%Y%m%d)/
cp *.md performance_history/$(date +%Y%m%d)/
```

### **Regression Detection**
```bash
# Compare with previous results
python performance_analyzer.py --compare baseline.json current.json
```

---

## 🎯 Best Practices

### **Before Evaluation**
1. **Close unnecessary applications** - Ensure accurate measurements
2. **Warm up the system** - Run a few compilations first
3. **Check disk space** - Ensure enough space for results
4. **Verify dependencies** - Install required packages

### **During Evaluation**
1. **Run complete suite** - Use all evaluation tools
2. **Monitor system load** - Ensure consistent testing environment
3. **Save results** - Keep all generated files
4. **Document findings** - Note any anomalies

### **After Evaluation**
1. **Review comprehensive report** - Understand overall performance
2. **Implement recommendations** - Prioritize critical issues
3. **Set up monitoring** - Track performance over time
4. **Update baselines** - Establish new performance targets

---

## 📞 Support

### **Getting Help**
- Check this guide for common issues
- Review generated reports for insights
- Examine error logs for specific problems
- Use individual tools for targeted analysis

### **Performance Optimization**
- Focus on highest priority recommendations
- Implement changes incrementally
- Re-evaluate after each optimization
- Track improvements over time

---

**🎉 Your DSL compiler performance evaluation system is ready to use!**
