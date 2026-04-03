import os
import json
import hashlib
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class Helpers:
    """Utility helper functions for the application"""
    
    @staticmethod
    def safe_json_load(file_path: str, default: Any = None) -> Any:
        """Safely load JSON file"""
        
        try:
            if not os.path.exists(file_path):
                return default
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {str(e)}")
            return default
    
    @staticmethod
    def safe_json_save(data: Any, file_path: str) -> bool:
        """Safely save data to JSON file"""
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving JSON file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Get SHA256 hash of file"""
        
        try:
            hash_sha256 = hashlib.sha256()
            
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            
            return hash_sha256.hexdigest()
            
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return ""
    
    @staticmethod
    def get_string_hash(text: str) -> str:
        """Get SHA256 hash of string"""
        
        try:
            return hashlib.sha256(text.encode('utf-8')).hexdigest()
            
        except Exception as e:
            logger.error(f"Error calculating string hash: {str(e)}")
            return ""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        
        try:
            if size_bytes == 0:
                return "0B"
            
            size_names = ["B", "KB", "MB", "GB", "TB"]
            i = 0
            
            while size_bytes >= 1024 and i < len(size_names) - 1:
                size_bytes /= 1024.0
                i += 1
            
            return f"{size_bytes:.1f}{size_names[i]}"
            
        except Exception as e:
            logger.error(f"Error formatting file size: {str(e)}")
            return "Unknown"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human readable format"""
        
        try:
            if seconds < 1:
                return f"{seconds * 1000:.0f}ms"
            elif seconds < 60:
                return f"{seconds:.1f}s"
            elif seconds < 3600:
                minutes = seconds / 60
                return f"{minutes:.1f}m"
            else:
                hours = seconds / 3600
                return f"{hours:.1f}h"
                
        except Exception as e:
            logger.error(f"Error formatting duration: {str(e)}")
            return "Unknown"
    
    @staticmethod
    def clean_code(code: str) -> str:
        """Clean and normalize code"""
        
        try:
            # Remove leading/trailing whitespace
            code = code.strip()
            
            # Normalize line endings
            code = code.replace('\r\n', '\n').replace('\r', '\n')
            
            # Remove excessive blank lines
            code = re.sub(r'\n\s*\n\s*\n+', '\n\n', code)
            
            return code
            
        except Exception as e:
            logger.error(f"Error cleaning code: {str(e)}")
            return code
    
    @staticmethod
    def extract_function_signatures(code: str, language: str) -> List[str]:
        """Extract function signatures from code"""
        
        try:
            signatures = []
            
            if language == 'python':
                pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*:'
                matches = re.finditer(pattern, code)
                signatures = [match.group(0) for match in matches]
            
            elif language == 'javascript':
                patterns = [
                    r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*\{',
                    r'const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>\s*\{',
                    r'let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>\s*\{'
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, code)
                    signatures.extend([match.group(0) for match in matches])
            
            elif language == 'cpp':
                pattern = r'(?:\w+\s+)*([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:const\s*)?\{'
                matches = re.finditer(pattern, code)
                signatures = [match.group(0) for match in matches]
            
            return signatures
            
        except Exception as e:
            logger.error(f"Error extracting function signatures: {str(e)}")
            return []
    
    @staticmethod
    def count_lines_of_code(code: str) -> Dict[str, int]:
        """Count lines of code with different categories"""
        
        try:
            lines = code.split('\n')
            
            total_lines = len(lines)
            empty_lines = len([line for line in lines if not line.strip()])
            comment_lines = len([line for line in lines if line.strip().startswith('#') or 
                               line.strip().startswith('//') or line.strip().startswith('/*')])
            code_lines = total_lines - empty_lines - comment_lines
            
            return {
                'total': total_lines,
                'code': code_lines,
                'empty': empty_lines,
                'comments': comment_lines
            }
            
        except Exception as e:
            logger.error(f"Error counting lines of code: {str(e)}")
            return {'total': 0, 'code': 0, 'empty': 0, 'comments': 0}
    
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """Detect file encoding"""
        
        try:
            import chardet
            
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
                
        except ImportError:
            # Fallback to utf-8 if chardet is not available
            return 'utf-8'
        except Exception as e:
            logger.error(f"Error detecting encoding: {str(e)}")
            return 'utf-8'
    
    @staticmethod
    def validate_code_syntax(code: str, language: str) -> Dict[str, Any]:
        """Validate code syntax without executing"""
        
        try:
            result = {'valid': True, 'errors': []}
            
            if language == 'python':
                import ast
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    result['valid'] = False
                    result['errors'].append({
                        'type': 'SyntaxError',
                        'message': str(e),
                        'line': e.lineno,
                        'column': e.offset
                    })
            
            elif language == 'javascript':
                # Basic validation - in practice, you'd use a proper JS parser
                if code.count('{') != code.count('}'):
                    result['valid'] = False
                    result['errors'].append({
                        'type': 'SyntaxError',
                        'message': 'Unbalanced braces'
                    })
                
                if code.count('(') != code.count(')'):
                    result['valid'] = False
                    result['errors'].append({
                        'type': 'SyntaxError',
                        'message': 'Unbalanced parentheses'
                    })
            
            elif language == 'cpp':
                # Basic validation - in practice, you'd use a proper C++ parser
                if code.count('{') != code.count('}'):
                    result['valid'] = False
                    result['errors'].append({
                        'type': 'SyntaxError',
                        'message': 'Unbalanced braces'
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating syntax: {str(e)}")
            return {'valid': False, 'errors': [{'type': 'Error', 'message': str(e)}]}
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file system usage"""
        
        try:
            # Remove or replace invalid characters
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                filename = filename.replace(char, '_')
            
            # Remove leading/trailing spaces and dots
            filename = filename.strip(' .')
            
            # Limit length
            if len(filename) > 255:
                filename = filename[:255]
            
            return filename
            
        except Exception as e:
            logger.error(f"Error sanitizing filename: {str(e)}")
            return filename
    
    @staticmethod
    def create_directory_if_not_exists(directory: str) -> bool:
        """Create directory if it doesn't exist"""
        
        try:
            os.makedirs(directory, exist_ok=True)
            return True
            
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {str(e)}")
            return False
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp as ISO string"""
        
        try:
            return datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error getting timestamp: {str(e)}")
            return ""
    
    @staticmethod
    def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp string to datetime object"""
        
        try:
            return datetime.fromisoformat(timestamp_str)
            
        except Exception as e:
            logger.error(f"Error parsing timestamp: {str(e)}")
            return None
    
    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0-1)"""
        
        try:
            # Simple similarity using Jaccard similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            if not union:
                return 1.0 if not words1 and not words2 else 0.0
            
            return len(intersection) / len(union)
            
        except Exception as e:
            logger.error(f"Error calculating text similarity: {str(e)}")
            return 0.0
    
    @staticmethod
    def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """Flatten nested dictionary"""
        
        try:
            items = []
            
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                
                if isinstance(v, dict):
                    items.extend(Helpers.flatten_dict(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            
            return dict(items)
            
        except Exception as e:
            logger.error(f"Error flattening dictionary: {str(e)}")
            return {}
    
    @staticmethod
    def deep_merge_dict(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        
        try:
            result = dict1.copy()
            
            for key, value in dict2.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = Helpers.deep_merge_dict(result[key], value)
                else:
                    result[key] = value
            
            return result
            
        except Exception as e:
            logger.error(f"Error deep merging dictionaries: {str(e)}")
            return dict1
    
    @staticmethod
    def clamp(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
        """Clamp value between min and max"""
        
        try:
            return max(min_val, min(value, max_val))
            
        except Exception as e:
            logger.error(f"Error clamping value: {str(e)}")
            return value
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address"""
        
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
            
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            return False
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        
        try:
            url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            return re.findall(url_pattern, text)
            
        except Exception as e:
            logger.error(f"Error extracting URLs: {str(e)}")
            return []
    
    @staticmethod
    def generate_unique_id(prefix: str = "", length: int = 8) -> str:
        """Generate unique ID"""
        
        try:
            import uuid
            unique_id = str(uuid.uuid4()).replace('-', '')[:length]
            return f"{prefix}{unique_id}" if prefix else unique_id
            
        except Exception as e:
            logger.error(f"Error generating unique ID: {str(e)}")
            return prefix + "unknown"
    
    @staticmethod
    def retry_operation(func, max_retries: int = 3, delay: float = 1.0, *args, **kwargs):
        """Retry operation with exponential backoff"""
        
        try:
            import time
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    wait_time = delay * (2 ** attempt)
                    logger.warning(f"Operation failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s: {str(e)}")
                    time.sleep(wait_time)
                    
        except Exception as e:
            logger.error(f"Error in retry operation: {str(e)}")
            raise
