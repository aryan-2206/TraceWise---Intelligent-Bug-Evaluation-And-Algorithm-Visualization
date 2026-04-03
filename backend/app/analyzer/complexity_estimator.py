import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ComplexityEstimator:
    """Estimate time and space complexity of algorithms"""
    
    def __init__(self):
        self.complexity_patterns = {
            'O(1)': [
                r'array\[0\]',
                r'array\[.*\]\s*=',
                r'push\s*\(',
                r'pop\s*\(',
                r'append\s*\(',
                r'len\s*\(',
                r'size\s*\(',
                r'first|last|front|back'
            ],
            'O(log n)': [
                r'binary_search',
                r'while\s+.*<=.*\s*:\s*\n.*mid\s*=',
                r'mid\s*=\s*.*[+\-].*/\s*2',
                r'left\s*=\s*mid\s*[+\-]\s*1',
                r'right\s*=\s*mid\s*[+\-]\s*1',
                r'log\s*\(',
                r'log2\s*\(',
                r'math\.log'
            ],
            'O(n)': [
                r'for\s+.*\s*in\s+.*:',
                r'for\s*\([^)]*\):\s*\n.*[^{]*$',
                r'while\s+.*<\s*.*:',
                r'find\s*\(',
                r'index\s*\(',
                r'search\s*\(',
                r'linear_search'
            ],
            'O(n log n)': [
                r'merge_sort',
                r'quick_sort',
                r'heap_sort',
                r'sort\s*\(',
                r'heapify',
                r'merge\s*\(',
                r'partition',
                r'while\s+.*:\s*\n.*for\s+.*'
            ],
            'O(n²)': [
                r'for\s+.*:\s*\n.*for\s+.*:',
                r'for\s*\([^)]*\):\s*\n.*for\s*\([^)]*\):',
                r'bubble_sort',
                r'selection_sort',
                r'insertion_sort',
                r'nested.*loop'
            ],
            'O(n³)': [
                r'for\s+.*:\s*\n.*for\s+.*:\s*\n.*for\s+.*:',
                r'triple.*nested',
                r'cubic.*algorithm'
            ],
            'O(2^n)': [
                r'fibonacci.*recursive',
                r'power\s*\(.*,\s*n\)',
                r'subset.*generation',
                r'permutation',
                r'combination.*recursive',
                r'2\s*\*\s*n'
            ],
            'O(n!)': [
                r'factorial',
                r'permutation.*all',
                r'traveling.*salesman',
                r'n!',
                r'factorial\s*\('
            ]
        }
        
        self.space_complexity_patterns = {
            'O(1)': [
                r'constant.*space',
                r'in.*place',
                r'swap',
                r'temp\s*=',
                r'no.*extra.*space'
            ],
            'O(n)': [
                r'array\s*=.*\[.*\]',
                r'list\s*=.*\[.*\]',
                r'vector\s*=',
                r'dynamic.*array',
                r'copy.*array'
            ],
            'O(log n)': [
                r'recursion.*depth',
                r'call.*stack',
                r'divide.*conquer'
            ],
            'O(n²)': [
                r'2d.*array',
                r'matrix',
                r'nested.*array',
                r'double.*array'
            ]
        }
    
    def estimate(self, structure: Dict[str, Any], algorithm: str = None, language: str = 'python') -> Dict[str, Any]:
        """Estimate time and space complexity"""
        
        try:
            # Get all function bodies
            function_bodies = self._extract_function_bodies(structure)
            all_code = '\n'.join(function_bodies)
            
            # Estimate time complexity
            time_complexity = self._estimate_time_complexity(all_code, algorithm, language)
            
            # Estimate space complexity
            space_complexity = self._estimate_space_complexity(all_code, algorithm, language)
            
            # Get complexity details
            complexity_details = self._get_complexity_details(all_code, time_complexity, space_complexity)
            
            return {
                'time_complexity': time_complexity,
                'space_complexity': space_complexity,
                'details': complexity_details,
                'confidence': self._calculate_confidence(all_code, algorithm),
                'factors': self._identify_complexity_factors(all_code, algorithm)
            }
            
        except Exception as e:
            logger.error(f"Error estimating complexity: {str(e)}")
            return {
                'time_complexity': 'Unknown',
                'space_complexity': 'Unknown',
                'details': {},
                'confidence': 0,
                'factors': []
            }
    
    def _extract_function_bodies(self, structure: Dict[str, Any]) -> List[str]:
        """Extract function bodies from structure"""
        
        try:
            bodies = []
            functions = structure.get('functions', [])
            
            for func in functions:
                if 'body' in func:
                    bodies.append(func['body'])
            
            return bodies
            
        except Exception as e:
            logger.error(f"Error extracting function bodies: {str(e)}")
            return []
    
    def _estimate_time_complexity(self, code: str, algorithm: str = None, language: str = 'python') -> str:
        """Estimate time complexity"""
        
        try:
            # If algorithm is known, use predefined complexity
            if algorithm:
                algorithm_complexity = self._get_algorithm_complexity(algorithm)
                if algorithm_complexity:
                    return algorithm_complexity
            
            # Analyze code patterns
            scores = {}
            
            for complexity, patterns in self.complexity_patterns.items():
                score = 0
                for pattern in patterns:
                    matches = len(re.findall(pattern, code, re.IGNORECASE | re.MULTILINE))
                    score += matches
                
                if score > 0:
                    scores[complexity] = score
            
            # Determine complexity based on scores
            if scores:
                # Higher complexity wins if there are multiple patterns
                complexity_order = ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)', 'O(n³)', 'O(2^n)', 'O(n!)']
                
                for complexity in reversed(complexity_order):
                    if complexity in scores:
                        return complexity
            
            return 'O(n)'  # Default assumption
            
        except Exception as e:
            logger.error(f"Error estimating time complexity: {str(e)}")
            return 'Unknown'
    
    def _estimate_space_complexity(self, code: str, algorithm: str = None, language: str = 'python') -> str:
        """Estimate space complexity"""
        
        try:
            # If algorithm is known, use predefined complexity
            if algorithm:
                algorithm_space = self._get_algorithm_space_complexity(algorithm)
                if algorithm_space:
                    return algorithm_space
            
            # Analyze code patterns
            scores = {}
            
            for complexity, patterns in self.space_complexity_patterns.items():
                score = 0
                for pattern in patterns:
                    matches = len(re.findall(pattern, code, re.IGNORECASE | re.MULTILINE))
                    score += matches
                
                if score > 0:
                    scores[complexity] = score
            
            # Determine complexity based on scores
            if scores:
                complexity_order = ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']
                
                for complexity in reversed(complexity_order):
                    if complexity in scores:
                        return complexity
            
            # Check for recursion (adds stack space)
            if self._has_recursion(code):
                return 'O(n)'  # Recursive call stack
            
            return 'O(1)'  # Default assumption
            
        except Exception as e:
            logger.error(f"Error estimating space complexity: {str(e)}")
            return 'Unknown'
    
    def _get_algorithm_complexity(self, algorithm: str) -> str:
        """Get known time complexity for algorithms"""
        
        algorithm_complexities = {
            'binary_search': 'O(log n)',
            'linear_search': 'O(n)',
            'bubble_sort': 'O(n²)',
            'selection_sort': 'O(n²)',
            'insertion_sort': 'O(n²)',
            'quick_sort': 'O(n log n)',
            'merge_sort': 'O(n log n)',
            'heap_sort': 'O(n log n)',
            'counting_sort': 'O(n)',
            'radix_sort': 'O(nk)',
            'dfs': 'O(V + E)',
            'bfs': 'O(V + E)',
            'dijkstra': 'O((V + E) log V)',
            'bellman_ford': 'O(VE)',
            'floyd_warshall': 'O(V³)',
            'kruskal': 'O(E log V)',
            'prim': 'O(E log V)',
            'topological_sort': 'O(V + E)',
            'fibonacci_recursive': 'O(2^n)',
            'fibonacci_iterative': 'O(n)',
            'factorial_recursive': 'O(n)',
            'power_recursive': 'O(log n)',
            'power_iterative': 'O(n)'
        }
        
        return algorithm_complexities.get(algorithm)
    
    def _get_algorithm_space_complexity(self, algorithm: str) -> str:
        """Get known space complexity for algorithms"""
        
        space_complexities = {
            'binary_search': 'O(1)',
            'linear_search': 'O(1)',
            'bubble_sort': 'O(1)',
            'selection_sort': 'O(1)',
            'insertion_sort': 'O(1)',
            'quick_sort': 'O(log n)',
            'merge_sort': 'O(n)',
            'heap_sort': 'O(1)',
            'counting_sort': 'O(n)',
            'radix_sort': 'O(n)',
            'dfs': 'O(V)',
            'bfs': 'O(V)',
            'dijkstra': 'O(V)',
            'bellman_ford': 'O(V)',
            'floyd_warshall': 'O(V²)',
            'kruskal': 'O(V)',
            'prim': 'O(V)',
            'topological_sort': 'O(V)',
            'fibonacci_recursive': 'O(n)',
            'fibonacci_iterative': 'O(1)',
            'factorial_recursive': 'O(n)',
            'power_recursive': 'O(log n)',
            'power_iterative': 'O(1)'
        }
        
        return space_complexities.get(algorithm)
    
    def _get_complexity_details(self, code: str, time_complexity: str, space_complexity: str) -> Dict[str, Any]:
        """Get detailed analysis of complexity factors"""
        
        try:
            details = {
                'loops': self._analyze_loops(code),
                'recursion': self._analyze_recursion(code),
                'data_structures': self._analyze_data_structures(code),
                'operations': self._analyze_operations(code)
            }
            
            # Add complexity-specific details
            if 'O(n²)' in time_complexity:
                details['nested_loops'] = self._find_nested_loops(code)
            
            if 'O(log n)' in time_complexity:
                details['logarithmic_patterns'] = self._find_logarithmic_patterns(code)
            
            if 'O(2^n)' in time_complexity:
                details['exponential_patterns'] = self._find_exponential_patterns(code)
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting complexity details: {str(e)}")
            return {}
    
    def _calculate_confidence(self, code: str, algorithm: str = None) -> float:
        """Calculate confidence in complexity estimation"""
        
        try:
            confidence = 0.5  # Base confidence
            
            # Higher confidence if algorithm is known
            if algorithm:
                confidence += 0.4
            
            # Check for clear patterns
            pattern_count = 0
            for patterns in self.complexity_patterns.values():
                for pattern in patterns:
                    if re.search(pattern, code, re.IGNORECASE):
                        pattern_count += 1
            
            if pattern_count > 0:
                confidence += min(0.3, pattern_count * 0.1)
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.0
    
    def _identify_complexity_factors(self, code: str, algorithm: str = None) -> List[str]:
        """Identify factors contributing to complexity"""
        
        try:
            factors = []
            
            # Check for loops
            if re.search(r'for\s+.*\s*in\s+.*:', code):
                factors.append('Linear iteration')
            
            if re.search(r'for\s+.*:\s*\n.*for\s+.*:', code):
                factors.append('Nested loops')
            
            # Check for recursion
            if self._has_recursion(code):
                factors.append('Recursion')
            
            # Check for divide and conquer
            if re.search(r'divide|conquer|merge|partition', code, re.IGNORECASE):
                factors.append('Divide and conquer')
            
            # Check for exponential patterns
            if re.search(r'2\s*\*\s*n|factorial|permutation', code, re.IGNORECASE):
                factors.append('Exponential growth')
            
            # Check for data structures
            if re.search(r'heap|priority.*queue', code, re.IGNORECASE):
                factors.append('Heap operations')
            
            if re.search(r'hash.*map|dictionary|set', code, re.IGNORECASE):
                factors.append('Hash table operations')
            
            return factors
            
        except Exception as e:
            logger.error(f"Error identifying complexity factors: {str(e)}")
            return []
    
    def _analyze_loops(self, code: str) -> Dict[str, Any]:
        """Analyze loop structures"""
        
        try:
            loops = {
                'for_loops': len(re.findall(r'\bfor\s+', code)),
                'while_loops': len(re.findall(r'\bwhile\s+', code)),
                'nested_loops': len(re.findall(r'for\s+.*:\s*\n.*for\s+.*:', code, re.MULTILINE)),
                'loop_patterns': []
            }
            
            # Identify specific loop patterns
            if re.search(r'for\s+i\s+in\s+range\s*\(\s*len\s*\(', code):
                loops['loop_patterns'].append('Array iteration')
            
            if re.search(r'while\s+left\s*<=?\s*right', code):
                loops['loop_patterns'].append('Binary search pattern')
            
            return loops
            
        except Exception as e:
            logger.error(f"Error analyzing loops: {str(e)}")
            return {}
    
    def _analyze_recursion(self, code: str) -> Dict[str, Any]:
        """Analyze recursive patterns"""
        
        try:
            recursion = {
                'has_recursion': self._has_recursion(code),
                'recursive_functions': [],
                'tail_recursion': False
            }
            
            if recursion['has_recursion']:
                # Find recursive function calls
                func_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:'
                matches = re.finditer(func_pattern, code)
                
                for match in matches:
                    func_name = match.group(1)
                    if re.search(rf'\b{func_name}\s*\(', code):
                        recursion['recursive_functions'].append(func_name)
                
                # Check for tail recursion (simplified)
                if re.search(r'return\s+\w+\s*\([^)]*\)\s*$', code, re.MULTILINE):
                    recursion['tail_recursion'] = True
            
            return recursion
            
        except Exception as e:
            logger.error(f"Error analyzing recursion: {str(e)}")
            return {}
    
    def _analyze_data_structures(self, code: str) -> Dict[str, Any]:
        """Analyze data structure usage"""
        
        try:
            structures = {
                'arrays': len(re.findall(r'\[\s*\]|list\s*\(|array\s*\(', code)),
                'hash_maps': len(re.findall(r'dictionary|dict\s*\(|hash.*map|map\s*\(', code, re.IGNORECASE)),
                'sets': len(re.findall(r'set\s*\(|hash.*set', code, re.IGNORECASE)),
                'heaps': len(re.search(r'heap|priority.*queue', code, re.IGNORECASE)),
                'trees': len(re.search(r'tree|node|root|leaf', code, re.IGNORECASE)),
                'graphs': len(re.search(r'graph|vertex|edge|adjacency', code, re.IGNORECASE))
            }
            
            return structures
            
        except Exception as e:
            logger.error(f"Error analyzing data structures: {str(e)}")
            return {}
    
    def _analyze_operations(self, code: str) -> Dict[str, Any]:
        """Analyze operation patterns"""
        
        try:
            operations = {
                'comparisons': len(re.findall(r'[<>=!]=?', code)),
                'arithmetic': len(re.findall(r'[+\-*/%]', code)),
                'function_calls': len(re.findall(r'\w+\s*\(', code)),
                'array_access': len(re.findall(r'\w+\[.*\]', code)),
                'memory_allocation': len(re.findall(r'new\s+|malloc|calloc|alloc', code, re.IGNORECASE))
            }
            
            return operations
            
        except Exception as e:
            logger.error(f"Error analyzing operations: {str(e)}")
            return {}
    
    def _has_recursion(self, code: str) -> bool:
        """Check if code has recursion"""
        
        try:
            # Find function definitions
            func_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:|function\s+(\w+)\s*\([^)]*\)\s*\{'
            matches = re.finditer(func_pattern, code)
            
            for match in matches:
                func_name = match.group(1) or match.group(2)
                if func_name and re.search(rf'\b{func_name}\s*\(', code):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking recursion: {str(e)}")
            return False
    
    def _find_nested_loops(self, code: str) -> List[str]:
        """Find nested loop patterns"""
        
        try:
            nested_patterns = []
            
            # Two-level nesting
            if re.search(r'for\s+.*:\s*\n.*for\s+.*:', code, re.MULTILINE):
                nested_patterns.append('Double nested loop')
            
            # Three-level nesting
            if re.search(r'for\s+.*:\s*\n.*for\s+.*:\s*\n.*for\s+.*:', code, re.MULTILINE):
                nested_patterns.append('Triple nested loop')
            
            # Mixed loop types
            if re.search(r'for\s+.*:\s*\n.*while\s+.*:', code, re.MULTILINE):
                nested_patterns.append('Mixed for-while loop')
            
            return nested_patterns
            
        except Exception as e:
            logger.error(f"Error finding nested loops: {str(e)}")
            return []
    
    def _find_logarithmic_patterns(self, code: str) -> List[str]:
        """Find logarithmic patterns"""
        
        try:
            patterns = []
            
            if re.search(r'while\s+.*<=.*\s*:\s*\n.*mid\s*=.*[+\-].*/\s*2', code):
                patterns.append('Binary division pattern')
            
            if re.search(r'mid\s*=\s*.*[+\-].*/\s*2', code):
                patterns.append('Midpoint calculation')
            
            if re.search(r'log\s*\(|log2\s*\(|math\.log', code):
                patterns.append('Logarithmic function')
            
            if re.search(r'left\s*=\s*mid\s*[+\-]\s*1|right\s*=\s*mid\s*[+\-]\s*1', code):
                patterns.append('Range halving')
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error finding logarithmic patterns: {str(e)}")
            return []
    
    def _find_exponential_patterns(self, code: str) -> List[str]:
        """Find exponential patterns"""
        
        try:
            patterns = []
            
            if re.search(r'fibonacci.*recursive', code, re.IGNORECASE):
                patterns.append('Recursive Fibonacci')
            
            if re.search(r'2\s*\*\s*n|2\^n', code):
                patterns.append('Exponential growth (2^n)')
            
            if re.search(r'factorial\s*\(', code):
                patterns.append('Factorial computation')
            
            if re.search(r'permutation|combination', code, re.IGNORECASE):
                patterns.append('Combinatorial generation')
            
            if re.search(r'power\s*\([^,]*,\s*n\)', code):
                patterns.append('Exponential power')
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error finding exponential patterns: {str(e)}")
            return []
