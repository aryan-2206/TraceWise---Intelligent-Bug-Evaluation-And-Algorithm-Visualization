import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class StructureExtractor:
    """Extract structural information from code"""
    
    def __init__(self):
        self.function_patterns = {
            'python': r'def\s+(\w+)\s*\([^)]*\)\s*:',
            'javascript': r'(?:function\s+(\w+)\s*\([^)]*\)\s*\{|(?:const|let|var)\s+(\w+)\s*=\s*(?:function\s*\([^)]*\)\s*\{|\([^)]*\)\s*=>\s*\{))',
            'cpp': r'(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*\{'
        }
        
        self.class_patterns = {
            'python': r'class\s+(\w+)\s*(?:\([^)]*\))?\s*:',
            'javascript': r'class\s+(\w+)\s*(?:extends\s+\w+)?\s*\{',
            'cpp': r'class\s+(\w+)\s*(?::\s*(?:public|private|protected)\s+\w+)?\s*\{'
        }
        
        self.loop_patterns = {
            'python': r'\b(for|while)\s+',
            'javascript': r'\b(for|while)\s+',
            'cpp': r'\b(for|while)\s+'
        }
        
        self.conditional_patterns = {
            'python': r'\b(if|elif|else)\s+',
            'javascript': r'\b(if|else\s+if|else)\s+',
            'cpp': r'\b(if|else\s+if|else)\s+'
        }
    
    def extract(self, code: str, language: str, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract structural information from code"""
        
        try:
            structure = {
                'functions': self.extract_functions(code, language),
                'classes': self.extract_classes(code, language),
                'loops': self.extract_loops(code, language),
                'conditionals': self.extract_conditionals(code, language),
                'imports': self.extract_imports(code, language),
                'variables': self.extract_variables(code, language, tokens),
                'complexity_indicators': self.extract_complexity_indicators(code, language),
                'nesting_level': self.calculate_max_nesting_level(code, language)
            }
            
            return structure
            
        except Exception as e:
            logger.error(f"Error extracting structure: {str(e)}")
            return {}
    
    def extract_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract function definitions"""
        
        try:
            functions = []
            
            if language in self.function_patterns:
                pattern = self.function_patterns[language]
                matches = re.finditer(pattern, code, re.MULTILINE)
                
                for match in matches:
                    func_name = match.group(1) if match.group(1) else match.group(2)
                    start_line = code[:match.start()].count('\n') + 1
                    
                    # Find function body (simplified)
                    func_body_start = match.end()
                    func_body = self.extract_block_body(code, func_body_start, language)
                    
                    functions.append({
                        'name': func_name,
                        'line': start_line,
                        'body': func_body,
                        'parameters': self.extract_parameters(match.group(0)),
                        'complexity': self.calculate_function_complexity(func_body)
                    })
            
            return functions
            
        except Exception as e:
            logger.error(f"Error extracting functions: {str(e)}")
            return []
    
    def extract_classes(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract class definitions"""
        
        try:
            classes = []
            
            if language in self.class_patterns:
                pattern = self.class_patterns[language]
                matches = re.finditer(pattern, code, re.MULTILINE)
                
                for match in matches:
                    class_name = match.group(1)
                    start_line = code[:match.start()].count('\n') + 1
                    
                    # Find class body (simplified)
                    class_body_start = match.end()
                    class_body = self.extract_block_body(code, class_body_start, language)
                    
                    classes.append({
                        'name': class_name,
                        'line': start_line,
                        'body': class_body,
                        'methods': self.extract_methods_from_class(class_body, language)
                    })
            
            return classes
            
        except Exception as e:
            logger.error(f"Error extracting classes: {str(e)}")
            return []
    
    def extract_loops(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract loop structures"""
        
        try:
            loops = []
            
            if language in self.loop_patterns:
                pattern = self.loop_patterns[language]
                matches = re.finditer(pattern, code, re.MULTILINE)
                
                for match in matches:
                    loop_type = match.group(1)
                    start_line = code[:match.start()].count('\n') + 1
                    
                    loops.append({
                        'type': loop_type,
                        'line': start_line,
                        'nested': self.is_nested_structure(code, match.start())
                    })
            
            return loops
            
        except Exception as e:
            logger.error(f"Error extracting loops: {str(e)}")
            return []
    
    def extract_conditionals(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract conditional statements"""
        
        try:
            conditionals = []
            
            if language in self.conditional_patterns:
                pattern = self.conditional_patterns[language]
                matches = re.finditer(pattern, code, re.MULTILINE)
                
                for match in matches:
                    conditional_type = match.group(1)
                    start_line = code[:match.start()].count('\n') + 1
                    
                    conditionals.append({
                        'type': conditional_type,
                        'line': start_line,
                        'nested': self.is_nested_structure(code, match.start())
                    })
            
            return conditionals
            
        except Exception as e:
            logger.error(f"Error extracting conditionals: {str(e)}")
            return []
    
    def extract_imports(self, code: str, language: str) -> List[str]:
        """Extract import statements"""
        
        try:
            imports = []
            
            if language == 'python':
                pattern = r'(?:import\s+([^#\n]+)|from\s+([^#\s]+)\s+import\s+([^#\n]+))'
                matches = re.finditer(pattern, code, re.MULTILINE)
                for match in matches:
                    if match.group(1):
                        imports.append(match.group(1).strip())
                    elif match.group(2):
                        imports.append(match.group(2).strip())
            
            elif language == 'javascript':
                pattern = r'(?:import\s+.*?from\s+["\']([^"\']+)["\']|const\s+.*?=\s*require\(["\']([^"\']+)["\']\))'
                matches = re.finditer(pattern, code, re.MULTILINE)
                for match in matches:
                    module_name = match.group(1) or match.group(2)
                    imports.append(module_name.strip())
            
            elif language == 'cpp':
                pattern = r'#include\s*[<"]([^>"]+)[>"]'
                matches = re.finditer(pattern, code, re.MULTILINE)
                for match in matches:
                    imports.append(match.group(1).strip())
            
            return imports
            
        except Exception as e:
            logger.error(f"Error extracting imports: {str(e)}")
            return []
    
    def extract_variables(self, code: str, language: str, tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract variable declarations"""
        
        try:
            variables = []
            
            # Extract from tokens for more accurate results
            for i, token in enumerate(tokens):
                if token['type'] == 'keyword' and token['value'] in ['var', 'let', 'const']:
                    # JavaScript variable declaration
                    if i + 1 < len(tokens) and tokens[i + 1]['type'] == 'identifier':
                        variables.append({
                            'name': tokens[i + 1]['value'],
                            'type': token['value'],
                            'line': token['line']
                        })
                elif token['type'] == 'identifier':
                    # Check if this is a variable assignment (simplified)
                    if (i + 1 < len(tokens) and 
                        tokens[i + 1]['value'] in ['=', ':='] and
                        token['value'] not in ['if', 'for', 'while', 'def', 'class']):
                        variables.append({
                            'name': token['value'],
                            'type': 'unknown',
                            'line': token['line']
                        })
            
            return variables
            
        except Exception as e:
            logger.error(f"Error extracting variables: {str(e)}")
            return []
    
    def extract_complexity_indicators(self, code: str, language: str) -> Dict[str, int]:
        """Extract indicators of code complexity"""
        
        try:
            indicators = {
                'nested_loops': 0,
                'recursive_calls': 0,
                'multiple_returns': 0,
                'complex_conditions': 0
            }
            
            # Count nested loops
            lines = code.split('\n')
            loop_depth = 0
            max_loop_depth = 0
            
            for line in lines:
                stripped = line.strip()
                if any(keyword in stripped for keyword in ['for ', 'while ']):
                    loop_depth += 1
                    max_loop_depth = max(max_loop_depth, loop_depth)
                elif stripped in ['}', 'pass', 'break', 'continue']:
                    loop_depth = max(0, loop_depth - 1)
            
            indicators['nested_loops'] = max_loop_depth
            
            # Count recursive calls (simplified)
            function_names = re.findall(r'def\s+(\w+)\s*\(', code) if language == 'python' else []
            for func_name in function_names:
                pattern = rf'\b{func_name}\s*\('
                calls = len(re.findall(pattern, code))
                indicators['recursive_calls'] += max(0, calls - 1)  # Subtract 1 for the definition
            
            # Count multiple returns
            return_count = len(re.findall(r'\breturn\b', code))
            indicators['multiple_returns'] = max(0, return_count - 1)
            
            # Count complex conditions (multiple && or ||)
            complex_cond_pattern = r'(&&|\|\||and\s+|or\s+).*(&&|\|\||and\s+|or\s+)'
            indicators['complex_conditions'] = len(re.findall(complex_cond_pattern, code))
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error extracting complexity indicators: {str(e)}")
            return {}
    
    def calculate_max_nesting_level(self, code: str, language: str) -> int:
        """Calculate maximum nesting level in the code"""
        
        try:
            lines = code.split('\n')
            max_depth = 0
            current_depth = 0
            
            for line in lines:
                stripped = line.strip()
                
                # Increase depth for opening structures
                if any(keyword in stripped for keyword in ['if ', 'for ', 'while ', 'try:', 'def ', 'class ']):
                    current_depth += 1
                    max_depth = max(max_depth, current_depth)
                
                # Decrease depth for closing structures (simplified)
                if (language == 'python' and stripped and not stripped.startswith(' ') and not stripped.startswith('\t')) or \
                   (language in ['javascript', 'cpp'] and stripped == '}'):
                    current_depth = max(0, current_depth - 1)
            
            return max_depth
            
        except Exception as e:
            logger.error(f"Error calculating nesting level: {str(e)}")
            return 0
    
    def extract_parameters(self, function_signature: str) -> List[str]:
        """Extract parameter names from function signature"""
        
        try:
            param_match = re.search(r'\(([^)]*)\)', function_signature)
            if param_match:
                params = param_match.group(1)
                return [p.strip().split('=')[0].strip() for p in params.split(',') if p.strip()]
            return []
            
        except Exception as e:
            logger.error(f"Error extracting parameters: {str(e)}")
            return []
    
    def extract_block_body(self, code: str, start_pos: int, language: str) -> str:
        """Extract the body of a code block (simplified implementation)"""
        
        try:
            # This is a simplified implementation
            # In practice, you'd want to parse the code more carefully
            remaining_code = code[start_pos:]
            lines = remaining_code.split('\n')
            
            body_lines = []
            indent_level = None
            
            for line in lines:
                if line.strip():
                    if indent_level is None:
                        indent_level = len(line) - len(line.lstrip())
                    
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent_level and body_lines:
                        break
                    
                    body_lines.append(line)
            
            return '\n'.join(body_lines)
            
        except Exception as e:
            logger.error(f"Error extracting block body: {str(e)}")
            return ''
    
    def extract_methods_from_class(self, class_body: str, language: str) -> List[Dict[str, Any]]:
        """Extract methods from a class body"""
        
        try:
            # Use the same function extraction logic but limit to class body
            return self.extract_functions(class_body, language)
            
        except Exception as e:
            logger.error(f"Error extracting methods from class: {str(e)}")
            return []
    
    def calculate_function_complexity(self, function_body: str) -> int:
        """Calculate cyclomatic complexity of a function"""
        
        try:
            complexity = 1  # Base complexity
            
            # Add complexity for decision points
            decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'case', '&&', '||', 'and', 'or']
            
            for keyword in decision_keywords:
                complexity += len(re.findall(r'\b' + keyword + r'\b', function_body))
            
            return complexity
            
        except Exception as e:
            logger.error(f"Error calculating function complexity: {str(e)}")
            return 1
    
    def is_nested_structure(self, code: str, position: int) -> bool:
        """Check if a structure is nested within another"""
        
        try:
            before_position = code[:position]
            # Count opening vs closing structures before this position
            opens = len(re.findall(r'[\{\(]', before_position))
            closes = len(re.findall(r'[\}\)]', before_position))
            return opens > closes
            
        except Exception as e:
            logger.error(f"Error checking if structure is nested: {str(e)}")
            return False
