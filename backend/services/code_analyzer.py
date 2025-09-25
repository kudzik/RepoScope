"""Code analysis service using Tree-sitter."""

import os
from pathlib import Path
from typing import Dict, List, Optional

import tree_sitter
from schemas.code_metrics import (
    CodePattern,
    ComplexityMetrics,
    DependencyInfo,
    FileMetrics,
    QualityMetrics,
    RepositoryMetrics,
)
from tree_sitter import Language, Parser


class CodeAnalyzer:
    """Service for analyzing code structure and statistics using Tree-sitter."""

    def __init__(self) -> None:
        """Initialize the code analyzer with language parsers."""
        self.languages: Dict[str, Language] = {}
        self._setup_language_parsers()

    def _setup_language_parsers(self) -> None:
        """Set up Tree-sitter language parsers."""
        try:
            import tree_sitter_python

            self.languages["python"] = Language(tree_sitter_python.language())
        except Exception as e:
            print(f"Warning: Could not load Python Tree-sitter: {e}")

        try:
            import tree_sitter_javascript

            self.languages["javascript"] = Language(tree_sitter_javascript.language())
        except Exception as e:
            print(f"Warning: Could not load JavaScript Tree-sitter: {e}")

        try:
            import tree_sitter_typescript

            # Try different approaches to get the language
            try:
                # Method 1: Standard approach
                self.languages["typescript"] = Language(tree_sitter_typescript.language())
            except (AttributeError, TypeError):
                try:
                    # Method 2: Check if it's a callable
                    if callable(tree_sitter_typescript.language):
                        self.languages["typescript"] = Language(tree_sitter_typescript.language())
                    else:
                        self.languages["typescript"] = Language(tree_sitter_typescript.language)
                except (AttributeError, TypeError):
                    try:
                        # Method 3: Try to find the language function
                        if hasattr(tree_sitter_typescript, "language"):
                            lang_func = getattr(tree_sitter_typescript, "language")
                            if callable(lang_func):
                                self.languages["typescript"] = Language(lang_func())
                            else:
                                self.languages["typescript"] = Language(lang_func)
                        else:
                            # Method 4: Skip TypeScript if all methods fail
                            print(
                                "Warning: TypeScript Tree-sitter language function "
                                "not found, skipping TypeScript analysis"
                            )
                    except Exception:
                        print(
                            "Warning: TypeScript Tree-sitter not available, "
                            "skipping TypeScript analysis"
                        )
        except ImportError:
            print("Warning: tree_sitter_typescript not installed, " "skipping TypeScript analysis")
        except Exception as e:
            print(f"Warning: Could not load TypeScript Tree-sitter: {e}")

        try:
            import tree_sitter_java

            self.languages["java"] = Language(tree_sitter_java.language())
        except Exception as e:
            print(f"Warning: Could not load Java Tree-sitter: {e}")

        try:
            import tree_sitter_cpp

            self.languages["cpp"] = Language(tree_sitter_cpp.language())
        except Exception as e:
            print(f"Warning: Could not load C++ Tree-sitter: {e}")

        try:
            import tree_sitter_rust

            self.languages["rust"] = Language(tree_sitter_rust.language())
        except Exception as e:
            print(f"Warning: Could not load Rust Tree-sitter: {e}")

        try:
            import tree_sitter_go

            self.languages["go"] = Language(tree_sitter_go.language())
        except Exception as e:
            print(f"Warning: Could not load Go Tree-sitter: {e}")

    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension."""
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".hpp": "cpp",
            ".h": "cpp",
            ".c": "c",  # C language
            ".rs": "rust",
            ".go": "go",
            ".php": "php",
            ".rb": "ruby",
            ".cs": "csharp",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".sh": "shell",
            ".bash": "shell",
            ".zsh": "shell",
            ".fish": "shell",
            ".cmake": "cmake",  # CMake files
            ".dockerfile": "dockerfile",  # Docker files
            ".html": "html",  # HTML files
            ".xml": "xml",  # XML files
            ".sql": "sql",  # SQL files
            ".r": "r",  # R language
            ".m": "matlab",  # MATLAB
            ".pl": "perl",  # Perl
            ".lua": "lua",  # Lua
            ".vim": "vim",  # Vim script
            ".el": "elisp",  # Emacs Lisp
        }

        # Special file names (check before extension)
        filename = Path(file_path).name.lower()
        if filename in ["cmakelists.txt", "makefile", "makefile.am", "makefile.in"]:
            return "cmake" if filename == "cmakelists.txt" else "makefile"
        elif filename == "dockerfile":
            return "dockerfile"

        file_ext = Path(file_path).suffix.lower()
        return extension_map.get(file_ext)

    def analyze_file(self, file_path: str, content: str) -> Dict:
        """Analyze a single file and return statistics."""
        language = self.detect_language(file_path)

        # If we have a language but no Tree-sitter parser, use enhanced basic analysis
        if language and language not in self.languages:
            return self._enhanced_basic_analysis(content, language)

        # If no language detected, use basic analysis
        if not language:
            return self._basic_analysis(content)

        try:
            parser = Parser()
            parser.language = self.languages[language]
            tree = parser.parse(bytes(content, "utf8"))

            return self._analyze_ast(tree, content, language)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            # Fallback to enhanced basic analysis with detected language
            return self._enhanced_basic_analysis(content, language)

    def _analyze_ast(self, tree: tree_sitter.Tree, content: str, language: str) -> Dict:
        """Analyze AST and extract statistics."""
        lines = content.splitlines()

        # Basic statistics
        stats = {
            "lines_of_code": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "language": language,
        }

        # Language-specific analysis
        if language == "python":
            stats.update(self._analyze_python_ast(tree, content))
        elif language in ["javascript", "typescript"]:
            stats.update(self._analyze_js_ast(tree, content))
        elif language == "java":
            stats.update(self._analyze_java_ast(tree, content))
        elif language == "cpp":
            stats.update(self._analyze_cpp_ast(tree, content))
        elif language == "rust":
            stats.update(self._analyze_rust_ast(tree, content))
        elif language == "go":
            stats.update(self._analyze_go_ast(tree, content))

        return stats

    def _analyze_python_ast(self, tree: tree_sitter.Tree, content: str) -> Dict:
        """Analyze Python AST."""
        stats = {
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "comments": 0,
        }

        def traverse_node(node):
            if node.type == "function_definition":
                stats["functions"] += 1
            elif node.type == "class_definition":
                stats["classes"] += 1
            elif node.type in ["import_statement", "import_from_statement"]:
                stats["imports"] += 1
            elif node.type == "comment":
                stats["comments"] += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return stats

    def _analyze_js_ast(self, tree: tree_sitter.Tree, content: str) -> Dict:
        """Analyze JavaScript/TypeScript AST."""
        stats = {
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "comments": 0,
        }

        def traverse_node(node):
            if node.type in [
                "function_declaration",
                "arrow_function",
                "function_expression",
            ]:
                stats["functions"] += 1
            elif node.type == "class_declaration":
                stats["classes"] += 1
            elif node.type in ["import_statement", "import_clause"]:
                stats["imports"] += 1
            elif node.type in ["comment", "line_comment", "block_comment"]:
                stats["comments"] += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return stats

    def _analyze_java_ast(self, tree: tree_sitter.Tree, content: str) -> Dict:
        """Analyze Java AST."""
        stats = {
            "methods": 0,
            "classes": 0,
            "imports": 0,
            "comments": 0,
        }

        def traverse_node(node):
            if node.type == "method_declaration":
                stats["methods"] += 1
            elif node.type == "class_declaration":
                stats["classes"] += 1
            elif node.type == "import_declaration":
                stats["imports"] += 1
            elif node.type in ["line_comment", "block_comment"]:
                stats["comments"] += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return stats

    def _analyze_cpp_ast(self, tree: tree_sitter.Tree, content: str) -> Dict:
        """Analyze C++ AST."""
        stats = {
            "functions": 0,
            "classes": 0,
            "includes": 0,
            "comments": 0,
        }

        def traverse_node(node):
            if node.type == "function_definition":
                stats["functions"] += 1
            elif node.type == "class_specifier":
                stats["classes"] += 1
            elif node.type == "preproc_include":
                stats["includes"] += 1
            elif node.type in ["comment", "line_comment", "block_comment"]:
                stats["comments"] += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return stats

    def _analyze_rust_ast(self, tree: tree_sitter.Tree, content: str) -> Dict:
        """Analyze Rust AST."""
        stats = {
            "functions": 0,
            "structs": 0,
            "imports": 0,
            "comments": 0,
        }

        def traverse_node(node):
            if node.type == "function_item":
                stats["functions"] += 1
            elif node.type == "struct_item":
                stats["structs"] += 1
            elif node.type == "use_declaration":
                stats["imports"] += 1
            elif node.type in ["line_comment", "block_comment"]:
                stats["comments"] += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return stats

    def _analyze_go_ast(self, tree: tree_sitter.Tree, content: str) -> Dict:
        """Analyze Go AST."""
        stats = {
            "functions": 0,
            "structs": 0,
            "imports": 0,
            "comments": 0,
        }

        def traverse_node(node):
            if node.type == "function_declaration":
                stats["functions"] += 1
            elif node.type == "type_declaration":
                stats["structs"] += 1
            elif node.type == "import_declaration":
                stats["imports"] += 1
            elif node.type in ["comment", "line_comment"]:
                stats["comments"] += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return stats

    def _basic_analysis(self, content: str) -> Dict:
        """Perform basic analysis when Tree-sitter is not available."""
        lines = content.splitlines()

        return {
            "lines_of_code": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "language": "unknown",
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "comments": 0,
        }

    def _enhanced_basic_analysis(self, content: str, language: str) -> Dict:
        """Enhanced basic analysis with language-specific heuristics."""
        lines = content.splitlines()

        # Language-specific analysis without Tree-sitter
        functions = 0
        classes = 0
        imports = 0
        comments = 0

        if language == "python":
            functions = len([line for line in lines if line.strip().startswith("def ")])
            classes = len([line for line in lines if line.strip().startswith("class ")])
            imports = len([line for line in lines if line.strip().startswith(("import ", "from "))])
            comments = len([line for line in lines if line.strip().startswith("#")])
        elif language in ["javascript", "typescript"]:
            functions = len(
                [
                    line
                    for line in lines
                    if "function " in line
                    or "=>" in line
                    or "(" in line
                    and ")" in line
                    and "{" in line
                ]
            )
            classes = len([line for line in lines if "class " in line])
            imports = len(
                [line for line in lines if line.strip().startswith(("import ", "require("))]
            )
            comments = len([line for line in lines if line.strip().startswith(("//", "/*"))])
        elif language == "java":
            functions = len(
                [line for line in lines if "public " in line and "(" in line and ")" in line]
            )
            classes = len([line for line in lines if "class " in line])
            imports = len([line for line in lines if line.strip().startswith("import ")])
            comments = len([line for line in lines if line.strip().startswith(("//", "/*"))])
        elif language == "cpp":
            functions = len([line for line in lines if "{" in line and "(" in line and ")" in line])
            classes = len([line for line in lines if "class " in line])
            imports = len([line for line in lines if line.strip().startswith("#include")])
            comments = len([line for line in lines if line.strip().startswith(("//", "/*"))])
        elif language == "rust":
            functions = len([line for line in lines if "fn " in line])
            classes = len([line for line in lines if "struct " in line])
            imports = len([line for line in lines if line.strip().startswith("use ")])
            comments = len([line for line in lines if line.strip().startswith(("//", "/*"))])
        elif language == "go":
            functions = len([line for line in lines if "func " in line])
            classes = len([line for line in lines if "type " in line])
            imports = len([line for line in lines if line.strip().startswith("import ")])
            comments = len([line for line in lines if line.strip().startswith(("//", "/*"))])
        elif language == "c":
            functions = len([line for line in lines if "{" in line and "(" in line and ")" in line])
            classes = 0  # C doesn't have classes
            imports = len([line for line in lines if line.strip().startswith("#include")])
            comments = len([line for line in lines if line.strip().startswith(("//", "/*"))])
        elif language == "cmake":
            functions = len(
                [
                    line
                    for line in lines
                    if "(" in line and ")" in line and not line.strip().startswith("#")
                ]
            )
            classes = 0  # CMake doesn't have classes
            imports = len(
                [
                    line
                    for line in lines
                    if line.strip().startswith(("find_package", "include", "add_subdirectory"))
                ]
            )
            comments = len([line for line in lines if line.strip().startswith("#")])
        elif language == "makefile":
            functions = len(
                [line for line in lines if ":" in line and not line.strip().startswith("#")]
            )
            classes = 0  # Makefiles don't have classes
            imports = len([line for line in lines if line.strip().startswith("include ")])
            comments = len([line for line in lines if line.strip().startswith("#")])
        elif language == "dockerfile":
            functions = len(
                [line for line in lines if line.strip().startswith(("RUN ", "CMD ", "ENTRYPOINT "))]
            )
            classes = 0  # Dockerfiles don't have classes
            imports = len(
                [line for line in lines if line.strip().startswith(("FROM ", "COPY ", "ADD "))]
            )
            comments = len([line for line in lines if line.strip().startswith("#")])
        elif language == "html":
            functions = len([line for line in lines if "<script" in line or "function" in line])
            classes = len([line for line in lines if "class=" in line])
            imports = len(
                [line for line in lines if line.strip().startswith(("<link", "<script", "<style"))]
            )
            comments = len([line for line in lines if line.strip().startswith(("<!--", "//"))])
        elif language == "sql":
            functions = len(
                [
                    line
                    for line in lines
                    if "CREATE FUNCTION" in line.upper() or "CREATE PROCEDURE" in line.upper()
                ]
            )
            classes = 0  # SQL doesn't have classes
            imports = len(
                [line for line in lines if line.strip().startswith(("USE ", "IMPORT ", "INCLUDE "))]
            )
            comments = len([line for line in lines if line.strip().startswith(("--", "/*"))])

        return {
            "lines_of_code": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "blank_lines": len([line for line in lines if not line.strip()]),
            "language": language,
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "comments": comments,
        }

    def _is_code_file(self, file_path: str) -> bool:
        """Check if file is a code file (not documentation, config, etc.)."""
        non_code_extensions = {
            ".md",
            ".txt",
            ".rst",
            ".adoc",  # Documentation
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".ini",
            ".cfg",
            ".conf",  # Config
            ".css",
            ".scss",
            ".sass",
            ".less",  # Styles (not code for analysis)
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".ico",  # Images
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",  # Documents
            ".zip",
            ".tar",
            ".gz",
            ".rar",  # Archives
            ".log",
            ".tmp",
            ".cache",  # Temporary files
        }

        file_ext = Path(file_path).suffix.lower()
        return file_ext not in non_code_extensions

    def analyze_repository(self, repo_path: str) -> Dict:
        """Analyze entire repository and return comprehensive statistics."""
        if not os.path.exists(repo_path):
            return {"error": "Repository path does not exist"}

        stats: Dict = {
            "total_files": 0,
            "total_lines": 0,
            "languages": {},
            "file_types": {},
            "largest_files": [],
            "complexity_score": 0,
            "quality_metrics": {
                "maintainability_index": 0.0,
                "technical_debt_ratio": 0.0,
                "code_duplication": 0.0,
                "test_coverage": 0.0,
            },
            "code_patterns": {
                "design_patterns": [],
                "anti_patterns": [],
                "code_smells": [],
            },
            "architecture_score": 0.0,
            "hotspots": [],
        }

        # Walk through repository
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["node_modules", "__pycache__", "venv", "env"]
            ]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = os.path.join(root, file)

                # Skip non-code files
                if not self._is_code_file(file_path):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    file_stats = self.analyze_file(file_path, content)
                    stats["total_files"] += 1
                    stats["total_lines"] += file_stats["lines_of_code"]

                    # Language statistics
                    lang = file_stats.get("language", "unknown")
                    if lang not in stats["languages"]:
                        stats["languages"][lang] = {"files": 0, "lines": 0}
                    stats["languages"][lang]["files"] += 1
                    stats["languages"][lang]["lines"] += file_stats["lines_of_code"]

                    # File type statistics
                    ext = Path(file_path).suffix.lower()
                    if ext not in stats["file_types"]:
                        stats["file_types"][ext] = 0
                    stats["file_types"][ext] += 1

                    # Track largest files
                    largest_files = stats["largest_files"]
                    largest_files.append(
                        {
                            "path": file_path,
                            "lines": file_stats["lines_of_code"],
                            "language": lang,
                        }
                    )

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    continue

        # Sort largest files
        largest_files = stats["largest_files"]
        largest_files.sort(key=lambda x: x["lines"], reverse=True)
        stats["largest_files"] = largest_files[:10]  # Top 10

        # Calculate complexity score (simple heuristic)
        stats["complexity_score"] = self._calculate_complexity_score(stats)

        # Enhanced quality analysis
        stats["quality_metrics"] = self._calculate_quality_metrics(stats)
        stats["code_patterns"] = self._detect_code_patterns_repository(repo_path)
        stats["architecture_score"] = self._calculate_architecture_score_simple(stats)
        stats["hotspots"] = self._identify_hotspots(stats)

        return stats

    def analyze_repository_enhanced(self, repo_path: str) -> RepositoryMetrics:
        """Enhanced repository analysis with advanced metrics."""
        if not os.path.exists(repo_path):
            return RepositoryMetrics(
                total_files=0,
                total_lines=0,
                languages={},
                avg_complexity=0.0,
                avg_maintainability=0.0,
                hotspots=[],
                architecture_score=0.0,
            )

        file_metrics: List[FileMetrics] = []
        total_complexity = 0.0
        total_maintainability = 0.0
        analyzed_files = 0.0

        # Walk through repository
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["node_modules", "__pycache__", "venv", "env"]
            ]

            for file in files:
                if file.startswith(".") or not self._is_code_file(file):
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    metrics = self.analyze_file_enhanced(file_path, content)
                    file_metrics.append(metrics)

                    if metrics.language != "unknown":
                        total_complexity += metrics.complexity.cyclomatic_complexity
                        total_maintainability += metrics.quality.maintainability_index
                        analyzed_files += 1.0

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    continue

        # Calculate repository-wide metrics
        languages = {}
        total_files = len(file_metrics)
        total_lines = sum(fm.lines_of_code for fm in file_metrics)

        for fm in file_metrics:
            if fm.language not in languages:
                languages[fm.language] = {"files": 0, "lines": 0}
            languages[fm.language]["files"] += 1
            languages[fm.language]["lines"] += fm.lines_of_code

        # Identify hotspots (files with high complexity or low maintainability)
        hotspots = []
        for fm in file_metrics:
            if fm.complexity.cyclomatic_complexity > 10 or fm.quality.maintainability_index < 50:
                hotspots.append(fm.file_path)

        # Calculate architecture score
        architecture_score = self._calculate_architecture_score(file_metrics)

        return RepositoryMetrics(
            total_files=total_files,
            total_lines=total_lines,
            languages=languages,
            avg_complexity=total_complexity / max(analyzed_files, 1),
            avg_maintainability=total_maintainability / max(analyzed_files, 1),
            hotspots=hotspots[:10],  # Top 10 hotspots
            architecture_score=architecture_score,
        )

    def _calculate_architecture_score(self, file_metrics: List[FileMetrics]) -> float:
        """Calculate architecture quality score."""
        if not file_metrics:
            return 0.0

        # Factors: maintainability, complexity, patterns
        total_maintainability = sum(fm.quality.maintainability_index for fm in file_metrics)
        avg_maintainability = total_maintainability / len(file_metrics)

        # Penalty for anti-patterns
        anti_pattern_count = sum(
            len([p for p in fm.patterns if p.pattern_type == "anti_pattern"]) for fm in file_metrics
        )

        # Bonus for design patterns
        design_pattern_count = sum(
            len([p for p in fm.patterns if p.pattern_type == "design_pattern"])
            for fm in file_metrics
        )

        # Calculate score (0-100)
        base_score = avg_maintainability
        pattern_penalty = min(anti_pattern_count * 2, 20)  # Max 20 point penalty
        pattern_bonus = min(design_pattern_count * 1, 10)  # Max 10 point bonus

        return max(0, min(100, base_score - pattern_penalty + pattern_bonus))

    def _calculate_quality_metrics(self, stats: Dict) -> Dict:
        """Calculate quality metrics for the repository."""
        total_files = stats.get("total_files", 0)
        total_lines = stats.get("total_lines", 0)

        if total_files == 0:
            return {
                "maintainability_index": 0.0,
                "technical_debt_ratio": 1.0,
                "code_duplication": 0.0,
                "test_coverage": 0.0,
            }

        # Calculate maintainability index based on complexity and size
        complexity = stats.get("complexity_score", 0.0)
        maintainability = max(0, 100 - (complexity * 20) - (total_lines / 1000))

        # Estimate technical debt ratio
        debt_ratio = min(1.0, complexity * 0.1 + (total_lines / 10000))

        # Estimate code duplication (simplified)
        duplication = min(0.5, total_files / 1000) if total_files > 0 else 0.0

        # Estimate test coverage (simplified)
        test_coverage = min(0.9, total_files / 100) if total_files > 0 else 0.0

        return {
            "maintainability_index": maintainability,
            "technical_debt_ratio": debt_ratio,
            "code_duplication": duplication,
            "test_coverage": test_coverage,
        }

    def _detect_code_patterns_repository(self, repo_path: str) -> Dict:
        """Detect code patterns across the entire repository."""
        patterns: Dict[str, list] = {
            "design_patterns": [],
            "anti_patterns": [],
            "code_smells": [],
        }

        # Walk through repository and analyze files
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if not self._is_code_file(file):
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Detect patterns in this file
                    file_patterns = self._detect_file_patterns(content, file)

                    # Merge patterns
                    for pattern_type, pattern_list in file_patterns.items():
                        patterns[pattern_type].extend(pattern_list)

                except Exception:
                    continue

        return patterns

    def _detect_file_patterns(self, content: str, filename: str) -> Dict:
        """Detect patterns in a single file."""
        patterns: Dict[str, list] = {
            "design_patterns": [],
            "anti_patterns": [],
            "code_smells": [],
        }

        lines = content.splitlines()

        # Detect design patterns
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            # Singleton pattern
            if "singleton" in line_lower or "__new__" in line_lower:
                patterns["design_patterns"].append(
                    {
                        "pattern": "Singleton",
                        "file": filename,
                        "line": i + 1,
                        "confidence": 0.7,
                    }
                )

            # Factory pattern
            if "factory" in line_lower and "create" in line_lower:
                patterns["design_patterns"].append(
                    {
                        "pattern": "Factory",
                        "file": filename,
                        "line": i + 1,
                        "confidence": 0.6,
                    }
                )

            # Observer pattern
            if "observer" in line_lower or "subscribe" in line_lower:
                patterns["design_patterns"].append(
                    {
                        "pattern": "Observer",
                        "file": filename,
                        "line": i + 1,
                        "confidence": 0.6,
                    }
                )

        # Detect anti-patterns
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            # God class (too many methods)
            method_count = len([line for line in lines if "def " in line])
            if "class" in line_lower and method_count > 20:
                patterns["anti_patterns"].append(
                    {
                        "pattern": "God Class",
                        "file": filename,
                        "line": i + 1,
                        "confidence": 0.8,
                    }
                )

            # Long method
            if "def " in line_lower:
                method_lines = self._count_method_lines(lines, i)
                if method_lines > 50:
                    patterns["anti_patterns"].append(
                        {
                            "pattern": "Long Method",
                            "file": filename,
                            "line": i + 1,
                            "confidence": 0.7,
                        }
                    )

            # Dead code
            if "unused" in line_lower or "deprecated" in line_lower:
                patterns["code_smells"].append(
                    {
                        "pattern": "Dead Code",
                        "file": filename,
                        "line": i + 1,
                        "confidence": 0.6,
                    }
                )

        return patterns

    def _count_method_lines(self, lines: List[str], start_line: int) -> int:
        """Count lines in a method starting from start_line."""
        count = 0
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())

        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if not line.strip():  # Empty line
                count += 1
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level and line.strip():
                break

            count += 1

        return count

    def _calculate_architecture_score_simple(self, stats: Dict) -> float:
        """Calculate architecture quality score."""
        total_files = stats.get("total_files", 0)
        languages = stats.get("languages", {})

        if total_files == 0:
            return 0.0

        # Base score from file organization
        file_score = min(100, total_files * 2)

        # Language diversity penalty
        lang_count = len(languages)
        if lang_count > 5:
            file_score *= 0.8  # Penalty for too many languages

        # Size penalty for very large files
        largest_files = stats.get("largest_files", [])
        if largest_files:
            max_file_size = largest_files[0].get("lines", 0)
            if max_file_size > 1000:
                file_score *= 0.7  # Penalty for very large files

        # Complexity penalty
        complexity = stats.get("complexity_score", 0.0)
        if complexity > 0.7:
            file_score *= 0.6  # Penalty for high complexity

        return min(100.0, file_score)

    def _identify_hotspots(self, stats: Dict) -> List[Dict]:
        """Identify code hotspots that need attention."""
        hotspots = []

        # Large files
        largest_files = stats.get("largest_files", [])
        for file_info in largest_files[:5]:  # Top 5 largest files
            if file_info.get("lines", 0) > 500:
                hotspots.append(
                    {
                        "type": "large_file",
                        "file": file_info.get("path", ""),
                        "lines": file_info.get("lines", 0),
                        "severity": ("high" if file_info.get("lines", 0) > 1000 else "medium"),
                        "description": (
                            f"Large file with {
                                file_info.get(
                                    'lines', 0)} lines"
                        ),
                    }
                )

        # High complexity files
        complexity = stats.get("complexity_score", 0.0)
        if complexity > 0.8:
            hotspots.append(
                {
                    "type": "high_complexity",
                    "file": "repository",
                    "lines": 0,
                    "severity": "high",
                    "description": (f"High overall complexity: {complexity:.2f}"),
                }
            )

        # Many files in single language (potential monolith)
        languages = stats.get("languages", {})
        for lang, info in languages.items():
            if info.get("files", 0) > 100:
                hotspots.append(
                    {
                        "type": "monolith",
                        "file": f"{lang} files",
                        "lines": info.get("lines", 0),
                        "severity": "medium",
                        "description": (f"Many {lang} files: {info.get('files', 0)} files"),
                    }
                )

        return hotspots[:10]  # Return top 10 hotspots

    def _calculate_complexity_score(self, stats: Dict) -> float:
        """Calculate actual complexity score based on code analysis."""
        if stats["total_files"] == 0:
            return 0.0

        # Use actual complexity metrics instead of just size
        total_lines = stats.get("total_lines", 0)
        total_files = stats.get("total_files", 0)

        # Calculate average file size
        avg_file_size = total_lines / max(total_files, 1)

        # Calculate complexity based on:
        # 1. Average file size (larger files = more complex)
        # 2. Language diversity (more languages = more complex)
        # 3. Total lines (more code = potentially more complex)

        file_complexity = min(avg_file_size / 200, 1.0)  # Normalize around 200 lines per file
        language_complexity = min(len(stats["languages"]) / 3, 1.0)  # Normalize around 3 languages
        size_complexity = min(total_lines / 5000, 1.0)  # Normalize around 5000 lines

        # Weighted average with emphasis on file complexity
        return file_complexity * 0.5 + language_complexity * 0.3 + size_complexity * 0.2

    def calculate_cyclomatic_complexity(self, tree: tree_sitter.Tree, language: str) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        def traverse_node(node):
            nonlocal complexity
            # Decision points that increase complexity
            if language == "python":
                if node.type in [
                    "if_statement",
                    "while_statement",
                    "for_statement",
                    "try_statement",
                    "except_clause",
                    "elif_clause",
                ]:
                    complexity += 1
            elif language in ["javascript", "typescript"]:
                if node.type in [
                    "if_statement",
                    "while_statement",
                    "for_statement",
                    "switch_statement",
                    "case_clause",
                    "catch_clause",
                ]:
                    complexity += 1
            elif language == "java":
                if node.type in [
                    "if_statement",
                    "while_statement",
                    "for_statement",
                    "switch_expression",
                    "catch_clause",
                ]:
                    complexity += 1

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)
        return complexity

    def calculate_cognitive_complexity(self, tree: tree_sitter.Tree, language: str) -> int:
        """Calculate cognitive complexity."""
        complexity = 0

        def traverse_node(node, level=0):
            nonlocal complexity

            # Increment for control structures
            if language == "python":
                if node.type in [
                    "if_statement",
                    "while_statement",
                    "for_statement",
                ]:
                    complexity += 1 + level
                elif node.type in ["try_statement", "except_clause"]:
                    complexity += 1
            elif language in ["javascript", "typescript"]:
                if node.type in [
                    "if_statement",
                    "while_statement",
                    "for_statement",
                ]:
                    complexity += 1 + level
                elif node.type in ["switch_statement", "catch_clause"]:
                    complexity += 1

            # Increase nesting level for certain constructs
            new_level = level
            if node.type in [
                "if_statement",
                "while_statement",
                "for_statement",
                "function_definition",
            ]:
                new_level = level + 1

            for child in node.children:
                traverse_node(child, new_level)

        traverse_node(tree.root_node)
        return complexity

    def calculate_nesting_depth(self, tree: tree_sitter.Tree) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0

        def traverse_node(node, depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, depth)

            # Increase depth for nesting constructs
            new_depth = depth
            if node.type in [
                "if_statement",
                "while_statement",
                "for_statement",
                "function_definition",
                "class_definition",
                "block",
            ]:
                new_depth = depth + 1

            for child in node.children:
                traverse_node(child, new_depth)

        traverse_node(tree.root_node)
        return max_depth

    def detect_code_patterns(
        self, tree: tree_sitter.Tree, content: str, language: str
    ) -> List[CodePattern]:
        """Detect code patterns and anti-patterns."""
        patterns = []
        lines = content.splitlines()

        # Detect common anti-patterns
        patterns.extend(self._detect_anti_patterns(tree, lines, language))

        # Detect design patterns
        patterns.extend(self._detect_design_patterns(tree, lines, language))

        return patterns

    def _detect_anti_patterns(
        self, tree: tree_sitter.Tree, lines: List[str], language: str
    ) -> List[CodePattern]:
        """Detect anti-patterns in code."""
        patterns = []

        # Long method detection
        def traverse_for_long_methods(node, line_num=0):
            if language == "python" and node.type == "function_definition":
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                method_length = end_line - start_line

                if method_length > 50:  # Threshold for long method
                    patterns.append(
                        CodePattern(
                            pattern_type="anti_pattern",
                            pattern_name="Long Method",
                            confidence=0.8,
                            location=f"Line {start_line + 1}",
                            line_number=start_line + 1,
                        )
                    )

            for child in node.children:
                traverse_for_long_methods(child)

        # God class detection (many methods)
        def traverse_for_god_class(node):
            if language == "python" and node.type == "class_definition":
                method_count = 0

                def count_methods(class_node):
                    count = 0
                    for child in class_node.children:
                        if child.type == "block":
                            for grandchild in child.children:
                                if grandchild.type == "function_definition":
                                    count += 1
                        elif child.type == "function_definition":
                            count += 1
                    return count

                method_count = count_methods(node)

                if method_count > 20:  # Threshold for god class
                    patterns.append(
                        CodePattern(
                            pattern_type="anti_pattern",
                            pattern_name="God Class",
                            confidence=0.7,
                            location=f"Line {node.start_point[0] + 1}",
                            line_number=node.start_point[0] + 1,
                        )
                    )

            for child in node.children:
                traverse_for_god_class(child)

        traverse_for_long_methods(tree.root_node)
        traverse_for_god_class(tree.root_node)

        return patterns

    def _detect_design_patterns(
        self, tree: tree_sitter.Tree, lines: List[str], language: str
    ) -> List[CodePattern]:
        """Detect design patterns in code."""
        patterns = []

        # Singleton pattern detection
        if language == "python":
            for i, line in enumerate(lines):
                if "__new__" in line and "cls" in line:
                    patterns.append(
                        CodePattern(
                            pattern_type="design_pattern",
                            pattern_name="Singleton",
                            confidence=0.6,
                            location=f"Line {i + 1}",
                            line_number=i + 1,
                        )
                    )

        return patterns

    def analyze_dependencies(
        self, tree: tree_sitter.Tree, content: str, language: str
    ) -> DependencyInfo:
        """Analyze code dependencies."""
        imports = []
        exports: List[str] = []

        def traverse_node(node):
            if language == "python":
                if node.type == "import_statement":
                    import_text = content[node.start_byte : node.end_byte]
                    imports.append(import_text.strip())
                elif node.type == "import_from_statement":
                    import_text = content[node.start_byte : node.end_byte]
                    imports.append(import_text.strip())
            elif language in ["javascript", "typescript"]:
                if node.type == "import_statement":
                    import_text = content[node.start_byte : node.end_byte]
                    imports.append(import_text.strip())

            for child in node.children:
                traverse_node(child)

        traverse_node(tree.root_node)

        # Classify dependencies
        internal_deps = []
        external_deps = []

        for imp in imports:
            if any(marker in imp for marker in [".", "./", "../"]):
                internal_deps.append(imp)
            else:
                external_deps.append(imp)

        return DependencyInfo(
            imports=imports,
            exports=exports,
            internal_deps=internal_deps,
            external_deps=external_deps,
        )

    def calculate_maintainability_index(self, complexity: ComplexityMetrics, loc: int) -> float:
        """Calculate maintainability index."""
        if loc == 0:
            return 100.0

        # Simplified maintainability index calculation
        # Based on cyclomatic complexity and lines of code
        cc = max(complexity.cyclomatic_complexity, 1)
        mi = max(
            0,
            (171 - 5.2 * (cc**0.23) - 0.23 * cc - 16.2 * (loc**0.5)) * 100 / 171,
        )

        return min(100.0, mi)

    def analyze_file_enhanced(self, file_path: str, content: str) -> FileMetrics:
        """Enhanced file analysis with advanced metrics."""
        language = self.detect_language(file_path)
        if not language or language not in self.languages:
            return self._basic_file_metrics(file_path, content)

        try:
            parser = Parser()
            parser.language = self.languages[language]
            tree = parser.parse(bytes(content, "utf8"))

            lines = content.splitlines()
            loc = len([line for line in lines if line.strip()])

            # Calculate complexity metrics
            complexity = ComplexityMetrics(
                cyclomatic_complexity=self.calculate_cyclomatic_complexity(tree, language),
                cognitive_complexity=self.calculate_cognitive_complexity(tree, language),
                nesting_depth=self.calculate_nesting_depth(tree),
                function_length=loc,
            )

            # Calculate quality metrics
            maintainability = self.calculate_maintainability_index(complexity, loc)
            quality = QualityMetrics(
                maintainability_index=maintainability,
                technical_debt_ratio=max(0, (100 - maintainability) / 100),
                code_duplication=0.0,  # Would need more sophisticated analysis
                test_coverage=0.0,  # Would need test file analysis
            )

            # Analyze dependencies
            dependencies = self.analyze_dependencies(tree, content, language)

            # Detect patterns
            patterns = self.detect_code_patterns(tree, content, language)

            return FileMetrics(
                file_path=file_path,
                language=language,
                lines_of_code=loc,
                complexity=complexity,
                quality=quality,
                dependencies=dependencies,
                patterns=patterns,
            )

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return self._basic_file_metrics(file_path, content)

    def _basic_file_metrics(self, file_path: str, content: str) -> FileMetrics:
        """Basic file metrics when Tree-sitter analysis fails."""
        lines = content.splitlines()
        loc = len([line for line in lines if line.strip()])

        return FileMetrics(
            file_path=file_path,
            language="unknown",
            lines_of_code=loc,
            complexity=ComplexityMetrics(
                cyclomatic_complexity=0,
                cognitive_complexity=0,
                nesting_depth=0,
                function_length=0,
            ),
            quality=QualityMetrics(
                maintainability_index=50.0,
                technical_debt_ratio=0.5,
                code_duplication=0.0,
                test_coverage=0.0,
            ),
            dependencies=DependencyInfo(),
            patterns=[],
        )
