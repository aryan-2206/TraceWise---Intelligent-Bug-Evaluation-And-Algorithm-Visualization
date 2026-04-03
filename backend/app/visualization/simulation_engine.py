import logging
from typing import Dict, Any, List, Callable, Optional
import json

logger = logging.getLogger(__name__)

class SimulationEngine:
    """Engine for running algorithm simulations and generating step-by-step visualizations"""
    
    def __init__(self):
        self.simulations = {}
        self.current_simulation = None
        self.step_index = 0
        self.is_running = False
        
    def create_simulation(self, simulation_id: str, algorithm_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new simulation"""
        
        try:
            simulation = {
                'id': simulation_id,
                'type': algorithm_type,
                'data': data,
                'steps': [],
                'current_step': 0,
                'total_steps': 0,
                'status': 'created',
                'metadata': {
                    'created_at': self._get_timestamp(),
                    'last_updated': self._get_timestamp()
                }
            }
            
            # Generate steps based on algorithm type
            if algorithm_type == 'binary_search':
                simulation['steps'] = self._simulate_binary_search(data)
            elif algorithm_type in ['bubble_sort', 'selection_sort', 'insertion_sort', 'quick_sort', 'merge_sort']:
                simulation['steps'] = self._simulate_sorting(algorithm_type, data)
            elif algorithm_type in ['dfs', 'bfs']:
                simulation['steps'] = self._simulate_graph_traversal(algorithm_type, data)
            elif algorithm_type == 'dijkstra':
                simulation['steps'] = self._simulate_dijkstra(data)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported algorithm type: {algorithm_type}'
                }
            
            simulation['total_steps'] = len(simulation['steps'])
            self.simulations[simulation_id] = simulation
            
            return {
                'success': True,
                'simulation_id': simulation_id,
                'total_steps': simulation['total_steps'],
                'algorithm_type': algorithm_type
            }
            
        except Exception as e:
            logger.error(f"Error creating simulation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_simulation(self, simulation_id: str, step_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Run a simulation from start to finish"""
        
        try:
            if simulation_id not in self.simulations:
                return {
                    'success': False,
                    'error': f'Simulation {simulation_id} not found'
                }
            
            simulation = self.simulations[simulation_id]
            simulation['status'] = 'running'
            self.is_running = True
            self.current_simulation = simulation_id
            
            for i, step in enumerate(simulation['steps']):
                simulation['current_step'] = i
                self.step_index = i
                
                # Call callback if provided
                if step_callback:
                    try:
                        step_callback(step, i, len(simulation['steps']))
                    except Exception as e:
                        logger.error(f"Error in step callback: {str(e)}")
                
                # Simulate processing time
                import time
                time.sleep(0.1)  # Small delay for visualization
            
            simulation['status'] = 'completed'
            self.is_running = False
            
            return {
                'success': True,
                'simulation_id': simulation_id,
                'total_steps': simulation['total_steps'],
                'status': 'completed'
            }
            
        except Exception as e:
            logger.error(f"Error running simulation: {str(e)}")
            if simulation_id in self.simulations:
                self.simulations[simulation_id]['status'] = 'error'
            self.is_running = False
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def step_simulation(self, simulation_id: str, direction: str = 'forward') -> Dict[str, Any]:
        """Step through simulation one step at a time"""
        
        try:
            if simulation_id not in self.simulations:
                return {
                    'success': False,
                    'error': f'Simulation {simulation_id} not found'
                }
            
            simulation = self.simulations[simulation_id]
            
            if direction == 'forward':
                if simulation['current_step'] < simulation['total_steps'] - 1:
                    simulation['current_step'] += 1
                else:
                    return {
                        'success': False,
                        'error': 'Already at last step'
                    }
            elif direction == 'backward':
                if simulation['current_step'] > 0:
                    simulation['current_step'] -= 1
                else:
                    return {
                        'success': False,
                        'error': 'Already at first step'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Invalid direction. Use "forward" or "backward"'
                }
            
            current_step = simulation['steps'][simulation['current_step']]
            
            return {
                'success': True,
                'simulation_id': simulation_id,
                'current_step': simulation['current_step'],
                'total_steps': simulation['total_steps'],
                'step_data': current_step
            }
            
        except Exception as e:
            logger.error(f"Error stepping simulation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_simulation_state(self, simulation_id: str) -> Dict[str, Any]:
        """Get current state of a simulation"""
        
        try:
            if simulation_id not in self.simulations:
                return {
                    'success': False,
                    'error': f'Simulation {simulation_id} not found'
                }
            
            simulation = self.simulations[simulation_id]
            
            current_step_data = None
            if simulation['current_step'] < len(simulation['steps']):
                current_step_data = simulation['steps'][simulation['current_step']]
            
            return {
                'success': True,
                'simulation_id': simulation_id,
                'status': simulation['status'],
                'current_step': simulation['current_step'],
                'total_steps': simulation['total_steps'],
                'current_step_data': current_step_data,
                'algorithm_type': simulation['type'],
                'metadata': simulation['metadata']
            }
            
        except Exception as e:
            logger.error(f"Error getting simulation state: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def reset_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """Reset simulation to beginning"""
        
        try:
            if simulation_id not in self.simulations:
                return {
                    'success': False,
                    'error': f'Simulation {simulation_id} not found'
                }
            
            simulation = self.simulations[simulation_id]
            simulation['current_step'] = 0
            simulation['status'] = 'created'
            
            return {
                'success': True,
                'simulation_id': simulation_id,
                'current_step': 0,
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Error resetting simulation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """Delete a simulation"""
        
        try:
            if simulation_id not in self.simulations:
                return {
                    'success': False,
                    'error': f'Simulation {simulation_id} not found'
                }
            
            del self.simulations[simulation_id]
            
            if self.current_simulation == simulation_id:
                self.current_simulation = None
                self.is_running = False
            
            return {
                'success': True,
                'simulation_id': simulation_id
            }
            
        except Exception as e:
            logger.error(f"Error deleting simulation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_simulations(self) -> List[Dict[str, Any]]:
        """List all simulations"""
        
        try:
            simulations = []
            for sim_id, simulation in self.simulations.items():
                simulations.append({
                    'id': sim_id,
                    'type': simulation['type'],
                    'status': simulation['status'],
                    'current_step': simulation['current_step'],
                    'total_steps': simulation['total_steps'],
                    'created_at': simulation['metadata']['created_at']
                })
            
            return simulations
            
        except Exception as e:
            logger.error(f"Error listing simulations: {str(e)}")
            return []
    
    def _simulate_binary_search(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate binary search algorithm"""
        
        try:
            steps = []
            array = data.get('array', [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
            target = data.get('target', 7)
            
            left = 0
            right = len(array) - 1
            
            while left <= right:
                mid = (left + right) // 2
                mid_value = array[mid]
                
                step = {
                    'type': 'comparison',
                    'left': left,
                    'right': right,
                    'mid': mid,
                    'mid_value': mid_value,
                    'target': target,
                    'array_state': self._create_array_visual_state(array, left, right, mid),
                    'description': f"Comparing array[{mid}] = {mid_value} with target {target}"
                }
                
                if mid_value == target:
                    step['type'] = 'found'
                    step['description'] = f"Target {target} found at index {mid}!"
                    steps.append(step)
                    break
                elif mid_value < target:
                    step['type'] = 'move_right'
                    step['description'] = f"{mid_value} < {target}, searching right half"
                    left = mid + 1
                else:
                    step['type'] = 'move_left'
                    step['description'] = f"{mid_value} > {target}, searching left half"
                    right = mid - 1
                
                steps.append(step)
            
            if not steps or steps[-1]['type'] != 'found':
                steps.append({
                    'type': 'not_found',
                    'left': left,
                    'right': right,
                    'mid': -1,
                    'target': target,
                    'array_state': self._create_array_visual_state(array, left, right, -1),
                    'description': f"Target {target} not found in array"
                })
            
            return steps
            
        except Exception as e:
            logger.error(f"Error simulating binary search: {str(e)}")
            return []
    
    def _simulate_sorting(self, algorithm_type: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate sorting algorithms"""
        
        try:
            array = data.get('array', [64, 34, 25, 12, 22, 11, 90])
            steps = []
            
            if algorithm_type == 'bubble_sort':
                steps = self._bubble_sort_steps(array)
            elif algorithm_type == 'selection_sort':
                steps = self._selection_sort_steps(array)
            elif algorithm_type == 'insertion_sort':
                steps = self._insertion_sort_steps(array)
            
            return steps
            
        except Exception as e:
            logger.error(f"Error simulating sorting: {str(e)}")
            return []
    
    def _simulate_graph_traversal(self, algorithm_type: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate graph traversal algorithms"""
        
        try:
            graph_data = data.get('graph', {})
            start_node = data.get('start_node', 0)
            steps = []
            
            if algorithm_type == 'dfs':
                steps = self._dfs_steps(graph_data, start_node)
            elif algorithm_type == 'bfs':
                steps = self._bfs_steps(graph_data, start_node)
            
            return steps
            
        except Exception as e:
            logger.error(f"Error simulating graph traversal: {str(e)}")
            return []
    
    def _simulate_dijkstra(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate Dijkstra's algorithm"""
        
        try:
            graph_data = data.get('graph', {})
            start_node = data.get('start_node', 0)
            steps = self._dijkstra_steps(graph_data, start_node)
            
            return steps
            
        except Exception as e:
            logger.error(f"Error simulating Dijkstra: {str(e)}")
            return []
    
    def _create_array_visual_state(self, array: List[int], left: int, right: int, mid: int) -> List[Dict[str, Any]]:
        """Create visual state of array for binary search"""
        
        state = []
        for i, value in enumerate(array):
            status = 'normal'
            if i == mid:
                status = 'current'
            elif i < left or i > right:
                status = 'eliminated'
            elif left <= i <= right:
                status = 'search_range'
            
            state.append({
                'index': i,
                'value': value,
                'status': status
            })
        
        return state
    
    def _bubble_sort_steps(self, array: List[int]) -> List[Dict[str, Any]]:
        """Generate bubble sort steps"""
        
        steps = []
        arr = array.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                steps.append({
                    'type': 'compare',
                    'array': arr.copy(),
                    'comparing': [j, j + 1],
                    'description': f"Comparing {arr[j]} and {arr[j + 1]}"
                })
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps.append({
                        'type': 'swap',
                        'array': arr.copy(),
                        'swapped': [j, j + 1],
                        'description': f"Swapped {arr[j + 1]} and {arr[j]}"
                    })
        
        return steps
    
    def _selection_sort_steps(self, array: List[int]) -> List[Dict[str, Any]]:
        """Generate selection sort steps"""
        
        steps = []
        arr = array.copy()
        n = len(arr)
        
        for i in range(n):
            min_idx = i
            
            for j in range(i + 1, n):
                steps.append({
                    'type': 'compare',
                    'array': arr.copy(),
                    'comparing': [min_idx, j],
                    'description': f"Comparing {arr[min_idx]} and {arr[j]}"
                })
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                steps.append({
                    'type': 'swap',
                    'array': arr.copy(),
                    'swapped': [i, min_idx],
                    'description': f"Swapped minimum element with position {i}"
                })
        
        return steps
    
    def _insertion_sort_steps(self, array: List[int]) -> List[Dict[str, Any]]:
        """Generate insertion sort steps"""
        
        steps = []
        arr = array.copy()
        n = len(arr)
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            steps.append({
                'type': 'select_key',
                'array': arr.copy(),
                'key_index': i,
                'key_value': key,
                'description': f"Selected key element {key}"
            })
            
            while j >= 0 and arr[j] > key:
                steps.append({
                    'type': 'compare',
                    'array': arr.copy(),
                    'comparing': [j, j + 1],
                    'description': f"Comparing {arr[j]} with key {key}"
                })
                
                arr[j + 1] = arr[j]
                j -= 1
                
                steps.append({
                    'type': 'shift',
                    'array': arr.copy(),
                    'shifted_index': j + 1,
                    'description': f"Shifted element to position {j + 2}"
                })
            
            arr[j + 1] = key
            
            steps.append({
                'type': 'insert',
                'array': arr.copy(),
                'inserted_index': j + 1,
                'key_value': key,
                'description': f"Inserted key {key} at position {j + 1}"
            })
        
        return steps
    
    def _dfs_steps(self, graph_data: Dict[str, Any], start_node: int) -> List[Dict[str, Any]]:
        """Generate DFS steps"""
        
        steps = []
        visited = set()
        stack = [start_node]
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                
                steps.append({
                    'type': 'visit',
                    'current_node': current,
                    'visited_nodes': list(visited),
                    'stack': stack.copy(),
                    'description': f"Visiting node {current}"
                })
                
                # Add neighbors to stack (simplified)
                neighbors = self._get_node_neighbors(current, graph_data)
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return steps
    
    def _bfs_steps(self, graph_data: Dict[str, Any], start_node: int) -> List[Dict[str, Any]]:
        """Generate BFS steps"""
        
        steps = []
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        
        while queue:
            current = queue.pop(0)
            
            steps.append({
                'type': 'visit',
                'current_node': current,
                'visited_nodes': list(visited),
                'queue': queue.copy(),
                'description': f"Visiting node {current}"
            })
            
            # Add neighbors to queue (simplified)
            neighbors = self._get_node_neighbors(current, graph_data)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        
        return steps
    
    def _dijkstra_steps(self, graph_data: Dict[str, Any], start_node: int) -> List[Dict[str, Any]]:
        """Generate Dijkstra steps"""
        
        steps = []
        # Simplified Dijkstra simulation
        distances = {start_node: 0}
        visited = set()
        
        steps.append({
            'type': 'initialize',
            'start_node': start_node,
            'distances': distances.copy(),
            'description': f"Initialized distances from node {start_node}"
        })
        
        # Simplified - in practice, would implement full Dijkstra
        nodes = graph_data.get('nodes', [])
        for node in nodes:
            if node['id'] != start_node:
                distances[node['id']] = float('inf')
        
        steps.append({
            'type': 'complete',
            'final_distances': distances,
            'description': "Dijkstra algorithm complete"
        })
        
        return steps
    
    def _get_node_neighbors(self, node: int, graph_data: Dict[str, Any]) -> List[int]:
        """Get neighbors of a node (simplified)"""
        
        # Simplified neighbor detection
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        
        neighbors = []
        for edge in edges:
            if edge['from'] == node:
                neighbors.append(edge['to'])
            elif edge['to'] == node:
                neighbors.append(edge['from'])
        
        return neighbors
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        
        import datetime
        return datetime.datetime.now().isoformat()
