import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TestCaseRunner:
    """Manage and run test cases for code validation"""
    
    def __init__(self, test_cases_dir: str = "test_cases"):
        self.test_cases_dir = Path(test_cases_dir)
        self.test_cases = {}
        self.load_test_cases()
    
    def load_test_cases(self):
        """Load test cases from JSON files"""
        
        try:
            # Load binary search test cases
            binary_search_file = self.test_cases_dir / "binary_search_tests.json"
            if binary_search_file.exists():
                with open(binary_search_file, 'r') as f:
                    self.test_cases['binary_search'] = json.load(f)
            
            # Load sorting test cases
            sorting_file = self.test_cases_dir / "sorting_tests.json"
            if sorting_file.exists():
                with open(sorting_file, 'r') as f:
                    self.test_cases['sorting'] = json.load(f)
            
            # Load graph test cases
            graph_file = self.test_cases_dir / "graph_tests.json"
            if graph_file.exists():
                with open(graph_file, 'r') as f:
                    self.test_cases['graph'] = json.load(f)
            
            logger.info(f"Loaded test cases for {len(self.test_cases)} algorithms")
            
        except Exception as e:
            logger.error(f"Error loading test cases: {str(e)}")
    
    def get_test_cases(self, algorithm: str) -> List[Dict[str, Any]]:
        """Get test cases for a specific algorithm"""
        
        try:
            return self.test_cases.get(algorithm, [])
            
        except Exception as e:
            logger.error(f"Error getting test cases for {algorithm}: {str(e)}")
            return []
    
    def run_algorithm_tests(self, algorithm: str, code_runner, code: str, language: str) -> Dict[str, Any]:
        """Run all test cases for a specific algorithm"""
        
        try:
            test_cases = self.get_test_cases(algorithm)
            
            if not test_cases:
                return {
                    'algorithm': algorithm,
                    'total_tests': 0,
                    'passed_tests': 0,
                    'failed_tests': 0,
                    'test_results': [],
                    'message': f'No test cases available for {algorithm}'
                }
            
            # Run test cases using code runner
            results = code_runner.run_test_cases(code, language, test_cases)
            results['algorithm'] = algorithm
            
            return results
            
        except Exception as e:
            logger.error(f"Error running algorithm tests: {str(e)}")
            return {
                'algorithm': algorithm,
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'test_results': [],
                'error': str(e)
            }
    
    def generate_test_cases(self, algorithm: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate test cases for an algorithm"""
        
        try:
            if algorithm == 'binary_search':
                return self._generate_binary_search_tests(parameters)
            elif algorithm in ['bubble_sort', 'selection_sort', 'insertion_sort', 'quick_sort', 'merge_sort']:
                return self._generate_sorting_tests(algorithm, parameters)
            elif algorithm in ['dfs', 'bfs']:
                return self._generate_graph_traversal_tests(algorithm, parameters)
            elif algorithm == 'dijkstra':
                return self._generate_dijkstra_tests(parameters)
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error generating test cases for {algorithm}: {str(e)}")
            return []
    
    def _generate_binary_search_tests(self, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate test cases for binary search"""
        
        try:
            test_cases = []
            
            # Basic test cases
            test_cases.extend([
                {
                    'description': 'Element found in middle',
                    'input': '5\n[1, 3, 5, 7, 9]\n',
                    'expected_output': '2'
                },
                {
                    'description': 'Element found at beginning',
                    'input': '1\n[1, 3, 5, 7, 9]\n',
                    'expected_output': '0'
                },
                {
                    'description': 'Element found at end',
                    'input': '9\n[1, 3, 5, 7, 9]\n',
                    'expected_output': '4'
                },
                {
                    'description': 'Element not found',
                    'input': '4\n[1, 3, 5, 7, 9]\n',
                    'expected_output': '-1'
                },
                {
                    'description': 'Empty array',
                    'input': '5\n[]\n',
                    'expected_output': '-1'
                },
                {
                    'description': 'Single element - found',
                    'input': '5\n[5]\n',
                    'expected_output': '0'
                },
                {
                    'description': 'Single element - not found',
                    'input': '3\n[5]\n',
                    'expected_output': '-1'
                }
            ])
            
            # Edge cases
            test_cases.extend([
                {
                    'description': 'Large array - element found',
                    'input': '500\n' + str(list(range(1, 1001, 2))) + '\n',
                    'expected_output': '249'
                },
                {
                    'description': 'Negative numbers',
                    'input': '-3\n[-9, -7, -5, -3, -1]\n',
                    'expected_output': '3'
                }
            ])
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Error generating binary search tests: {str(e)}")
            return []
    
    def _generate_sorting_tests(self, algorithm: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate test cases for sorting algorithms"""
        
        try:
            test_cases = []
            
            # Basic test cases
            test_cases.extend([
                {
                    'description': 'Already sorted array',
                    'input': '[1, 2, 3, 4, 5]\n',
                    'expected_output': '[1, 2, 3, 4, 5]'
                },
                {
                    'description': 'Reverse sorted array',
                    'input': '[5, 4, 3, 2, 1]\n',
                    'expected_output': '[1, 2, 3, 4, 5]'
                },
                {
                    'description': 'Random array',
                    'input': '[3, 1, 4, 1, 5, 9, 2, 6]\n',
                    'expected_output': '[1, 1, 2, 3, 4, 5, 6, 9]'
                },
                {
                    'description': 'Single element',
                    'input': '[42]\n',
                    'expected_output': '[42]'
                },
                {
                    'description': 'Empty array',
                    'input': '[]\n',
                    'expected_output': '[]'
                },
                {
                    'description': 'Array with duplicates',
                    'input': '[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\n',
                    'expected_output': '[1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]'
                }
            ])
            
            # Edge cases
            test_cases.extend([
                {
                    'description': 'All same elements',
                    'input': '[7, 7, 7, 7, 7]\n',
                    'expected_output': '[7, 7, 7, 7, 7]'
                },
                {
                    'description': 'Two elements - sorted',
                    'input': '[1, 2]\n',
                    'expected_output': '[1, 2]'
                },
                {
                    'description': 'Two elements - reverse',
                    'input': '[2, 1]\n',
                    'expected_output': '[1, 2]'
                }
            ])
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Error generating sorting tests: {str(e)}")
            return []
    
    def _generate_graph_traversal_tests(self, algorithm: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate test cases for graph traversal algorithms"""
        
        try:
            test_cases = []
            
            # Simple graph test cases
            test_cases.extend([
                {
                    'description': 'Simple connected graph',
                    'input': '4\n[[1, 2], [0, 3], [0, 3], [1, 2]]\n0\n',
                    'expected_output': '0 1 2 3' if algorithm == 'bfs' else '0 1 3 2'
                },
                {
                    'description': 'Disconnected graph',
                    'input': '4\n[[1], [0], [3], [2]]\n0\n',
                    'expected_output': '0 1'
                },
                {
                    'description': 'Single node',
                    'input': '1\n[[]]\n0\n',
                    'expected_output': '0'
                },
                {
                    'description': 'Linear graph',
                    'input': '5\n[[1], [0, 2], [1, 3], [2, 4], [3]]\n0\n',
                    'expected_output': '0 1 2 3 4'
                }
            ])
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Error generating graph traversal tests: {str(e)}")
            return []
    
    def _generate_dijkstra_tests(self, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate test cases for Dijkstra's algorithm"""
        
        try:
            test_cases = []
            
            # Basic graph test cases
            test_cases.extend([
                {
                    'description': 'Simple weighted graph',
                    'input': '4\n[[0, 1, 4, 0], [1, 0, 2, 5], [4, 2, 0, 1], [0, 5, 1, 0]]\n0\n',
                    'expected_output': '[0, 1, 3, 4]'
                },
                {
                    'description': 'Disconnected graph',
                    'input': '3\n[[0, 1, 0], [1, 0, 0], [0, 0, 0]]\n0\n',
                    'expected_output': '[0, 1, 999999]'
                }
            ])
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Error generating Dijkstra tests: {str(e)}")
            return []
    
    def validate_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single test case"""
        
        try:
            required_fields = ['description', 'input', 'expected_output']
            missing_fields = [field for field in required_fields if field not in test_case]
            
            if missing_fields:
                return {
                    'valid': False,
                    'error': f'Missing required fields: {missing_fields}'
                }
            
            # Check if input and expected_output are strings
            if not isinstance(test_case['input'], str) or not isinstance(test_case['expected_output'], str):
                return {
                    'valid': False,
                    'error': 'Input and expected_output must be strings'
                }
            
            return {'valid': True}
            
        except Exception as e:
            logger.error(f"Error validating test case: {str(e)}")
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }
    
    def save_test_cases(self, algorithm: str, test_cases: List[Dict[str, Any]]):
        """Save test cases to file"""
        
        try:
            filename = f"{algorithm}_tests.json"
            filepath = self.test_cases_dir / filename
            
            # Validate all test cases
            for test_case in test_cases:
                validation = self.validate_test_case(test_case)
                if not validation['valid']:
                    logger.warning(f"Invalid test case: {validation['error']}")
                    continue
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(test_cases, f, indent=2)
            
            # Update in-memory test cases
            self.test_cases[algorithm] = test_cases
            
            logger.info(f"Saved {len(test_cases)} test cases for {algorithm}")
            
        except Exception as e:
            logger.error(f"Error saving test cases: {str(e)}")
    
    def get_test_case_statistics(self, algorithm: str) -> Dict[str, Any]:
        """Get statistics about test cases for an algorithm"""
        
        try:
            test_cases = self.get_test_cases(algorithm)
            
            if not test_cases:
                return {
                    'algorithm': algorithm,
                    'total_test_cases': 0,
                    'categories': {},
                    'complexity_levels': {}
                }
            
            # Analyze test cases
            categories = {}
            complexity_levels = {'basic': 0, 'intermediate': 0, 'advanced': 0}
            
            for test_case in test_cases:
                # Categorize by description keywords
                description = test_case.get('description', '').lower()
                
                if 'basic' in description or 'simple' in description:
                    complexity_levels['basic'] += 1
                elif 'advanced' in description or 'complex' in description or 'large' in description:
                    complexity_levels['advanced'] += 1
                else:
                    complexity_levels['intermediate'] += 1
                
                # Extract categories
                if 'edge' in description:
                    categories['edge_cases'] = categories.get('edge_cases', 0) + 1
                elif 'empty' in description:
                    categories['empty_cases'] = categories.get('empty_cases', 0) + 1
                elif 'single' in description:
                    categories['single_element'] = categories.get('single_element', 0) + 1
                else:
                    categories['general'] = categories.get('general', 0) + 1
            
            return {
                'algorithm': algorithm,
                'total_test_cases': len(test_cases),
                'categories': categories,
                'complexity_levels': complexity_levels
            }
            
        except Exception as e:
            logger.error(f"Error getting test case statistics: {str(e)}")
            return {}
    
    def compare_outputs(self, actual: str, expected: str, tolerance: float = 0.0) -> bool:
        """Compare actual and expected outputs with optional tolerance"""
        
        try:
            # Strip whitespace and normalize line endings
            actual_clean = actual.strip().replace('\r\n', '\n')
            expected_clean = expected.strip().replace('\r\n', '\n')
            
            # If tolerance is 0, exact match
            if tolerance == 0.0:
                return actual_clean == expected_clean
            
            # For numeric outputs, allow tolerance
            try:
                actual_nums = [float(x) for x in actual_clean.split()]
                expected_nums = [float(x) for x in expected_clean.split()]
                
                if len(actual_nums) != len(expected_nums):
                    return False
                
                for a, e in zip(actual_nums, expected_nums):
                    if abs(a - e) > tolerance:
                        return False
                
                return True
                
            except ValueError:
                # If not numeric, fall back to exact comparison
                return actual_clean == expected_clean
                
        except Exception as e:
            logger.error(f"Error comparing outputs: {str(e)}")
            return False
