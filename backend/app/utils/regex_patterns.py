import re
from typing import Dict, List, Pattern

class RegexPatterns:
    """Centralized regex patterns for code analysis"""
    
    # Python patterns
    PYTHON_PATTERNS = {
        'function_def': r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*:',
        'class_def': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\([^)]*\))?\s*:',
        'import': r'(?:from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import\s+([a-zA-Z_][a-zA-Z0-9_,\s]*)|import\s+([a-zA-Z_][a-zA-Z0-9_.\s]*))',
        'variable_assignment': r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^#\n]+)',
        'for_loop': r'for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+([^:]+):',
        'while_loop': r'while\s+([^:]+):',
        'if_statement': r'if\s+([^:]+):',
        'elif_statement': r'elif\s+([^:]+):',
        'else_statement': r'else:',
        'try_statement': r'try:',
        'except_statement': r'except\s*(?:\([^)]*\))?\s*([a-zA-Z_][a-zA-Z0-9_]*)?:',
        'return_statement': r'return\s+([^#\n]+)',
        'comment': r'#.*$',
        'string_literal': r'(["\'])(?:(?=(\\?))\2.)*?\1',
        'number': r'\b\d+\.?\d*\b',
        'boolean': r'\b(True|False)\b',
        'none': r'\bNone\b',
        'list_comprehension': r'\[.*for.*in.*\]',
        'dict_comprehension': r'\{.*:.*for.*in.*\}',
        'decorator': r'@[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*',
        'lambda': r'lambda\s+[^:]+:\s*[^#\n]+',
        'list_literal': r'\[([^\]]*)\]',
        'dict_literal': r'\{([^}]*)\}',
        'tuple_literal': r'\(([^)]*)\)',
        'set_literal': r'\{([^}]*)\}'
    }
    
    # JavaScript patterns
    JAVASCRIPT_PATTERNS = {
        'function_def': r'(?:function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*\{|const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:function\s*\([^)]*\)\s*\{|\([^)]*\)\s*=>\s*\{)|let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:function\s*\([^)]*\)\s*\{|\([^)]*\)\s*=>\s*\{))',
        'class_def': r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:extends\s+([a-zA-Z_$][a-zA-Z0-9_$]*))?\s*\{',
        'import': r'(?:import\s+(?:\{[^}]*\}|\*\s+as\s+[a-zA-Z_$][a-zA-Z0-9_$]*|[a-zA-Z_$][a-zA-Z0-9_$]*)\s+from\s+["\']([^"\']+)["\']|const\s+([^=]+)\s*=\s*require\s*\(["\']([^"\']+)["\']))',
        'variable_assignment': r'(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*([^;]+)',
        'for_loop': r'for\s*\([^)]*\)',
        'while_loop': r'while\s*\([^)]*\)',
        'if_statement': r'if\s*\([^)]*\)',
        'else_if_statement': r'else\s+if\s*\([^)]*\)',
        'else_statement': r'else',
        'try_statement': r'try\s*\{',
        'catch_statement': r'catch\s*\([^)]*\)\s*\{',
        'return_statement': r'return\s+([^;]+)',
        'comment': r'//.*$|/\*[\s\S]*?\*/',
        'string_literal': r'(["\'])(?:(?=(\\?))\2.)*?\1',
        'template_literal': r'`[^`]*`',
        'number': r'\b\d+\.?\d*\b',
        'boolean': r'\b(true|false)\b',
        'null_undefined': r'\b(null|undefined)\b',
        'arrow_function': r'\([^)]*\)\s*=>\s*[^{]*',
        'object_literal': r'\{([^}]*)\}',
        'array_literal': r'\[([^\]]*)\]',
        'method_call': r'\.([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(',
        'property_access': r'\.([a-zA-Z_$][a-zA-Z0-9_$]*)'
    }
    
    # C++ patterns
    CPP_PATTERNS = {
        'function_def': r'(?:\w+\s+)*([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:const\s*)?\{',
        'class_def': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::\s*(?:public|private|protected)\s+[a-zA-Z_][a-zA-Z0-9_]*)?\s*\{',
        'include': r'#include\s*[<"]([^>"]+)[>"]',
        'using_namespace': r'using\s+namespace\s+([a-zA-Z_][a-zA-Z0-9_:]*)',
        'variable_declaration': r'(?:\w+\s+)+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*([^;]+))?;',
        'for_loop': r'for\s*\([^)]*\)',
        'while_loop': r'while\s*\([^)]*\)',
        'if_statement': r'if\s*\([^)]*\)',
        'else_if_statement': r'else\s+if\s*\([^)]*\)',
        'else_statement': r'else',
        'try_statement': r'try\s*\{',
        'catch_statement': r'catch\s*\([^)]*\)\s*\{',
        'return_statement': r'return\s+([^;]+)',
        'comment': r'//.*$|/\*[\s\S]*?\*/',
        'string_literal': r'(["\'])(?:(?=(\\?))\2.)*?\1',
        'char_literal': r'\'([^\']*)\'',
        'number': r'\b\d+\.?\d*[fFlL]?\b',
        'boolean': r'\b(true|false)\b',
        'pointer_declaration': r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*)',
        'reference_declaration': r'([a-zA-Z_][a-zA-Z0-9_]*)\s*&\s*([a-zA-Z_][a-zA-Z0-9_]*)',
        'template_declaration': r'template\s*<[^>]*>',
        'namespace': r'namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\{'
    }
    
    # Algorithm-specific patterns
    ALGORITHM_PATTERNS = {
        'binary_search': {
            'keywords': [r'binary', r'search', r'left', r'right', r'mid'],
            'structures': [
                r'while\s+.*<=.*',
                r'mid\s*=\s*.*[+\-].*/\s*2',
                r'if\s+.*\[.*\]\s*==\s*',
                r'left\s*=\s*mid\s*[+\-]\s*1',
                r'right\s*=\s*mid\s*[+\-]\s*1'
            ]
        },
        'bubble_sort': {
            'keywords': [r'bubble', r'sort', r'swap'],
            'structures': [
                r'for\s+.*for\s+.*',
                r'if\s+.*[<>].*',
                r'swap|.*=.*;.*=.*;.*=.*'
            ]
        },
        'selection_sort': {
            'keywords': [r'selection', r'sort', r'min', r'index'],
            'structures': [
                r'for\s+.*for\s+.*',
                r'min_index\s*=',
                r'if\s+.*\[.*\]\s*<\s*.*\[.*\]'
            ]
        },
        'insertion_sort': {
            'keywords': [r'insertion', r'sort', r'key'],
            'structures': [
                r'key\s*=',
                r'while\s+.*>\s*0',
                r'arr\[.*\]\s*=\s*arr\[.*\s*-\s*1\]'
            ]
        },
        'quick_sort': {
            'keywords': [r'quick', r'sort', r'partition', r'pivot'],
            'structures': [
                r'pivot\s*=',
                r'partition',
                r'quick_sort\s*\('
            ]
        },
        'merge_sort': {
            'keywords': [r'merge', r'sort', r'merge_sort'],
            'structures': [
                r'merge_sort\s*\(',
                r'merge\s*\(',
                r'left.*right'
            ]
        },
        'dfs': {
            'keywords': [r'dfs', r'depth', r'search', r'stack', r'visited'],
            'structures': [
                r'dfs\s*\(',
                r'visited\s*=',
                r'stack\s*='
            ]
        },
        'bfs': {
            'keywords': [r'bfs', r'breadth', r'search', r'queue', r'visited'],
            'structures': [
                r'bfs\s*\(',
                r'queue\s*=',
                r'visited\s*='
            ]
        },
        'dijkstra': {
            'keywords': [r'dijkstra', r'shortest', r'path', r'distance', r'priority'],
            'structures': [
                r'dijkstra\s*\(',
                r'distance\s*=',
                r'priority_queue|heap'
            ]
        }
    }
    
    # Bug detection patterns
    BUG_PATTERNS = {
        'infinite_loop': [
            r'while\s+True\s*:\s*\n(?!.*break)',
            r'for\s+.*\s*in\s+.*:\s*\n.*i\s*=',
            r'while\s+.*<\s*.*:\s*\n.*\+\s*0'
        ],
        'off_by_one': [
            r'for\s+i\s+in\s+range\s*\(\s*len\s*\(\s*arr\s*\)\s*\)',
            r'arr\[len\s*\(\s*arr\s*\)\]',
            r'arr\[.*\.length\]'
        ],
        'memory_leak': [
            r'new\s+\w+',
            r'malloc\s*\(',
            r'calloc\s*\('
        ],
        'null_pointer': [
            r'\*\s*[a-zA-Z_][a-zA-Z0-9_]*(?!\s*=)',
            r'->\s*[a-zA-Z_][a-zA-Z0-9_]*(?!\s*=)'
        ],
        'division_by_zero': [
            r'/\s*0',
            r'/\s*zero',
            r'/\s*null'
        ],
        'security_issues': [
            r'eval\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\('
        ],
        'performance_issues': [
            r'for\s+.*:\s*\n.*for\s+.*:',
            r'\.append\s*\(\s*\)\s*inside\s+loop',
            r'len\s*\(\s*.*\s*\)\s*inside\s+loop'
        ]
    }
    
    # Quality patterns
    QUALITY_PATTERNS = {
        'long_line': r'.{81,}',  # Lines longer than 80 characters
        'trailing_whitespace': r'.+\s+$',
        'multiple_empty_lines': r'\n\s*\n\s*\n+',
        'tab_character': r'\t',
        'magic_number': r'\b(?<![\w.])[-+]?(?!0|1| -1)\d+(?![\w.])\b',
        'todo_comment': r'//.*?(TODO|FIXME|HACK|XXX).*|/\*.*?(TODO|FIXME|HACK|XXX).*?\*/|#.*?(TODO|FIXME|HACK|XXX).*',
        'debug_statement': [
            r'print\s*\(',
            r'console\.log',
            r'cout\s*<<',
            r'System\.out\.print',
            r'alert\s*\('
        ],
        'hardcoded_url': r'["\']http[s]?://[^"\']+["\']',
        'hardcoded_email': r'["\'][\w.-]+@[\w.-]+\.\w+["\']',
        'hardcoded_ip': r'["\']\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}["\']'
    }
    
    @classmethod
    def get_patterns(cls, language: str) -> Dict[str, Pattern]:
        """Get compiled regex patterns for a language"""
        
        try:
            if language == 'python':
                return {name: re.compile(pattern) for name, pattern in cls.PYTHON_PATTERNS.items()}
            elif language == 'javascript':
                return {name: re.compile(pattern) for name, pattern in cls.JAVASCRIPT_PATTERNS.items()}
            elif language == 'cpp':
                return {name: re.compile(pattern) for name, pattern in cls.CPP_PATTERNS.items()}
            else:
                return {}
                
        except Exception as e:
            print(f"Error getting patterns for {language}: {str(e)}")
            return {}
    
    @classmethod
    def get_algorithm_patterns(cls, algorithm: str) -> Dict[str, List[Pattern]]:
        """Get patterns for specific algorithm detection"""
        
        try:
            if algorithm in cls.ALGORITHM_PATTERNS:
                patterns = cls.ALGORITHM_PATTERNS[algorithm]
                compiled = {}
                
                if 'keywords' in patterns:
                    compiled['keywords'] = [re.compile(keyword) for keyword in patterns['keywords']]
                
                if 'structures' in patterns:
                    compiled['structures'] = [re.compile(structure) for structure in patterns['structures']]
                
                return compiled
            
            return {}
            
        except Exception as e:
            print(f"Error getting algorithm patterns for {algorithm}: {str(e)}")
            return {}
    
    @classmethod
    def get_bug_patterns(cls) -> Dict[str, List[Pattern]]:
        """Get bug detection patterns"""
        
        try:
            compiled = {}
            for category, patterns in cls.BUG_PATTERNS.items():
                if isinstance(patterns, list):
                    compiled[category] = [re.compile(pattern) for pattern in patterns]
                else:
                    compiled[category] = [re.compile(patterns)]
            
            return compiled
            
        except Exception as e:
            print(f"Error getting bug patterns: {str(e)}")
            return {}
    
    @classmethod
    def get_quality_patterns(cls) -> Dict[str, Pattern]:
        """Get code quality patterns"""
        
        try:
            compiled = {}
            for name, pattern in cls.QUALITY_PATTERNS.items():
                if isinstance(pattern, list):
                    compiled[name] = [re.compile(p) for p in pattern]
                else:
                    compiled[name] = re.compile(pattern)
            
            return compiled
            
        except Exception as e:
            print(f"Error getting quality patterns: {str(e)}")
            return {}
    
    @classmethod
    def find_all_matches(cls, text: str, pattern: Pattern) -> List[re.Match]:
        """Find all matches of a pattern in text"""
        
        try:
            return list(pattern.finditer(text))
            
        except Exception as e:
            print(f"Error finding matches: {str(e)}")
            return []
    
    @classmethod
    def count_matches(cls, text: str, pattern: Pattern) -> int:
        """Count matches of a pattern in text"""
        
        try:
            return len(cls.find_all_matches(text, pattern))
            
        except Exception as e:
            print(f"Error counting matches: {str(e)}")
            return 0
    
    @classmethod
    def extract_groups(cls, text: str, pattern: Pattern) -> List[str]:
        """Extract all groups from pattern matches"""
        
        try:
            matches = cls.find_all_matches(text, pattern)
            groups = []
            
            for match in matches:
                if match.groups():
                    groups.extend(match.groups())
                else:
                    groups.append(match.group(0))
            
            return groups
            
        except Exception as e:
            print(f"Error extracting groups: {str(e)}")
            return []
    
    @classmethod
    def validate_pattern(cls, pattern: str) -> bool:
        """Validate if a regex pattern is valid"""
        
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
