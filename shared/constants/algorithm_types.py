"""
Algorithm Types and Constants for TraceWise
Shared constants used across frontend and backend
"""

from enum import Enum
from typing import Dict, List

class AlgorithmType(Enum):
    """Supported algorithm types"""
    BINARY_SEARCH = "binary_search"
    LINEAR_SEARCH = "linear_search"
    BUBBLE_SORT = "bubble_sort"
    SELECTION_SORT = "selection_sort"
    INSERTION_SORT = "insertion_sort"
    QUICK_SORT = "quick_sort"
    MERGE_SORT = "merge_sort"
    HEAP_SORT = "heap_sort"
    DFS = "dfs"
    BFS = "bfs"
    DIJKSTRA = "dijkstra"
    FIBONACCI = "fibonacci"
    FACTORIAL = "factorial"

class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    CPP = "cpp"

class Severity(Enum):
    """Bug severity levels"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class Complexity(Enum):
    """Time complexity types"""
    O_1 = "O(1)"
    O_LOG_N = "O(log n)"
    O_N = "O(n)"
    O_N_LOG_N = "O(n log n)"
    O_N_2 = "O(n²)"
    O_N_3 = "O(n³)"
    O_2_N = "O(2^n)"
    O_N_FACT = "O(n!)"

# Algorithm metadata
ALGORITHM_INFO = {
    AlgorithmType.BINARY_SEARCH: {
        "name": "Binary Search",
        "description": "Efficient search algorithm that works on sorted arrays",
        "category": "search",
        "default_complexity": Complexity.O_LOG_N,
        "space_complexity": "O(1)",
        "use_cases": ["Searching in sorted arrays", "Finding insertion points"]
    },
    AlgorithmType.LINEAR_SEARCH: {
        "name": "Linear Search",
        "description": "Simple search algorithm that checks each element sequentially",
        "category": "search",
        "default_complexity": Complexity.O_N,
        "space_complexity": "O(1)",
        "use_cases": ["Small datasets", "Unsorted data"]
    },
    AlgorithmType.BUBBLE_SORT: {
        "name": "Bubble Sort",
        "description": "Simple sorting algorithm that repeatedly swaps adjacent elements",
        "category": "sorting",
        "default_complexity": Complexity.O_N_2,
        "space_complexity": "O(1)",
        "use_cases": ["Educational purposes", "Small datasets"]
    },
    AlgorithmType.SELECTION_SORT: {
        "name": "Selection Sort",
        "description": "Sorting algorithm that selects the minimum element repeatedly",
        "category": "sorting",
        "default_complexity": Complexity.O_N_2,
        "space_complexity": "O(1)",
        "use_cases": ["Small datasets", "Memory constraints"]
    },
    AlgorithmType.INSERTION_SORT: {
        "name": "Insertion Sort",
        "description": "Builds final sorted array one item at a time",
        "category": "sorting",
        "default_complexity": Complexity.O_N_2,
        "space_complexity": "O(1)",
        "use_cases": ["Small datasets", "Nearly sorted data"]
    },
    AlgorithmType.QUICK_SORT: {
        "name": "Quick Sort",
        "description": "Efficient divide-and-conquer sorting algorithm",
        "category": "sorting",
        "default_complexity": Complexity.O_N_LOG_N,
        "space_complexity": "O(log n)",
        "use_cases": ["Large datasets", "General purpose sorting"]
    },
    AlgorithmType.MERGE_SORT: {
        "name": "Merge Sort",
        "description": "Divide-and-conquer sorting algorithm with stable sorting",
        "category": "sorting",
        "default_complexity": Complexity.O_N_LOG_N,
        "space_complexity": "O(n)",
        "use_cases": ["Large datasets", "Stable sorting required"]
    },
    AlgorithmType.HEAP_SORT: {
        "name": "Heap Sort",
        "description": "Comparison-based sorting algorithm using heap data structure",
        "category": "sorting",
        "default_complexity": Complexity.O_N_LOG_N,
        "space_complexity": "O(1)",
        "use_cases": ["In-place sorting", "Memory constraints"]
    },
    AlgorithmType.DFS: {
        "name": "Depth-First Search",
        "description": "Graph traversal algorithm that explores as far as possible",
        "category": "graph",
        "default_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "use_cases": ["Path finding", "Topological sorting", "Cycle detection"]
    },
    AlgorithmType.BFS: {
        "name": "Breadth-First Search",
        "description": "Graph traversal algorithm that explores level by level",
        "category": "graph",
        "default_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "use_cases": ["Shortest path", "Level-order traversal"]
    },
    AlgorithmType.DIJKSTRA: {
        "name": "Dijkstra's Algorithm",
        "description": "Algorithm for finding shortest paths in weighted graphs",
        "category": "graph",
        "default_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "use_cases": ["Shortest path", "Network routing", "GPS navigation"]
    },
    AlgorithmType.FIBONACCI: {
        "name": "Fibonacci Sequence",
        "description": "Generate Fibonacci numbers",
        "category": "mathematical",
        "default_complexity": Complexity.O_2_N,
        "space_complexity": "O(n)",
        "use_cases": ["Mathematical sequences", "Dynamic programming examples"]
    },
    AlgorithmType.FACTORIAL: {
        "name": "Factorial",
        "description": "Calculate factorial of a number",
        "category": "mathematical",
        "default_complexity": Complexity.O_N,
        "space_complexity": "O(n)",
        "use_cases": ["Mathematical calculations", "Permutations"]
    }
}

# Language information
LANGUAGE_INFO = {
    Language.PYTHON: {
        "name": "Python",
        "version": "3.8+",
        "extensions": [".py"],
        "mimetypes": ["text/x-python"],
        "compiler": None,
        "interpreter": "python3"
    },
    Language.JAVASCRIPT: {
        "name": "JavaScript",
        "version": "ES6+",
        "extensions": [".js", ".jsx"],
        "mimetypes": ["text/javascript", "application/javascript"],
        "compiler": None,
        "interpreter": "node"
    },
    Language.CPP: {
        "name": "C++",
        "version": "C++17",
        "extensions": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
        "mimetypes": ["text/x-c++src"],
        "compiler": "g++",
        "interpreter": None
    }
}

# Severity information
SEVERITY_INFO = {
    Severity.CRITICAL: {
        "level": 4,
        "color": "#dc3545",
        "icon": "🔴",
        "description": "Critical issues that must be fixed immediately"
    },
    Severity.ERROR: {
        "level": 3,
        "color": "#fd7e14",
        "icon": "🟠",
        "description": "Error conditions that need attention"
    },
    Severity.WARNING: {
        "level": 2,
        "color": "#ffc107",
        "icon": "🟡",
        "description": "Warning conditions that should be addressed"
    },
    Severity.INFO: {
        "level": 1,
        "color": "#17a2b8",
        "icon": "🔵",
        "description": "Informational messages"
    }
}

# Quality score ranges
QUALITY_SCORE_RANGES = {
    "excellent": {"min": 90, "max": 100, "grade": "A", "color": "#28a745"},
    "good": {"min": 80, "max": 89, "grade": "B", "color": "#17a2b8"},
    "average": {"min": 70, "max": 79, "grade": "C", "color": "#ffc107"},
    "below_average": {"min": 60, "max": 69, "grade": "D", "color": "#fd7e14"},
    "poor": {"min": 0, "max": 59, "grade": "F", "color": "#dc3545"}
}

# Default test data
DEFAULT_TEST_DATA = {
    AlgorithmType.BINARY_SEARCH: {
        "array": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
        "target": 7
    },
    AlgorithmType.BUBBLE_SORT: {
        "array": [64, 34, 25, 12, 22, 11, 90]
    },
    AlgorithmType.SELECTION_SORT: {
        "array": [64, 34, 25, 12, 22, 11, 90]
    },
    AlgorithmType.INSERTION_SORT: {
        "array": [64, 34, 25, 12, 22, 11, 90]
    },
    AlgorithmType.QUICK_SORT: {
        "array": [64, 34, 25, 12, 22, 11, 90]
    },
    AlgorithmType.MERGE_SORT: {
        "array": [64, 34, 25, 12, 22, 11, 90]
    },
    AlgorithmType.DFS: {
        "graph": {
            "nodes": [
                {"id": 0, "label": "A"},
                {"id": 1, "label": "B"},
                {"id": 2, "label": "C"},
                {"id": 3, "label": "D"},
                {"id": 4, "label": "E"}
            ],
            "edges": [
                {"from": 0, "to": 1},
                {"from": 0, "to": 2},
                {"from": 1, "to": 3},
                {"from": 2, "to": 3},
                {"from": 3, "to": 4}
            ]
        },
        "start_node": 0
    },
    AlgorithmType.BFS: {
        "graph": {
            "nodes": [
                {"id": 0, "label": "A"},
                {"id": 1, "label": "B"},
                {"id": 2, "label": "C"},
                {"id": 3, "label": "D"},
                {"id": 4, "label": "E"}
            ],
            "edges": [
                {"from": 0, "to": 1},
                {"from": 0, "to": 2},
                {"from": 1, "to": 3},
                {"from": 2, "to": 3},
                {"from": 3, "to": 4}
            ]
        },
        "start_node": 0
    },
    AlgorithmType.DIJKSTRA: {
        "graph": {
            "nodes": [
                {"id": 0, "label": "A"},
                {"id": 1, "label": "B"},
                {"id": 2, "label": "C"},
                {"id": 3, "label": "D"},
                {"id": 4, "label": "E"}
            ],
            "edges": [
                {"from": 0, "to": 1, "weight": 1},
                {"from": 0, "to": 2, "weight": 4},
                {"from": 1, "to": 3, "weight": 2},
                {"from": 2, "to": 3, "weight": 1},
                {"from": 3, "to": 4, "weight": 1}
            ]
        },
        "start_node": 0
    }
}

# Utility functions
def get_algorithm_info(algorithm_type: AlgorithmType) -> Dict:
    """Get algorithm information by type"""
    return ALGORITHM_INFO.get(algorithm_type, {})

def get_language_info(language: Language) -> Dict:
    """Get language information by type"""
    return LANGUAGE_INFO.get(language, {})

def get_severity_info(severity: Severity) -> Dict:
    """Get severity information by type"""
    return SEVERITY_INFO.get(severity, {})

def get_quality_grade(score: int) -> Dict:
    """Get quality grade information by score"""
    for range_name, range_info in QUALITY_SCORE_RANGES.items():
        if range_info["min"] <= score <= range_info["max"]:
            return {"range": range_name, **range_info}
    return QUALITY_SCORE_RANGES["poor"]

def get_default_test_data(algorithm_type: AlgorithmType) -> Dict:
    """Get default test data for algorithm"""
    return DEFAULT_TEST_DATA.get(algorithm_type, {})
