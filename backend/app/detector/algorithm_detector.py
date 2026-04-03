import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class AlgorithmDetector:
    """Detect algorithms from code structure and patterns"""
    
    def __init__(self):
        self.algorithm_patterns = {
            'binary_search': {
                'keywords': ['mid', 'left', 'right', 'binary', 'search'],
                'patterns': [
                    r'while\s+.*<=.*',
                    r'mid\s*=\s*.*[+\-].*/\s*2',
                    r'if\s+.*\[.*\]\s*[<>=!]+\s*',
                    r'left\s*=\s*mid\s*[+\-]\s*1',
                    r'right\s*=\s*mid\s*[+\-]\s*1'
                ],
                'structure': {
                    'has_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'linear_search': {
                'keywords': ['search', 'find', 'linear'],
                'patterns': [
                    r'for\s+.*in\s*.*:',
                    r'if\s+.*==.*',
                    r'return\s+.*'
                ],
                'structure': {
                    'has_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'bubble_sort': {
                'keywords': ['bubble', 'sort', 'swap'],
                'patterns': [
                    r'for\s+.*for\s+.*',
                    r'if\s+.*[<>].*',
                    r'swap|.*=.*;.*=.*;.*=.*',
                    r'arr\[.*\].*=.*arr\[.*\]'
                ],
                'structure': {
                    'has_nested_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'selection_sort': {
                'keywords': ['selection', 'sort', 'min', 'index'],
                'patterns': [
                    r'for\s+.*for\s+.*',
                    r'min_index\s*=',
                    r'if\s+.*\[.*\]\s*<\s*.*\[.*\]',
                    r'swap'
                ],
                'structure': {
                    'has_nested_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'insertion_sort': {
                'keywords': ['insertion', 'sort', 'key'],
                'patterns': [
                    r'for\s+.*range\s*\(.*,\s*len.*\)',
                    r'key\s*=',
                    r'while\s+.*>\s*0',
                    r'arr\[.*\]\s*=\s*arr\[.*\s*-\s*1\]'
                ],
                'structure': {
                    'has_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'quick_sort': {
                'keywords': ['quick', 'sort', 'partition', 'pivot'],
                'patterns': [
                    r'pivot\s*=',
                    r'partition',
                    r'quick_sort\s*\(',
                    r'if\s+.*<\s*.*'
                ],
                'structure': {
                    'has_recursion': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'merge_sort': {
                'keywords': ['merge', 'sort', 'merge_sort'],
                'patterns': [
                    r'merge_sort\s*\(',
                    r'merge\s*\(',
                    r'left.*right',
                    r'if\s+.*<\s*.*'
                ],
                'structure': {
                    'has_recursion': True,
                    'has_conditionals': True,
                    'min_functions': 2
                }
            },
            'dfs': {
                'keywords': ['dfs', 'depth', 'search', 'stack', 'visited'],
                'patterns': [
                    r'dfs\s*\(',
                    r'visited\s*=',
                    r'stack\s*=',
                    r'for\s+.*in\s*.*'
                ],
                'structure': {
                    'has_recursion': True,
                    'has_loops': True,
                    'min_functions': 1
                }
            },
            'bfs': {
                'keywords': ['bfs', 'breadth', 'search', 'queue', 'visited'],
                'patterns': [
                    r'bfs\s*\(',
                    r'queue\s*=',
                    r'visited\s*=',
                    r'while\s+queue'
                ],
                'structure': {
                    'has_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            },
            'dijkstra': {
                'keywords': ['dijkstra', 'shortest', 'path', 'distance', 'priority'],
                'patterns': [
                    r'dijkstra\s*\(',
                    r'distance\s*=',
                    r'priority_queue|heap',
                    r'while\s+.*'
                ],
                'structure': {
                    'has_loops': True,
                    'has_conditionals': True,
                    'min_functions': 1
                }
            }
        }
        
        self.algorithm_info = {
            'binary_search': {
                'name': 'Binary Search',
                'description': 'Efficient search algorithm that works on sorted arrays by repeatedly dividing the search interval in half.',
                'timeComplexity': 'O(log n)',
                'spaceComplexity': 'O(1)',
                'bestCase': 'O(1) - element found at middle',
                'worstCase': 'O(log n) - element not found',
                'useCases': ['Searching in sorted arrays', 'Finding insertion points', 'Binary search trees']
            },
            'linear_search': {
                'name': 'Linear Search',
                'description': 'Simple search algorithm that checks each element in sequence until the target is found.',
                'timeComplexity': 'O(n)',
                'spaceComplexity': 'O(1)',
                'bestCase': 'O(1) - element found at first position',
                'worstCase': 'O(n) - element not found or at last position',
                'useCases': ['Small datasets', 'Unsorted data', 'Simple implementations']
            },
            'bubble_sort': {
                'name': 'Bubble Sort',
                'description': 'Simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in wrong order.',
                'timeComplexity': 'O(n²)',
                'spaceComplexity': 'O(1)',
                'bestCase': 'O(n) - already sorted',
                'worstCase': 'O(n²) - reverse sorted',
                'useCases': ['Educational purposes', 'Small datasets', 'Nearly sorted data']
            },
            'selection_sort': {
                'name': 'Selection Sort',
                'description': 'Sorting algorithm that divides the input into sorted and unsorted regions, repeatedly selecting the smallest element from unsorted region.',
                'timeComplexity': 'O(n²)',
                'spaceComplexity': 'O(1)',
                'bestCase': 'O(n²)',
                'worstCase': 'O(n²)',
                'useCases': ['Small datasets', 'Memory constraints', 'Educational purposes']
            },
            'insertion_sort': {
                'name': 'Insertion Sort',
                'description': 'Simple sorting algorithm that builds the final sorted array one item at a time by inserting each element into its proper position.',
                'timeComplexity': 'O(n²)',
                'spaceComplexity': 'O(1)',
                'bestCase': 'O(n) - already sorted',
                'worstCase': 'O(n²) - reverse sorted',
                'useCases': ['Small datasets', 'Nearly sorted data', 'Online algorithms']
            },
            'quick_sort': {
                'name': 'Quick Sort',
                'description': 'Efficient divide-and-conquer sorting algorithm that picks a pivot element and partitions the array around it.',
                'timeComplexity': 'O(n log n) average, O(n²) worst',
                'spaceComplexity': 'O(log n)',
                'bestCase': 'O(n log n)',
                'worstCase': 'O(n²)',
                'useCases': ['Large datasets', 'General purpose sorting', 'In-place sorting']
            },
            'merge_sort': {
                'name': 'Merge Sort',
                'description': 'Divide-and-conquer sorting algorithm that divides the array into halves, sorts them, and then merges them back together.',
                'timeComplexity': 'O(n log n)',
                'spaceComplexity': 'O(n)',
                'bestCase': 'O(n log n)',
                'worstCase': 'O(n log n)',
                'useCases': ['Large datasets', 'Stable sorting required', 'External sorting']
            },
            'dfs': {
                'name': 'Depth-First Search',
                'description': 'Graph traversal algorithm that explores as far as possible along each branch before backtracking.',
                'timeComplexity': 'O(V + E)',
                'spaceComplexity': 'O(V)',
                'bestCase': 'O(V + E)',
                'worstCase': 'O(V + E)',
                'useCases': ['Graph traversal', 'Path finding', 'Topological sorting', 'Cycle detection']
            },
            'bfs': {
                'name': 'Breadth-First Search',
                'description': 'Graph traversal algorithm that explores all neighbors at the present depth before moving on to nodes at the next depth level.',
                'timeComplexity': 'O(V + E)',
                'spaceComplexity': 'O(V)',
                'bestCase': 'O(V + E)',
                'worstCase': 'O(V + E)',
                'useCases': ['Shortest path in unweighted graphs', 'Level-order traversal', 'Connected components']
            },
            'dijkstra': {
                'name': 'Dijkstra\'s Algorithm',
                'description': 'Algorithm for finding the shortest paths between nodes in a weighted graph.',
                'timeComplexity': 'O((V + E) log V)',
                'spaceComplexity': 'O(V)',
                'bestCase': 'O((V + E) log V)',
                'worstCase': 'O((V + E) log V)',
                'useCases': ['Shortest path in weighted graphs', 'Network routing', 'GPS navigation']
            }
        }
    
    def detect(self, structure: Dict[str, Any], language: str) -> Optional[str]:
        """Detect the algorithm based on code structure"""
        
        try:
            scores = {}
            
            for algorithm, pattern_info in self.algorithm_patterns.items():
                score = self.calculate_algorithm_score(structure, pattern_info, language)
                scores[algorithm] = score
            
            # Return the algorithm with the highest score if it meets minimum threshold
            if scores:
                best_algorithm = max(scores, key=scores.get)
                if scores[best_algorithm] > 0.3:  # Minimum confidence threshold
                    return best_algorithm
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting algorithm: {str(e)}")
            return None
    
    def calculate_algorithm_score(self, structure: Dict[str, Any], pattern_info: Dict[str, Any], language: str) -> float:
        """Calculate confidence score for algorithm detection"""
        
        try:
            score = 0.0
            total_weight = 0.0
            
            # Check keyword matches
            if 'functions' in structure:
                all_code = ' '.join([func.get('body', '') for func in structure['functions']])
                keyword_matches = 0
                for keyword in pattern_info.get('keywords', []):
                    if keyword.lower() in all_code.lower():
                        keyword_matches += 1
                
                if pattern_info['keywords']:
                    score += (keyword_matches / len(pattern_info['keywords'])) * 0.3
                total_weight += 0.3
            
            # Check pattern matches
            if 'functions' in structure:
                all_code = ' '.join([func.get('body', '') for func in structure['functions']])
                pattern_matches = 0
                for pattern in pattern_info.get('patterns', []):
                    if re.search(pattern, all_code, re.IGNORECASE):
                        pattern_matches += 1
                
                if pattern_info['patterns']:
                    score += (pattern_matches / len(pattern_info['patterns'])) * 0.4
                total_weight += 0.4
            
            # Check structural requirements
            structure_requirements = pattern_info.get('structure', {})
            structure_score = 0
            structure_checks = 0
            
            if 'has_loops' in structure_requirements:
                structure_checks += 1
                if structure_requirements['has_loops'] and len(structure.get('loops', [])) > 0:
                    structure_score += 1
                elif not structure_requirements['has_loops'] and len(structure.get('loops', [])) == 0:
                    structure_score += 1
            
            if 'has_nested_loops' in structure_requirements:
                structure_checks += 1
                nested_loops = any(loop.get('nested', False) for loop in structure.get('loops', []))
                if structure_requirements['has_nested_loops'] and nested_loops:
                    structure_score += 1
                elif not structure_requirements['has_nested_loops'] and not nested_loops:
                    structure_score += 1
            
            if 'has_conditionals' in structure_requirements:
                structure_checks += 1
                if structure_requirements['has_conditionals'] and len(structure.get('conditionals', [])) > 0:
                    structure_score += 1
                elif not structure_requirements['has_conditionals'] and len(structure.get('conditionals', [])) == 0:
                    structure_score += 1
            
            if 'has_recursion' in structure_requirements:
                structure_checks += 1
                recursive_calls = structure.get('complexity_indicators', {}).get('recursive_calls', 0)
                if structure_requirements['has_recursion'] and recursive_calls > 0:
                    structure_score += 1
                elif not structure_requirements['has_recursion'] and recursive_calls == 0:
                    structure_score += 1
            
            if 'min_functions' in structure_requirements:
                structure_checks += 1
                if len(structure.get('functions', [])) >= structure_requirements['min_functions']:
                    structure_score += 1
            
            if structure_checks > 0:
                score += (structure_score / structure_checks) * 0.3
                total_weight += 0.3
            
            # Normalize score
            if total_weight > 0:
                return score / total_weight
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating algorithm score: {str(e)}")
            return 0.0
    
    def get_algorithm_info(self, algorithm: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a detected algorithm"""
        
        try:
            return self.algorithm_info.get(algorithm)
            
        except Exception as e:
            logger.error(f"Error getting algorithm info: {str(e)}")
            return None
    
    def get_all_supported_algorithms(self) -> List[str]:
        """Get list of all supported algorithms"""
        
        try:
            return list(self.algorithm_patterns.keys())
            
        except Exception as e:
            logger.error(f"Error getting supported algorithms: {str(e)}")
            return []
