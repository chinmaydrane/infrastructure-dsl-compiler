#!/usr/bin/env python3
"""
Automated Benchmark Testing Suite for DSL Compiler
Provides comprehensive performance testing and analysis
"""

import os
import sys
import json
import time
import statistics
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class BenchmarkSuite:
    def __init__(self):
        self.results = {}
        self.test_categories = {
            'small_files': [],    # < 1KB
            'medium_files': [],   # 1-10KB  
            'large_files': [],    # > 10KB
            'error_files': [],    # Files with errors
            'success_files': []   # Files that compile successfully
        }
        
    def categorize_file(self, file_path: str) -> str:
        """Categorize file by size and expected outcome"""
        size_kb = os.path.getsize(file_path) / 1024
        
        if size_kb < 1:
            size_category = 'small_files'
        elif size_kb <= 10:
            size_category = 'medium_files'
        else:
            size_category = 'large_files'
            
        # Check if it's likely an error file based on name
        filename = os.path.basename(file_path).lower()
        if any(keyword in filename for keyword in ['error', 'broken', 'invalid']):
            return 'error_files'
        elif any(keyword in filename for keyword in ['fixed', 'working', 'simple']):
            return 'success_files'
        else:
            return size_category
    
    def run_single_benchmark(self, file_path: str, iterations: int = 5) -> Dict:
        """Run benchmark for a single file with multiple iterations"""
        category = self.categorize_file(file_path)
        filename = os.path.basename(file_path)
        
        print(f"Benchmarking {filename} ({category})...")
        
        times = []
        memory_usage = []
        success_count = 0
        
        for i in range(iterations):
            try:
                start_time = time.time()
                
                result = subprocess.run([
                    sys.executable, 'main.py', file_path, '--verbose'
                ], capture_output=True, text=True, timeout=30)
                
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000  # ms
                
                if result.returncode == 0:
                    success_count += 1
                    
                times.append(execution_time)
                
                # Parse memory usage from output if available
                if "Memory Used:" in result.stdout:
                    for line in result.stdout.split('\n'):
                        if "Memory Used:" in line:
                            memory_mb = float(line.split(':')[1].strip().split()[0])
                            memory_usage.append(memory_mb)
                            break
                
            except subprocess.TimeoutExpired:
                print(f"  Timeout on iteration {i+1}")
                times.append(30000)  # 30 second timeout
            except Exception as e:
                print(f"  Error on iteration {i+1}: {e}")
                times.append(0)
        
        # Calculate statistics
        valid_times = [t for t in times if t > 0 and t < 30000]
        
        if not valid_times:
            return {
                'filename': filename,
                'category': category,
                'error': 'All iterations failed',
                'iterations': iterations
            }
        
        benchmark_result = {
            'filename': filename,
            'category': category,
            'iterations': iterations,
            'success_rate': (success_count / iterations) * 100,
            'avg_time_ms': statistics.mean(valid_times),
            'median_time_ms': statistics.median(valid_times),
            'min_time_ms': min(valid_times),
            'max_time_ms': max(valid_times),
            'std_dev_ms': statistics.stdev(valid_times) if len(valid_times) > 1 else 0,
            'file_size_kb': os.path.getsize(file_path) / 1024
        }
        
        if memory_usage:
            benchmark_result.update({
                'avg_memory_mb': statistics.mean(memory_usage),
                'median_memory_mb': statistics.median(memory_usage),
                'min_memory_mb': min(memory_usage),
                'max_memory_mb': max(memory_usage)
            })
        
        return benchmark_result
    
    def run_stress_test(self, file_path: str, duration_seconds: int = 60) -> Dict:
        """Run stress test - continuous compilation for specified duration"""
        filename = os.path.basename(file_path)
        print(f"Stress testing {filename} for {duration_seconds} seconds...")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        compilation_count = 0
        success_count = 0
        total_time = 0
        errors = []
        
        while time.time() < end_time:
            try:
                compile_start = time.time()
                
                result = subprocess.run([
                    sys.executable, 'main.py', file_path
                ], capture_output=True, text=True, timeout=10)
                
                compile_end = time.time()
                compilation_time = (compile_end - compile_start) * 1000
                
                compilation_count += 1
                total_time += compilation_time
                
                if result.returncode == 0:
                    success_count += 1
                else:
                    errors.append(result.stderr[:200])  # First 200 chars of error
                
            except subprocess.TimeoutExpired:
                errors.append("Timeout")
            except Exception as e:
                errors.append(str(e)[:200])
        
        return {
            'filename': filename,
            'test_type': 'stress_test',
            'duration_seconds': duration_seconds,
            'total_compilations': compilation_count,
            'successful_compilations': success_count,
            'success_rate': (success_count / compilation_count * 100) if compilation_count > 0 else 0,
            'avg_time_ms': total_time / compilation_count if compilation_count > 0 else 0,
            'compilations_per_second': compilation_count / duration_seconds,
            'unique_errors': len(set(errors)),
            'sample_errors': list(set(errors))[:3]  # First 3 unique errors
        }
    
    def run_scalability_test(self) -> Dict:
        """Test compiler performance with increasing file sizes"""
        print("Running scalability test...")
        
        # Create test files of increasing size
        test_sizes = [100, 500, 1000, 2000, 5000]  # characters
        scalability_results = []
        
        for size in test_sizes:
            # Generate test DSL content
            test_content = self._generate_test_dsl(size)
            test_file = f"scalability_test_{size}.dsl"
            
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Benchmark this file
            result = self.run_single_benchmark(test_file, iterations=3)
            result['test_size'] = size
            scalability_results.append(result)
            
            # Clean up
            os.remove(test_file)
        
        return {
            'test_type': 'scalability',
            'results': scalability_results
        }
    
    def _generate_test_dsl(self, size: int) -> str:
        """Generate test DSL content of specified size"""
        base_content = """
server "web_server_{i}" {
    cpu = 2
    memory = "4GB"
    os = "ubuntu-20.04"
    enabled = true
}

database "db_{i}" {
    engine = "mysql"
    version = "8.0"
    storage = "100GB"
    instance_class = "db.t3.medium"
}
"""
        
        content = ""
        i = 0
        while len(content) < size:
            content += base_content.format(i=i)
            i += 1
            
        return content[:size]
    
    def run_comprehensive_benchmark(self) -> Dict:
        """Run comprehensive benchmark suite"""
        print("🚀 Starting Comprehensive Benchmark Suite")
        print("=" * 60)
        
        # Find all DSL files
        dsl_files = []
        for file in os.listdir('input'):
            if file.endswith('.dsl'):
                dsl_files.append(os.path.join('input', file))
        
        print(f"Found {len(dsl_files)} DSL files")
        
        # Run single file benchmarks
        benchmark_results = []
        for file_path in sorted(dsl_files):
            result = self.run_single_benchmark(file_path)
            benchmark_results.append(result)
        
        # Categorize results
        categorized_results = {}
        for result in benchmark_results:
            category = result['category']
            if category not in categorized_results:
                categorized_results[category] = []
            categorized_results[category].append(result)
        
        # Run stress tests on a few representative files
        stress_test_files = []
        for category in ['small_files', 'medium_files', 'large_files']:
            if category in categorized_results and categorized_results[category]:
                # Pick fastest file from each category
                fastest = min(categorized_results[category], 
                            key=lambda x: x.get('avg_time_ms', float('inf')))
                stress_test_files.append(fastest['filename'])
        
        stress_results = []
        for filename in stress_test_files[:2]:  # Test up to 2 files
            file_path = os.path.join('input', filename)
            stress_result = self.run_stress_test(file_path, duration_seconds=30)
            stress_results.append(stress_result)
        
        # Run scalability test
        scalability_result = self.run_scalability_test()
        
        # Compile final results
        comprehensive_results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files_benchmarked': len(benchmark_results),
                'categories_tested': list(categorized_results.keys()),
                'stress_tests_run': len(stress_results),
                'scalability_test_completed': True
            },
            'benchmark_results': benchmark_results,
            'categorized_results': categorized_results,
            'stress_test_results': stress_results,
            'scalability_results': scalability_result,
            'performance_analysis': self._analyze_performance(categorized_results)
        }
        
        return comprehensive_results
    
    def _analyze_performance(self, categorized_results: Dict) -> Dict:
        """Analyze performance across categories"""
        analysis = {}
        
        for category, results in categorized_results.items():
            if not results:
                continue
                
            times = [r['avg_time_ms'] for r in results if 'avg_time_ms' in r]
            success_rates = [r['success_rate'] for r in results if 'success_rate' in r]
            
            if times:
                analysis[category] = {
                    'avg_time_ms': statistics.mean(times),
                    'median_time_ms': statistics.median(times),
                    'min_time_ms': min(times),
                    'max_time_ms': max(times),
                    'std_dev_ms': statistics.stdev(times) if len(times) > 1 else 0,
                    'avg_success_rate': statistics.mean(success_rates) if success_rates else 0,
                    'file_count': len(results)
                }
        
        return analysis
    
    def generate_benchmark_report(self, results: Dict) -> str:
        """Generate comprehensive benchmark report"""
        report = f"""
# DSL Compiler Benchmark Report
Generated: {results['timestamp']}

## Executive Summary
- Total Files Benchmarked: {results['summary']['total_files_benchmarked']}
- Categories Tested: {', '.join(results['summary']['categories_tested'])}
- Stress Tests Run: {results['summary']['stress_tests_run']}
- Scalability Test: {'Completed' if results['summary']['scalability_test_completed'] else 'Failed'}

## Performance Analysis by Category
"""
        
        for category, analysis in results['performance_analysis'].items():
            report += f"""
### {category.replace('_', ' ').title()}
- Files Tested: {analysis['file_count']}
- Average Time: {analysis['avg_time_ms']:.2f} ms
- Median Time: {analysis['median_time_ms']:.2f} ms
- Fastest: {analysis['min_time_ms']:.2f} ms
- Slowest: {analysis['max_time_ms']:.2f} ms
- Standard Deviation: {analysis['std_dev_ms']:.2f} ms
- Success Rate: {analysis['avg_success_rate']:.1f}%
"""
        
        # Stress test results
        if results['stress_test_results']:
            report += "\n## Stress Test Results\n"
            for stress in results['stress_test_results']:
                report += f"""
### {stress['filename']}
- Duration: {stress['duration_seconds']} seconds
- Total Compilations: {stress['total_compilations']}
- Success Rate: {stress['success_rate']:.1f}%
- Compilations/Second: {stress['compilations_per_second']:.2f}
- Average Time: {stress['avg_time_ms']:.2f} ms
"""
        
        # Scalability results
        if 'scalability_results' in results:
            report += "\n## Scalability Test Results\n"
            for result in results['scalability_results']['results']:
                report += f"""
### File Size: {result['test_size']} characters
- Time: {result['avg_time_ms']:.2f} ms
- Throughput: {result['test_size']/result['avg_time_ms']*1000:.0f} chars/sec
"""
        
        # Detailed results
        report += "\n## Detailed Results by File\n"
        for result in results['benchmark_results']:
            status = "✅" if result.get('success_rate', 0) > 50 else "❌"
            report += f"""
{status} **{result['filename']}** ({result['category']})
- Time: {result.get('avg_time_ms', 'N/A'):.2f} ms
- Success Rate: {result.get('success_rate', 0):.1f}%
- File Size: {result['file_size_kb']:.1f} KB
"""
        
        return report
    
    def save_results(self, results: Dict, filename: str = "benchmark_results.json"):
        """Save benchmark results to file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Benchmark results saved to {filename}")

def main():
    """Main execution"""
    suite = BenchmarkSuite()
    
    # Run comprehensive benchmark
    results = suite.run_comprehensive_benchmark()
    
    # Generate and save report
    report = suite.generate_benchmark_report(results)
    
    with open("benchmark_report.md", "w") as f:
        f.write(report)
    
    suite.save_results(results)
    
    print("\n" + "=" * 60)
    print("📊 BENCHMARK COMPLETED")
    print("📄 Report saved to: benchmark_report.md")
    print("💾 Results saved to: benchmark_results.json")
    
    # Print quick summary
    print(f"\n🎯 QUICK SUMMARY:")
    print(f"   Files Tested: {results['summary']['total_files_benchmarked']}")
    print(f"   Categories: {len(results['summary']['categories_tested'])}")
    print(f"   Stress Tests: {results['summary']['stress_tests_run']}")

if __name__ == "__main__":
    main()
