#!/usr/bin/env python3
"""
Complete Performance Evaluation Report Generator - Fixed Version
Combines all performance data into a comprehensive evaluation report
"""

import json
import os
import sys
from datetime import datetime

class PerformanceReportGenerator:
    def __init__(self):
        self.report_data = {}
        
    def collect_all_data(self):
        """Collect data from all performance evaluation sources"""
        print("Collecting performance data...")
        
        # Load existing reports
        if os.path.exists("performance_results.json"):
            with open("performance_results.json", 'r') as f:
                self.report_data['basic_performance'] = json.load(f)
            print("Loaded basic performance results")
        
        if os.path.exists("benchmark_results.json"):
            with open("benchmark_results.json", 'r') as f:
                self.report_data['benchmark_results'] = json.load(f)
            print("Loaded benchmark results")
        
        if os.path.exists("performance_analysis.json"):
            with open("performance_analysis.json", 'r') as f:
                self.report_data['analysis_results'] = json.load(f)
            print("Loaded analysis results")
        
        # Load existing reports
        reports = {}
        for report_file in ["performance_report.md", "benchmark_report.md", "performance_analysis_report.md"]:
            if os.path.exists(report_file):
                with open(report_file, 'r') as f:
                    reports[report_file] = f.read()
                print(f"Loaded {report_file}")
        
        self.report_data['existing_reports'] = reports
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary of all performance evaluations"""
        summary = "# DSL Compiler Performance Evaluation - Executive Summary\n\n"
        summary += f"**Evaluation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Basic performance summary
        if 'basic_performance' in self.report_data:
            basic = self.report_data['basic_performance']
            stats = basic.get('statistics', {})
            
            summary += "## Overall Performance Assessment\n\n"
            
            if 'summary' in stats:
                summary += f"- **Total Files Evaluated**: {stats['summary']['total_files']}\n"
                summary += f"- **Successful Compilations**: {stats['summary']['successful_files']}\n"
                summary += f"- **Overall Success Rate**: {stats['summary']['success_rate']:.1f}%\n\n"
            
            if 'compilation_performance' in stats:
                comp = stats['compilation_performance']
                summary += "### Compilation Performance\n"
                summary += f"- **Average Compilation Time**: {comp['avg_time_ms']:.2f} ms\n"
                summary += f"- **Fastest Compilation**: {comp['min_time_ms']:.2f} ms\n"
                summary += f"- **Slowest Compilation**: {comp['max_time_ms']:.2f} ms\n"
                summary += f"- **Performance Consistency**: Std Dev = {comp['std_dev_ms']:.2f} ms\n\n"
                
                # Performance rating
                avg_time = comp['avg_time_ms']
                if avg_time < 50:
                    rating = "EXCELLENT"
                elif avg_time < 100:
                    rating = "GOOD"
                elif avg_time < 200:
                    rating = "ACCEPTABLE"
                else:
                    rating = "NEEDS OPTIMIZATION"
                
                summary += f"- **Performance Rating**: {rating}\n\n"
            
            if 'memory_performance' in stats:
                mem = stats['memory_performance']
                summary += "### Memory Efficiency\n"
                summary += f"- **Average Memory Usage**: {mem['avg_memory_mb']:.2f} MB\n"
                summary += f"- **Peak Memory Usage**: {mem['max_memory_mb']:.2f} MB\n"
                summary += f"- **Total Memory Consumed**: {mem['total_memory_mb']:.2f} MB\n\n"
                
                # Memory rating
                avg_mem = mem['avg_memory_mb']
                if avg_mem < 20:
                    mem_rating = "EXCELLENT"
                elif avg_mem < 50:
                    mem_rating = "GOOD"
                elif avg_mem < 100:
                    mem_rating = "ACCEPTABLE"
                else:
                    mem_rating = "NEEDS OPTIMIZATION"
                
                summary += f"- **Memory Efficiency Rating**: {mem_rating}\n\n"
            
            if 'processing_efficiency' in stats:
                eff = stats['processing_efficiency']
                summary += "### Processing Efficiency\n"
                summary += f"- **Average Throughput**: {eff['avg_tokens_per_ms'] * 1000:.0f} tokens/second\n"
                summary += f"- **Total Tokens Processed**: {eff['total_tokens_processed']:,}\n"
                summary += f"- **Total Data Processed**: {eff['total_kb_processed']:.1f} KB\n\n"
        
        # Benchmark summary
        if 'benchmark_results' in self.report_data:
            bench = self.report_data['benchmark_results']
            summary += "## Benchmark Testing Results\n\n"
            
            if 'summary' in bench:
                summary += f"- **Files Benchmarked**: {bench['summary']['total_files_benchmarked']}\n"
                summary += f"- **Categories Tested**: {len(bench['summary']['categories_tested'])}\n"
                summary += f"- **Stress Tests Completed**: {bench['summary']['stress_tests_run']}\n\n"
        
        # Analysis summary
        if 'analysis_results' in self.report_data:
            analysis = self.report_data['analysis_results']
            
            if 'compilation_performance' in analysis:
                comp = analysis['compilation_performance']
                summary += "## Advanced Statistical Analysis\n\n"
                summary += "### Performance Distribution\n"
                summary += f"- **Coefficient of Variation**: {comp['coefficient_of_variation']:.3f}\n"
                summary += f"- **95th Percentile**: {comp['percentiles']['p95']:.2f} ms\n"
                summary += f"- **99th Percentile**: {comp['percentiles']['p99']:.2f} ms\n\n"
        
        return summary
    
    def generate_detailed_metrics(self) -> str:
        """Generate detailed metrics section"""
        detailed = "## Detailed Performance Metrics\n\n"
        
        if 'basic_performance' in self.report_data:
            basic = self.report_data['basic_performance']
            results = basic.get('results', [])
            
            detailed += "### Individual File Performance\n\n"
            detailed += "| Filename | Size (KB) | Time (ms) | Memory (MB) | Tokens | Errors | Status |\n"
            detailed += "|----------|-----------|-----------|------------|--------|--------|--------|\n"
            
            for result in results:
                if 'error' not in result:
                    filename = result['filename']
                    size = result['file_size_kb']
                    time = result['compilation_time_ms']
                    memory = result['memory_used_mb']
                    tokens = result['token_count']
                    errors = result['error_count']
                    status = "[OK]" if result['success'] else "[FAIL]"
                    
                    detailed += f"| {filename} | {size:.1f} | {time:.1f} | {memory:.2f} | {tokens} | {errors} | {status} |\n"
        
        return detailed
    
    def generate_recommendations(self) -> str:
        """Generate performance improvement recommendations"""
        recommendations = "## Performance Improvement Recommendations\n\n"
        
        recommendations += "### Priority 1: Critical Issues\n\n"
        
        # Analyze for critical issues
        critical_issues = []
        
        if 'basic_performance' in self.report_data:
            stats = self.report_data['basic_performance'].get('statistics', {})
            
            # Check success rate
            if 'summary' in stats and stats['summary']['success_rate'] < 90:
                critical_issues.append("Low success rate - improve error handling and recovery")
            
            # Check performance
            if 'compilation_performance' in stats:
                avg_time = stats['compilation_performance']['avg_time_ms']
                if avg_time > 200:
                    critical_issues.append("Slow compilation speed - optimize parsing and code generation")
            
            # Check memory
            if 'memory_performance' in stats:
                avg_memory = stats['memory_performance']['avg_memory_mb']
                if avg_memory > 100:
                    critical_issues.append("High memory usage - implement memory optimization")
        
        if critical_issues:
            for issue in critical_issues:
                recommendations += f"- [CRITICAL] **{issue}**\n"
        else:
            recommendations += "- [OK] No critical issues identified\n"
        
        recommendations += "\n### Priority 2: Performance Optimizations\n\n"
        
        optimizations = []
        
        if 'analysis_results' in self.report_data:
            analysis = self.report_data['analysis_results']
            
            # Check consistency
            if 'compilation_performance' in analysis:
                cv = analysis['compilation_performance']['coefficient_of_variation']
                if cv > 0.5:
                    optimizations.append("High performance variance - improve consistency")
        
        if optimizations:
            for opt in optimizations:
                recommendations += f"- [OPTIMIZE] **{opt}**\n"
        else:
            recommendations += "- [OK] Performance is well-optimized\n"
        
        recommendations += "\n### Priority 3: Enhancements\n\n"
        recommendations += "- [ENHANCE] Add more comprehensive error messages\n"
        recommendations += "- [ENHANCE] Implement performance monitoring dashboard\n"
        recommendations += "- [ENHANCE] Add automated performance regression testing\n"
        recommendations += "- [ENHANCE] Optimize for specific use cases\n"
        
        return recommendations
    
    def generate_appendix(self) -> str:
        """Generate appendix with technical details"""
        appendix = "## Appendix\n\n"
        
        appendix += "### Test Environment\n\n"
        appendix += "- **Operating System**: Windows\n"
        appendix += "- **Python Version**: 3.8+\n"
        appendix += "- **Test Date**: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
        
        appendix += "### Evaluation Methodology\n\n"
        appendix += "#### Performance Metrics Collected\n"
        appendix += "- **Compilation Time**: Total time from start to finish (milliseconds)\n"
        appendix += "- **Memory Usage**: Peak memory consumption during compilation (MB)\n"
        appendix += "- **Token Count**: Number of tokens generated by lexical analysis\n"
        appendix += "- **Error Count**: Number of compilation errors detected\n"
        appendix += "- **File Size**: Input file size in kilobytes\n\n"
        
        appendix += "#### Statistical Methods\n"
        appendix += "- **Descriptive Statistics**: Mean, median, standard deviation, percentiles\n"
        appendix += "- **Distribution Analysis**: Normality testing, skewness, kurtosis\n"
        appendix += "- **Outlier Detection**: IQR and Z-score methods\n"
        appendix += "- **Correlation Analysis**: Pearson correlation coefficients\n\n"
        
        appendix += "### Data Files Generated\n\n"
        appendix += "- `performance_results.json`: Basic performance measurements\n"
        appendix += "- `benchmark_results.json`: Comprehensive benchmark results\n"
        appendix += "- `performance_analysis.json`: Statistical analysis results\n"
        appendix += "- `performance_report.md`: Basic performance report\n"
        appendix += "- `benchmark_report.md`: Benchmark testing report\n"
        appendix += "- `performance_analysis_report.md`: Advanced analysis report\n"
        appendix += "- `comprehensive_performance_report.md`: This consolidated report\n\n"
        
        return appendix
    
    def generate_comprehensive_report(self) -> str:
        """Generate complete comprehensive performance evaluation report"""
        print("Generating comprehensive performance report...")
        
        # Collect all data
        self.collect_all_data()
        
        # Generate report sections
        report = ""
        report += self.generate_executive_summary()
        report += "\n---\n\n"
        report += self.generate_detailed_metrics()
        report += "\n---\n\n"
        report += self.generate_recommendations()
        report += "\n---\n\n"
        report += self.generate_appendix()
        
        # Add footer
        report += "\n---\n\n"
        report += f"**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "**DSL Compiler Performance Evaluation System**\n"
        report += "*Automated performance analysis and reporting*\n"
        
        return report
    
    def save_report(self, report: str, filename: str = "comprehensive_performance_report.md"):
        """Save comprehensive report"""
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Comprehensive report saved to: {filename}")

def main():
    """Main execution"""
    print("Starting Comprehensive Performance Report Generation")
    print("=" * 70)
    
    generator = PerformanceReportGenerator()
    
    # Generate comprehensive report
    report = generator.generate_comprehensive_report()
    
    # Save report
    generator.save_report(report)
    
    print("\n" + "=" * 70)
    print("COMPREHENSIVE PERFORMANCE EVALUATION COMPLETED")
    print("Report saved to: comprehensive_performance_report.md")
    print("\nAvailable Reports:")
    
    # List all generated reports
    reports = [
        "comprehensive_performance_report.md",
        "performance_report.md",
        "benchmark_report.md", 
        "performance_analysis_report.md"
    ]
    
    for report in reports:
        if os.path.exists(report):
            size = os.path.getsize(report) / 1024
            print(f"   {report} ({size:.1f} KB)")
    
    print("\nAvailable Data Files:")
    data_files = [
        "performance_results.json",
        "benchmark_results.json",
        "performance_analysis.json"
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            size = os.path.getsize(data_file) / 1024
            print(f"   {data_file} ({size:.1f} KB)")
    
    print("\nNext Steps:")
    print("   1. Review comprehensive report for insights")
    print("   2. Implement priority recommendations")
    print("   3. Set up continuous performance monitoring")
    print("   4. Update performance baselines regularly")

if __name__ == "__main__":
    main()
