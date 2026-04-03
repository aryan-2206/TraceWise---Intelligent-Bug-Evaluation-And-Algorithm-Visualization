import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Tokenizer:
    """Tokenize code into meaningful components"""
    
    def __init__(self):
        self.token_patterns = {
            'python': {
                'keyword': r'\b(def|class|if|elif|else|for|while|return|import|from|try|except|with|as|lambda|yield|and|or|not|in|is|pass|break|continue|global|nonlocal)\b',
                'identifier': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
                'number': r'\b\d+\.?\d*\b',
                'operator': r'[\+\-\*/%=<>!&|^~]',
                'delimiter': r'[(){}\[\],;:.]',
                'string': r'(["\'])(?:(?=(\\?))\2.)*?\1',
                'comment': r'#.*$',
                'whitespace': r'\s+'
            },
            'javascript': {
                'keyword': r'\b(function|var|let|const|if|else|for|while|return|import|export|from|try|catch|finally|throw|new|this|class|extends|super|static|async|await|break|continue|switch|case|default|do|typeof|instanceof|in|of|void|delete|with|debugger)\b',
                'identifier': r'\b[a-zA-Z_$][a-zA-Z0-9_$]*\b',
                'number': r'\b\d+\.?\d*\b',
                'operator': r'[\+\-\*/%=<>!&|^~]+',
                'delimiter': r'[(){}\[\],;:.]',
                'string': r'(["\'])(?:(?=(\\?))\2.)*?\1',
                'comment': r'//.*$|/\*[\s\S]*?\*/',
                'whitespace': r'\s+'
            },
            'cpp': {
                'keyword': r'\b(int|float|double|char|bool|void|if|else|for|while|return|include|using|namespace|class|struct|public|private|protected|virtual|static|const|extern|inline|template|typename|auto|break|continue|switch|case|default|do|goto|sizeof|typedef|enum|union|friend|operator|new|delete|this|try|catch|throw|reinterpret_cast|static_cast|dynamic_cast|const_cast)\b',
                'identifier': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
                'number': r'\b\d+\.?\d*[fFlL]?\b',
                'operator': r'[\+\-\*/%=<>!&|^~]+',
                'delimiter': r'[(){}\[\],;:.]',
                'string': r'(["\'])(?:(?=(\\?))\2.)*?\1',
                'comment': r'//.*$|/\*[\s\S]*?\*/',
                'whitespace': r'\s+'
            }
        }
    
    def tokenize(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Tokenize code into a list of tokens with metadata"""
        
        try:
            if language not in self.token_patterns:
                logger.warning(f"Language '{language}' not supported for tokenization")
                return []
            
            patterns = self.token_patterns[language]
            tokens = []
            position = 0
            
            while position < len(code):
                matched = False
                
                for token_type, pattern in patterns.items():
                    regex = re.compile(pattern)
                    match = regex.match(code, position)
                    
                    if match:
                        token_value = match.group(0)
                        
                        # Skip whitespace but track position
                        if token_type != 'whitespace':
                            tokens.append({
                                'type': token_type,
                                'value': token_value,
                                'position': position,
                                'line': code[:position].count('\n') + 1,
                                'column': position - code.rfind('\n', 0, position)
                            })
                        
                        position = match.end()
                        matched = True
                        break
                
                if not matched:
                    # Handle unrecognized characters
                    tokens.append({
                        'type': 'unknown',
                        'value': code[position],
                        'position': position,
                        'line': code[:position].count('\n') + 1,
                        'column': position - code.rfind('\n', 0, position)
                    })
                    position += 1
            
            return tokens
            
        except Exception as e:
            logger.error(f"Error tokenizing code: {str(e)}")
            return []
    
    def get_token_frequency(self, tokens: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get frequency count of token types"""
        
        try:
            frequency = {}
            for token in tokens:
                token_type = token['type']
                frequency[token_type] = frequency.get(token_type, 0) + 1
            return frequency
            
        except Exception as e:
            logger.error(f"Error calculating token frequency: {str(e)}")
            return {}
    
    def extract_keywords(self, tokens: List[Dict[str, Any]]) -> List[str]:
        """Extract all keyword tokens"""
        
        try:
            keywords = [token['value'] for token in tokens if token['type'] == 'keyword']
            return list(set(keywords))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def extract_identifiers(self, tokens: List[Dict[str, Any]]) -> List[str]:
        """Extract all identifier tokens"""
        
        try:
            identifiers = [token['value'] for token in tokens if token['type'] == 'identifier']
            return list(set(identifiers))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error extracting identifiers: {str(e)}")
            return []
    
    def extract_operators(self, tokens: List[Dict[str, Any]]) -> List[str]:
        """Extract all operator tokens"""
        
        try:
            operators = [token['value'] for token in tokens if token['type'] == 'operator']
            return list(set(operators))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error extracting operators: {str(e)}")
            return []
