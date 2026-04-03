import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DetectionRules:
    """Specific detection rules for common programming patterns and bugs"""
    
    def __init__(self):
        self.binary_search_rules = {
            'correct_implementation': {
                'patterns': [
                    r'left\s*<=\s*right',
                    r'mid\s*=\s*left\s*\+\s*\(\s*right\s*-\s*left\s*\)\s*/\s*2',
                    r'if\s+.*\[.*mid.*\]\s*==\s*target',
                    r'elif\s+.*\[.*mid.*\]\s*<\s*target',
                    r'left\s*=\s*mid\s*\+\s*1',
                    r'right\s*=\s*mid\s*-\s*1'
                ],
                'anti_patterns': [
                    r'mid\s*=\s*\(\s*left\s*\+\s*right\s*\)\s*/\s*2',  # Potential overflow
                    r'left\s*<\s*right',  # Should be <=
                    r'while\s+left\s*<\s*right'  # Missing equality case
                ]
            },
            'common_bugs': [
                {
                    'pattern': r'mid\s*=\s*\(\s*left\s*\+\s*right\s*\)\s*/\s*2',
                    'severity': 'warning',
                    'message': 'Potential integer overflow in mid calculation',
                    'suggestion': 'Use mid = left + (right - left) // 2'
                },
                {
                    'pattern': r'while\s+left\s*<\s*right',
                    'severity': 'warning',
                    'message': 'Loop condition should be <= for complete search',
                    'suggestion': 'Change to while left <= right'
                },
                {
                    'pattern': r'if\s+mid\s*==\s*target',
                    'severity': 'error',
                    'message': 'Should compare array[mid] with target, not mid itself',
                    'suggestion': 'Change to if array[mid] == target'
                }
            ]
        }
        
        self.sorting_rules = {
            'bubble_sort': {
                'correct_patterns': [
                    r'for\s+i\s+in\s+range\s*\(\s*n\s*\)',
                    r'for\s+j\s+in\s+range\s*\(\s*0\s*,\s*n\s*-\s*i\s*-\s*1\s*\)',
                    r'if\s+arr\[j\]\s*>\s*arr\[j\s*\+\s*1\]',
                    r'arr\[j\],\s*arr\[j\s*\+\s*1\]\s*=\s*arr\[j\s*\+\s*1\],\s*arr\[j\]'
                ],
                'optimization_opportunities': [
                    {
                        'pattern': r'for\s+j\s+in\s+range\s*\(\s*n\s*-\s*i\s*-\s*1\s*\)',
                        'message': 'Consider adding early termination if no swaps occurred',
                        'suggestion': 'Add a flag to detect if array is already sorted'
                    }
                ]
            },
            'selection_sort': {
                'correct_patterns': [
                    r'min_idx\s*=\s*i',
                    r'for\s+j\s+in\s+range\s*\(\s*i\s*\+\s*1\s*,\s*n\s*\)',
                    r'if\s+arr\[j\]\s*<\s*arr\[min_idx\]',
                    r'min_idx\s*=\s*j',
                    r'arr\[i\],\s*arr\[min_idx\]\s*=\s*arr\[min_idx\],\s*arr\[i\]'
                ]
            },
            'insertion_sort': {
                'correct_patterns': [
                    r'key\s*=\s*arr\[i\]',
                    r'j\s*=\s*i\s*-\s*1',
                    r'while\s+j\s*>=\s*0\s+and\s+key\s*<\s*arr\[j\]',
                    r'arr\[j\s*\+\s*1\]\s*=\s*arr\[j\]',
                    r'j\s*-=\s*1',
                    r'arr\[j\s*\+\s*1\]\s*=\s*key'
                ]
            }
        }
        
        self.graph_algorithms_rules = {
            'dfs': {
                'recursive_patterns': [
                    r'def\s+dfs\s*\(',
                    r'visited\s*=\s*\[.*\]',
                    r'if\s+not\s+visited\[.*\]',
                    r'visited\[.*\]\s*=\s*True',
                    r'for\s+neighbor\s+in\s+graph\[.*\]',
                    r'dfs\s*\('
                ],
                'iterative_patterns': [
                    r'stack\s*=\s*\[.*\]',
                    r'while\s+stack',
                    r'node\s*=\s*stack\.pop\s*\(\s*\)',
                    r'if\s+not\s+visited\[node\]',
                    r'for\s+neighbor\s+in\s+graph\[node\]',
                    r'stack\.append\s*\('
                ]
            },
            'bfs': {
                'patterns': [
                    r'from\s+collections\s+import\s+deque',
                    r'queue\s*=\s*deque\s*\(\s*\[.*\]\s*\)',
                    r'while\s+queue',
                    r'node\s*=\s*queue\.popleft\s*\(\s*\)',
                    r'if\s+not\s+visited\[node\]',
                    r'queue\.append\s*\('
                ]
            },
            'dijkstra': {
                'patterns': [
                    r'import\s+heapq',
                    r'distances\s*=\s*\{.*:\s*float\s*\(\s*\'inf\'\s*\)\s*\}',
                    r'priority_queue\s*=\s*\[\s*\(\s*0\s*,\s*start\s*\)\s*\]',
                    r'heapq\.heappush\s*\(',
                    r'heapq\.heappop\s*\(',
                    r'if\s+dist\s*<\s*distances\[node\]'
                ]
            }
        }
        
        self.general_bugs = {
            'off_by_one': [
                {
                    'pattern': r'for\s+i\s+in\s+range\s*\(\s*len\s*\(\s*arr\s*\)\s*\)',
                    'message': 'Potential off-by-one error when accessing arr[i]',
                    'suggestion': 'Ensure array bounds are checked when accessing arr[i]'
                },
                {
                    'pattern': r'arr\[len\s*\(\s*arr\s*\)\s*\]',
                    'severity': 'error',
                    'message': 'Array index out of bounds - last index is len(arr)-1',
                    'suggestion': 'Use arr[len(arr)-1] or check bounds before access'
                }
            ],
            'infinite_loops': [
                {
                    'pattern': r'while\s+True\s*:\s*\n\s*(?!.*break)',
                    'message': 'Infinite loop detected - no break statement found',
                    'suggestion': 'Add a break condition or use a specific loop condition'
                },
                {
                    'pattern': r'for\s+i\s+in\s+range\s*\(\s*\):\s*\n\s*i\s*=\s*.*',
                    'message': 'Modifying loop variable may cause infinite loop',
                    'suggestion': 'Avoid modifying loop variable inside the loop'
                }
            ],
            'memory_issues': [
                {
                    'pattern': r'new\s+\w+',
                    'languages': ['cpp'],
                    'message': 'Memory allocated with new should be freed with delete',
                    'suggestion': 'Use smart pointers or ensure proper deallocation'
                },
                {
                    'pattern': r'malloc\s*\(',
                    'languages': ['cpp'],
                    'message': 'Memory allocated with malloc should be freed with free',
                    'suggestion': 'Ensure every malloc has a corresponding free'
                }
            ],
            'performance_issues': [
                {
                    'pattern': r'for\s+.*\s*in\s+.*:\s*for\s+.*\s*in\s+.*',
                    'message': 'Nested loops may indicate O(n²) complexity',
                    'suggestion': 'Consider optimizing with better algorithms or data structures'
                },
                {
                    'pattern': r'\.append\s*\(\s*\)\s*inside\s+loop',
                    'message': 'Repeated list appending may be inefficient',
                    'suggestion': 'Consider pre-allocating or using list comprehensions'
                }
            ]
        }
    
    def check_binary_search(self, code: str) -> List[Dict[str, Any]]:
        """Check binary search implementation for common bugs"""
        
        try:
            issues = []
            rules = self.binary_search_rules
            
            # Check for anti-patterns
            for anti_pattern in rules['correct_implementation']['anti_patterns']:
                if re.search(anti_pattern, code, re.IGNORECASE):
                    bug_info = self._find_bug_info(anti_pattern, rules['common_bugs'])
                    if bug_info:
                        issues.append({
                            'type': 'binary_search_bug',
                            'pattern': anti_pattern,
                            'severity': bug_info['severity'],
                            'message': bug_info['message'],
                            'suggestion': bug_info['suggestion'],
                            'line': self._find_line_number(code, anti_pattern)
                        })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking binary search: {str(e)}")
            return []
    
    def check_sorting_algorithm(self, code: str, algorithm_type: str) -> List[Dict[str, Any]]:
        """Check sorting algorithm implementation"""
        
        try:
            issues = []
            
            if algorithm_type in self.sorting_rules:
                rules = self.sorting_rules[algorithm_type]
                
                # Check for optimization opportunities
                if 'optimization_opportunities' in rules:
                    for opportunity in rules['optimization_opportunities']:
                        if re.search(opportunity['pattern'], code, re.IGNORECASE):
                            issues.append({
                                'type': 'optimization_opportunity',
                                'pattern': opportunity['pattern'],
                                'severity': 'info',
                                'message': opportunity['message'],
                                'suggestion': opportunity['suggestion'],
                                'line': self._find_line_number(code, opportunity['pattern'])
                            })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking sorting algorithm: {str(e)}")
            return []
    
    def check_graph_algorithm(self, code: str, algorithm_type: str) -> List[Dict[str, Any]]:
        """Check graph algorithm implementation"""
        
        try:
            issues = []
            
            if algorithm_type in self.graph_algorithms_rules:
                rules = self.graph_algorithms_rules[algorithm_type]
                
                # Check for required patterns
                if 'patterns' in rules:
                    for pattern in rules['patterns']:
                        if not re.search(pattern, code, re.IGNORECASE):
                            issues.append({
                                'type': 'missing_pattern',
                                'pattern': pattern,
                                'severity': 'warning',
                                'message': f'Missing expected pattern for {algorithm_type}',
                                'suggestion': f'Ensure implementation includes: {pattern}',
                                'line': None
                            })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking graph algorithm: {str(e)}")
            return []
    
    def check_general_bugs(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for general programming bugs"""
        
        try:
            issues = []
            
            for bug_category, bug_rules in self.general_bugs.items():
                for bug_rule in bug_rules:
                    # Check if rule applies to current language
                    if 'languages' in bug_rule and language not in bug_rule['languages']:
                        continue
                    
                    if re.search(bug_rule['pattern'], code, re.IGNORECASE):
                        issues.append({
                            'type': bug_category,
                            'pattern': bug_rule['pattern'],
                            'severity': bug_rule.get('severity', 'warning'),
                            'message': bug_rule['message'],
                            'suggestion': bug_rule['suggestion'],
                            'line': self._find_line_number(code, bug_rule['pattern'])
                        })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking general bugs: {str(e)}")
            return []
    
    def _find_bug_info(self, pattern: str, bug_list: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find bug information for a given pattern"""
        
        try:
            for bug in bug_list:
                if bug['pattern'] == pattern:
                    return bug
            return None
            
        except Exception as e:
            logger.error(f"Error finding bug info: {str(e)}")
            return None
    
    def _find_line_number(self, code: str, pattern: str) -> Optional[int]:
        """Find the line number where a pattern occurs"""
        
        try:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    return i
            return None
            
        except Exception as e:
            logger.error(f"Error finding line number: {str(e)}")
            return None
    
    def get_complexity_analysis(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity based on patterns"""
        
        try:
            analysis = {
                'time_complexity': 'O(1)',
                'space_complexity': 'O(1)',
                'nested_loops': 0,
                'recursive_calls': 0,
                'factors': []
            }
            
            # Check for nested loops
            nested_loop_pattern = r'for\s+.*:\s*\n\s*for\s+.*:'
            nested_loops = len(re.findall(nested_loop_pattern, code, re.MULTILINE))
            if nested_loops > 0:
                analysis['nested_loops'] = nested_loops
                analysis['time_complexity'] = f'O(n^{nested_loops + 1})'
                analysis['factors'].append(f'{nested_loops + 1} nested loops')
            
            # Check for recursion
            recursive_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:.*\b\1\s*\('
            recursive_calls = len(re.findall(recursive_pattern, code, re.DOTALL))
            if recursive_calls > 0:
                analysis['recursive_calls'] = recursive_calls
                analysis['factors'].append('recursion')
            
            # Check for data structures
            if re.search(r'list\s*\[.*\]|array\s*\[.*\]', code):
                analysis['space_complexity'] = 'O(n)'
                analysis['factors'].append('array/list usage')
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in complexity analysis: {str(e)}")
            return {
                'time_complexity': 'Unknown',
                'space_complexity': 'Unknown',
                'nested_loops': 0,
                'recursive_calls': 0,
                'factors': []
            }
