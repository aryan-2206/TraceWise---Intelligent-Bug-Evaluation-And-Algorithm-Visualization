import logging
from typing import Dict, Any, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate comprehensive analysis reports"""
    
    def __init__(self):
        self.report_templates = {
            'summary': self._generate_summary_report,
            'detailed': self._generate_detailed_report,
            'executive': self._generate_executive_report
        }
    
    def generate(self, code: str, language: str, algorithm: str, complexity: str, 
                 bugs: List[Dict[str, Any]], quality_metrics: Dict[str, Any], 
                 score: int, report_type: str = 'detailed') -> Dict[str, Any]:
        """Generate analysis report"""
        
        try:
            if report_type not in self.report_templates:
                report_type = 'detailed'
            
            report_data = {
                'code': code,
                'language': language,
                'algorithm': algorithm,
                'complexity': complexity,
                'bugs': bugs,
                'quality_metrics': quality_metrics,
                'score': score,
                'timestamp': datetime.now().isoformat(),
                'report_type': report_type
            }
            
            # Generate report using template
            report = self.report_templates[report_type](report_data)
            
            # Add metadata
            report['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'report_version': '1.0',
                'analyzer_version': 'TraceWise v1.0.0',
                'code_lines': len(code.split('\n')),
                'analysis_duration': 'N/A'  # Would be calculated in real implementation
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {
                'error': str(e),
                'report_type': report_type,
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_summary_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary report"""
        
        return {
            'title': 'Code Analysis Summary',
            'type': 'summary',
            'overall_score': data['score'],
            'grade': self._calculate_grade(data['score']),
            'algorithm_detected': data['algorithm'] or 'Unknown',
            'complexity': data['complexity'] or 'Unknown',
            'language': data['language'],
            'key_metrics': {
                'total_bugs': len(data['bugs']),
                'critical_issues': len([b for b in data['bugs'] if b.get('severity') == 'critical']),
                'warnings': len([b for b in data['bugs'] if b.get('severity') == 'warning']),
                'code_quality': data['quality_metrics'].get('overall_score', 0)
            },
            'recommendations': self._generate_summary_recommendations(data),
            'status': self._get_overall_status(data)
        }
    
    def _generate_detailed_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed report"""
        
        return {
            'title': 'Detailed Code Analysis Report',
            'type': 'detailed',
            'executive_summary': self._generate_executive_summary(data),
            'code_information': {
                'language': data['language'],
                'lines_of_code': len(data['code'].split('\n')),
                'algorithm_detected': data['algorithm'],
                'time_complexity': data['complexity'],
                'overall_score': data['score'],
                'grade': self._calculate_grade(data['score'])
            },
            'bug_analysis': {
                'total_issues': len(data['bugs']),
                'critical_issues': [b for b in data['bugs'] if b.get('severity') == 'critical'],
                'warnings': [b for b in data['bugs'] if b.get('severity') == 'warning'],
                'info': [b for b in data['bugs'] if b.get('severity') == 'info'],
                'bug_categories': self._categorize_bugs(data['bugs'])
            },
            'quality_analysis': {
                'overall_quality_score': data['quality_metrics'].get('overall_score', 0),
                'readability': data['quality_metrics'].get('readability', {}),
                'maintainability': data['quality_metrics'].get('maintainability', {}),
                'documentation': data['quality_metrics'].get('documentation', {}),
                'complexity': data['quality_metrics'].get('complexity', {}),
                'style': data['quality_metrics'].get('style', {}),
                'best_practices': data['quality_metrics'].get('best_practices', {})
            },
            'recommendations': self._generate_detailed_recommendations(data),
            'improvement_roadmap': self._generate_improvement_roadmap(data)
        }
    
    def _generate_executive_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive report"""
        
        return {
            'title': 'Executive Analysis Report',
            'type': 'executive',
            'key_findings': self._generate_key_findings(data),
            'risk_assessment': self._generate_risk_assessment(data),
            'business_impact': self._generate_business_impact(data),
            'action_items': self._generate_action_items(data),
            'next_steps': self._generate_next_steps(data)
        }
    
    def _calculate_grade(self, score: int) -> str:
        """Calculate letter grade from score"""
        
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_summary_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate summary recommendations"""
        
        recommendations = []
        
        # Based on score
        if data['score'] < 60:
            recommendations.append("Code requires significant improvements before production use")
        elif data['score'] < 80:
            recommendations.append("Code has several issues that should be addressed")
        
        # Based on bugs
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        if critical_bugs:
            recommendations.append(f"Fix {len(critical_bugs)} critical issues immediately")
        
        # Based on algorithm
        if not data['algorithm']:
            recommendations.append("Consider using standard algorithms for better performance")
        
        # Based on quality metrics
        quality_score = data['quality_metrics'].get('overall_score', 0)
        if quality_score < 70:
            recommendations.append("Improve code quality through refactoring and documentation")
        
        return recommendations
    
    def _get_overall_status(self, data: Dict[str, Any]) -> str:
        """Get overall status"""
        
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        
        if critical_bugs:
            return 'Critical Issues Found'
        elif data['score'] < 60:
            return 'Needs Improvement'
        elif data['score'] < 80:
            return 'Acceptable with Reservations'
        else:
            return 'Good'
    
    def _generate_executive_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        
        return {
            'overview': f"Analysis of {data['language']} code revealed an overall score of {data['score']}/100.",
            'algorithm': data['algorithm'] or 'No specific algorithm detected',
            'complexity': data['complexity'] or 'Complexity could not be determined',
            'key_issues': {
                'total_bugs': len(data['bugs']),
                'critical_issues': len([b for b in data['bugs'] if b.get('severity') == 'critical']),
                'quality_score': data['quality_metrics'].get('overall_score', 0)
            },
            'summary': self._get_overall_status(data)
        }
    
    def _categorize_bugs(self, bugs: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize bugs by type"""
        
        categories = {}
        for bug in bugs:
            category = bug.get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
        
        return categories
    
    def _generate_detailed_recommendations(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate detailed recommendations"""
        
        recommendations = {
            'immediate': [],
            'short_term': [],
            'long_term': []
        }
        
        # Immediate recommendations (critical issues)
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        for bug in critical_bugs:
            recommendations['immediate'].append(f"Fix: {bug.get('title', 'Critical issue')}")
        
        # Short-term recommendations
        warning_bugs = [b for b in data['bugs'] if b.get('severity') == 'warning']
        for bug in warning_bugs[:5]:  # Top 5 warnings
            recommendations['short_term'].append(f"Address: {bug.get('title', 'Warning')}")
        
        # Long-term recommendations
        quality_score = data['quality_metrics'].get('overall_score', 0)
        if quality_score < 80:
            recommendations['long_term'].append("Improve overall code quality through refactoring")
        
        if not data['algorithm']:
            recommendations['long_term'].append("Implement standard algorithms for better performance")
        
        return recommendations
    
    def _generate_improvement_roadmap(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement roadmap"""
        
        roadmap = []
        
        # Phase 1: Critical fixes
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        if critical_bugs:
            roadmap.append({
                'phase': 1,
                'title': 'Critical Issue Resolution',
                'duration': '1-2 days',
                'tasks': [f"Fix {bug.get('title', 'critical issue')}" for bug in critical_bugs],
                'priority': 'High'
            })
        
        # Phase 2: Quality improvements
        quality_score = data['quality_metrics'].get('overall_score', 0)
        if quality_score < 80:
            roadmap.append({
                'phase': 2,
                'title': 'Code Quality Enhancement',
                'duration': '3-5 days',
                'tasks': ['Improve code readability', 'Add documentation', 'Refactor complex functions'],
                'priority': 'Medium'
            })
        
        # Phase 3: Performance optimization
        roadmap.append({
            'phase': 3,
            'title': 'Performance Optimization',
            'duration': '2-3 days',
            'tasks': ['Optimize algorithms', 'Reduce complexity', 'Improve efficiency'],
            'priority': 'Medium'
        })
        
        return roadmap
    
    def _generate_key_findings(self, data: Dict[str, Any]) -> List[str]:
        """Generate key findings for executive report"""
        
        findings = []
        
        findings.append(f"Overall code quality score: {data['score']}/100 ({self._calculate_grade(data['score'])})")
        
        if data['algorithm']:
            findings.append(f"Algorithm detected: {data['algorithm']} with {data['complexity']} complexity")
        else:
            findings.append("No standard algorithm detected - consider implementing known patterns")
        
        critical_count = len([b for b in data['bugs'] if b.get('severity') == 'critical'])
        if critical_count > 0:
            findings.append(f"{critical_count} critical issues require immediate attention")
        
        quality_score = data['quality_metrics'].get('overall_score', 0)
        if quality_score < 70:
            findings.append("Code quality below acceptable standards")
        
        return findings
    
    def _generate_risk_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk assessment"""
        
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        warning_bugs = [b for b in data['bugs'] if b.get('severity') == 'warning']
        
        risk_level = 'Low'
        if critical_bugs:
            risk_level = 'High'
        elif warning_bugs > 3:
            risk_level = 'Medium'
        
        return {
            'overall_risk': risk_level,
            'security_risks': len([b for b in data['bugs'] if 'security' in b.get('category', '').lower()]),
            'performance_risks': len([b for b in data['bugs'] if 'performance' in b.get('category', '').lower()]),
            'maintainability_risks': 'High' if data['quality_metrics'].get('overall_score', 0) < 60 else 'Low',
            'recommendations': self._generate_risk_recommendations(data)
        }
    
    def _generate_business_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate business impact assessment"""
        
        return {
            'development_impact': self._assess_development_impact(data),
            'maintenance_impact': self._assess_maintenance_impact(data),
            'performance_impact': self._assess_performance_impact(data),
            'security_impact': self._assess_security_impact(data)
        }
    
    def _generate_action_items(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate action items"""
        
        actions = []
        
        # Critical fixes
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        for bug in critical_bugs:
            actions.append({
                'action': f"Fix critical issue: {bug.get('title', 'Critical bug')}",
                'priority': 'High',
                'owner': 'Development Team',
                'timeline': 'Immediate'
            })
        
        # Quality improvements
        if data['quality_metrics'].get('overall_score', 0) < 80:
            actions.append({
                'action': 'Improve code quality through refactoring',
                'priority': 'Medium',
                'owner': 'Development Team',
                'timeline': '1-2 weeks'
            })
        
        return actions
    
    def _generate_next_steps(self, data: Dict[str, Any]) -> List[str]:
        """Generate next steps"""
        
        steps = []
        
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        if critical_bugs:
            steps.append("Address all critical issues before deployment")
        
        steps.append("Schedule code review with team")
        steps.append("Implement automated testing")
        steps.append("Set up continuous integration")
        
        return steps
    
    def _generate_risk_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate risk-specific recommendations"""
        
        recommendations = []
        
        critical_bugs = [b for b in data['bugs'] if b.get('severity') == 'critical']
        if critical_bugs:
            recommendations.append("Implement code review process to catch critical issues early")
        
        if data['quality_metrics'].get('overall_score', 0) < 70:
            recommendations.append("Invest in code quality training and tools")
        
        return recommendations
    
    def _assess_development_impact(self, data: Dict[str, Any]) -> str:
        """Assess development impact"""
        
        if data['score'] < 60:
            return "High - significant refactoring required"
        elif data['score'] < 80:
            return "Medium - moderate improvements needed"
        else:
            return "Low - minor optimizations only"
    
    def _assess_maintenance_impact(self, data: Dict[str, Any]) -> str:
        """Assess maintenance impact"""
        
        quality_score = data['quality_metrics'].get('overall_score', 0)
        if quality_score < 60:
            return "High - difficult to maintain and extend"
        elif quality_score < 80:
            return "Medium - some maintenance challenges"
        else:
            return "Low - easy to maintain"
    
    def _assess_performance_impact(self, data: Dict[str, Any]) -> str:
        """Assess performance impact"""
        
        if not data['algorithm']:
            return "Medium - suboptimal algorithm choice"
        elif 'O(n^2)' in data.get('complexity', ''):
            return "Medium - quadratic complexity may impact performance"
        else:
            return "Low - acceptable performance characteristics"
    
    def _assess_security_impact(self, data: Dict[str, Any]) -> str:
        """Assess security impact"""
        
        security_bugs = [b for b in data['bugs'] if 'security' in b.get('category', '').lower()]
        if security_bugs:
            return "High - security vulnerabilities present"
        else:
            return "Low - no obvious security issues"
    
    def export_report(self, report: Dict[str, Any], format: str = 'json') -> str:
        """Export report in specified format"""
        
        try:
            if format == 'json':
                return json.dumps(report, indent=2)
            elif format == 'html':
                return self._generate_html_report(report)
            elif format == 'markdown':
                return self._generate_markdown_report(report)
            else:
                return json.dumps(report, indent=2)
                
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            return str(e)
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML report"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report.get('title', 'Code Analysis Report')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                .critical {{ color: red; }}
                .warning {{ color: orange; }}
                .good {{ color: green; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report.get('title', 'Code Analysis Report')}</h1>
                <p>Generated: {report.get('metadata', {}).get('generated_at', 'Unknown')}</p>
            </div>
            
            <div class="section">
                <h2>Overall Score: {report.get('overall_score', 'N/A')}/100</h2>
                <p>Grade: {report.get('grade', 'N/A')}</p>
            </div>
            
            <!-- More HTML content would be generated here -->
            
        </body>
        </html>
        """
        
        return html
    
    def _generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        
        markdown = f"""# {report.get('title', 'Code Analysis Report')}

**Generated:** {report.get('metadata', {}).get('generated_at', 'Unknown')}

## Overall Score: {report.get('overall_score', 'N/A')}/100

**Grade:** {report.get('grade', 'N/A')}

## Key Findings

"""
        
        # Add more markdown content based on report type
        if report.get('type') == 'summary':
            markdown += f"- Algorithm: {report.get('algorithm_detected', 'Unknown')}\n"
            markdown += f"- Complexity: {report.get('complexity', 'Unknown')}\n"
            markdown += f"- Total Issues: {report.get('key_metrics', {}).get('total_bugs', 0)}\n"
        
        return markdown
