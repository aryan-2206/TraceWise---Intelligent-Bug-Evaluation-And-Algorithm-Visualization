import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class QualityAnalyzer:
    """Analyze code quality metrics"""
    
    def __init__(self):
        self.quality_metrics = {
            'readability': {
                'line_length': 80,
                'function_length': 50,
                'complexity_threshold': 10
            },
            'maintainability': {
                'max_nesting': 4,
                'max_parameters': 5,
                'max_functions': 20
            },
            'documentation': {
                'requires_docstrings': True,
                'min_comment_ratio': 0.1
            }
        }
    
    def analyze(self, code: str, structure: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Analyze code quality across multiple dimensions"""
        
        try:
            quality_report = {
                'overall_score': 0,
                'readability': self._analyze_readability(code, language),
                'maintainability': self._analyze_maintainability(code, structure, language),
                'documentation': self._analyze_documentation(code, language),
                'complexity': self._analyze_complexity(code, structure, language),
                'style': self._analyze_style(code, language),
                'best_practices': self._analyze_best_practices(code, structure, language)
            }
            
            # Calculate overall score
            quality_report['overall_score'] = self._calculate_overall_score(quality_report)
            
            return quality_report
            
        except Exception as e:
            logger.error(f"Error analyzing code quality: {str(e)}")
            return {
                'overall_score': 0,
                'readability': {'score': 0, 'issues': []},
                'maintainability': {'score': 0, 'issues': []},
                'documentation': {'score': 0, 'issues': []},
                'complexity': {'score': 0, 'issues': []},
                'style': {'score': 0, 'issues': []},
                'best_practices': {'score': 0, 'issues': []}
            }
    
    def _analyze_readability(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code readability"""
        
        try:
            issues = []
            score = 100
            lines = code.split('\n')
            
            # Check line length
            max_line_length = self.quality_metrics['readability']['line_length']
            long_lines = []
            for i, line in enumerate(lines, 1):
                if len(line) > max_line_length:
                    long_lines.append(i)
                    if len(line) > max_line_length * 1.5:
                        score -= 5
                    else:
                        score -= 2
            
            if long_lines:
                issues.append({
                    'type': 'long_lines',
                    'message': f'{len(long_lines)} lines exceed {max_line_length} characters',
                    'lines': long_lines[:10],  # Show first 10
                    'suggestion': 'Break long lines into multiple lines'
                })
            
            # Check function length
            functions = self._extract_functions(code, language)
            max_func_length = self.quality_metrics['readability']['function_length']
            long_functions = []
            
            for func in functions:
                func_lines = len(func['body'].split('\n'))
                if func_lines > max_func_length:
                    long_functions.append({
                        'name': func['name'],
                        'lines': func_lines,
                        'line': func.get('line', 0)
                    })
                    score -= min(10, func_lines // 10)
            
            if long_functions:
                issues.append({
                    'type': 'long_functions',
                    'message': f'{len(long_functions)} functions exceed {max_func_length} lines',
                    'functions': long_functions[:5],  # Show first 5
                    'suggestion': 'Break large functions into smaller, more focused functions'
                })
            
            # Check naming conventions
            naming_issues = self._check_naming_conventions(code, language)
            issues.extend(naming_issues)
            score -= len(naming_issues) * 3
            
            # Check for magic numbers
            magic_numbers = self._find_magic_numbers(code)
            if magic_numbers:
                issues.append({
                    'type': 'magic_numbers',
                    'message': f'{len(magic_numbers)} magic numbers found',
                    'numbers': magic_numbers[:10],
                    'suggestion': 'Replace magic numbers with named constants'
                })
                score -= len(magic_numbers) * 2
            
            return {
                'score': max(0, score),
                'issues': issues,
                'metrics': {
                    'total_lines': len(lines),
                    'long_lines': len(long_lines),
                    'functions_count': len(functions),
                    'long_functions': len(long_functions)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing readability: {str(e)}")
            return {'score': 0, 'issues': []}
    
    def _analyze_maintainability(self, code: str, structure: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Analyze code maintainability"""
        
        try:
            issues = []
            score = 100
            
            # Check nesting level
            max_nesting = self.quality_metrics['maintainability']['max_nesting']
            actual_nesting = structure.get('nesting_level', 0)
            
            if actual_nesting > max_nesting:
                issues.append({
                    'type': 'deep_nesting',
                    'message': f'Maximum nesting level ({actual_nesting}) exceeds recommended ({max_nesting})',
                    'suggestion': 'Reduce nesting by extracting functions or using early returns'
                })
                score -= (actual_nesting - max_nesting) * 10
            
            # Check function parameters
            functions = self._extract_functions(code, language)
            max_params = self.quality_metrics['maintainability']['max_parameters']
            functions_with_many_params = []
            
            for func in functions:
                param_count = len(func.get('parameters', []))
                if param_count > max_params:
                    functions_with_many_params.append({
                        'name': func['name'],
                        'parameters': param_count,
                        'line': func.get('line', 0)
                    })
                    score -= 5
            
            if functions_with_many_params:
                issues.append({
                    'type': 'too_many_parameters',
                    'message': f'{len(functions_with_many_params)} functions have too many parameters',
                    'functions': functions_with_many_params,
                    'suggestion': 'Consider using parameter objects or configuration dictionaries'
                })
            
            # Check code duplication (simplified)
            duplication_score = self._check_code_duplication(code)
            if duplication_score < 80:
                issues.append({
                    'type': 'code_duplication',
                    'message': 'Code duplication detected',
                    'suggestion': 'Extract duplicated code into reusable functions'
                })
                score -= (100 - duplication_score) // 2
            
            # Check function count
            max_functions = self.quality_metrics['maintainability']['max_functions']
            function_count = len(functions)
            
            if function_count > max_functions:
                issues.append({
                    'type': 'too_many_functions',
                    'message': f'Too many functions ({function_count}) in single file',
                    'suggestion': 'Consider splitting into multiple modules'
                })
                score -= (function_count - max_functions) * 2
            
            return {
                'score': max(0, score),
                'issues': issues,
                'metrics': {
                    'nesting_level': actual_nesting,
                    'function_count': function_count,
                    'functions_with_many_params': len(functions_with_many_params),
                    'duplication_score': duplication_score
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing maintainability: {str(e)}")
            return {'score': 0, 'issues': []}
    
    def _analyze_documentation(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code documentation"""
        
        try:
            issues = []
            score = 100
            lines = code.split('\n')
            
            # Check comment ratio
            comment_lines = 0
            code_lines = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped:
                    if self._is_comment_line(stripped, language):
                        comment_lines += 1
                    else:
                        code_lines += 1
            
            if code_lines > 0:
                comment_ratio = comment_lines / code_lines
                min_ratio = self.quality_metrics['documentation']['min_comment_ratio']
                
                if comment_ratio < min_ratio:
                    issues.append({
                        'type': 'insufficient_comments',
                        'message': f'Comment ratio ({comment_ratio:.2%}) below recommended ({min_ratio:.2%})',
                        'suggestion': 'Add more comments to explain complex logic'
                    })
                    score -= int((min_ratio - comment_ratio) * 200)
            
            # Check for missing docstrings (Python)
            if language == 'python':
                functions = self._extract_functions(code, language)
                functions_without_docstrings = []
                
                for func in functions:
                    if not self._has_docstring(func['body']):
                        functions_without_docstrings.append({
                            'name': func['name'],
                            'line': func.get('line', 0)
                        })
                
                if functions_without_docstrings:
                    issues.append({
                        'type': 'missing_docstrings',
                        'message': f'{len(functions_without_docstrings)} functions missing docstrings',
                        'functions': functions_without_docstrings,
                        'suggestion': 'Add docstrings to all functions'
                    })
                    score -= len(functions_without_docstrings) * 5
            
            # Check for TODO/FIXME comments
            todo_comments = self._find_todo_comments(code)
            if todo_comments:
                issues.append({
                    'type': 'todo_comments',
                    'message': f'{len(todo_comments)} TODO/FIXME comments found',
                    'comments': todo_comments,
                    'suggestion': 'Address TODO items or convert to proper issues'
                })
                score -= len(todo_comments) * 2
            
            return {
                'score': max(0, score),
                'issues': issues,
                'metrics': {
                    'comment_lines': comment_lines,
                    'code_lines': code_lines,
                    'comment_ratio': comment_lines / max(code_lines, 1),
                    'todo_count': len(todo_comments)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing documentation: {str(e)}")
            return {'score': 0, 'issues': []}
    
    def _analyze_complexity(self, code: str, structure: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        
        try:
            issues = []
            score = 100
            
            # Calculate cyclomatic complexity
            complexity_indicators = structure.get('complexity_indicators', {})
            
            # Check nested loops
            nested_loops = complexity_indicators.get('nested_loops', 0)
            if nested_loops > 2:
                issues.append({
                    'type': 'high_nesting',
                    'message': f'High nesting level ({nested_loops}) detected',
                    'suggestion': 'Consider refactoring to reduce nesting'
                })
                score -= (nested_loops - 2) * 15
            
            # Check recursive calls
            recursive_calls = complexity_indicators.get('recursive_calls', 0)
            if recursive_calls > 0:
                issues.append({
                    'type': 'recursion',
                    'message': f'Recursive calls detected ({recursive_calls})',
                    'suggestion': 'Ensure proper base cases to prevent stack overflow'
                })
                score -= recursive_calls * 5
            
            # Check multiple returns
            multiple_returns = complexity_indicators.get('multiple_returns', 0)
            if multiple_returns > 3:
                issues.append({
                    'type': 'multiple_returns',
                    'message': f'Multiple return statements ({multiple_returns}) may reduce readability',
                    'suggestion': 'Consider restructuring to reduce multiple exit points'
                })
                score -= (multiple_returns - 3) * 3
            
            # Check complex conditions
            complex_conditions = complexity_indicators.get('complex_conditions', 0)
            if complex_conditions > 2:
                issues.append({
                    'type': 'complex_conditions',
                    'message': f'Complex conditional logic detected ({complex_conditions} instances)',
                    'suggestion': 'Break complex conditions into separate variables or functions'
                })
                score -= complex_conditions * 4
            
            # Calculate cognitive complexity (simplified)
            cognitive_complexity = self._calculate_cognitive_complexity(code, language)
            if cognitive_complexity > 15:
                issues.append({
                    'type': 'high_cognitive_complexity',
                    'message': f'High cognitive complexity ({cognitive_complexity})',
                    'suggestion': 'Simplify logic to improve readability'
                })
                score -= (cognitive_complexity - 15) * 2
            
            return {
                'score': max(0, score),
                'issues': issues,
                'metrics': {
                    'nested_loops': nested_loops,
                    'recursive_calls': recursive_calls,
                    'multiple_returns': multiple_returns,
                    'complex_conditions': complex_conditions,
                    'cognitive_complexity': cognitive_complexity
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing complexity: {str(e)}")
            return {'score': 0, 'issues': []}
    
    def _analyze_style(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code style and formatting"""
        
        try:
            issues = []
            score = 100
            
            # Check for consistent indentation
            indentation_issues = self._check_indentation(code, language)
            issues.extend(indentation_issues)
            score -= len(indentation_issues) * 5
            
            # Check for trailing whitespace
            trailing_whitespace = self._check_trailing_whitespace(code)
            if trailing_whitespace > 0:
                issues.append({
                    'type': 'trailing_whitespace',
                    'message': f'{trailing_whitespace} lines with trailing whitespace',
                    'suggestion': 'Remove trailing whitespace'
                })
                score -= min(10, trailing_whitespace)
            
            # Check for blank lines at end of file
            if code.endswith('\n\n') or code.endswith('\n\n\n'):
                issues.append({
                    'type': 'excessive_blank_lines',
                    'message': 'Too many blank lines at end of file',
                    'suggestion': 'End file with a single newline'
                })
                score -= 5
            
            # Check language-specific style issues
            if language == 'python':
                python_issues = self._check_python_style(code)
                issues.extend(python_issues)
                score -= len(python_issues) * 3
            elif language == 'javascript':
                js_issues = self._check_javascript_style(code)
                issues.extend(js_issues)
                score -= len(js_issues) * 3
            elif language == 'cpp':
                cpp_issues = self._check_cpp_style(code)
                issues.extend(cpp_issues)
                score -= len(cpp_issues) * 3
            
            return {
                'score': max(0, score),
                'issues': issues,
                'metrics': {
                    'indentation_issues': len(indentation_issues),
                    'trailing_whitespace': trailing_whitespace
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing style: {str(e)}")
            return {'score': 0, 'issues': []}
    
    def _analyze_best_practices(self, code: str, structure: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Analyze adherence to best practices"""
        
        try:
            issues = []
            score = 100
            
            # Check for hardcoded values
            hardcoded_values = self._find_hardcoded_values(code)
            if hardcoded_values:
                issues.append({
                    'type': 'hardcoded_values',
                    'message': f'{len(hardcoded_values)} hardcoded values found',
                    'values': hardcoded_values[:10],
                    'suggestion': 'Use configuration files or environment variables'
                })
                score -= len(hardcoded_values) * 2
            
            # Check for error handling
            error_handling = self._check_error_handling(code, language)
            if error_handling['missing']:
                issues.append({
                    'type': 'missing_error_handling',
                    'message': f'{len(error_handling["missing"])} operations lack error handling',
                    'operations': error_handling['missing'],
                    'suggestion': 'Add proper try-catch blocks or error checking'
                })
                score -= len(error_handling['missing']) * 5
            
            # Check for security best practices
            security_issues = self._check_security_practices(code, language)
            issues.extend(security_issues)
            score -= len(security_issues) * 10
            
            # Check for performance best practices
            performance_issues = self._check_performance_practices(code, language)
            issues.extend(performance_issues)
            score -= len(performance_issues) * 5
            
            return {
                'score': max(0, score),
                'issues': issues,
                'metrics': {
                    'hardcoded_values': len(hardcoded_values),
                    'missing_error_handling': len(error_handling['missing']),
                    'security_issues': len(security_issues),
                    'performance_issues': len(performance_issues)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing best practices: {str(e)}")
            return {'score': 0, 'issues': []}
    
    def _calculate_overall_score(self, quality_report: Dict[str, Any]) -> int:
        """Calculate overall quality score"""
        
        try:
            weights = {
                'readability': 0.25,
                'maintainability': 0.25,
                'documentation': 0.15,
                'complexity': 0.20,
                'style': 0.10,
                'best_practices': 0.05
            }
            
            overall_score = 0
            for category, weight in weights.items():
                category_score = quality_report.get(category, {}).get('score', 0)
                overall_score += category_score * weight
            
            return int(round(overall_score))
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 0
    
    # Helper methods
    def _extract_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract function information from code"""
        
        try:
            functions = []
            
            if language == 'python':
                pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:'
                matches = re.finditer(pattern, code)
                
                for match in matches:
                    func_name = match.group(1)
                    start_line = code[:match.start()].count('\n') + 1
                    
                    # Extract function body (simplified)
                    func_start = match.end()
                    func_body = self._extract_function_body(code, func_start, language)
                    parameters = self._extract_parameters(match.group(0))
                    
                    functions.append({
                        'name': func_name,
                        'line': start_line,
                        'body': func_body,
                        'parameters': parameters
                    })
            
            elif language == 'javascript':
                patterns = [
                    r'function\s+(\w+)\s*\([^)]*\)\s*\{',
                    r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{',
                    r'let\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{'
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, code)
                    for match in matches:
                        func_name = match.group(1)
                        start_line = code[:match.start()].count('\n') + 1
                        func_start = match.end()
                        func_body = self._extract_function_body(code, func_start, language)
                        parameters = self._extract_parameters(match.group(0))
                        
                        functions.append({
                            'name': func_name,
                            'line': start_line,
                            'body': func_body,
                            'parameters': parameters
                        })
            
            elif language == 'cpp':
                pattern = r'(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*\{'
                matches = re.finditer(pattern, code)
                
                for match in matches:
                    func_name = match.group(1)
                    start_line = code[:match.start()].count('\n') + 1
                    func_start = match.end()
                    func_body = self._extract_function_body(code, func_start, language)
                    parameters = self._extract_parameters(match.group(0))
                    
                    functions.append({
                        'name': func_name,
                        'line': start_line,
                        'body': func_body,
                        'parameters': parameters
                    })
            
            return functions
            
        except Exception as e:
            logger.error(f"Error extracting functions: {str(e)}")
            return []
    
    def _extract_function_body(self, code: str, start_pos: int, language: str) -> str:
        """Extract function body from code"""
        
        try:
            remaining_code = code[start_pos:]
            lines = remaining_code.split('\n')
            
            body_lines = []
            base_indent = None
            
            for line in lines:
                if line.strip():
                    if base_indent is None:
                        base_indent = len(line) - len(line.lstrip())
                    
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= base_indent and body_lines:
                        break
                    
                    body_lines.append(line)
                else:
                    body_lines.append(line)
            
            return '\n'.join(body_lines)
            
        except Exception as e:
            logger.error(f"Error extracting function body: {str(e)}")
            return ''
    
    def _extract_parameters(self, function_signature: str) -> List[str]:
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
    
    def _check_naming_conventions(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check naming conventions"""
        
        try:
            issues = []
            
            if language == 'python':
                # Check for camelCase (should be snake_case)
                camel_case_pattern = r'\b[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b'
                matches = re.findall(camel_case_pattern, code)
                
                for match in matches:
                    if not match[0].isupper():  # Exclude class names
                        issues.append({
                            'type': 'naming_convention',
                            'message': f'Variable "{match}" should use snake_case convention',
                            'suggestion': f'Rename to "{self._to_snake_case(match)}"'
                        })
            
            elif language in ['javascript', 'cpp']:
                # Check for snake_case in variables (should be camelCase)
                snake_case_pattern = r'\b[a-z][a-z0-9]*_[a-z0-9_]*\b'
                matches = re.findall(snake_case_pattern, code)
                
                for match in matches:
                    issues.append({
                        'type': 'naming_convention',
                        'message': f'Variable "{match}" should use camelCase convention',
                        'suggestion': f'Rename to "{self._to_camel_case(match)}"'
                    })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking naming conventions: {str(e)}")
            return []
    
    def _find_magic_numbers(self, code: str) -> List[str]:
        """Find magic numbers in code"""
        
        try:
            # Find numbers that aren't 0, 1, or -1
            magic_pattern = r'\b(?<![\w.])[-+]?(?!0|1| -1)\d+(?![\w.])\b'
            matches = re.findall(magic_pattern, code)
            return list(set(matches))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error finding magic numbers: {str(e)}")
            return []
    
    def _is_comment_line(self, line: str, language: str) -> bool:
        """Check if a line is a comment"""
        
        try:
            if language == 'python':
                return line.startswith('#')
            elif language in ['javascript', 'cpp']:
                return line.startswith('//') or line.startswith('/*') or line.startswith('*')
            return False
            
        except Exception as e:
            logger.error(f"Error checking if line is comment: {str(e)}")
            return False
    
    def _has_docstring(self, function_body: str) -> bool:
        """Check if function has a docstring"""
        
        try:
            lines = function_body.split('\n')
            for line in lines[:3]:  # Check first 3 lines
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Error checking docstring: {str(e)}")
            return False
    
    def _find_todo_comments(self, code: str) -> List[str]:
        """Find TODO/FIXME comments"""
        
        try:
            todo_pattern = r'//.*?(TODO|FIXME|HACK|XXX).*|/\\*.*?(TODO|FIXME|HACK|XXX).*?\\*/|#.*?(TODO|FIXME|HACK|XXX).*'
            matches = re.findall(todo_pattern, code, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            return [match.strip() for match in matches]
            
        except Exception as e:
            logger.error(f"Error finding TODO comments: {str(e)}")
            return []
    
    def _check_code_duplication(self, code: str) -> int:
        """Check for code duplication (simplified)"""
        
        try:
            lines = [line.strip() for line in code.split('\n') if line.strip()]
            unique_lines = set(lines)
            
            if len(lines) > 0:
                return int((len(unique_lines) / len(lines)) * 100)
            return 100
            
        except Exception as e:
            logger.error(f"Error checking code duplication: {str(e)}")
            return 100
    
    def _calculate_cognitive_complexity(self, code: str, language: str) -> int:
        """Calculate cognitive complexity (simplified)"""
        
        try:
            complexity = 0
            lines = code.split('\n')
            
            nesting_level = 0
            for line in lines:
                stripped = line.strip()
                
                # Increase complexity for control structures
                if any(keyword in stripped for keyword in ['if', 'elif', 'else', 'for', 'while', 'try', 'except']):
                    complexity += 1 + nesting_level
                    if not any(keyword in stripped for keyword in ['else', 'except']):
                        nesting_level += 1
                
                # Decrease nesting for closing structures
                if (language == 'python' and stripped and not stripped.startswith(' ') and not stripped.startswith('\t')) or \
                   (language in ['javascript', 'cpp'] and stripped == '}'):
                    nesting_level = max(0, nesting_level - 1)
            
            return complexity
            
        except Exception as e:
            logger.error(f"Error calculating cognitive complexity: {str(e)}")
            return 0
    
    def _check_indentation(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for consistent indentation"""
        
        try:
            issues = []
            lines = code.split('\n')
            
            for i, line in enumerate(lines, 1):
                if line.strip():
                    # Check for tabs mixed with spaces
                    if '\t' in line and '  ' in line:
                        issues.append({
                            'type': 'mixed_indentation',
                            'message': f'Mixed tabs and spaces on line {i}',
                            'line': i,
                            'suggestion': 'Use consistent indentation (tabs or spaces)'
                        })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking indentation: {str(e)}")
            return []
    
    def _check_trailing_whitespace(self, code: str) -> int:
        """Count lines with trailing whitespace"""
        
        try:
            return sum(1 for line in code.split('\n') if line.rstrip() != line)
            
        except Exception as e:
            logger.error(f"Error checking trailing whitespace: {str(e)}")
            return 0
    
    def _check_python_style(self, code: str) -> List[Dict[str, Any]]:
        """Check Python-specific style issues"""
        
        try:
            issues = []
            
            # Check for import style
            if re.search(r'from\s+\w+\s+import\s+\*', code):
                issues.append({
                    'type': 'wildcard_import',
                    'message': 'Wildcard import detected',
                    'suggestion': 'Import specific modules or functions'
                })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking Python style: {str(e)}")
            return []
    
    def _check_javascript_style(self, code: str) -> List[Dict[str, Any]]:
        """Check JavaScript-specific style issues"""
        
        try:
            issues = []
            
            # Check for var usage
            if re.search(r'\bvar\s+', code):
                issues.append({
                    'type': 'var_usage',
                    'message': 'Using var instead of let/const',
                    'suggestion': 'Use let or const instead of var'
                })
            
            # Check for == vs ===
            if re.search(r'==\s*[^=]', code):
                issues.append({
                    'type': 'loose_equality',
                    'message': 'Using == instead of ===',
                    'suggestion': 'Use === for strict equality comparison'
                })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking JavaScript style: {str(e)}")
            return []
    
    def _check_cpp_style(self, code: str) -> List[Dict[str, Any]]:
        """Check C++-specific style issues"""
        
        try:
            issues = []
            
            # Check for using namespace std
            if re.search(r'using\s+namespace\s+std', code):
                issues.append({
                    'type': 'using_namespace_std',
                    'message': 'Using namespace std in header files',
                    'suggestion': 'Avoid using namespace std in headers'
                })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking C++ style: {str(e)}")
            return []
    
    def _find_hardcoded_values(self, code: str) -> List[str]:
        """Find hardcoded values that should be configurable"""
        
        try:
            hardcoded_patterns = [
                r'["\']http[s]?://[^"\']+["\']',  # URLs
                r'["\'][\w.-]+@[\w.-]+\.\w+["\']',  # Email addresses
                r'["\']\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}["\']',  # IP addresses
                r'["\'][A-Za-z0-9+/]{20,}["\']'  # Long alphanumeric strings (possible keys/tokens)
            ]
            
            hardcoded_values = []
            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, code)
                hardcoded_values.extend(matches)
            
            return hardcoded_values
            
        except Exception as e:
            logger.error(f"Error finding hardcoded values: {str(e)}")
            return []
    
    def _check_error_handling(self, code: str, language: str) -> Dict[str, Any]:
        """Check for proper error handling"""
        
        try:
            missing_handling = []
            
            if language == 'python':
                # Check for file operations without try-except
                file_operations = re.findall(r'open\s*\([^)]+\)', code)
                for op in file_operations:
                    # Check if it's in a try block (simplified check)
                    op_pos = code.find(op)
                    try_pos = code.rfind('try', 0, op_pos)
                    if try_pos == -1 or code[try_pos:op_pos].count('\n') > 5:
                        missing_handling.append(op)
            
            elif language == 'javascript':
                # Check for JSON.parse without try-catch
                json_operations = re.findall(r'JSON\.parse\s*\([^)]+\)', code)
                for op in json_operations:
                    op_pos = code.find(op)
                    try_pos = code.rfind('try', 0, op_pos)
                    if try_pos == -1 or code[try_pos:op_pos].count('\n') > 5:
                        missing_handling.append(op)
            
            elif language == 'cpp':
                # Check for file operations without exception handling
                file_operations = re.findall(r'ifstream|ofstream|fopen', code)
                for op in file_operations:
                    missing_handling.append(op)
            
            return {'missing': missing_handling}
            
        except Exception as e:
            logger.error(f"Error checking error handling: {str(e)}")
            return {'missing': []}
    
    def _check_security_practices(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for security best practices"""
        
        try:
            issues = []
            
            # Check for dangerous functions
            dangerous_functions = {
                'python': ['eval', 'exec', 'input'],
                'javascript': ['eval', 'Function', 'setTimeout', 'setInterval'],
                'cpp': ['system', 'strcpy', 'strcat', 'sprintf']
            }
            
            if language in dangerous_functions:
                for func in dangerous_functions[language]:
                    pattern = rf'\b{func}\s*\('
                    if re.search(pattern, code):
                        issues.append({
                            'type': 'dangerous_function',
                            'message': f'Use of potentially dangerous function: {func}',
                            'suggestion': f'Consider safer alternatives to {func}'
                        })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking security practices: {str(e)}")
            return []
    
    def _check_performance_practices(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for performance best practices"""
        
        try:
            issues = []
            
            # Check for inefficient string concatenation in loops
            if language == 'python':
                if re.search(r'for.*:\s*\n.*\w+\s*\+=', code, re.MULTILINE):
                    issues.append({
                        'type': 'inefficient_concatenation',
                        'message': 'String concatenation in loop detected',
                        'suggestion': 'Use list and join for better performance'
                    })
            
            # Check for repeated calculations in loops
            if re.search(r'for.*:\s*\n.*len\s*\(', code, re.MULTILINE):
                issues.append({
                    'type': 'repeated_calculation',
                    'message': 'Repeated calculation in loop detected',
                    'suggestion': 'Calculate once before loop'
                })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error checking performance practices: {str(e)}")
            return []
    
    def _to_snake_case(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        
        try:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
            
        except Exception as e:
            logger.error(f"Error converting to snake_case: {str(e)}")
            return name
    
    def _to_camel_case(self, name: str) -> str:
        """Convert snake_case to camelCase"""
        
        try:
            components = name.split('_')
            return components[0] + ''.join(word.capitalize() for word in components[1:])
            
        except Exception as e:
            logger.error(f"Error converting to camelCase: {str(e)}")
            return name
