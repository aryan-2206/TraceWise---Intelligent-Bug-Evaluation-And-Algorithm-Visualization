import signal
import logging
from typing import Any, Callable, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class TimeoutHandler:
    """Handle execution timeouts for code execution"""
    
    def __init__(self, default_timeout: int = 30):
        self.default_timeout = default_timeout
        self.current_timeout = default_timeout
    
    @contextmanager
    def timeout_context(self, timeout_seconds: Optional[int] = None):
        """Context manager for handling timeouts"""
        
        if timeout_seconds is None:
            timeout_seconds = self.default_timeout
        
        self.current_timeout = timeout_seconds
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Execution timed out after {timeout_seconds} seconds")
        
        # Set up signal handler
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        
        try:
            # Set the alarm
            signal.alarm(timeout_seconds)
            yield
        finally:
            # Cancel the alarm and restore old handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    
    def execute_with_timeout(self, func: Callable, *args, timeout: Optional[int] = None, **kwargs) -> Any:
        """Execute a function with timeout"""
        
        try:
            with self.timeout_context(timeout):
                return func(*args, **kwargs)
        except TimeoutError as e:
            logger.warning(f"Function execution timed out: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in timeout execution: {str(e)}")
            raise
    
    def check_timeout_risk(self, code: str, language: str) -> dict:
        """Analyze code for potential timeout risks"""
        
        try:
            risk_factors = {
                'risk_level': 'low',
                'factors': [],
                'suggestions': []
            }
            
            # Check for infinite loop patterns
            infinite_patterns = [
                r'while\s+True\s*:\s*\n(?!.*break)',
                r'for\s+.*\s*in\s+.*:\s*\n.*i\s*=',
                r'while\s+.*<\s*.*:\s*\n.*\+\s*0'  # No increment
            ]
            
            for pattern in infinite_patterns:
                import re
                if re.search(pattern, code, re.MULTILINE):
                    risk_factors['risk_level'] = 'high'
                    risk_factors['factors'].append('Potential infinite loop detected')
                    risk_factors['suggestions'].append('Add proper loop termination conditions')
            
            # Check for recursion without base case
            if 'def' in code and 'return' in code:
                import re
                func_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:'
                matches = re.finditer(func_pattern, code)
                
                for match in matches:
                    func_name = match.group(1)
                    if re.search(rf'\b{func_name}\s*\(', code):
                        # Check if there's a base case
                        if not re.search(r'if\s+.*:\s*\n.*return', code):
                            risk_factors['risk_level'] = 'medium'
                            risk_factors['factors'].append(f'Recursion without clear base case in {func_name}')
                            risk_factors['suggestions'].append('Add proper base case for recursion')
            
            # Check for exponential algorithms
            exponential_patterns = [
                r'fibonacci.*recursive',
                r'2\s*\*\s*n',
                r'factorial.*recursive'
            ]
            
            for pattern in exponential_patterns:
                import re
                if re.search(pattern, code, re.IGNORECASE):
                    if risk_factors['risk_level'] == 'low':
                        risk_factors['risk_level'] = 'medium'
                    risk_factors['factors'].append('Exponential complexity algorithm detected')
                    risk_factors['suggestions'].append('Consider iterative approach or memoization')
            
            # Check for large input processing
            large_input_patterns = [
                r'for.*in.*range\s*\(\s*len\s*\(',
                r'while\s+.*<\s*len\s*\(',
                r'n\s*\*\s*n'  # O(n²) operations
            ]
            
            pattern_count = 0
            for pattern in large_input_patterns:
                import re
                if re.search(pattern, code):
                    pattern_count += 1
            
            if pattern_count >= 2:
                if risk_factors['risk_level'] == 'low':
                    risk_factors['risk_level'] = 'medium'
                risk_factors['factors'].append('Multiple nested loops or large input processing')
                risk_factors['suggestions'].append('Consider optimizing algorithm complexity')
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error checking timeout risk: {str(e)}")
            return {
                'risk_level': 'unknown',
                'factors': ['Error analyzing code'],
                'suggestions': ['Manual review recommended']
            }
    
    def get_recommended_timeout(self, code: str, language: str, input_size: int = 100) -> int:
        """Get recommended timeout based on code analysis"""
        
        try:
            risk_analysis = self.check_timeout_risk(code, language)
            
            base_timeout = self.default_timeout
            
            # Adjust timeout based on risk level
            if risk_analysis['risk_level'] == 'high':
                return min(base_timeout // 2, 10)  # Reduce timeout for high risk
            elif risk_analysis['risk_level'] == 'medium':
                return min(base_timeout * 2, 60)  # Increase timeout for medium risk
            
            # Adjust based on input size
            if input_size > 1000:
                base_timeout = min(base_timeout * 3, 120)
            elif input_size > 10000:
                base_timeout = min(base_timeout * 5, 300)
            
            return base_timeout
            
        except Exception as e:
            logger.error(f"Error getting recommended timeout: {str(e)}")
            return self.default_timeout
    
    def create_timeout_safe_wrapper(self, func: Callable, timeout: Optional[int] = None) -> Callable:
        """Create a timeout-safe wrapper for a function"""
        
        def wrapper(*args, **kwargs):
            return self.execute_with_timeout(func, *args, timeout=timeout, **kwargs)
        
        return wrapper
    
    def monitor_execution_time(self, func: Callable, *args, **kwargs) -> dict:
        """Monitor execution time of a function"""
        
        try:
            import time
            
            start_time = time.time()
            
            try:
                with self.timeout_context():
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    
                    return {
                        'success': True,
                        'result': result,
                        'execution_time': end_time - start_time,
                        'timeout_reached': False
                    }
            except TimeoutError:
                end_time = time.time()
                return {
                    'success': False,
                    'error': 'Timeout reached',
                    'execution_time': end_time - start_time,
                    'timeout_reached': True
                }
                
        except Exception as e:
            logger.error(f"Error monitoring execution time: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'execution_time': 0,
                'timeout_reached': False
            }
    
    def set_timeout(self, timeout_seconds: int):
        """Set the default timeout"""
        
        if timeout_seconds > 0:
            self.default_timeout = timeout_seconds
            logger.info(f"Default timeout set to {timeout_seconds} seconds")
        else:
            logger.warning("Invalid timeout value. Must be positive.")
    
    def get_timeout_info(self) -> dict:
        """Get current timeout configuration"""
        
        return {
            'default_timeout': self.default_timeout,
            'current_timeout': self.current_timeout,
            'platform': 'signal-based' if hasattr(signal, 'SIGALRM') else 'not available'
        }
