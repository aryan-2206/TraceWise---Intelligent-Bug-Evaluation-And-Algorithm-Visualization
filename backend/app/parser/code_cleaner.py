import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CodeCleaner:
    """Clean and preprocess code for analysis"""
    
    def __init__(self):
        self.comment_patterns = {
            'python': r'#.*$',
            'javascript': r'//.*$|/\*[\s\S]*?\*/',
            'cpp': r'//.*$|/\*[\s\S]*?\*/'
        }
        
        self.whitespace_patterns = {
            'python': r'\n\s*\n',
            'javascript': r'\n\s*\n',
            'cpp': r'\n\s*\n'
        }
    
    def clean(self, code: str, language: str) -> str:
        """Clean code by removing comments and normalizing whitespace"""
        
        try:
            cleaned = code
            
            # Remove comments
            if language in self.comment_patterns:
                comment_pattern = self.comment_patterns[language]
                cleaned = re.sub(comment_pattern, '', cleaned, flags=re.MULTILINE)
            
            # Normalize whitespace
            cleaned = re.sub(r'\t', '    ', cleaned)  # Convert tabs to spaces
            cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Remove excessive blank lines
            cleaned = cleaned.strip()  # Remove leading/trailing whitespace
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning code: {str(e)}")
            return code  # Return original code if cleaning fails
    
    def normalize_indentation(self, code: str, language: str) -> str:
        """Normalize code indentation"""
        
        try:
            lines = code.split('\n')
            normalized_lines = []
            
            for line in lines:
                if line.strip():  # Skip empty lines
                    # Count leading spaces
                    leading_spaces = len(line) - len(line.lstrip())
                    # Normalize to 4 spaces per indent level
                    indent_level = leading_spaces // 4
                    normalized_line = '    ' * indent_level + line.strip()
                    normalized_lines.append(normalized_line)
                else:
                    normalized_lines.append('')
            
            return '\n'.join(normalized_lines)
            
        except Exception as e:
            logger.error(f"Error normalizing indentation: {str(e)}")
            return code
    
    def extract_functions(self, code: str, language: str) -> list:
        """Extract function definitions from code"""
        
        try:
            functions = []
            
            if language == 'python':
                # Python function pattern
                pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:'
                matches = re.finditer(pattern, code)
                for match in matches:
                    functions.append({
                        'name': match.group(1),
                        'line': code[:match.start()].count('\n') + 1,
                        'type': 'function'
                    })
            
            elif language == 'javascript':
                # JavaScript function patterns
                patterns = [
                    r'function\s+(\w+)\s*\([^)]*\)\s*{',
                    r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
                    r'let\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{'
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, code)
                    for match in matches:
                        functions.append({
                            'name': match.group(1),
                            'line': code[:match.start()].count('\n') + 1,
                            'type': 'function'
                        })
            
            elif language == 'cpp':
                # C++ function pattern
                pattern = r'(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*\{'
                matches = re.finditer(pattern, code)
                for match in matches:
                    functions.append({
                        'name': match.group(1),
                        'line': code[:match.start()].count('\n') + 1,
                        'type': 'function'
                    })
            
            return functions
            
        except Exception as e:
            logger.error(f"Error extracting functions: {str(e)}")
            return []
    
    def remove_strings(self, code: str, language: str) -> str:
        """Remove string literals from code for pattern matching"""
        
        try:
            # Remove string literals (single and double quotes)
            code_without_strings = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '', code)
            return code_without_strings
            
        except Exception as e:
            logger.error(f"Error removing strings: {str(e)}")
            return code
