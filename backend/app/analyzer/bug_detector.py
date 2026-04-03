import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BugDetector:
    """Detect bugs and issues in code using pattern matching and static analysis"""
    
    def __init__(self):
        self.bug_patterns = {
            'syntax_errors': [
                {
                    'pattern': r':\s*\n\s*[^\s]',
                    'message': 'Possible indentation error',
                    'severity': 'error',
                    'languages': ['python']
                },
                {
                    'pattern': r'\{\s*\n\s*\}',
                    'message': 'Empty block detected',
                    'severity': 'warning',
                    'languages': ['javascript', 'cpp']
                }
            ],
            'runtime_errors': [
                {
                    'pattern': r'\w+\[len\(\w+\)\]',
                    'message': 'Index out of bounds - array indices go from 0 to len(array)-1',
                    'severity': 'critical',
                    'languages': ['python']
                },
                {
                    'pattern': r'\w+\[.*\.length\]',
                    'message': 'Index out of bounds - array indices go from 0 to length-1',
                    'severity': 'critical',
                    'languages': ['javascript', 'cpp']
                },
                {
                    'pattern': r'division by zero|/ 0',
                    'message': 'Division by zero error',
                    'severity': 'critical',
                    'languages': ['python', 'javascript', 'cpp']
                }
            ],
            'logic_errors': [
                {
                    'pattern': r'if\s+x\s*=\s*y',
                    'message': 'Assignment in conditional - should be == for comparison',
                    'severity': 'warning',
                    'languages': ['python', 'javascript', 'cpp']
                },
                {
                    'pattern': r'while\s+True\s*:\s*\n\s*(?!.*break)',
                    'message': 'Infinite loop - no break statement found',
                    'severity': 'warning',
                    'languages': ['python', 'javascript', 'cpp']
                },
                {
                    'pattern': r'for\s+i\s+in\s+range\s*\(\s*len\s*\(\s*arr\s*\)\s*\):\s*\n.*arr\[i\]',
                    'message': 'Potential index out of bounds in loop',
                    'severity': 'warning',
                    'languages': ['python']
                }
            ],
            'performance_issues': [
                {
                    'pattern': r'for\s+.*\s*in\s+.*:\s*for\s+.*\s*in\s+.*',
                    'message': 'Nested loops detected - O(n²) complexity',
                    'severity': 'info',
                    'languages': ['python', 'javascript', 'cpp']
                },
                {
                    'pattern': r'\.append\s*\(\s*\)\s*inside\s+loop',
                    'message': 'Inefficient list appending in loop',
                    'severity': 'info',
                    'languages': ['python']
                }
            ],
            'security_issues': [
                {
                    'pattern': r'eval\s*\(',
                    'message': 'Use of eval() function - potential security risk',
                    'severity': 'critical',
                    'languages': ['python', 'javascript']
                },
                {
                    'pattern': r'exec\s*\(',
                    'message': 'Use of exec() function - potential security risk',
                    'severity': 'critical',
                    'languages': ['python']
                },
                {
                    'pattern': r'system\s*\(',
                    'message': 'Use of system() function - potential security risk',
                    'severity': 'warning',
                    'languages': ['cpp']
                }
            ],
            'code_quality': [
                {
                    'pattern': r'print\s*\(',
                    'message': 'Debug print statement found',
                    'severity': 'info',
                    'languages': ['python']
                },
                {
                    'pattern': r'console\.log',
                    'message': 'Debug console.log statement found',
                    'severity': 'info',
                    'languages': ['javascript']
                },
                {
                    'pattern': r'cout\s*<<',
                    'message': 'Debug cout statement found',
                    'severity': 'info',
                    'languages': ['cpp']
                }
            ]
        }
    
    def detect(self, code: str, structure: Dict[str, Any], rules: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
        """Detect bugs and issues in code"""
        
        try:
            bugs = []
            
            # Detect bugs using built-in patterns
            pattern_bugs = self._detect_with_patterns(code, language)
            bugs.extend(pattern_bugs)
            
            # Detect bugs using custom rules
            rule_bugs = self._detect_with_rules(code, structure, rules, language)
            bugs.extend(rule_bugs)
            
            # Detect algorithm-specific bugs
            algorithm_bugs = self._detect_algorithm_bugs(code, structure, language)
            bugs.extend(algorithm_bugs)
            
            # Remove duplicates and sort by severity
            bugs = self._deduplicate_bugs(bugs)
            bugs = self._sort_bugs_by_severity(bugs)
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting bugs: {str(e)}")
            return []
    
    def _detect_with_patterns(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect bugs using predefined patterns"""
        
        try:
            bugs = []
            lines = code.split('\n')
            
            for category, patterns in self.bug_patterns.items():
                for pattern_info in patterns:
                    # Check if pattern applies to current language
                    if 'languages' in pattern_info and language not in pattern_info['languages']:
                        continue
                    
                    pattern = pattern_info['pattern']
                    
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            bugs.append({
                                'id': f"{category}_{len(bugs)}",
                                'category': category,
                                'title': pattern_info['message'],
                                'description': pattern_info['message'],
                                'severity': pattern_info['severity'],
                                'line': line_num,
                                'code_snippet': line.strip(),
                                'pattern': pattern,
                                'suggestion': self._get_suggestion_for_pattern(pattern_info)
                            })
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting with patterns: {str(e)}")
            return []
    
    def _detect_with_rules(self, code: str, structure: Dict[str, Any], rules: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
        """Detect bugs using custom rules"""
        
        try:
            bugs = []
            
            for rule in rules:
                pattern = rule.get('pattern', '')
                if not pattern:
                    continue
                
                matches = list(re.finditer(pattern, code, re.MULTILINE | re.IGNORECASE))
                
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    line_content = code.split('\n')[line_num - 1]
                    
                    bugs.append({
                        'id': rule.get('id', f"rule_{len(bugs)}"),
                        'category': 'rule_violation',
                        'title': rule.get('name', 'Rule Violation'),
                        'description': rule.get('description', ''),
                        'severity': rule.get('severity', 'warning'),
                        'line': line_num,
                        'code_snippet': line_content.strip(),
                        'pattern': pattern,
                        'suggestion': rule.get('suggestion', 'Review and fix the identified issue')
                    })
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting with rules: {str(e)}")
            return []
    
    def _detect_algorithm_bugs(self, code: str, structure: Dict[str, Any], language: str) -> List[Dict[str, Any]]:
        """Detect algorithm-specific bugs"""
        
        try:
            bugs = []
            
            # Detect binary search bugs
            if self._is_binary_search(code):
                binary_search_bugs = self._detect_binary_search_bugs(code)
                bugs.extend(binary_search_bugs)
            
            # Detect sorting algorithm bugs
            sorting_type = self._detect_sorting_algorithm(code)
            if sorting_type:
                sorting_bugs = self._detect_sorting_bugs(code, sorting_type)
                bugs.extend(sorting_bugs)
            
            # Detect graph algorithm bugs
            graph_type = self._detect_graph_algorithm(code)
            if graph_type:
                graph_bugs = self._detect_graph_bugs(code, graph_type)
                bugs.extend(graph_bugs)
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting algorithm bugs: {str(e)}")
            return []
    
    def _is_binary_search(self, code: str) -> bool:
        """Check if code implements binary search"""
        
        binary_search_indicators = [
            r'binary_search',
            r'left\s*=\s*0',
            r'right\s*=\s*len',
            r'mid\s*=',
            r'while\s+left\s*<=?\s*right'
        ]
        
        matches = 0
        for indicator in binary_search_indicators:
            if re.search(indicator, code, re.IGNORECASE):
                matches += 1
        
        return matches >= 3  # At least 3 indicators to consider it binary search
    
    def _detect_binary_search_bugs(self, code: str) -> List[Dict[str, Any]]:
        """Detect binary search specific bugs"""
        
        try:
            bugs = []
            lines = code.split('\n')
            
            # Check for overflow in mid calculation
            overflow_pattern = r'mid\s*=\s*\(\s*left\s*\+\s*right\s*\)\s*/\s*2'
            for line_num, line in enumerate(lines, 1):
                if re.search(overflow_pattern, line):
                    bugs.append({
                        'id': f'binary_search_overflow_{len(bugs)}',
                        'category': 'algorithm_bug',
                        'title': 'Binary Search Overflow Risk',
                        'description': 'Integer overflow may occur in mid calculation with large arrays',
                        'severity': 'warning',
                        'line': line_num,
                        'code_snippet': line.strip(),
                        'pattern': overflow_pattern,
                        'suggestion': 'Use mid = left + (right - left) // 2 to prevent overflow'
                    })
            
            # Check for incorrect loop condition
            loop_pattern = r'while\s+left\s*<\s*right'
            for line_num, line in enumerate(lines, 1):
                if re.search(loop_pattern, line):
                    bugs.append({
                        'id': f'binary_search_loop_{len(bugs)}',
                        'category': 'algorithm_bug',
                        'title': 'Binary Search Loop Condition',
                        'description': 'Loop condition should be <= for complete search coverage',
                        'severity': 'warning',
                        'line': line_num,
                        'code_snippet': line.strip(),
                        'pattern': loop_pattern,
                        'suggestion': 'Change to while left <= right to include all elements'
                    })
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting binary search bugs: {str(e)}")
            return []
    
    def _detect_sorting_algorithm(self, code: str) -> str:
        """Detect type of sorting algorithm"""
        
        if re.search(r'bubble_sort', code, re.IGNORECASE) or re.search(r'swap.*adjacent', code, re.IGNORECASE):
            return 'bubble_sort'
        elif re.search(r'selection_sort', code, re.IGNORECASE) or re.search(r'min_idx', code, re.IGNORECASE):
            return 'selection_sort'
        elif re.search(r'insertion_sort', code, re.IGNORECASE) or re.search(r'key\s*=', code, re.IGNORECASE):
            return 'insertion_sort'
        elif re.search(r'quick_sort', code, re.IGNORECASE) or re.search(r'pivot', code, re.IGNORECASE):
            return 'quick_sort'
        elif re.search(r'merge_sort', code, re.IGNORECASE) or re.search(r'merge\s*\(', code, re.IGNORECASE):
            return 'merge_sort'
        
        return None
    
    def _detect_sorting_bugs(self, code: str, sorting_type: str) -> List[Dict[str, Any]]:
        """Detect sorting algorithm specific bugs"""
        
        try:
            bugs = []
            
            if sorting_type == 'bubble_sort':
                # Check for missing optimization
                if not re.search(r'swapped|flag', code, re.IGNORECASE):
                    bugs.append({
                        'id': 'bubble_sort_optimization',
                        'category': 'performance',
                        'title': 'Missing Bubble Sort Optimization',
                        'description': 'Consider adding early termination when no swaps occur',
                        'severity': 'info',
                        'line': None,
                        'code_snippet': '',
                        'pattern': 'swapped_flag_missing',
                        'suggestion': 'Add a flag to detect if array is already sorted and break early'
                    })
            
            elif sorting_type == 'quick_sort':
                # Check for potential stack overflow
                if not re.search(r'random|pivot.*random', code, re.IGNORECASE):
                    bugs.append({
                        'id': 'quick_sort_pivot',
                        'category': 'performance',
                        'title': 'Quick Sort Pivot Selection',
                        'description': 'Consider using random pivot selection to avoid worst-case performance',
                        'severity': 'info',
                        'line': None,
                        'code_snippet': '',
                        'pattern': 'deterministic_pivot',
                        'suggestion': 'Use random pivot selection or median-of-three for better average performance'
                    })
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting sorting bugs: {str(e)}")
            return []
    
    def _detect_graph_algorithm(self, code: str) -> str:
        """Detect type of graph algorithm"""
        
        if re.search(r'dfs|depth.*search', code, re.IGNORECASE):
            return 'dfs'
        elif re.search(r'bfs|breadth.*search', code, re.IGNORECASE):
            return 'bfs'
        elif re.search(r'dijkstra|shortest.*path', code, re.IGNORECASE):
            return 'dijkstra'
        
        return None
    
    def _detect_graph_bugs(self, code: str, graph_type: str) -> List[Dict[str, Any]]:
        """Detect graph algorithm specific bugs"""
        
        try:
            bugs = []
            
            if graph_type == 'dfs':
                # Check for missing visited set
                if not re.search(r'visited', code, re.IGNORECASE):
                    bugs.append({
                        'id': 'dfs_visited_missing',
                        'category': 'algorithm_bug',
                        'title': 'Missing Visited Tracking in DFS',
                        'description': 'DFS should track visited nodes to avoid infinite recursion',
                        'severity': 'warning',
                        'line': None,
                        'code_snippet': '',
                        'pattern': 'visited_missing',
                        'suggestion': 'Add a visited set or array to track visited nodes'
                    })
            
            elif graph_type == 'bfs':
                # Check for missing queue
                if not re.search(r'queue|deque', code, re.IGNORECASE):
                    bugs.append({
                        'id': 'bfs_queue_missing',
                        'category': 'algorithm_bug',
                        'title': 'Missing Queue in BFS',
                        'description': 'BFS requires a queue for level-order traversal',
                        'severity': 'error',
                        'line': None,
                        'code_snippet': '',
                        'pattern': 'queue_missing',
                        'suggestion': 'Use a queue (deque in Python) for BFS implementation'
                    })
            
            return bugs
            
        except Exception as e:
            logger.error(f"Error detecting graph bugs: {str(e)}")
            return []
    
    def _get_suggestion_for_pattern(self, pattern_info: Dict[str, Any]) -> str:
        """Get suggestion for a pattern-based bug"""
        
        suggestions = {
            'Index out of bounds': 'Check array bounds before accessing elements',
            'Division by zero': 'Add zero check before division operations',
            'Assignment in conditional': 'Use == for comparison instead of =',
            'Infinite loop': 'Add break condition or modify loop condition',
            'Use of eval()': 'Consider using safer alternatives like ast.literal_eval',
            'Debug print': 'Remove debug statements before production'
        }
        
        message = pattern_info.get('message', '')
        for key, suggestion in suggestions.items():
            if key in message:
                return suggestion
        
        return 'Review and fix the identified issue'
    
    def _deduplicate_bugs(self, bugs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate bugs"""
        
        try:
            seen = set()
            unique_bugs = []
            
            for bug in bugs:
                # Create a unique key based on line and pattern
                key = (bug.get('line'), bug.get('pattern'), bug.get('title'))
                if key not in seen:
                    seen.add(key)
                    unique_bugs.append(bug)
            
            return unique_bugs
            
        except Exception as e:
            logger.error(f"Error deduplicating bugs: {str(e)}")
            return bugs
    
    def _sort_bugs_by_severity(self, bugs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort bugs by severity (critical > error > warning > info)"""
        
        try:
            severity_order = {'critical': 0, 'error': 1, 'warning': 2, 'info': 3}
            
            return sorted(bugs, key=lambda bug: severity_order.get(bug.get('severity', 'info'), 3))
            
        except Exception as e:
            logger.error(f"Error sorting bugs by severity: {str(e)}")
            return bugs
