import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BinarySearchVisualizer:
    """Generate visualization data for binary search algorithm"""
    
    def __init__(self):
        self.visualization_type = "binary_search"
    
    def visualize(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visualization data for binary search"""
        
        try:
            # Extract array and target from the code structure
            array_data = self._extract_array_data(structure)
            if not array_data:
                return self._generate_default_visualization()
            
            visualization_data = {
                'type': self.visualization_type,
                'title': 'Binary Search Visualization',
                'description': 'Step-by-step visualization of binary search algorithm',
                'array': array_data['array'],
                'target': array_data['target'],
                'steps': self._generate_search_steps(array_data['array'], array_data['target']),
                'metadata': {
                    'total_steps': 0,
                    'comparisons': 0,
                    'found': False,
                    'final_index': -1
                }
            }
            
            # Update metadata
            if visualization_data['steps']:
                visualization_data['metadata']['total_steps'] = len(visualization_data['steps'])
                visualization_data['metadata']['comparisons'] = len(visualization_data['steps'])
                
                # Check if target was found
                final_step = visualization_data['steps'][-1]
                visualization_data['metadata']['found'] = final_step.get('found', False)
                if visualization_data['metadata']['found']:
                    visualization_data['metadata']['final_index'] = final_step.get('mid', -1)
            
            return visualization_data
            
        except Exception as e:
            logger.error(f"Error generating binary search visualization: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _extract_array_data(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Extract array and target data from code structure"""
        
        try:
            # Try to extract from function bodies
            functions = structure.get('functions', [])
            
            for func in functions:
                body = func.get('body', '')
                
                # Look for array initialization
                array_match = self._find_array_in_code(body)
                if array_match:
                    # Look for target value
                    target_match = self._find_target_in_code(body)
                    
                    return {
                        'array': array_match,
                        'target': target_match
                    }
            
            # If no function data, try to extract from overall code
            # This is a fallback - in practice, you'd need more sophisticated parsing
            return {
                'array': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
                'target': 7
            }
            
        except Exception as e:
            logger.error(f"Error extracting array data: {str(e)}")
            return {}
    
    def _find_array_in_code(self, code: str) -> List[int]:
        """Find array data in code"""
        
        try:
            import re
            
            # Look for common array patterns
            patterns = [
                r'array\s*=\s*\[([^\]]+)\]',
                r'arr\s*=\s*\[([^\]]+)\]',
                r'nums\s*=\s*\[([^\]]+)\]',
                r'list\s*=\s*\[([^\]]+)\]'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, code)
                if match:
                    array_str = match.group(1)
                    # Parse the array elements
                    elements = []
                    for elem in array_str.split(','):
                        elem = elem.strip()
                        if elem.isdigit():
                            elements.append(int(elem))
                        elif elem.replace('-', '').isdigit():
                            elements.append(int(elem))
                    return elements if elements else [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
            
            # Default array if none found
            return [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
            
        except Exception as e:
            logger.error(f"Error finding array in code: {str(e)}")
            return [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    def _find_target_in_code(self, code: str) -> int:
        """Find target value in code"""
        
        try:
            import re
            
            # Look for target variable patterns
            patterns = [
                r'target\s*=\s*(\d+)',
                r'key\s*=\s*(\d+)',
                r'x\s*=\s*(\d+)',
                r'search\s*=\s*(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, code)
                if match:
                    return int(match.group(1))
            
            # Default target if none found
            return 7
            
        except Exception as e:
            logger.error(f"Error finding target in code: {str(e)}")
            return 7
    
    def _generate_search_steps(self, array: List[int], target: int) -> List[Dict[str, Any]]:
        """Generate step-by-step search visualization"""
        
        try:
            steps = []
            left = 0
            right = len(array) - 1
            
            while left <= right:
                mid = (left + right) // 2
                mid_value = array[mid]
                
                step = {
                    'step': len(steps) + 1,
                    'left': left,
                    'right': right,
                    'mid': mid,
                    'mid_value': mid_value,
                    'target': target,
                    'found': mid_value == target,
                    'comparison': f"Compare array[{mid}] = {mid_value} with target {target}",
                    'action': '',
                    'array_state': self._create_array_state(array, left, right, mid, target)
                }
                
                if mid_value == target:
                    step['action'] = f"Target {target} found at index {mid}!"
                    steps.append(step)
                    break
                elif mid_value < target:
                    step['action'] = f"{mid_value} < {target}, search right half"
                    left = mid + 1
                else:
                    step['action'] = f"{mid_value} > {target}, search left half"
                    right = mid - 1
                
                steps.append(step)
            
            # If target not found
            if not steps or not steps[-1]['found']:
                steps.append({
                    'step': len(steps) + 1,
                    'left': left,
                    'right': right,
                    'mid': -1,
                    'mid_value': None,
                    'target': target,
                    'found': False,
                    'comparison': "Search complete",
                    'action': f"Target {target} not found in array",
                    'array_state': self._create_array_state(array, left, right, -1, target)
                })
            
            return steps
            
        except Exception as e:
            logger.error(f"Error generating search steps: {str(e)}")
            return []
    
    def _create_array_state(self, array: List[int], left: int, right: int, mid: int, target: int) -> List[Dict[str, Any]]:
        """Create visual representation of array state"""
        
        try:
            array_state = []
            
            for i, value in enumerate(array):
                state = {
                    'index': i,
                    'value': value,
                    'status': 'normal'
                }
                
                # Determine the status of each element
                if i == mid:
                    state['status'] = 'current'
                elif i < left or i > right:
                    state['status'] = 'eliminated'
                elif left <= i <= right:
                    state['status'] = 'search_range'
                
                if value == target:
                    state['is_target'] = True
                
                array_state.append(state)
            
            return array_state
            
        except Exception as e:
            logger.error(f"Error creating array state: {str(e)}")
            return []
    
    def _generate_default_visualization(self) -> Dict[str, Any]:
        """Generate default visualization when no data is available"""
        
        return {
            'type': self.visualization_type,
            'title': 'Binary Search Visualization',
            'description': 'Step-by-step visualization of binary search algorithm',
            'array': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            'target': 7,
            'steps': self._generate_search_steps([1, 3, 5, 7, 9, 11, 13, 15, 17, 19], 7),
            'metadata': {
                'total_steps': 0,
                'comparisons': 0,
                'found': False,
                'final_index': -1,
                'note': 'Using default example data'
            }
        }
    
    def _generate_error_visualization(self, error_message: str) -> Dict[str, Any]:
        """Generate error visualization"""
        
        return {
            'type': self.visualization_type,
            'title': 'Binary Search Visualization',
            'description': 'Error generating visualization',
            'error': error_message,
            'array': [],
            'target': None,
            'steps': [],
            'metadata': {
                'error': True,
                'message': error_message
            }
        }
    
    def get_complexity_info(self) -> Dict[str, Any]:
        """Get complexity information for binary search"""
        
        return {
            'time_complexity': 'O(log n)',
            'space_complexity': 'O(1)',
            'best_case': 'O(1) - target found at middle',
            'worst_case': 'O(log n) - target not found or at ends',
            'description': 'Binary search works on sorted arrays by repeatedly dividing the search interval in half.'
        }
    
    def generate_step_description(self, step: Dict[str, Any]) -> str:
        """Generate human-readable description for a step"""
        
        try:
            if step['found']:
                return f"Step {step['step']}: Target {step['target']} found at index {step['mid']}!"
            
            if step['mid'] == -1:
                return f"Step {step['step']}: Search complete - target {step['target']} not found"
            
            return f"Step {step['step']}: {step['comparison']}. {step['action']}"
            
        except Exception as e:
            logger.error(f"Error generating step description: {str(e)}")
            return f"Step {step.get('step', '?')}: Binary search step"
