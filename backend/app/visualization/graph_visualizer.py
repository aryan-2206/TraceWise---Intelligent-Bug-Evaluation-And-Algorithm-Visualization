import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class GraphVisualizer:
    """Generate visualization data for graph algorithms"""
    
    def __init__(self):
        self.supported_algorithms = ['dfs', 'bfs', 'dijkstra']
    
    def visualize(self, structure: Dict[str, Any], algorithm_type: str) -> Dict[str, Any]:
        """Generate visualization data for graph algorithms"""
        
        try:
            if algorithm_type not in self.supported_algorithms:
                return self._generate_error_visualization(f"Unsupported algorithm: {algorithm_type}")
            
            # Extract graph data
            graph_data = self._extract_graph_data(structure)
            if not graph_data:
                graph_data = self._get_default_graph()
            
            # Generate visualization based on algorithm type
            if algorithm_type == 'dfs':
                return self._visualize_dfs(graph_data)
            elif algorithm_type == 'bfs':
                return self._visualize_bfs(graph_data)
            elif algorithm_type == 'dijkstra':
                return self._visualize_dijkstra(graph_data)
            else:
                return self._generate_error_visualization(f"Algorithm {algorithm_type} not implemented")
                
        except Exception as e:
            logger.error(f"Error generating graph visualization: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _extract_graph_data(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Extract graph data from code structure"""
        
        try:
            functions = structure.get('functions', [])
            
            for func in functions:
                body = func.get('body', '')
                graph_match = self._find_graph_in_code(body)
                if graph_match:
                    return graph_match
            
            return self._get_default_graph()
            
        except Exception as e:
            logger.error(f"Error extracting graph data: {str(e)}")
            return self._get_default_graph()
    
    def _find_graph_in_code(self, code: str) -> Dict[str, Any]:
        """Find graph data in code"""
        
        try:
            import re
            
            # Look for adjacency matrix or list patterns
            matrix_pattern = r'graph\s*=\s*\[([^\]]+(?:\[[^\]]*\][^\]]*)*)\]'
            list_pattern = r'graph\s*=\s*\{[^}]*\}'
            
            if re.search(matrix_pattern, code, re.DOTALL):
                return self._parse_adjacency_matrix(code)
            elif re.search(list_pattern, code):
                return self._parse_adjacency_list(code)
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding graph in code: {str(e)}")
            return None
    
    def _parse_adjacency_matrix(self, code: str) -> Dict[str, Any]:
        """Parse adjacency matrix from code"""
        
        try:
            import re
            
            match = re.search(r'graph\s*=\s*\[([^\]]+(?:\[[^\]]*\][^\]]*)*)\]', code, re.DOTALL)
            if match:
                matrix_str = match.group(1)
                # Simple parsing - in practice, you'd need more sophisticated parsing
                return {
                    'type': 'adjacency_matrix',
                    'data': self._get_default_graph()['data'],
                    'start_node': 0
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing adjacency matrix: {str(e)}")
            return None
    
    def _parse_adjacency_list(self, code: str) -> Dict[str, Any]:
        """Parse adjacency list from code"""
        
        try:
            # Simple parsing - in practice, you'd need more sophisticated parsing
            return {
                'type': 'adjacency_list',
                'data': self._get_default_graph()['data'],
                'start_node': 0
            }
            
        except Exception as e:
            logger.error(f"Error parsing adjacency list: {str(e)}")
            return None
    
    def _get_default_graph(self) -> Dict[str, Any]:
        """Get default graph for visualization"""
        
        return {
            'type': 'adjacency_list',
            'data': {
                'nodes': [
                    {'id': 0, 'label': 'A', 'x': 100, 'y': 100},
                    {'id': 1, 'label': 'B', 'x': 200, 'y': 50},
                    {'id': 2, 'label': 'C', 'x': 200, 'y': 150},
                    {'id': 3, 'label': 'D', 'x': 300, 'y': 100},
                    {'id': 4, 'label': 'E', 'x': 400, 'y': 100}
                ],
                'edges': [
                    {'from': 0, 'to': 1, 'weight': 1},
                    {'from': 0, 'to': 2, 'weight': 1},
                    {'from': 1, 'to': 3, 'weight': 1},
                    {'from': 2, 'to': 3, 'weight': 1},
                    {'from': 3, 'to': 4, 'weight': 1}
                ]
            },
            'start_node': 0
        }
    
    def _visualize_dfs(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate DFS visualization"""
        
        try:
            nodes = graph_data['data']['nodes']
            edges = graph_data['data']['edges']
            start_node = graph_data.get('start_node', 0)
            
            steps = []
            visited = set()
            stack = [start_node]
            
            while stack:
                current = stack.pop()
                
                if current not in visited:
                    visited.add(current)
                    
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'visit',
                        'current_node': current,
                        'visited_nodes': list(visited),
                        'stack': stack.copy(),
                        'description': f"Visiting node {nodes[current]['label']}",
                        'node_states': self._create_node_states(nodes, visited, current, [])
                    })
                    
                    # Find neighbors
                    neighbors = self._get_neighbors(current, edges)
                    unvisited_neighbors = [n for n in neighbors if n not in visited]
                    
                    for neighbor in reversed(unvisited_neighbors):  # Reverse for stack order
                        stack.append(neighbor)
                    
                    if unvisited_neighbors:
                        steps.append({
                            'step': len(steps) + 1,
                            'type': 'push_neighbors',
                            'current_node': current,
                            'neighbors': unvisited_neighbors,
                            'stack': stack.copy(),
                            'description': f"Pushing neighbors {[nodes[n]['label'] for n in unvisited_neighbors]} to stack",
                            'node_states': self._create_node_states(nodes, visited, current, unvisited_neighbors)
                        })
            
            return {
                'type': 'dfs',
                'title': 'Depth-First Search Visualization',
                'description': 'DFS explores as far as possible along each branch before backtracking.',
                'graph_data': graph_data,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'visited_nodes': len(visited),
                    'time_complexity': 'O(V + E)',
                    'space_complexity': 'O(V)',
                    'traversal_order': visited
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing DFS: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _visualize_bfs(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate BFS visualization"""
        
        try:
            nodes = graph_data['data']['nodes']
            edges = graph_data['data']['edges']
            start_node = graph_data.get('start_node', 0)
            
            steps = []
            visited = set()
            queue = [start_node]
            visited.add(start_node)
            
            while queue:
                current = queue.pop(0)
                
                steps.append({
                    'step': len(steps) + 1,
                    'type': 'visit',
                    'current_node': current,
                    'visited_nodes': list(visited),
                    'queue': queue.copy(),
                    'description': f"Visiting node {nodes[current]['label']}",
                    'node_states': self._create_node_states(nodes, visited, current, [])
                })
                
                # Find neighbors
                neighbors = self._get_neighbors(current, edges)
                unvisited_neighbors = [n for n in neighbors if n not in visited]
                
                for neighbor in unvisited_neighbors:
                    queue.append(neighbor)
                    visited.add(neighbor)
                
                if unvisited_neighbors:
                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'enqueue_neighbors',
                        'current_node': current,
                        'neighbors': unvisited_neighbors,
                        'queue': queue.copy(),
                        'description': f"Enqueuing neighbors {[nodes[n]['label'] for n in unvisited_neighbors]}",
                        'node_states': self._create_node_states(nodes, visited, current, unvisited_neighbors)
                    })
            
            return {
                'type': 'bfs',
                'title': 'Breadth-First Search Visualization',
                'description': 'BFS explores all neighbors at the present depth before moving to nodes at the next depth level.',
                'graph_data': graph_data,
                'steps': steps,
                'metadata': {
                    'total_steps': len(steps),
                    'visited_nodes': len(visited),
                    'time_complexity': 'O(V + E)',
                    'space_complexity': 'O(V)',
                    'traversal_order': list(visited)
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing BFS: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _visualize_dijkstra(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Dijkstra's algorithm visualization"""
        
        try:
            nodes = graph_data['data']['nodes']
            edges = graph_data['data']['edges']
            start_node = graph_data.get('start_node', 0)
            
            steps = []
            distances = {node['id']: float('inf') for node in nodes}
            distances[start_node] = 0
            visited = set()
            previous = {}
            
            import heapq
            priority_queue = [(0, start_node)]
            
            while priority_queue:
                current_distance, current = heapq.heappop(priority_queue)
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                steps.append({
                    'step': len(steps) + 1,
                    'type': 'visit',
                    'current_node': current,
                    'current_distance': current_distance,
                    'distances': distances.copy(),
                    'visited_nodes': list(visited),
                    'description': f"Visiting node {nodes[current]['label']} with distance {current_distance}",
                    'node_states': self._create_dijkstra_node_states(nodes, distances, visited, current)
                })
                
                # Check neighbors
                neighbors = self._get_neighbors_with_weights(current, edges)
                
                for neighbor, weight in neighbors:
                    if neighbor not in visited:
                        distance = current_distance + weight
                        
                        if distance < distances[neighbor]:
                            distances[neighbor] = distance
                            previous[neighbor] = current
                            heapq.heappush(priority_queue, (distance, neighbor))
                
                steps.append({
                    'step': len(steps) + 1,
                    'type': 'update_distances',
                    'current_node': current,
                    'neighbors': list(neighbors),
                    'updated_distances': distances.copy(),
                    'description': f"Updated distances for neighbors of {nodes[current]['label']}",
                    'node_states': self._create_dijkstra_node_states(nodes, distances, visited, current)
                })
            
            # Reconstruct shortest paths
            shortest_paths = {}
            for node in nodes:
                if node['id'] != start_node and distances[node['id']] != float('inf'):
                    path = self._reconstruct_path(node['id'], previous)
                    shortest_paths[node['id']] = path
            
            return {
                'type': 'dijkstra',
                'title': 'Dijkstra\'s Algorithm Visualization',
                'description': 'Dijkstra\'s algorithm finds the shortest paths from a source node to all other nodes in a weighted graph.',
                'graph_data': graph_data,
                'steps': steps,
                'shortest_paths': shortest_paths,
                'metadata': {
                    'total_steps': len(steps),
                    'visited_nodes': len(visited),
                    'final_distances': distances,
                    'time_complexity': 'O((V + E) log V)',
                    'space_complexity': 'O(V)'
                }
            }
            
        except Exception as e:
            logger.error(f"Error visualizing Dijkstra: {str(e)}")
            return self._generate_error_visualization(str(e))
    
    def _get_neighbors(self, node: int, edges: List[Dict[str, Any]]) -> List[int]:
        """Get neighbors of a node"""
        
        neighbors = []
        for edge in edges:
            if edge['from'] == node:
                neighbors.append(edge['to'])
            elif edge['to'] == node:
                neighbors.append(edge['from'])
        return neighbors
    
    def _get_neighbors_with_weights(self, node: int, edges: List[Dict[str, Any]]) -> List[Tuple[int, int]]:
        """Get neighbors with weights"""
        
        neighbors = []
        for edge in edges:
            if edge['from'] == node:
                neighbors.append((edge['to'], edge.get('weight', 1)))
            elif edge['to'] == node:
                neighbors.append((edge['from'], edge.get('weight', 1)))
        return neighbors
    
    def _create_node_states(self, nodes: List[Dict[str, Any]], visited: set, current: int, highlighted: List[int]) -> List[Dict[str, Any]]:
        """Create node states for visualization"""
        
        states = []
        for node in nodes:
            state = {
                'id': node['id'],
                'label': node['label'],
                'status': 'unvisited'
            }
            
            if node['id'] in visited:
                state['status'] = 'visited'
            if node['id'] == current:
                state['status'] = 'current'
            if node['id'] in highlighted:
                state['status'] = 'highlighted'
            
            states.append(state)
        
        return states
    
    def _create_dijkstra_node_states(self, nodes: List[Dict[str, Any]], distances: Dict[int, float], visited: set, current: int) -> List[Dict[str, Any]]:
        """Create node states for Dijkstra visualization"""
        
        states = []
        for node in nodes:
            state = {
                'id': node['id'],
                'label': node['label'],
                'distance': distances[node['id']],
                'status': 'unvisited'
            }
            
            if node['id'] in visited:
                state['status'] = 'visited'
            if node['id'] == current:
                state['status'] = 'current'
            
            states.append(state)
        
        return states
    
    def _reconstruct_path(self, target: int, previous: Dict[int, int]) -> List[int]:
        """Reconstruct path from previous nodes"""
        
        path = []
        current = target
        
        while current in previous:
            path.append(current)
            current = previous[current]
        
        path.append(current)
        return list(reversed(path))
    
    def _generate_error_visualization(self, error_message: str) -> Dict[str, Any]:
        """Generate error visualization"""
        
        return {
            'type': 'error',
            'title': 'Graph Algorithm Visualization Error',
            'description': 'Error generating graph visualization',
            'error': error_message,
            'graph_data': {},
            'steps': [],
            'metadata': {
                'error': True,
                'message': error_message
            }
        }
