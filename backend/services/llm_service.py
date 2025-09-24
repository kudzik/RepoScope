"""LLM service for generating code summaries and recommendations."""

from typing import Dict, List, Optional

from config.llm_optimization import TaskComplexity, llm_config
from middleware.cost_optimization import CostOptimizationMiddleware
from schemas.code_metrics import FileMetrics, RepositoryMetrics


class LLMService:
    """Service for generating AI-powered code analysis and recommendations."""

    def __init__(self) -> None:
        """Initialize LLM service."""
        self.config = llm_config

    async def generate_repository_summary(
        self, repo_metrics: RepositoryMetrics, repo_name: str
    ) -> Dict:
        """Generate comprehensive repository summary."""
        prompt = self._build_repository_prompt(repo_metrics, repo_name)

        # Simulate LLM call (replace with actual LangChain integration)
        summary = await self._call_llm(prompt, TaskComplexity.MEDIUM)

        return {
            "summary": summary,
            "key_insights": self._extract_key_insights(repo_metrics),
            "recommendations": await self._generate_recommendations(repo_metrics),
            "risk_assessment": self._assess_risks(repo_metrics),
        }

    async def generate_file_summary(self, file_metrics: FileMetrics) -> Dict:
        """Generate summary for individual file."""
        prompt = self._build_file_prompt(file_metrics)

        summary = await self._call_llm(prompt, TaskComplexity.SIMPLE)

        return {
            "summary": summary,
            "complexity_analysis": self._analyze_complexity(file_metrics),
            "suggestions": self._generate_file_suggestions(file_metrics),
        }

    async def generate_architecture_analysis(self, repo_metrics: RepositoryMetrics) -> Dict:
        """Generate detailed architecture analysis."""
        prompt = self._build_architecture_prompt(repo_metrics)

        analysis = await self._call_llm(prompt, TaskComplexity.COMPLEX)

        return {
            "architecture_analysis": analysis,
            "design_patterns": self._identify_patterns(repo_metrics),
            "improvement_suggestions": await self._suggest_improvements(repo_metrics),
            "technical_debt": self._calculate_technical_debt(repo_metrics),
        }

    def _build_repository_prompt(self, repo_metrics: RepositoryMetrics, repo_name: str) -> str:
        """Build prompt for repository analysis."""
        return f"""
Analyze the following repository: {repo_name}

Repository Statistics:
- Total files: {repo_metrics.total_files}
- Total lines of code: {repo_metrics.total_lines}
- Languages: {list(repo_metrics.languages.keys())}
- Average complexity: {repo_metrics.avg_complexity:.2f}
- Average maintainability: {repo_metrics.avg_maintainability:.2f}
- Architecture score: {repo_metrics.architecture_score:.2f}
- Code hotspots: {len(repo_metrics.hotspots)}

Please provide:
1. Overall code quality assessment
2. Main strengths and weaknesses
3. Technology stack evaluation
4. Scalability considerations
5. Security implications

Keep the analysis concise and actionable.
"""

    def _build_file_prompt(self, file_metrics: FileMetrics) -> str:
        """Build prompt for file analysis."""
        return f"""
Analyze the following file: {file_metrics.file_path}

File Statistics:
- Language: {file_metrics.language}
- Lines of code: {file_metrics.lines_of_code}
- Cyclomatic complexity: {file_metrics.complexity.cyclomatic_complexity}
- Cognitive complexity: {file_metrics.complexity.cognitive_complexity}
- Maintainability index: {file_metrics.quality.maintainability_index:.2f}
- Detected patterns: {len(file_metrics.patterns)}

Provide a brief analysis focusing on:
1. Code quality assessment
2. Complexity evaluation
3. Specific improvement suggestions
"""

    def _build_architecture_prompt(self, repo_metrics: RepositoryMetrics) -> str:
        """Build prompt for architecture analysis."""
        return f"""
Perform detailed architecture analysis for repository with:
- {repo_metrics.total_files} files
- {len(repo_metrics.languages)} programming languages
- Architecture score: {repo_metrics.architecture_score:.2f}
- {len(repo_metrics.hotspots)} identified hotspots

Focus on:
1. Overall architecture quality
2. Design patterns usage
3. Code organization
4. Dependency management
5. Scalability and maintainability
6. Technical debt assessment
"""

    async def _call_llm(self, prompt: str, complexity: TaskComplexity) -> str:
        """Call LLM with optimized model selection."""
        # Placeholder for actual LangChain integration
        # This would use the cost optimization middleware to select appropriate model

        model_name = self.config.get_optimal_model(complexity)

        # Simulate different response lengths based on complexity
        if complexity == TaskComplexity.SIMPLE:
            return "Brief analysis: Code quality is acceptable with minor improvements needed."
        elif complexity == TaskComplexity.MEDIUM:
            return """
Repository Analysis Summary:
- Good overall structure with clear separation of concerns
- Modern technology stack with appropriate dependencies
- Some areas need refactoring to reduce complexity
- Security practices are generally followed
- Recommended: Focus on test coverage and documentation
"""
        else:  # COMPLEX complexity
            return """
Comprehensive Architecture Analysis:

Strengths:
- Well-organized modular structure
- Appropriate use of design patterns
- Good separation between layers
- Modern development practices

Areas for Improvement:
- Some modules show high complexity
- Technical debt in legacy components
- Dependency management could be optimized
- Performance bottlenecks in data processing

Recommendations:
1. Refactor high-complexity modules
2. Implement comprehensive testing strategy
3. Optimize database queries
4. Consider microservices architecture for scalability
5. Implement proper monitoring and logging
"""

    def _extract_key_insights(self, repo_metrics: RepositoryMetrics) -> List[str]:
        """Extract key insights from repository metrics."""
        insights = []

        if repo_metrics.avg_complexity > 10:
            insights.append("High average complexity detected - consider refactoring")

        if repo_metrics.avg_maintainability < 50:
            insights.append("Low maintainability score - technical debt present")

        if len(repo_metrics.hotspots) > 5:
            insights.append("Multiple code hotspots identified - prioritize cleanup")

        if repo_metrics.architecture_score > 80:
            insights.append("Excellent architecture quality")
        elif repo_metrics.architecture_score < 50:
            insights.append("Architecture needs significant improvement")

        return insights

    async def _generate_recommendations(self, repo_metrics: RepositoryMetrics) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if repo_metrics.avg_complexity > 8:
            recommendations.append("Break down complex functions into smaller units")

        if repo_metrics.avg_maintainability < 60:
            recommendations.append("Improve code documentation and naming conventions")

        if len(repo_metrics.hotspots) > 0:
            recommendations.append("Address identified code hotspots first")

        recommendations.append("Implement automated testing for critical components")
        recommendations.append("Set up continuous integration pipeline")

        return recommendations

    def _assess_risks(self, repo_metrics: RepositoryMetrics) -> Dict:
        """Assess project risks based on metrics."""
        risk_level = "LOW"
        risk_factors = []

        if repo_metrics.avg_complexity > 15:
            risk_level = "HIGH"
            risk_factors.append("Very high code complexity")
        elif repo_metrics.avg_complexity > 10:
            risk_level = "MEDIUM"
            risk_factors.append("Elevated code complexity")

        if repo_metrics.avg_maintainability < 40:
            risk_level = "HIGH"
            risk_factors.append("Poor maintainability")

        if len(repo_metrics.hotspots) > 10:
            risk_level = "HIGH"
            risk_factors.append("Numerous code hotspots")

        return {
            "level": risk_level,
            "factors": risk_factors,
            "mitigation_priority": "HIGH" if risk_level == "HIGH" else "MEDIUM",
        }

    def _analyze_complexity(self, file_metrics: FileMetrics) -> Dict:
        """Analyze file complexity metrics."""
        complexity = file_metrics.complexity

        return {
            "cyclomatic_complexity": {
                "value": complexity.cyclomatic_complexity,
                "assessment": self._assess_cyclomatic_complexity(complexity.cyclomatic_complexity),
            },
            "cognitive_complexity": {
                "value": complexity.cognitive_complexity,
                "assessment": self._assess_cognitive_complexity(complexity.cognitive_complexity),
            },
            "maintainability": {
                "index": file_metrics.quality.maintainability_index,
                "assessment": self._assess_maintainability(
                    file_metrics.quality.maintainability_index
                ),
            },
        }

    def _generate_file_suggestions(self, file_metrics: FileMetrics) -> List[str]:
        """Generate specific suggestions for file improvement."""
        suggestions = []

        if file_metrics.complexity.cyclomatic_complexity > 10:
            suggestions.append("Reduce cyclomatic complexity by extracting methods")

        if file_metrics.complexity.cognitive_complexity > 15:
            suggestions.append("Simplify logic to reduce cognitive load")

        if file_metrics.quality.maintainability_index < 50:
            suggestions.append("Improve code readability and documentation")

        if file_metrics.lines_of_code > 500:
            suggestions.append("Consider splitting large file into smaller modules")

        # Always provide at least one suggestion for moderate complexity
        if not suggestions and file_metrics.complexity.cyclomatic_complexity > 5:
            suggestions.append("Consider refactoring for better maintainability")

        return suggestions

    def _identify_patterns(self, repo_metrics: RepositoryMetrics) -> List[str]:
        """Identify design patterns in repository."""
        # This would analyze the actual patterns detected in files
        patterns = ["Singleton", "Factory", "Observer", "Strategy"]
        return patterns[:2]  # Return subset for demo

    async def _suggest_improvements(self, repo_metrics: RepositoryMetrics) -> List[str]:
        """Suggest architectural improvements."""
        improvements = []

        if repo_metrics.architecture_score < 70:
            improvements.append("Implement proper layered architecture")
            improvements.append("Improve separation of concerns")

        improvements.append("Add comprehensive error handling")
        improvements.append("Implement proper logging strategy")
        improvements.append("Consider dependency injection pattern")

        return improvements

    def _calculate_technical_debt(self, repo_metrics: RepositoryMetrics) -> Dict:
        """Calculate technical debt metrics."""
        # Simplified calculation based on maintainability and complexity
        debt_ratio = (100 - repo_metrics.avg_maintainability) / 100
        debt_hours = repo_metrics.total_lines * debt_ratio * 0.01  # Rough estimate

        return {
            "debt_ratio": debt_ratio,
            "estimated_hours": debt_hours,
            "priority_areas": repo_metrics.hotspots[:5],
            "recommendation": (
                "Focus on hotspots first" if repo_metrics.hotspots else "Maintain current quality"
            ),
        }

    def _assess_cyclomatic_complexity(self, complexity: int) -> str:
        """Assess cyclomatic complexity level."""
        if complexity <= 5:
            return "Low - Easy to test and maintain"
        elif complexity <= 10:
            return "Moderate - Acceptable complexity"
        elif complexity <= 15:
            return "High - Consider refactoring"
        else:
            return "Very High - Refactoring required"

    def _assess_cognitive_complexity(self, complexity: int) -> str:
        """Assess cognitive complexity level."""
        if complexity <= 10:
            return "Low - Easy to understand"
        elif complexity <= 20:
            return "Moderate - Acceptable"
        elif complexity <= 30:
            return "High - May be difficult to understand"
        else:
            return "Very High - Difficult to understand and maintain"

    def _assess_maintainability(self, index: float) -> str:
        """Assess maintainability index."""
        if index >= 80:
            return "Excellent - Highly maintainable"
        elif index >= 60:
            return "Good - Well maintainable"
        elif index >= 40:
            return "Fair - Some maintenance challenges"
        else:
            return "Poor - Significant maintenance issues"
