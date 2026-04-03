import subprocess
import tempfile
import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class CodeRunner:
    """Execute code in a sandboxed environment"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.temp_dir = tempfile.gettempdir()
        self.supported_languages = {
            'python': {
                'extension': '.py',
                'command': ['python'],
                'compile': None
            },
            'javascript': {
                'extension': '.js',
                'command': ['node'],
                'compile': None
            },
            'cpp': {
                'extension': '.cpp',
                'command': ['./temp_executable'],
                'compile': ['g++', '-o', 'temp_executable']
            }
        }
    
    def run_code(self, code: str, language: str, input_data: str = None) -> Dict[str, Any]:
        """Execute code and return results"""
        
        try:
            if language not in self.supported_languages:
                return {
                    'success': False,
                    'error': f'Language {language} is not supported',
                    'output': '',
                    'execution_time': 0
                }
            
            # Create temporary file
            temp_file = self._create_temp_file(code, language)
            
            try:
                # Compile if necessary
                if self.supported_languages[language]['compile']:
                    compile_result = self._compile_code(temp_file, language)
                    if not compile_result['success']:
                        return compile_result
                
                # Execute the code
                execution_result = self._execute_code(temp_file, language, input_data)
                return execution_result
                
            finally:
                # Cleanup
                self._cleanup_temp_files(temp_file, language)
                
        except Exception as e:
            logger.error(f"Error running code: {str(e)}")
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'output': '',
                'execution_time': 0
            }
    
    def _create_temp_file(self, code: str, language: str) -> str:
        """Create temporary file with code"""
        
        try:
            extension = self.supported_languages[language]['extension']
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix=extension,
                dir=self.temp_dir,
                delete=False
            )
            
            temp_file.write(code)
            temp_file.flush()
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error creating temp file: {str(e)}")
            raise
    
    def _compile_code(self, file_path: str, language: str) -> Dict[str, Any]:
        """Compile code if necessary"""
        
        try:
            compile_command = self.supported_languages[language]['compile']
            if not compile_command:
                return {'success': True}
            
            # Add input file to compile command
            if language == 'cpp':
                compile_command = ['g++', '-o', 
                                 os.path.splitext(file_path)[0] + '_exec', 
                                 file_path]
            
            result = subprocess.run(
                compile_command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=os.path.dirname(file_path)
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'Compilation error: {result.stderr}',
                    'output': result.stdout,
                    'execution_time': 0
                }
            
            # Update command to use compiled executable
            if language == 'cpp':
                self.supported_languages[language]['command'] = [
                    os.path.splitext(file_path)[0] + '_exec'
                ]
            
            return {'success': True}
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Compilation timeout',
                'output': '',
                'execution_time': self.timeout
            }
        except Exception as e:
            logger.error(f"Error compiling code: {str(e)}")
            return {
                'success': False,
                'error': f'Compilation error: {str(e)}',
                'output': '',
                'execution_time': 0
            }
    
    def _execute_code(self, file_path: str, language: str, input_data: str = None) -> Dict[str, Any]:
        """Execute the compiled/interpreted code"""
        
        try:
            command = self.supported_languages[language]['command'].copy()
            
            # For C++, use the compiled executable
            if language == 'cpp':
                exec_path = os.path.splitext(file_path)[0] + '_exec'
                command = [exec_path]
            else:
                command = self.supported_languages[language]['command'].copy()
                command.append(file_path)
            
            # Run the process
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(file_path)
            )
            
            try:
                stdout, stderr = process.communicate(
                    input=input_data,
                    timeout=self.timeout
                )
                
                execution_time = 0  # Would need more sophisticated timing
                
                if process.returncode != 0:
                    return {
                        'success': False,
                        'error': f'Runtime error: {stderr}',
                        'output': stdout,
                        'execution_time': execution_time
                    }
                
                return {
                    'success': True,
                    'error': None,
                    'output': stdout,
                    'execution_time': execution_time
                }
                
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                
                return {
                    'success': False,
                    'error': f'Execution timeout after {self.timeout} seconds',
                    'output': '',
                    'execution_time': self.timeout
                }
                
        except Exception as e:
            logger.error(f"Error executing code: {str(e)}")
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'output': '',
                'execution_time': 0
            }
    
    def _cleanup_temp_files(self, file_path: str, language: str):
        """Clean up temporary files"""
        
        try:
            # Remove source file
            if os.path.exists(file_path):
                os.unlink(file_path)
            
            # Remove compiled executable for C++
            if language == 'cpp':
                exec_path = os.path.splitext(file_path)[0] + '_exec'
                if os.path.exists(exec_path):
                    os.unlink(exec_path)
                    
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {str(e)}")
    
    def run_test_cases(self, code: str, language: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run code against multiple test cases"""
        
        try:
            results = {
                'total_tests': len(test_cases),
                'passed_tests': 0,
                'failed_tests': 0,
                'test_results': [],
                'summary': {}
            }
            
            for i, test_case in enumerate(test_cases):
                input_data = test_case.get('input', '')
                expected_output = test_case.get('expected_output', '')
                description = test_case.get('description', f'Test case {i + 1}')
                
                # Run the code
                execution_result = self.run_code(code, language, input_data)
                
                # Compare results
                actual_output = execution_result.get('output', '').strip()
                expected_output = expected_output.strip()
                
                passed = (execution_result['success'] and 
                          actual_output == expected_output)
                
                test_result = {
                    'test_case': i + 1,
                    'description': description,
                    'input': input_data,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'passed': passed,
                    'execution_time': execution_result.get('execution_time', 0),
                    'error': execution_result.get('error')
                }
                
                results['test_results'].append(test_result)
                
                if passed:
                    results['passed_tests'] += 1
                else:
                    results['failed_tests'] += 1
            
            # Calculate summary
            results['summary'] = {
                'success_rate': (results['passed_tests'] / results['total_tests']) * 100,
                'all_passed': results['failed_tests'] == 0,
                'total_execution_time': sum(r['execution_time'] for r in results['test_results'])
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error running test cases: {str(e)}")
            return {
                'total_tests': len(test_cases),
                'passed_tests': 0,
                'failed_tests': len(test_cases),
                'test_results': [],
                'summary': {'error': str(e)}
            }
    
    def validate_code(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code syntax without executing"""
        
        try:
            if language not in self.supported_languages:
                return {
                    'valid': False,
                    'error': f'Language {language} is not supported'
                }
            
            # Create temp file for validation
            temp_file = self._create_temp_file(code, language)
            
            try:
                if language == 'python':
                    # Python syntax check
                    result = subprocess.run(
                        ['python', '-m', 'py_compile', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    return {
                        'valid': result.returncode == 0,
                        'error': result.stderr if result.returncode != 0 else None
                    }
                
                elif language == 'javascript':
                    # JavaScript syntax check (using node)
                    result = subprocess.run(
                        ['node', '-c', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    return {
                        'valid': result.returncode == 0,
                        'error': result.stderr if result.returncode != 0 else None
                    }
                
                elif language == 'cpp':
                    # C++ compilation check
                    compile_result = self._compile_code(temp_file, language)
                    return {
                        'valid': compile_result['success'],
                        'error': compile_result.get('error')
                    }
                
            finally:
                self._cleanup_temp_files(temp_file, language)
            
        except Exception as e:
            logger.error(f"Error validating code: {str(e)}")
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }
    
    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get information about supported language"""
        
        try:
            if language not in self.supported_languages:
                return {'supported': False}
            
            lang_info = self.supported_languages[language].copy()
            lang_info['supported'] = True
            
            # Test if language interpreter/compiler is available
            try:
                test_command = lang_info['command'][0]
                result = subprocess.run(
                    [test_command, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                lang_info['available'] = True
                lang_info['version'] = result.stdout or result.stderr
            except Exception:
                lang_info['available'] = False
                lang_info['version'] = None
            
            return lang_info
            
        except Exception as e:
            logger.error(f"Error getting language info: {str(e)}")
            return {'supported': False, 'error': str(e)}
