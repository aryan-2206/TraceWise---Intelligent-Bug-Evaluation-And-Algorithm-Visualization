import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Calculate quality scores for code analysis"""
    
    def __init__(self):
        self.scoring_weights = {
            'correctness': 0.30,
            'efficiency': 0.25,
            'readability': 0.20,
            'maintainability': 0.15,
            'best_practices': 0.10
        }
        
        self.severity_penalties = {
            'critical': 20,
            'error': 15,
            'warning': 5,
            'info': 1
        }
        
        self.complexity_scores = {
            'O(1)': 100,
            'O(log n)': 90,
            'O(n)': 80,
            'O(n log n)': 70,
            'O(n²)': 40,
            'O(n³)': 20,
            'O(2^n)': 10,
            'O(n!)': 5
        }
    
    def calculate_score(self, quality_metrics: Dict[str, Any], bugs: List[Dict[str, Any]], complexity: str) -> int:
        """Calculate overall quality score"""
        
        try:
            # Calculate individual component scores
            correctness_score = self._calculate_correctness_score(bugs)
            efficiency_score = self._calculate_efficiency_score(complexity, quality_metrics)
            readability_score = self._calculate_readability_score(quality_metrics)
            maintainability_score = self._calculate_maintainability_score(quality_metrics)
            best_practices_score = self._calculate_best_practices_score(quality_metrics, bugs)
            
            # Calculate weighted overall score
            overall_score = (
                correctness_score * self.scoring_weights['correctness'] +
                efficiency_score * self.scoring_weights['efficiency'] +
                readability_score * self.scoring_weights['readability'] +
                maintainability_score * self.scoring_weights['maintainability'] +
                best_practices_score * self.scoring_weights['best_practices']
            )
            
            # Ensure score is within bounds
            overall_score = max(0, min(100, int(overall_score)))
            
            return overall_score
            
        except Exception as e:
            logger.error(f"Error calculating score: {str(e)}")
            return 50  # Default middle score
    
    def get_score_details(self, quality_metrics: Dict[str, Any], bugs: List[Dict[str, Any]], complexity: str) -> Dict[str, Any]:
        """Get detailed scoring breakdown"""
        
        try:
            details = {
                'overall_score': self.calculate_score(quality_metrics, bugs, complexity),
                'component_scores': {},
                'penalties': {},
                'bonuses': {},
                'recommendations': []
            }
            
            # Calculate component scores
            details['component_scores']['correctness'] = self._calculate_correctness_score(bugs)
            details['component_scores']['efficiency'] = self._calculate_efficiency_score(complexity, quality_metrics)
            details['component_scores']['readability'] = self._calculate_readability_score(quality_metrics)
            details['component_scores']['maintainability'] = self._calculate_maintainability_score(quality_metrics)
            details['component_scores']['best_practices'] = self._calculate_best_practices_score(quality_metrics, bugs)
            
            # Calculate penalties
            details['penalties']['bugs'] = self._calculate_bug_penalties(bugs)
            details['penalties']['complexity'] = self._calculate_complexity_penalty(complexity)
            details['penalties']['quality'] = self._calculate_quality_penalties(quality_metrics)
            
            # Calculate bonuses
            details['bonuses']['algorithm'] = self._calculate_algorithm_bonus(quality_metrics)
            details['bonuses']['documentation'] = self._calculate_documentation_bonus(quality_metrics)
            details['bonuses']['structure'] = self._calculate_structure_bonus(quality_metrics)
            
            # Generate recommendations
            details['recommendations'] = self._generate_score_recommendations(details)
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting score details: {str(e)}")
            return {
                'overall_score': 50,
                'error': str(e)
            }
    
    def _calculate_correctness_score(self, bugs: List[Dict[str, Any]]) -> int:
        """Calculate correctness score based on bugs"""
        
        try:
            base_score = 100
            
            # Apply penalties for bugs
            for bug in bugs:
                severity = bug.get('severity', 'info')
                penalty = self.severity_penalties.get(severity, 1)
                base_score -= penalty
            
            # Ensure score doesn't go below 0
            return max(0, base_score)
            
        except Exception as e:
            logger.error(f"Error calculating correctness score: {str(e)}")
            return 50
    
    def _calculate_efficiency_score(self, complexity: str, quality_metrics: Dict[str, Any]) -> int:
        """Calculate efficiency score based on algorithm complexity"""
        
        try:
            # Base score from complexity
            complexity_score = self.complexity_scores.get(complexity, 50)
            
            # Adjust based on performance issues
            performance_issues = quality_metrics.get('best_practices', {}).get('performance_issues', 0)
            performance_penalty = performance_issues * 5
            
            # Adjust based on nested loops
            nested_loops = quality_metrics.get('complexity', {}).get('nested_loops', 0)
            nested_loop_penalty = nested_loops * 10
            
            # Adjust based on recursive calls
            recursive_calls = quality_metrics.get('complexity', {}).get('recursive_calls', 0)
            recursion_penalty = recursive_calls * 3
            
            final_score = complexity_score - performance_penalty - nested_loop_penalty - recursion_penalty
            return max(0, min(100, final_score))
            
        except Exception as e:
            logger.error(f"Error calculating efficiency score: {str(e)}")
            return 50
    
    def _calculate_readability_score(self, quality_metrics: Dict[str, Any]) -> int:
        """Calculate readability score"""
        
        try:
            readability_data = quality_metrics.get('readability', {})
            base_score = readability_data.get('score', 50)
            
            # Bonus for good naming conventions
            naming_issues = len([issue for issue in readability_data.get('issues', []) 
                               if issue.get('type') == 'naming_convention'])
            naming_bonus = max(0, 10 - naming_issues * 2)
            
            # Penalty for long lines
            long_lines = readability_data.get('metrics', {}).get('long_lines', 0)
            long_line_penalty = min(20, long_lines * 2)
            
            # Penalty for long functions
            long_functions = readability_data.get('metrics', {}).get('long_functions', 0)
            long_function_penalty = min(15, long_functions * 3)
            
            final_score = base_score + naming_bonus - long_line_penalty - long_function_penalty
            return max(0, min(100, final_score))
            
        except Exception as e:
            logger.error(f"Error calculating readability score: {str(e)}")
            return 50
    
    def _calculate_maintainability_score(self, quality_metrics: Dict[str, Any]) -> int:
        """Calculate maintainability score"""
        
        try:
            maintainability_data = quality_metrics.get('maintainability', {})
            base_score = maintainability_data.get('score', 50)
            
            # Penalty for deep nesting
            nesting_level = maintainability_data.get('metrics', {}).get('nesting_level', 0)
            nesting_penalty = max(0, (nesting_level - 3) * 10)
            
            # Penalty for too many parameters
            functions_with_many_params = maintainability_data.get('metrics', {}).get('functions_with_many_params', 0)
            param_penalty = functions_with_many_params * 5
            
            # Penalty for code duplication
            duplication_score = maintainability_data.get('metrics', {}).get('duplication_score', 100)
            duplication_penalty = (100 - duplication_score) // 2
            
            # Penalty for too many functions
            function_count = maintainability_data.get('metrics', {}).get('function_count', 0)
            function_penalty = max(0, (function_count - 20) * 2)
            
            final_score = base_score - nesting_penalty - param_penalty - duplication_penalty - function_penalty
            return max(0, min(100, final_score))
            
        except Exception as e:
            logger.error(f"Error calculating maintainability score: {str(e)}")
            return 50
    
    def _calculate_best_practices_score(self, quality_metrics: Dict[str, Any], bugs: List[Dict[str, Any]]) -> int:
        """Calculate best practices score"""
        
        try:
            best_practices_data = quality_metrics.get('best_practices', {})
            base_score = best_practices_data.get('score', 50)
            
            # Penalty for security issues
            security_issues = best_practices_data.get('metrics', {}).get('security_issues', 0)
            security_penalty = security_issues * 15
            
            # Penalty for missing error handling
            missing_error_handling = best_practices_data.get('metrics', {}).get('missing_error_handling', 0)
            error_handling_penalty = missing_error_handling * 8
            
            # Penalty for hardcoded values
            hardcoded_values = best_practices_data.get('metrics', {}).get('hardcoded_values', 0)
            hardcoded_penalty = hardcoded_values * 3
            
            # Penalty for performance issues
            performance_issues = best_practices_data.get('metrics', {}).get('performance_issues', 0)
            performance_penalty = performance_issues * 5
            
            final_score = base_score - security_penalty - error_handling_penalty - hardcoded_penalty - performance_penalty
            return max(0, min(100, final_score))
            
        except Exception as e:
            logger.error(f"Error calculating best practices score: {str(e)}")
            return 50
    
    def _calculate_bug_penalties(self, bugs: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate penalties for bugs"""
        
        try:
            penalties = {'total': 0}
            
            for bug in bugs:
                severity = bug.get('severity', 'info')
                penalty = self.severity_penalties.get(severity, 1)
                
                if severity not in penalties:
                    penalties[severity] = 0
                penalties[severity] += penalty
                penalties['total'] += penalty
            
            return penalties
            
        except Exception as e:
            logger.error(f"Error calculating bug penalties: {str(e)}")
            return {'total': 0}
    
    def _calculate_complexity_penalty(self, complexity: str) -> int:
        """Calculate penalty for algorithm complexity"""
        
        try:
            ideal_score = 100
            actual_score = self.complexity_scores.get(complexity, 50)
            return ideal_score - actual_score
            
        except Exception as e:
            logger.error(f"Error calculating complexity penalty: {str(e)}")
            return 0
    
    def _calculate_quality_penalties(self, quality_metrics: Dict[str, Any]) -> Dict[str, int]:
        """Calculate penalties for quality issues"""
        
        try:
            penalties = {
                'readability': 0,
                'maintainability': 0,
                'documentation': 0,
                'style': 0
            }
            
            # Readability penalties
            readability_issues = len(quality_metrics.get('readability', {}).get('issues', []))
            penalties['readability'] = readability_issues * 2
            
            # Maintainability penalties
            maintainability_issues = len(quality_metrics.get('maintainability', {}).get('issues', []))
            penalties['maintainability'] = maintainability_issues * 3
            
            # Documentation penalties
            documentation_issues = len(quality_metrics.get('documentation', {}).get('issues', []))
            penalties['documentation'] = documentation_issues * 4
            
            # Style penalties
            style_issues = len(quality_metrics.get('style', {}).get('issues', []))
            penalties['style'] = style_issues * 1
            
            return penalties
            
        except Exception as e:
            logger.error(f"Error calculating quality penalties: {str(e)}")
            return {'total': 0}
    
    def _calculate_algorithm_bonus(self, quality_metrics: Dict[str, Any]) -> int:
        """Calculate bonus for using good algorithms"""
        
        try:
            bonus = 0
            
            # Bonus for using standard algorithms
            # This would require detecting algorithm usage from quality metrics
            # For now, return a small bonus
            bonus += 5
            
            return bonus
            
        except Exception as e:
            logger.error(f"Error calculating algorithm bonus: {str(e)}")
            return 0
    
    def _calculate_documentation_bonus(self, quality_metrics: Dict[str, Any]) -> int:
        """Calculate bonus for good documentation"""
        
        try:
            documentation_data = quality_metrics.get('documentation', {})
            bonus = 0
            
            # Bonus for good comment ratio
            comment_ratio = documentation_data.get('metrics', {}).get('comment_ratio', 0)
            if comment_ratio > 0.2:
                bonus += 10
            elif comment_ratio > 0.1:
                bonus += 5
            
            # Bonus for having docstrings
            docstring_bonus = 10 if documentation_data.get('score', 0) > 80 else 0
            bonus += docstring_bonus
            
            # Penalty for TODO comments
            todo_count = documentation_data.get('metrics', {}).get('todo_count', 0)
            todo_penalty = min(10, todo_count * 2)
            bonus -= todo_penalty
            
            return max(0, bonus)
            
        except Exception as e:
            logger.error(f"Error calculating documentation bonus: {str(e)}")
            return 0
    
    def _calculate_structure_bonus(self, quality_metrics: Dict[str, Any]) -> int:
        """Calculate bonus for good code structure"""
        
        try:
            bonus = 0
            
            # Bonus for reasonable function count
            function_count = quality_metrics.get('maintainability', {}).get('metrics', {}).get('function_count', 0)
            if 5 <= function_count <= 15:
                bonus += 5
            
            # Bonus for reasonable nesting level
            nesting_level = quality_metrics.get('complexity', {}).get('nested_loops', 0)
            if nesting_level <= 2:
                bonus += 5
            
            return max(0, bonus)
            
        except Exception as e:
            logger.error(f"Error calculating structure bonus: {str(e)}")
            return 0
    
    def _generate_score_recommendations(self, score_details: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on score breakdown"""
        
        try:
            recommendations = []
            component_scores = score_details.get('component_scores', {})
            
            # Correctness recommendations
            if component_scores.get('correctness', 0) < 70:
                recommendations.append("Fix critical bugs and errors to improve correctness")
            
            # Efficiency recommendations
            if component_scores.get('efficiency', 0) < 70:
                recommendations.append("Optimize algorithm choice and reduce computational complexity")
            
            # Readability recommendations
            if component_scores.get('readability', 0) < 70:
                recommendations.append("Improve code readability through better naming and formatting")
            
            # Maintainability recommendations
            if component_scores.get('maintainability', 0) < 70:
                recommendations.append("Reduce code complexity and improve structure for better maintainability")
            
            # Best practices recommendations
            if component_scores.get('best_practices', 0) < 70:
                recommendations.append("Follow coding best practices and security guidelines")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating score recommendations: {str(e)}")
            return []
    
    def get_grade_info(self, score: int) -> Dict[str, Any]:
        """Get detailed grade information"""
        
        try:
            if score >= 90:
                return {
                    'grade': 'A',
                    'description': 'Excellent',
                    'color': 'green',
                    'message': 'Outstanding code quality with minimal issues'
                }
            elif score >= 80:
                return {
                    'grade': 'B',
                    'description': 'Good',
                    'color': 'blue',
                    'message': 'Good code quality with minor improvements needed'
                }
            elif score >= 70:
                return {
                    'grade': 'C',
                    'description': 'Average',
                    'color': 'yellow',
                    'message': 'Acceptable code quality but several areas need improvement'
                }
            elif score >= 60:
                return {
                    'grade': 'D',
                    'description': 'Below Average',
                    'color': 'orange',
                    'message': 'Code quality below standards, significant improvements needed'
                }
            else:
                return {
                    'grade': 'F',
                    'description': 'Poor',
                    'color': 'red',
                    'message': 'Code quality is poor, major refactoring required'
                }
                
        except Exception as e:
            logger.error(f"Error getting grade info: {str(e)}")
            return {
                'grade': 'N/A',
                'description': 'Unknown',
                'color': 'gray',
                'message': 'Unable to determine grade'
            }
    
    def compare_scores(self, current_score: int, previous_score: int) -> Dict[str, Any]:
        """Compare current score with previous score"""
        
        try:
            difference = current_score - previous_score
            percentage_change = (difference / previous_score * 100) if previous_score > 0 else 0
            
            return {
                'current_score': current_score,
                'previous_score': previous_score,
                'difference': difference,
                'percentage_change': percentage_change,
                'improvement': difference > 0,
                'significant_change': abs(percentage_change) > 10
            }
            
        except Exception as e:
            logger.error(f"Error comparing scores: {str(e)}")
            return {
                'current_score': current_score,
                'previous_score': previous_score,
                'error': str(e)
            }
