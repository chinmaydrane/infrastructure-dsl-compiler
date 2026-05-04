#!/usr/bin/env python3
"""
Performance Profiler for DSL Compiler
Provides comprehensive numerical evaluation of compiler performance
"""

import time
import psutil
import tracemalloc
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import statistics

class PerformanceProfiler:
    def __init__(self):
        self.results = []
        self.process = psutil.Process()
        
    def measure_compilation(self, filename: str) -> Dict:
        """Measure compilation performance for a single file"""
        print(f"Profiling {filename}...")
        
        # Start memory tracking
        tracemalloc.start()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        # Measure compilation time
        start_time = time.time()
        
        try:
            # Run the compiler
            result = subprocess.run([
                sys.executable, 'main.py', filename, '--verbose'
            ], capture_output=True, text=True, timeout=30)
            
            end_time = time.time()
            
            # Get memory usage
            current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            peak_memory = tracemalloc.get_traced_memory()[1] / 1024 / 1024  # MB
            tracemalloc.stop()
            
            # Parse output for metrics
            output_lines = result.stdout.split('\n')
            token_count = 0
            error_count = 0
            warning_count = 0
            
            for line in output_lines:
                if "Generated" in line and "tokens" in line:
                    # Find the number after "Generated"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.isdigit() and i > 0:
                            token_count = int(part)
                            break
                elif "Total Errors:" in line:
                    error_count = int(line.split(":")[1].strip())
                elif "Compilation completed with" in line and "warnings" in line:
                    warning_count = int(line.split()[3])
            
            # Get file size
            file_size = os.path.getsize(filename) / 1024  # KB
            
            return {
                'filename': os.path.basename(filename),
                'file_size_kb': file_size,
                'compilation_time_ms': (end_time - start_time) * 1000,
                'start_memory_mb': start_memory,
                'peak_memory_mb': peak_memory,
                'memory_used_mb': peak_memory - start_memory,
                'token_count': token_count,
                'error_count': error_count,
                'warning_count': warning_count,
                'exit_code': result.returncode,
                'success': result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                'filename': os.path.basename(filename),
                'error': 'timeout',
                'compilation_time_ms': 30000  # 30 second timeout
            }
        except Exception as e:
            return {
                'filename': os.path.basename(filename),
                'error': str(e),
                'compilation_time_ms': 0
            }
    
    def profile_all_files(self, input_directory: str = "input") -> List[Dict]:
        """Profile all DSL files in the input directory"""
        dsl_files = []
        for file in os.listdir(input_directory):
            if file.endswith('.dsl'):
                dsl_files.append(os.path.join(input_directory, file))
        
        print(f"Found {len(dsl_files)} DSL files to profile")
        
        for file_path in sorted(dsl_files):
            result = self.measure_compilation(file_path)
            self.results.append(result)
            
            # Print immediate results
            if 'error' in result:
                print(f"  ❌ {result['filename']}: {result['error']}")
            else:
                print(f"  ✅ {result['filename']}: {result['compilation_time_ms']:.1f}ms, "
                      f"{result['token_count']} tokens, {result['error_count']} errors")
        
        return self.results
    
    def calculate_statistics(self) -> Dict:
        """Calculate comprehensive performance statistics"""
        successful_results = [r for r in self.results if r.get('success', False)]
        error_results = [r for r in self.results if not r.get('success', False)]
        
        if not successful_results:
            return {"error": "No successful compilations found"}
        
        # Compilation time statistics
        compilation_times = [r['compilation_time_ms'] for r in successful_results]
        
        # Memory usage statistics
        memory_usage = [r['memory_used_mb'] for r in successful_results]
        
        # Token processing statistics
        token_counts = [r['token_count'] for r in successful_results]
        file_sizes = [r['file_size_kb'] for r in successful_results]
        
        # Performance ratios
        tokens_per_ms = [t/time for t, time in zip(token_counts, compilation_times)]
        kb_per_ms = [size/time for size, time in zip(file_sizes, compilation_times)]
        
        stats = {
            'summary': {
                'total_files': len(self.results),
                'successful_files': len(successful_results),
                'failed_files': len(error_results),
                'success_rate': (len(successful_results) / len(self.results)) * 100
            },
            'compilation_performance': {
                'avg_time_ms': statistics.mean(compilation_times),
                'median_time_ms': statistics.median(compilation_times),
                'min_time_ms': min(compilation_times),
                'max_time_ms': max(compilation_times),
                'std_dev_ms': statistics.stdev(compilation_times) if len(compilation_times) > 1 else 0
            },
            'memory_performance': {
                'avg_memory_mb': statistics.mean(memory_usage),
                'median_memory_mb': statistics.median(memory_usage),
                'min_memory_mb': min(memory_usage),
                'max_memory_mb': max(memory_usage),
                'total_memory_mb': sum(memory_usage)
            },
            'processing_efficiency': {
                'avg_tokens_per_ms': statistics.mean(tokens_per_ms),
                'avg_kb_per_ms': statistics.mean(kb_per_ms),
                'total_tokens_processed': sum(token_counts),
                'total_kb_processed': sum(file_sizes)
            },
            'error_analysis': {
                'total_errors': sum(r.get('error_count', 0) for r in self.results),
                'total_warnings': sum(r.get('warning_count', 0) for r in self.results),
                'files_with_errors': len([r for r in self.results if r.get('error_count', 0) > 0])
            }
        }
        
        return stats
    
    def generate_performance_report(self) -> str:
        """Generate a comprehensive performance evaluation report"""
        stats = self.calculate_statistics()
        
        if 'error' in stats:
            return f"Error generating report: {stats['error']}"
        
        report = f"""
# DSL Compiler Performance Evaluation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- Total Files Processed: {stats['summary']['total_files']}
- Successful Compilations: {stats['summary']['successful_files']}
- Failed Compilations: {stats['summary']['failed_files']}
- Overall Success Rate: {stats['summary']['success_rate']:.1f}%

## Compilation Performance Analysis
### Time Metrics
- Average Compilation Time: {stats['compilation_performance']['avg_time_ms']:.2f} ms
- Median Compilation Time: {stats['compilation_performance']['median_time_ms']:.2f} ms
- Fastest Compilation: {stats['compilation_performance']['min_time_ms']:.2f} ms
- Slowest Compilation: {stats['compilation_performance']['max_time_ms']:.2f} ms
- Standard Deviation: {stats['compilation_performance']['std_dev_ms']:.2f} ms

### Performance Classification
"""
        
        # Classify performance
        avg_time = stats['compilation_performance']['avg_time_ms']
        if avg_time < 50:
            report += "- Performance Rating: EXCELLENT (< 50ms average)\n"
        elif avg_time < 100:
            report += "- Performance Rating: GOOD (50-100ms average)\n"
        elif avg_time < 200:
            report += "- Performance Rating: ACCEPTABLE (100-200ms average)\n"
        else:
            report += "- Performance Rating: NEEDS OPTIMIZATION (> 200ms average)\n"
        
        report += f"""
## Memory Usage Analysis
- Average Memory Usage: {stats['memory_performance']['avg_memory_mb']:.2f} MB
- Median Memory Usage: {stats['memory_performance']['median_memory_mb']:.2f} MB
- Peak Memory Usage: {stats['memory_performance']['max_memory_mb']:.2f} MB
- Total Memory Consumed: {stats['memory_performance']['total_memory_mb']:.2f} MB

### Memory Efficiency
"""
        
        avg_memory = stats['memory_performance']['avg_memory_mb']
        if avg_memory < 20:
            report += "- Memory Efficiency: EXCELLENT (< 20MB average)\n"
        elif avg_memory < 50:
            report += "- Memory Efficiency: GOOD (20-50MB average)\n"
        elif avg_memory < 100:
            report += "- Memory Efficiency: ACCEPTABLE (50-100MB average)\n"
        else:
            report += "- Memory Efficiency: NEEDS OPTIMIZATION (> 100MB average)\n"
        
        report += f"""
## Processing Efficiency
- Average Tokens/Second: {stats['processing_efficiency']['avg_tokens_per_ms'] * 1000:.0f} tokens/sec
- Average KB/Second: {stats['processing_efficiency']['avg_kb_per_ms'] * 1000:.0f} KB/sec
- Total Tokens Processed: {stats['processing_efficiency']['total_tokens_processed']:,}
- Total Data Processed: {stats['processing_efficiency']['total_kb_processed']:.1f} KB

### Throughput Analysis
"""
        
        throughput = stats['processing_efficiency']['avg_tokens_per_ms'] * 1000
        if throughput > 10000:
            report += "- Throughput Rating: EXCELLENT (> 10,000 tokens/sec)\n"
        elif throughput > 5000:
            report += "- Throughput Rating: GOOD (5,000-10,000 tokens/sec)\n"
        elif throughput > 2000:
            report += "- Throughput Rating: ACCEPTABLE (2,000-5,000 tokens/sec)\n"
        else:
            report += "- Throughput Rating: NEEDS OPTIMIZATION (< 2,000 tokens/sec)\n"
        
        report += f"""
## Error Analysis
- Total Errors Detected: {stats['error_analysis']['total_errors']}
- Total Warnings Generated: {stats['error_analysis']['total_warnings']}
- Files with Errors: {stats['error_analysis']['files_with_errors']}

### Error Detection Performance
"""
        
        if stats['error_analysis']['files_with_errors'] > 0:
            report += "- Error Detection: ACTIVE (errors found and reported)\n"
        else:
            report += "- Error Detection: NO ERRORS (all files compiled successfully)\n"
        
        report += f"""
## Detailed Results by File
"""
        
        for result in self.results:
            if 'error' not in result:
                status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
                report += f"""
### {result['filename']} - {status}
- File Size: {result['file_size_kb']:.1f} KB
- Compilation Time: {result['compilation_time_ms']:.2f} ms
- Memory Used: {result['memory_used_mb']:.2f} MB
- Tokens Processed: {result['token_count']}
- Errors: {result['error_count']}, Warnings: {result['warning_count']}
"""
        
        return report
    
    def save_results(self, filename: str = "performance_results.json"):
        """Save detailed results to JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results,
                'statistics': self.calculate_statistics()
            }, f, indent=2)
        print(f"Results saved to {filename}")

def main():
    """Main execution function"""
    profiler = PerformanceProfiler()
    
    print("🚀 Starting DSL Compiler Performance Evaluation")
    print("=" * 60)
    
    # Profile all files
    results = profiler.profile_all_files()
    
    print("\n" + "=" * 60)
    print("📊 Generating Performance Analysis...")
    
    # Generate report
    report = profiler.generate_performance_report()
    
    # Save results
    profiler.save_results()
    
    # Save report
    with open("performance_report.md", "w") as f:
        f.write(report)
    
    print("\n📄 Performance report saved to: performance_report.md")
    print("💾 Detailed results saved to: performance_results.json")
    
    # Print summary
    stats = profiler.calculate_statistics()
    if 'error' not in stats:
        print(f"\n🎯 QUICK SUMMARY:")
        print(f"   Success Rate: {stats['summary']['success_rate']:.1f}%")
        print(f"   Avg Time: {stats['compilation_performance']['avg_time_ms']:.1f}ms")
        print(f"   Avg Memory: {stats['memory_performance']['avg_memory_mb']:.1f}MB")
        print(f"   Throughput: {stats['processing_efficiency']['avg_tokens_per_ms'] * 1000:.0f} tokens/sec")

if __name__ == "__main__":
    main()
