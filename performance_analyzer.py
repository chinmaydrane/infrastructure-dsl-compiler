#!/usr/bin/env python3
"""
Performance Data Analysis Script
Advanced statistical analysis of compiler performance data
"""

import json
import statistics
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import pandas as pd
from scipy import stats

class PerformanceAnalyzer:
    def __init__(self):
        self.data = None
        self.analysis_results = {}
        
    def load_data(self, filename: str = "performance_results.json"):
        """Load performance data from JSON file"""
        with open(filename, 'r') as f:
            self.data = json.load(f)
        print(f"Loaded performance data from {filename}")
        
    def calculate_comprehensive_metrics(self) -> Dict:
        """Calculate comprehensive performance metrics"""
        if not self.data:
            return {"error": "No data loaded"}
        
        results = self.data.get('results', [])
        successful_results = [r for r in results if r.get('success', False)]
        
        if not successful_results:
            return {"error": "No successful compilations found"}
        
        # Extract metrics
        compilation_times = [r['compilation_time_ms'] for r in successful_results]
        memory_usage = [r['memory_used_mb'] for r in successful_results]
        token_counts = [r['token_count'] for r in successful_results]
        file_sizes = [r['file_size_kb'] for r in successful_results]
        
        # Calculate efficiency metrics
        tokens_per_ms = [t/time for t, time in zip(token_counts, compilation_times)]
        kb_per_ms = [size/time for size, time in zip(file_sizes, compilation_times)]
        tokens_per_mb = [t/mem for t, mem in zip(token_counts, memory_usage) if mem > 0]
        
        # Statistical analysis
        metrics = {
            'compilation_performance': self._analyze_metric(compilation_times, 'ms'),
            'memory_efficiency': self._analyze_metric(memory_usage, 'MB'),
            'processing_throughput': {
                'tokens_per_second': self._analyze_metric([t*1000/time for t, time in zip(token_counts, compilation_times)], 'tokens/sec'),
                'kb_per_second': self._analyze_metric([size*1000/time for size, time in zip(file_sizes, compilation_times)], 'KB/sec'),
                'tokens_per_mb': self._analyze_metric(tokens_per_mb, 'tokens/MB')
            },
            'scalability_analysis': self._analyze_scalability(file_sizes, compilation_times),
            'reliability_metrics': self._analyze_reliability(results),
            'performance_distribution': self._analyze_distribution(compilation_times),
            'outlier_analysis': self._detect_outliers(compilation_times)
        }
        
        return metrics
    
    def _analyze_metric(self, values: List[float], unit: str) -> Dict:
        """Analyze a single metric with comprehensive statistics"""
        if not values:
            return {"error": "No data"}
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'mode': statistics.mode(values) if len(set(values)) < len(values) else None,
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
            'variance': statistics.variance(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values),
            'range': max(values) - min(values),
            'quartiles': {
                'q1': np.percentile(values, 25),
                'q2': np.percentile(values, 50),  # median
                'q3': np.percentile(values, 75)
            },
            'percentiles': {
                'p5': np.percentile(values, 5),
                'p10': np.percentile(values, 10),
                'p90': np.percentile(values, 90),
                'p95': np.percentile(values, 95),
                'p99': np.percentile(values, 99)
            },
            'unit': unit,
            'coefficient_of_variation': statistics.stdev(values) / statistics.mean(values) if len(values) > 1 and statistics.mean(values) != 0 else 0
        }
    
    def _analyze_scalability(self, file_sizes: List[float], compilation_times: List[float]) -> Dict:
        """Analyze scalability - performance vs input size"""
        if len(file_sizes) < 3:
            return {"error": "Insufficient data for scalability analysis"}
        
        # Calculate correlation
        correlation, p_value = stats.pearsonr(file_sizes, compilation_times)
        
        # Fit linear regression
        slope, intercept, r_value, p_value_reg, std_err = stats.linregress(file_sizes, compilation_times)
        
        # Calculate throughput at different sizes
        throughput_data = []
        for size, time in zip(file_sizes, compilation_times):
            if time > 0:
                throughput = size / time  # KB/ms
                throughput_data.append(throughput)
        
        return {
            'correlation_coefficient': correlation,
            'correlation_p_value': p_value,
            'linear_regression': {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value ** 2,
                'p_value': p_value_reg,
                'standard_error': std_err
            },
            'throughput_analysis': self._analyze_metric(throughput_data, 'KB/ms') if throughput_data else {},
            'scalability_rating': self._rate_scalability(correlation, r_value ** 2)
        }
    
    def _analyze_reliability(self, results: List[Dict]) -> Dict:
        """Analyze reliability and error handling"""
        total_runs = len(results)
        successful_runs = len([r for r in results if r.get('success', False)])
        failed_runs = total_runs - successful_runs
        
        # Error analysis
        error_types = {}
        for result in results:
            if not result.get('success', False):
                error_count = result.get('error_count', 0)
                if error_count not in error_types:
                    error_types[error_count] = 0
                error_types[error_count] += 1
        
        return {
            'success_rate': (successful_runs / total_runs) * 100 if total_runs > 0 else 0,
            'failure_rate': (failed_runs / total_runs) * 100 if total_runs > 0 else 0,
            'total_runs': total_runs,
            'successful_runs': successful_runs,
            'failed_runs': failed_runs,
            'error_distribution': error_types,
            'reliability_rating': self._rate_reliability((successful_runs / total_runs) * 100 if total_runs > 0 else 0)
        }
    
    def _analyze_distribution(self, values: List[float]) -> Dict:
        """Analyze the distribution of performance values"""
        if len(values) < 5:
            return {"error": "Insufficient data for distribution analysis"}
        
        # Normality test
        if len(values) >= 8:
            shapiro_stat, shapiro_p = stats.shapiro(values)
            is_normal = shapiro_p > 0.05
        else:
            is_normal = None
            shapiro_stat, shapiro_p = None, None
        
        # Skewness and kurtosis
        skewness = stats.skew(values)
        kurtosis = stats.kurtosis(values)
        
        return {
            'normality_test': {
                'shapiro_wilk_statistic': shapiro_stat,
                'shapiro_wilk_p_value': shapiro_p,
                'is_normal_distribution': is_normal
            },
            'skewness': skewness,
            'kurtosis': kurtosis,
            'distribution_shape': self._classify_distribution(skewness, kurtosis)
        }
    
    def _detect_outliers(self, values: List[float]) -> Dict:
        """Detect outliers using multiple methods"""
        if len(values) < 4:
            return {"error": "Insufficient data for outlier detection"}
        
        # IQR method
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        iqr_outliers = [v for v in values if v < lower_bound or v > upper_bound]
        
        # Z-score method
        z_scores = np.abs(stats.zscore(values))
        z_outliers = [v for v, z in zip(values, z_scores) if z > 3]
        
        return {
            'iqr_method': {
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outliers': iqr_outliers,
                'outlier_count': len(iqr_outliers),
                'outlier_percentage': (len(iqr_outliers) / len(values)) * 100
            },
            'z_score_method': {
                'threshold': 3.0,
                'outliers': z_outliers,
                'outlier_count': len(z_outliers),
                'outlier_percentage': (len(z_outliers) / len(values)) * 100
            }
        }
    
    def _rate_scalability(self, correlation: float, r_squared: float) -> str:
        """Rate scalability based on correlation and R²"""
        if abs(correlation) > 0.8 and r_squared > 0.64:
            return "EXCELLENT"
        elif abs(correlation) > 0.6 and r_squared > 0.36:
            return "GOOD"
        elif abs(correlation) > 0.4 and r_squared > 0.16:
            return "ACCEPTABLE"
        else:
            return "NEEDS_IMPROVEMENT"
    
    def _rate_reliability(self, success_rate: float) -> str:
        """Rate reliability based on success rate"""
        if success_rate >= 95:
            return "EXCELLENT"
        elif success_rate >= 85:
            return "GOOD"
        elif success_rate >= 70:
            return "ACCEPTABLE"
        else:
            return "NEEDS_IMPROVEMENT"
    
    def _classify_distribution(self, skewness: float, kurtosis: float) -> str:
        """Classify distribution shape"""
        if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
            return "NORMAL"
        elif skewness > 0.5:
            return "RIGHT_SKEWED"
        elif skewness < -0.5:
            return "LEFT_SKEWED"
        elif kurtosis > 0.5:
            return "LEPTOKURTIC"  # Heavy-tailed
        elif kurtosis < -0.5:
            return "PLATYKURTIC"  # Light-tailed
        else:
            return "IRREGULAR"
    
    def generate_performance_report(self) -> str:
        """Generate comprehensive performance analysis report"""
        if not self.data:
            return "Error: No data loaded"
        
        metrics = self.calculate_comprehensive_metrics()
        
        if 'error' in metrics:
            return f"Error in analysis: {metrics['error']}"
        
        report = f"""
# Advanced Performance Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- Total Files Analyzed: {len(self.data.get('results', []))}
- Analysis Methodology: Statistical analysis with {len(metrics)} metric categories
- Confidence Level: 95%

## Compilation Performance Analysis
### Time Metrics
- **Mean Compilation Time**: {metrics['compilation_performance']['mean']:.2f} ms
- **Median Compilation Time**: {metrics['compilation_performance']['median']:.2f} ms
- **Standard Deviation**: {metrics['compilation_performance']['std_dev']:.2f} ms
- **Coefficient of Variation**: {metrics['compilation_performance']['coefficient_of_variation']:.3f}
- **Performance Range**: {metrics['compilation_performance']['min']:.2f} - {metrics['compilation_performance']['max']:.2f} ms

### Percentile Analysis
- **5th Percentile**: {metrics['compilation_performance']['percentiles']['p5']:.2f} ms
- **10th Percentile**: {metrics['compilation_performance']['percentiles']['p10']:.2f} ms
- **90th Percentile**: {metrics['compilation_performance']['percentiles']['p90']:.2f} ms
- **95th Percentile**: {metrics['compilation_performance']['percentiles']['p95']:.2f} ms
- **99th Percentile**: {metrics['compilation_performance']['percentiles']['p99']:.2f} ms

### Performance Classification
"""
        
        # Classify performance
        avg_time = metrics['compilation_performance']['mean']
        cv = metrics['compilation_performance']['coefficient_of_variation']
        
        if avg_time < 50 and cv < 0.3:
            report += "- **Performance Rating**: EXCELLENT (Fast and consistent)\n"
        elif avg_time < 100 and cv < 0.5:
            report += "- **Performance Rating**: GOOD (Adequate speed, reasonable consistency)\n"
        elif avg_time < 200:
            report += "- **Performance Rating**: ACCEPTABLE (Usable but could be optimized)\n"
        else:
            report += "- **Performance Rating**: NEEDS OPTIMIZATION (Slow and/or inconsistent)\n"
        
        report += f"""
## Memory Efficiency Analysis
### Memory Usage Metrics
- **Mean Memory Usage**: {metrics['memory_efficiency']['mean']:.2f} MB
- **Median Memory Usage**: {metrics['memory_efficiency']['median']:.2f} MB
- **Peak Memory**: {metrics['memory_efficiency']['max']:.2f} MB
- **Memory Range**: {metrics['memory_efficiency']['min']:.2f} - {metrics['memory_efficiency']['max']:.2f} MB

### Memory Efficiency Rating
"""
        
        avg_memory = metrics['memory_efficiency']['mean']
        if avg_memory < 20:
            report += "- **Memory Efficiency**: EXCELLENT (< 20MB average)\n"
        elif avg_memory < 50:
            report += "- **Memory Efficiency**: GOOD (20-50MB average)\n"
        elif avg_memory < 100:
            report += "- **Memory Efficiency**: ACCEPTABLE (50-100MB average)\n"
        else:
            report += "- **Memory Efficiency**: NEEDS OPTIMIZATION (> 100MB average)\n"
        
        report += f"""
## Processing Throughput Analysis
### Token Processing
- **Mean Throughput**: {metrics['processing_throughput']['tokens_per_second']['mean']:.0f} tokens/second
- **Peak Throughput**: {metrics['processing_throughput']['tokens_per_second']['max']:.0f} tokens/second
- **Throughput Consistency**: CV = {metrics['processing_throughput']['tokens_per_second']['coefficient_of_variation']:.3f}

### Data Processing
- **Mean Data Rate**: {metrics['processing_throughput']['kb_per_second']['mean']:.0f} KB/second
- **Peak Data Rate**: {metrics['processing_throughput']['kb_per_second']['max']:.0f} KB/second

### Memory Efficiency
- **Tokens per MB**: {metrics['processing_throughput']['tokens_per_mb']['mean']:.0f} tokens/MB
"""
        
        # Scalability analysis
        if 'error' not in metrics['scalability_analysis']:
            scalability = metrics['scalability_analysis']
            report += f"""
## Scalability Analysis
### Correlation Analysis
- **Correlation Coefficient**: {scalability['correlation_coefficient']:.3f}
- **R-squared**: {scalability['linear_regression']['r_squared']:.3f}
- **P-value**: {scalability['correlation_p_value']:.6f}
- **Scalability Rating**: {scalability['scalability_rating']}

### Linear Regression Model
- **Slope**: {scalability['linear_regression']['slope']:.4f} ms/KB
- **Intercept**: {scalability['linear_regression']['intercept']:.2f} ms
- **Model**: Time = {scalability['linear_regression']['slope']:.4f} × FileSize + {scalability['linear_regression']['intercept']:.2f}
"""
        
        # Reliability analysis
        reliability = metrics['reliability_metrics']
        report += f"""
## Reliability Analysis
### Success Metrics
- **Success Rate**: {reliability['success_rate']:.1f}%
- **Failure Rate**: {reliability['failure_rate']:.1f}%
- **Total Runs**: {reliability['total_runs']}
- **Successful Runs**: {reliability['successful_runs']}
- **Reliability Rating**: {reliability['reliability_rating']}

### Error Distribution
"""
        
        for error_count, frequency in reliability['error_distribution'].items():
            report += f"- {error_count} errors: {frequency} files\n"
        
        # Distribution analysis
        if 'error' not in metrics['performance_distribution']:
            dist = metrics['performance_distribution']
            report += f"""
## Performance Distribution Analysis
### Distribution Characteristics
- **Distribution Shape**: {dist['distribution_shape']}
- **Skewness**: {dist['skewness']:.3f}
- **Kurtosis**: {dist['kurtosis']:.3f}
"""
            
            if dist['normality_test']['is_normal_distribution'] is not None:
                normality = dist['normality_test']
                report += f"""
### Normality Test
- **Shapiro-Wilk Statistic**: {normality['shapiro_wilk_statistic']:.4f}
- **P-value**: {normality['shapiro_wilk_p_value']:.6f}
- **Normal Distribution**: {'Yes' if normality['is_normal_distribution'] else 'No'}
"""
        
        # Outlier analysis
        if 'error' not in metrics['outlier_analysis']:
            outliers = metrics['outlier_analysis']
            report += f"""
## Outlier Analysis
### IQR Method
- **Outliers Detected**: {outliers['iqr_method']['outlier_count']}
- **Outlier Percentage**: {outliers['iqr_method']['outlier_percentage']:.1f}%
- **Bounds**: [{outliers['iqr_method']['lower_bound']:.2f}, {outliers['iqr_method']['upper_bound']:.2f}] ms

### Z-Score Method
- **Outliers Detected**: {outliers['z_score_method']['outlier_count']}
- **Outlier Percentage**: {outliers['z_score_method']['outlier_percentage']:.1f}%
- **Threshold**: ±{outliers['z_score_method']['threshold']} standard deviations
"""
        
        # Recommendations
        report += """
## Performance Recommendations

### Optimization Priorities
1. **High Impact Areas**: Focus on reducing compilation time variance
2. **Memory Management**: Monitor peak memory usage in large files
3. **Error Handling**: Improve error recovery for better reliability
4. **Scalability**: Optimize for larger input files if needed

### Performance Targets
- **Compilation Time**: < 100ms for medium files
- **Memory Usage**: < 50MB average
- **Success Rate**: > 95%
- **Consistency**: Coefficient of variation < 0.3

### Monitoring Recommendations
- Track performance trends over time
- Monitor regression in new versions
- Set up automated performance testing
- Establish performance baselines
"""
        
        return report
    
    def save_analysis(self, metrics: Dict, filename: str = "performance_analysis.json"):
        """Save analysis results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        print(f"Analysis results saved to {filename}")

def main():
    """Main execution"""
    analyzer = PerformanceAnalyzer()
    
    # Load data
    analyzer.load_data()
    
    # Perform analysis
    print("🔍 Performing advanced performance analysis...")
    metrics = analyzer.calculate_comprehensive_metrics()
    
    # Generate report
    print("📊 Generating analysis report...")
    report = analyzer.generate_performance_report()
    
    # Save results
    analyzer.save_analysis(metrics)
    
    with open("performance_analysis_report.md", "w") as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print("📈 PERFORMANCE ANALYSIS COMPLETED")
    print("📄 Report saved to: performance_analysis_report.md")
    print("💾 Analysis saved to: performance_analysis.json")
    
    # Print quick summary
    if 'error' not in metrics:
        print(f"\n🎯 ANALYSIS SUMMARY:")
        print(f"   Performance Rating: {metrics.get('compilation_performance', {}).get('coefficient_of_variation', 'N/A')}")
        print(f"   Memory Efficiency: {metrics.get('memory_efficiency', {}).get('mean', 'N/A'):.2f} MB")
        print(f"   Reliability: {metrics.get('reliability_metrics', {}).get('success_rate', 'N/A'):.1f}%")

if __name__ == "__main__":
    main()
