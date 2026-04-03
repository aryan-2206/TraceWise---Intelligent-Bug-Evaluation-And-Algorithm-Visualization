import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RuleEngine:
    """Rule engine for code analysis and bug detection"""
    
    def __init__(self):
        self.rules = {}
        self.load_default_rules()
    
    def load_default_rules(self):
        """Load default detection rules for different languages"""
        
        self.rules = {
            'python': [
                {
                    'id': 'py001',
                    'name': 'Infinite Loop Risk',
                    'description': 'Potential infinite loop detected - loop condition may never become false',
                    'severity': 'warning',
                    'pattern': r'while\s+True\s*:',
                    'explanation': 'While True loops should have a break statement or other exit condition',
                    'suggestion': 'Add a break condition or use a specific loop condition'
                },
                {
                    'id': 'py002',
                    'name': 'Unreachable Code',
                    'description': 'Code after return statement will never be executed',
                    'severity': 'info',
                    'pattern': r'return\s+.*\n\s*.*',
                    'explanation': 'Any code after a return statement in a function is unreachable',
                    'suggestion': 'Move code before the return statement or remove it'
                },
                {
                    'id': 'py003',
                    'name': 'Unused Variable',
                    'description': 'Variable is defined but never used',
                    'severity': 'info',
                    'pattern': r'(\w+)\s*=.*',
                    'explanation': 'Variables that are defined but never used may indicate dead code',
                    'suggestion': 'Remove the variable or use it in the code'
                },
                {
                    'id': 'py004',
                    'name': 'Missing Error Handling',
                    'description': 'File operations without proper error handling',
                    'severity': 'warning',
                    'pattern': r'open\s*\([^)]+\)',
                    'explanation': 'File operations should include proper error handling',
                    'suggestion': 'Use try-except blocks to handle potential file errors'
                },
                {
                    'id': 'py005',
                    'name': 'List Index Out of Range Risk',
                    'description': 'Potential list index out of bounds error',
                    'severity': 'critical',
                    'pattern': r'\w+\[len\(\w+\)\]',
                    'explanation': 'List indices go from 0 to len(list)-1',
                    'suggestion': 'Use len(list)-1 or check bounds before accessing'
                },
                {
                    'id': 'py006',
                    'name': 'Binary Search Implementation Issue',
                    'description': 'Binary search may not handle all cases correctly',
                    'severity': 'warning',
                    'pattern': r'mid\s*=\s*\(.*\s*\+\s*.*\)\s*/\s*2',
                    'explanation': 'Integer division may cause overflow in some languages',
                    'suggestion': 'Use mid = left + (right - left) // 2 to prevent overflow'
                },
                {
                    'id': 'py007',
                    'name': 'Sorting Algorithm Efficiency',
                    'description': 'Inefficient sorting implementation detected',
                    'severity': 'warning',
                    'pattern': r'for\s+.*\s*in\s*.*:\s*for\s+.*\s*in\s*.*:',
                    'explanation': 'Nested loops for sorting may indicate O(n²) complexity',
                    'suggestion': 'Consider using built-in sort() or more efficient algorithms'
                }
            ],
            'javascript': [
                {
                    'id': 'js001',
                    'name': 'Infinite Loop Risk',
                    'description': 'Potential infinite loop detected',
                    'severity': 'warning',
                    'pattern': r'while\s*\(\s*true\s*\)',
                    'explanation': 'While(true) loops should have a break statement',
                    'suggestion': 'Add a break condition or use a specific loop condition'
                },
                {
                    'id': 'js002',
                    'name': 'Missing Semicolon',
                    'description': 'Missing semicolon at end of statement',
                    'severity': 'info',
                    'pattern': r'[a-zA-Z0-9_]\s*\n',
                    'explanation': 'JavaScript statements should end with semicolons',
                    'suggestion': 'Add semicolon at the end of the statement'
                },
                {
                    'id': 'js003',
                    'name': 'Var Usage',
                    'description': 'Using var instead of let or const',
                    'severity': 'warning',
                    'pattern': r'\bvar\s+',
                    'explanation': 'var has function scope and can cause hoisting issues',
                    'suggestion': 'Use let for variables that change, const for constants'
                },
                {
                    'id': 'js004',
                    'name': 'Equality Comparison',
                    'description': 'Using == instead of ===',
                    'severity': 'warning',
                    'pattern': r'==\s*[^=]',
                    'explanation': '== performs type coercion, === requires strict equality',
                    'suggestion': 'Use === for strict equality comparison'
                },
                {
                    'id': 'js005',
                    'name': 'Array Index Out of Bounds',
                    'description': 'Potential array index out of bounds',
                    'severity': 'critical',
                    'pattern': r'\w+\[.*\.length\]',
                    'explanation': 'Array indices go from 0 to length-1',
                    'suggestion': 'Use length-1 or check bounds before accessing'
                },
                {
                    'id': 'js006',
                    'name': 'Binary Search Mid Calculation',
                    'description': 'Binary search mid calculation may cause overflow',
                    'severity': 'warning',
                    'pattern': r'Math\.floor\(\(.*\s*\+\s*.*\)\s*/\s*2\)',
                    'explanation': 'Large numbers may cause overflow in mid calculation',
                    'suggestion': 'Use Math.floor(left + (right - left) / 2)'
                }
            ],
            'cpp': [
                {
                    'id': 'cpp001',
                    'name': 'Memory Leak Risk',
                    'description': 'Potential memory leak - new without delete',
                    'severity': 'critical',
                    'pattern': r'new\s+\w+',
                    'explanation': 'Memory allocated with new should be freed with delete',
                    'suggestion': 'Ensure proper deallocation or use smart pointers'
                },
                {
                    'id': 'cpp002',
                    'name': 'Buffer Overflow Risk',
                    'description': 'Potential buffer overflow in array operations',
                    'severity': 'critical',
                    'pattern': r'\w+\[.*\.size\(\)\]',
                    'explanation': 'Array/vector indices go from 0 to size()-1',
                    'suggestion': 'Use size()-1 or check bounds before accessing'
                },
                {
                    'id': 'cpp003',
                    'name': 'Infinite Loop',
                    'description': 'Potential infinite loop detected',
                    'severity': 'warning',
                    'pattern': r'while\s*\(\s*true\s*\)',
                    'explanation': 'While(true) loops should have a break statement',
                    'suggestion': 'Add a break condition or use a specific loop condition'
                },
                {
                    'id': 'cpp004',
                    'name': 'Integer Division',
                    'description': 'Integer division may cause precision loss',
                    'severity': 'warning',
                    'pattern': r'/\s*2',
                    'explanation': 'Integer division truncates decimal part',
                    'suggestion': 'Use floating point division if needed: / 2.0'
                },
                {
                    'id': 'cpp005',
                    'name': 'Binary Search Overflow',
                    'description': 'Binary search mid calculation may cause overflow',
                    'severity': 'warning',
                    'pattern': r'mid\s*=\s*\(.*\s*\+\s*.*\)\s*/\s*2',
                    'explanation': 'Integer addition may overflow with large values',
                    'suggestion': 'Use mid = left + (right - left) / 2'
                },
                {
                    'id': 'cpp006',
                    'name': 'Missing Include',
                    'description': 'Using standard library functions without proper includes',
                    'severity': 'error',
                    'pattern': r'(cout|cin|vector|string)',
                    'explanation': 'Standard library functions require proper headers',
                    'suggestion': 'Add appropriate #include directives'
                }
            ]
        }
    
    def get_rules_for_language(self, language: str) -> List[Dict[str, Any]]:
        """Get all rules for a specific language"""
        
        try:
            return self.rules.get(language, [])
            
        except Exception as e:
            logger.error(f"Error getting rules for language {language}: {str(e)}")
            return []
    
    def add_rule(self, language: str, rule: Dict[str, Any]):
        """Add a new rule for a language"""
        
        try:
            if language not in self.rules:
                self.rules[language] = []
            
            self.rules[language].append(rule)
            logger.info(f"Added rule {rule.get('id', 'unknown')} for language {language}")
            
        except Exception as e:
            logger.error(f"Error adding rule: {str(e)}")
    
    def remove_rule(self, language: str, rule_id: str):
        """Remove a rule by ID for a language"""
        
        try:
            if language in self.rules:
                self.rules[language] = [
                    rule for rule in self.rules[language] 
                    if rule.get('id') != rule_id
                ]
                logger.info(f"Removed rule {rule_id} for language {language}")
            
        except Exception as e:
            logger.error(f"Error removing rule: {str(e)}")
    
    def update_rule(self, language: str, rule_id: str, updated_rule: Dict[str, Any]):
        """Update an existing rule"""
        
        try:
            if language in self.rules:
                for i, rule in enumerate(self.rules[language]):
                    if rule.get('id') == rule_id:
                        self.rules[language][i] = updated_rule
                        logger.info(f"Updated rule {rule_id} for language {language}")
                        return
            
            logger.warning(f"Rule {rule_id} not found for language {language}")
            
        except Exception as e:
            logger.error(f"Error updating rule: {str(e)}")
    
    def get_rule_by_id(self, language: str, rule_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific rule by ID"""
        
        try:
            rules = self.get_rules_for_language(language)
            for rule in rules:
                if rule.get('id') == rule_id:
                    return rule
            return None
            
        except Exception as e:
            logger.error(f"Error getting rule by ID: {str(e)}")
            return None
    
    def validate_rule(self, rule: Dict[str, Any]) -> bool:
        """Validate that a rule has all required fields"""
        
        try:
            required_fields = ['id', 'name', 'description', 'severity', 'pattern']
            return all(field in rule for field in required_fields)
            
        except Exception as e:
            logger.error(f"Error validating rule: {str(e)}")
            return False
    
    def export_rules(self, language: str = None) -> str:
        """Export rules to JSON format"""
        
        try:
            if language:
                return json.dumps(self.rules.get(language, []), indent=2)
            else:
                return json.dumps(self.rules, indent=2)
                
        except Exception as e:
            logger.error(f"Error exporting rules: {str(e)}")
            return "{}"
    
    def import_rules(self, rules_json: str, language: str = None):
        """Import rules from JSON format"""
        
        try:
            rules_data = json.loads(rules_json)
            
            if language:
                if language in rules_data and isinstance(rules_data[language], list):
                    self.rules[language] = rules_data[language]
            else:
                if isinstance(rules_data, dict):
                    self.rules.update(rules_data)
                    
            logger.info(f"Imported rules for language: {language or 'all'}")
            
        except Exception as e:
            logger.error(f"Error importing rules: {str(e)}")
    
    def get_severity_distribution(self, language: str) -> Dict[str, int]:
        """Get distribution of rules by severity for a language"""
        
        try:
            rules = self.get_rules_for_language(language)
            distribution = {}
            
            for rule in rules:
                severity = rule.get('severity', 'unknown')
                distribution[severity] = distribution.get(severity, 0) + 1
            
            return distribution
            
        except Exception as e:
            logger.error(f"Error getting severity distribution: {str(e)}")
            return {}
