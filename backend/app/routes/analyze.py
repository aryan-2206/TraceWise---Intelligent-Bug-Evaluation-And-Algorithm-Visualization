from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from app.parser.code_cleaner import CodeCleaner
from app.parser.tokenizer import Tokenizer
from app.parser.structure_extractor import StructureExtractor
from app.detector.algorithm_detector import AlgorithmDetector
from app.detector.rule_engine import RuleEngine
from app.analyzer.bug_detector import BugDetector
from app.analyzer.quality_analyzer import QualityAnalyzer
from app.analyzer.complexity_estimator import ComplexityEstimator
from app.visualization.binary_search_visualizer import BinarySearchVisualizer
from app.visualization.sorting_visualizer import SortingVisualizer
from app.visualization.graph_visualizer import GraphVisualizer
from app.report.report_generator import ReportGenerator
from app.report.scoring_engine import ScoringEngine
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    test_cases: Optional[List[Dict[str, Any]]] = None

class CodeAnalysisResponse(BaseModel):
    algorithm: Optional[str] = None
    algorithm_info: Optional[Dict[str, Any]] = None
    complexity: Optional[str] = None
    bugs: Optional[List[Dict[str, Any]]] = None
    score: Optional[int] = None
    score_details: Optional[Dict[str, Any]] = None
    visualization: Optional[Dict[str, Any]] = None
    execution_results: Optional[Dict[str, Any]] = None

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze code for algorithm detection, bug detection, and quality analysis"""
    
    try:
        # Validate input
        if len(request.code) > settings.MAX_CODE_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Code length exceeds maximum allowed length of {settings.MAX_CODE_LENGTH} characters"
            )
        
        if request.language not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' is not supported"
            )
        
        # Initialize components
        code_cleaner = CodeCleaner()
        tokenizer = Tokenizer()
        structure_extractor = StructureExtractor()
        algorithm_detector = AlgorithmDetector()
        rule_engine = RuleEngine()
        bug_detector = BugDetector()
        quality_analyzer = QualityAnalyzer()
        complexity_estimator = ComplexityEstimator()
        scoring_engine = ScoringEngine()
        report_generator = ReportGenerator()
        
        # Clean and preprocess code
        cleaned_code = code_cleaner.clean(request.code, request.language)
        
        # Tokenize and extract structure
        tokens = tokenizer.tokenize(cleaned_code, request.language)
        structure = structure_extractor.extract(cleaned_code, request.language, tokens)
        
        # Detect algorithm
        algorithm = algorithm_detector.detect(structure, request.language)
        algorithm_info = algorithm_detector.get_algorithm_info(algorithm)
        
        # Estimate complexity
        complexity = complexity_estimator.estimate(structure, algorithm, request.language)
        
        # Detect bugs using rule engine
        rules = rule_engine.get_rules_for_language(request.language)
        bugs = bug_detector.detect(cleaned_code, structure, rules, request.language)
        
        # Analyze quality
        quality_metrics = quality_analyzer.analyze(cleaned_code, structure, request.language)
        
        # Calculate overall score
        score = scoring_engine.calculate_score(quality_metrics, bugs, complexity)
        score_details = scoring_engine.get_score_details(quality_metrics, bugs, complexity)
        
        # Generate visualization if applicable
        visualization = None
        if algorithm:
            if algorithm == "binary_search":
                visualizer = BinarySearchVisualizer()
                visualization = visualizer.visualize(structure)
            elif algorithm in ["bubble_sort", "quick_sort", "merge_sort"]:
                visualizer = SortingVisualizer()
                visualization = visualizer.visualize(structure, algorithm)
            elif algorithm in ["dfs", "bfs", "dijkstra"]:
                visualizer = GraphVisualizer()
                visualization = visualizer.visualize(structure, algorithm)
        
        # Generate comprehensive report
        report = report_generator.generate(
            code=request.code,
            language=request.language,
            algorithm=algorithm,
            complexity=complexity,
            bugs=bugs,
            quality_metrics=quality_metrics,
            score=score
        )
        
        return CodeAnalysisResponse(
            algorithm=algorithm,
            algorithm_info=algorithm_info,
            complexity=complexity,
            bugs=bugs,
            score=score,
            score_details=score_details,
            visualization=visualization,
            execution_results=report.get("execution_results")
        )
        
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to analyze code")

@router.post("/execute")
async def execute_code(request: CodeAnalysisRequest):
    """Execute code with test cases"""
    
    try:
        # This would integrate with the executor module
        # For now, return a placeholder response
        return {
            "execution_results": {
                "status": "success",
                "output": "Code execution not yet implemented",
                "test_results": []
            }
        }
        
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to execute code")
