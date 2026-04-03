import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SortingVisualizer:
    """Generate visualization data for sorting algorithms"""
    
    def __init__(self):
        self.supported_algorithms = ['bubble_sort', 'selection_sort', 'insertion_sort', 'quick_sort', 'merge_sort']
    
    def visualize(self, structure: Dict[str, Any], algorithm_type: str) -> Dict[str, Any]:
        """Generate visualization data for sorting algorithms"""
        
        try:
            if algorithm_type not in self.supported_algorithms:
                return self._generate_error_visualization(f"Unsupported algorithm: {algorithm_type}")
            
            # Extract array data
            array_data = self._extract_array_data(structure)
            if not array_data:
                array_data = self._get_default_array()
            
            # Generate visualization based on algorithm type
            if algorithm_type == 'bubble_sort':
                return self._visualize_bubble_sort(array_data)
            elif algorithm_type == 'selection_sort':
                return self._visualize_selection_sort(array_data)
            elif algorithm_type == 'insertion_sort':
                return self._visualize_insertion_sort(array_data)
            elif algorithm_type == 'quick_sort':
                return self._visualize_quick_sort(array_data)
            elif algorithm_type == 'merge_sort':
                return self._visualize_merge_sort(array_data)
            else:
                return self._generate_error_visualization(f"Algorithm {algorithm_type} not implemented")
                
        except Exception as e:
            logger.error(f"Error generating sorting visualization: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _extract_array_data(self, structure: Dict[str, Any]) -> List[int]:
        """Extract array data from code structure"""
        
        try:
            functions = structure.get('functions', [])
            
            for func in functions:
                body = func.get('body', '')
                array_match = self._find_array_in_code(body)
                if array_match:
                    return array_match
            
            # Try to find array in overall structure
            return self._get_default_array()
            
        except Exception as e:
            logger.error(f"Error extracting array data: {str(e)}")
            return self._get_default_array()
    
    def _find_array_in_code(self, code: str) -> List[int]:
        """Find array data in code"""
        
        try:
            import re
            
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
                    elements = []
                    for elem in array_str.split(','):
                        elem = elem.strip()
                        if elem.isdigit():
                            elements.append(int(elem))
                        elif elem.replace('-', '').isdigit():
                            elements.append(int(elem))
                    return elements if elements else None
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding array in code: {str(e)}")
            return None
    
    def _get_default_array(self) -> List[int]:
        """Get default array for visualization"""
        
        return [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 42]
    
    def _visualize_bubble_sort(self, array: List[int]) -> Dict[str, Any]:
        """Generate bubble sort visualization"""
        
        try:
            steps = []
            arr = array.copy()
            n = len(arr)
            
            for i in range(n):
                swapped = False
                
                for j in range(0, n - i - 1):
                    # Comparison step
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'comparison',
                        'array': arr.copy(),
                        'comparing': [j, j + 1],
                        'swapped': [],
                        'description': f"Comparing {arr[j]} and {arr[j + 1]}",
                        'pass': i + 1,
                        'iteration': j + 1
                    })
                    
                    if arr[j] > arr[j + 1]:
                        # Swap step
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        swapped = True
                        
                        steps.append({
                            'step': len(steps) + 1,
                            'type': 'swap',
                            'array': arr.copy(),
                            'comparing': [],
                            'swapped': [j, j + 1],
                            'description': f"Swapped {arr[j + 1]} and {arr[j]}",
                            'pass': i + 1,
                            'iteration': j + 1
                        })
                
                if not swapped:
                    break
            
            return {
                'type': 'bubble_sort',
                'title': 'Bubble Sort Visualization',
                'description': 'Bubble sort repeatedly steps through the list, compares adjacent elements and swaps them if they are in wrong order.',
                'initial_array': array,
                'final_array': arr,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'comparisons': len([s for s in steps if s['type'] == 'comparison']),
                    'swaps': len([s for s in steps if s['type'] == 'swap']),
                    'passes': i + 1,
                    'time_complexity': 'O(n²)',
                    'space_complexity': 'O(1)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing bubble sort: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _visualize_selection_sort(self, array: List[int]) -> Dict[str, Any]:
        """Generate selection sort visualization"""
        
        try:
            steps = []
            arr = array.copy()
            n = len(arr)
            
            for i in range(n):
                min_idx = i
                
                # Find minimum element
                for j in range(i + 1, n):
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'comparison',
                        'array': arr.copy(),
                        'comparing': [min_idx, j],
                        'swapped': [],
                        'min_index': min_idx,
                        'description': f"Comparing {arr[min_idx]} and {arr[j]}",
                        'pass': i + 1,
                        'iteration': j
                    })
                    
                    if arr[j] < arr[min_idx]:
                        min_idx = j
                
                # Swap minimum element with first element
                if min_idx != i:
                    arr[i], arr[min_idx] = arr[min_idx], arr[i]
                    
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'swap',
                        'array': arr.copy(),
                        'comparing': [],
                        'swapped': [i, min_idx],
                        'min_index': min_idx,
                        'description': f"Swapped minimum element {arr[min_idx]} with {arr[i]}",
                        'pass': i + 1,
                        'iteration': n - 1
                    })
            
            return {
                'type': 'selection_sort',
                'title': 'Selection Sort Visualization',
                'description': 'Selection sort divides the input into sorted and unsorted regions, repeatedly selecting the smallest element from unsorted region.',
                'initial_array': array,
                'final_array': arr,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'comparisons': len([s for s in steps if s['type'] == 'comparison']),
                    'swaps': len([s for s in steps if s['type'] == 'swap']),
                    'passes': n,
                    'time_complexity': 'O(n²)',
                    'space_complexity': 'O(1)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing selection sort: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _visualize_insertion_sort(self, array: List[int]) -> Dict[str, Any]:
        """Generate insertion sort visualization"""
        
        try:
            steps = []
            arr = array.copy()
            n = len(arr)
            
            for i in range(1, n):
                key = arr[i]
                j = i - 1
                
                steps.append({
                    'step': len(steps) + 1,
                    'type': 'select_key',
                    'array': arr.copy(),
                    'key_index': i,
                    'key_value': key,
                    'description': f"Selected key element {key} at position {i}",
                    'pass': i
                })
                
                # Move elements greater than key to one position ahead
                while j >= 0 and arr[j] > key:
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'comparison',
                        'array': arr.copy(),
                        'comparing': [j, j + 1],
                        'key_value': key,
                        'description': f"Comparing {arr[j]} with key {key}",
                        'pass': i,
                        'iteration': j + 1
                    })
                    
                    arr[j + 1] = arr[j]
                    j -= 1
                    
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'shift',
                        'array': arr.copy(),
                        'shifted_index': j + 1,
                        'key_value': key,
                        'description': f"Shifted {arr[j + 1]} to position {j + 2}",
                        'pass': i,
                        'iteration': j + 2
                    })
                
                arr[j + 1] = key
                
                steps.append({
                    'step': len(steps) + 1,
                    'type': 'insert',
                    'array': arr.copy(),
                    'inserted_index': j + 1,
                    'key_value': key,
                    'description': f"Inserted key {key} at position {j + 1}",
                    'pass': i
                })
            
            return {
                'type': 'insertion_sort',
                'title': 'Insertion Sort Visualization',
                'description': 'Insertion sort builds the final sorted array one item at a time by inserting each element into its proper position.',
                'initial_array': array,
                'final_array': arr,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'comparisons': len([s for s in steps if s['type'] == 'comparison']),
                    'shifts': len([s for s in steps if s['type'] == 'shift']),
                    'insertions': len([s for s in steps if s['type'] == 'insert']),
                    'passes': n - 1,
                    'time_complexity': 'O(n²)',
                    'space_complexity': 'O(1)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing insertion sort: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _visualize_quick_sort(self, array: List[int]) -> Dict[str, Any]:
        """Generate quick sort visualization"""
        
        try:
            steps = []
            arr = array.copy()
            
            def quick_sort_recursive(low: int, high: int, depth: int = 0):
                if low < high:
                    pivot_index, partition_steps = partition(low, high)
                    steps.extend(partition_steps)
                    
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'recursive_call',
                        'array': arr.copy(),
                        'range': [low, high],
                        'pivot_index': pivot_index,
                        'description': f"Recursively sorting left subarray [{low}, {pivot_index - 1}]",
                        'depth': depth + 1
                    })
                    
                    quick_sort_recursive(low, pivot_index - 1, depth + 1)
                    
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'recursive_call',
                        'array': arr.copy(),
                        'range': [pivot_index + 1, high],
                        'pivot_index': pivot_index,
                        'description': f"Recursively sorting right subarray [{pivot_index + 1}, {high}]",
                        'depth': depth + 1
                    })
                    
                    quick_sort_recursive(pivot_index + 1, high, depth + 1)
            
            def partition(low: int, high: int):
                nonlocal arr
                partition_steps = []
                pivot = arr[high]
                
                partition_steps.append({
                    'step': len(steps) + len(partition_steps) + 1,
                    'type': 'select_pivot',
                    'array': arr.copy(),
                    'pivot_index': high,
                    'pivot_value': pivot,
                    'description': f"Selected pivot {pivot} at position {high}",
                    'range': [low, high]
                })
                
                i = low - 1
                
                for j in range(low, high):
                    partition_steps.append({
                        'step': len(steps) + len(partition_steps) + 1,
                        'type': 'comparison',
                        'array': arr.copy(),
                        'comparing': [j, high],
                        'pivot_value': pivot,
                        'description': f"Comparing {arr[j]} with pivot {pivot}",
                        'range': [low, high]
                    })
                    
                    if arr[j] < pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        
                        if i != j:
                            partition_steps.append({
                                'step': len(steps) + len(partition_steps) + 1,
                                'type': 'swap',
                                'array': arr.copy(),
                                'swapped': [i, j],
                                'pivot_value': pivot,
                                'description': f"Swapped {arr[j]} and {arr[i]}",
                                'range': [low, high]
                            })
                
                # Place pivot in correct position
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                
                partition_steps.append({
                    'step': len(steps) + len(partition_steps) + 1,
                    'type': 'place_pivot',
                    'array': arr.copy(),
                    'swapped': [i + 1, high],
                    'pivot_value': pivot,
                    'description': f"Placed pivot {pivot} at correct position {i + 1}",
                    'range': [low, high]
                })
                
                return i + 1, partition_steps
            
            quick_sort_recursive(0, len(arr) - 1)
            
            return {
                'type': 'quick_sort',
                'title': 'Quick Sort Visualization',
                'description': 'Quick sort picks a pivot element and partitions the array around it, then recursively sorts the sub-arrays.',
                'initial_array': array,
                'final_array': arr,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'comparisons': len([s for s in steps if s['type'] == 'comparison']),
                    'swaps': len([s for s in steps if s['type'] == 'swap']),
                    'partitions': len([s for s in steps if s['type'] == 'place_pivot']),
                    'time_complexity': 'O(n log n) average, O(n²) worst',
                    'space_complexity': 'O(log n)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing quick sort: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _visualize_merge_sort(self, array: List[int]) -> Dict[str, Any]:
        """Generate merge sort visualization"""
        
        try:
            steps = []
            arr = array.copy()
            
            def merge_sort_recursive(left: int, right: int, depth: int = 0):
                if left < right:
                    mid = (left + right) // 2
                    
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'divide',
                        'array': arr.copy(),
                        'range': [left, right],
                        'mid': mid,
                        'description': f"Dividing array [{left}, {right}] at midpoint {mid}",
                        'depth': depth
                    })
                    
                    merge_sort_recursive(left, mid, depth + 1)
                    merge_sort_recursive(mid + 1, right, depth + 1)
                    
                    merge_steps = merge(left, mid, right)
                    steps.extend(merge_steps)
            
            def merge(left: int, mid: int, right: int):
                nonlocal arr
                merge_steps = []
                
                left_arr = arr[left:mid + 1]
                right_arr = arr[mid + 1:right + 1]
                
                merge_steps.append({
                    'step': len(steps) + len(merge_steps) + 1,
                    'type': 'merge_start',
                    'array': arr.copy(),
                    'left_array': left_arr.copy(),
                    'right_array': right_arr.copy(),
                    'range': [left, right],
                    'description': f"Merging left {left_arr} and right {right_arr}",
                    'depth': 0
                })
                
                i = j = 0
                k = left
                
                while i < len(left_arr) and j < len(right_arr):
                    merge_steps.append({
                        'step': len(steps) + len(merge_steps) + 1,
                        'type': 'merge_compare',
                        'array': arr.copy(),
                        'comparing': [left + i, mid + 1 + j],
                        'left_val': left_arr[i],
                        'right_val': right_arr[j],
                        'description': f"Comparing {left_arr[i]} and {right_arr[j]}",
                        'range': [left, right]
                    })
                    
                    if left_arr[i] <= right_arr[j]:
                        arr[k] = left_arr[i]
                        i += 1
                    else:
                        arr[k] = right_arr[j]
                        j += 1
                    
                    merge_steps.append({
                        'step': len(steps) + len(merge_steps) + 1,
                        'type': 'merge_place',
                        'array': arr.copy(),
                        'placed_index': k,
                        'placed_value': arr[k],
                        'description': f"Placed {arr[k]} at position {k}",
                        'range': [left, right]
                    })
                    
                    k += 1
                
                # Copy remaining elements
                while i < len(left_arr):
                    arr[k] = left_arr[i]
                    merge_steps.append({
                        'step': len(steps) + len(merge_steps) + 1,
                        'type': 'merge_place',
                        'array': arr.copy(),
                        'placed_index': k,
                        'placed_value': arr[k],
                        'description': f"Placed remaining {arr[k]} at position {k}",
                        'range': [left, right]
                    })
                    i += 1
                    k += 1
                
                while j < len(right_arr):
                    arr[k] = right_arr[j]
                    merge_steps.append({
                        'step': len(steps) + len(merge_steps) + 1,
                        'type': 'merge_place',
                        'array': arr.copy(),
                        'placed_index': k,
                        'placed_value': arr[k],
                        'description': f"Placed remaining {arr[k]} at position {k}",
                        'range': [left, right]
                    })
                    j += 1
                    k += 1
                
                merge_steps.append({
                    'step': len(steps) + len(merge_steps) + 1,
                    'type': 'merge_complete',
                    'array': arr.copy(),
                    'range': [left, right],
                    'description': f"Merge complete for range [{left}, {right}]",
                    'merged_array': arr[left:right + 1].copy()
                })
                
                return merge_steps
            
            merge_sort_recursive(0, len(arr) - 1)
            
            return {
                'type': 'merge_sort',
                'title': 'Merge Sort Visualization',
                'description': 'Merge sort divides the array into halves, sorts them, and then merges them back together.',
                'initial_array': array,
                'final_array': arr,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'divisions': len([s for s in steps if s['type'] == 'divide']),
                    'merges': len([s for s in steps if s['type'] == 'merge_complete']),
                    'comparisons': len([s for s in steps if s['type'] == 'merge_compare']),
                    'time_complexity': 'O(n log n)',
                    'space_complexity': 'O(n)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing merge sort: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _generate_error_visualization(self, error_message: str) -> Dict[str, Any]:
        """Generate error visualization"""
        
        return {
            'type': 'error',
            'title': 'Sorting Visualization Error',
            'description': 'Error generating sorting visualization',
            'error': error_message,
            'initial_array': [],
            'final_array': [],
            'steps': [],
            'metadata': {
                'error': True,
                'message': error_message
            }
        }
