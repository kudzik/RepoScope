"""Code analysis service using Tree-sitter."""

import os
from pathlib import Path
from typing import Dict, Optional

import tree_sitter
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

            self.languages["typescript"] = Language(tree_sitter_typescript.language())
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
            ".rs": "rust",
            ".go": "go",
        }

        file_ext = Path(file_path).suffix.lower()
        return extension_map.get(file_ext)

    def analyze_file(self, file_path: str, content: str) -> Dict:
        """Analyze a single file and return statistics."""
        language = self.detect_language(file_path)
        if not language or language not in self.languages:
            return self._basic_analysis(content)

        try:
            parser = Parser()
            parser.language = self.languages[language]
            tree = parser.parse(bytes(content, "utf8"))

            return self._analyze_ast(tree, content, language)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return self._basic_analysis(content)

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
            if node.type in ["function_declaration", "arrow_function", "function_expression"]:
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
                        {"path": file_path, "lines": file_stats["lines_of_code"], "language": lang}
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

        return stats

    def _calculate_complexity_score(self, stats: Dict) -> float:
        """Calculate a simple complexity score."""
        if stats["total_files"] == 0:
            return 0.0

        # Simple complexity score based on file count, lines, and language diversity
        file_score = min(stats["total_files"] / 100, 1.0)  # Normalize to 0-1
        line_score = min(stats["total_lines"] / 10000, 1.0)  # Normalize to 0-1
        diversity_score = min(len(stats["languages"]) / 5, 1.0)  # Normalize to 0-1

        return (file_score + line_score + diversity_score) / 3.0
