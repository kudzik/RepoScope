"""Tests for language detection functionality."""

import pytest
from services.code_analyzer import CodeAnalyzer


class TestLanguageDetection:
    """Test language detection functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()

    def test_detect_python_language(self):
        """Test Python language detection."""
        test_cases = [
            ("main.py", "python"),
            ("script.py", "python"),
            ("test_file.py", "python"),
            ("module/__init__.py", "python"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_javascript_language(self):
        """Test JavaScript language detection."""
        test_cases = [
            ("main.js", "javascript"),
            ("script.js", "javascript"),
            ("app.js", "javascript"),
            ("component.jsx", "javascript"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_typescript_language(self):
        """Test TypeScript language detection."""
        test_cases = [
            ("main.ts", "typescript"),
            ("script.ts", "typescript"),
            ("app.ts", "typescript"),
            ("component.tsx", "typescript"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_java_language(self):
        """Test Java language detection."""
        test_cases = [
            ("Main.java", "java"),
            ("Test.java", "java"),
            ("App.java", "java"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_cpp_language(self):
        """Test C++ language detection."""
        test_cases = [
            ("main.cpp", "cpp"),
            ("script.cc", "cpp"),
            ("app.cxx", "cpp"),
            ("header.hpp", "cpp"),
            ("header.h", "cpp"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_rust_language(self):
        """Test Rust language detection."""
        test_cases = [
            ("main.rs", "rust"),
            ("lib.rs", "rust"),
            ("crate.rs", "rust"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_go_language(self):
        """Test Go language detection."""
        test_cases = [
            ("main.go", "go"),
            ("server.go", "go"),
            ("client.go", "go"),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_detect_unknown_language(self):
        """Test unknown language detection."""
        test_cases = [
            ("file.txt", None),
            ("README.md", None),
            ("config.json", None),
            ("data.csv", None),
            ("image.png", None),
        ]

        for file_path, expected_language in test_cases:
            result = self.analyzer.detect_language(file_path)
            assert (
                result == expected_language
            ), f"Failed for {file_path}: expected {expected_language}, got {result}"

    def test_enhanced_basic_analysis_python(self):
        """Test enhanced basic analysis for Python."""
        python_code = """
# This is a Python file
import os
from pathlib import Path

class MyClass:
    def __init__(self):
        self.value = 42

    def my_method(self):
        return self.value

def my_function():
    return "Hello World"

if __name__ == "__main__":
    print("Hello")
"""

        result = self.analyzer._enhanced_basic_analysis(python_code, "python")

        assert result["language"] == "python"
        assert result["functions"] >= 2  # __init__ and my_function
        assert result["classes"] == 1  # MyClass
        assert result["imports"] == 2  # import os, from pathlib import Path
        assert result["comments"] == 1  # # This is a Python file
        assert result["lines_of_code"] > 0

    def test_enhanced_basic_analysis_javascript(self):
        """Test enhanced basic analysis for JavaScript."""
        js_code = """
// This is a JavaScript file
import { useState } from 'react';
const fs = require('fs');

class MyClass {
    constructor() {
        this.value = 42;
    }

    myMethod() {
        return this.value;
    }
}

function myFunction() {
    return "Hello World";
}

const arrowFunction = () => {
    return "Arrow";
};
"""

        result = self.analyzer._enhanced_basic_analysis(js_code, "javascript")

        assert result["language"] == "javascript"
        assert result["functions"] >= 2  # myFunction and arrowFunction
        assert result["classes"] == 1  # MyClass
        assert result["imports"] >= 1  # import and require
        assert result["comments"] == 1  # // This is a JavaScript file
        assert result["lines_of_code"] > 0

    def test_enhanced_basic_analysis_java(self):
        """Test enhanced basic analysis for Java."""
        java_code = """
// This is a Java file
import java.util.List;
import java.util.ArrayList;

public class MyClass {
    private int value;

    public MyClass() {
        this.value = 42;
    }

    public int getValue() {
        return this.value;
    }

    public void setValue(int value) {
        this.value = value;
    }
}
"""

        result = self.analyzer._enhanced_basic_analysis(java_code, "java")

        assert result["language"] == "java"
        assert result["functions"] >= 3  # constructor, getValue, setValue
        assert result["classes"] == 1  # MyClass
        assert result["imports"] == 2  # import statements
        assert result["comments"] == 1  # // This is a Java file
        assert result["lines_of_code"] > 0

    def test_enhanced_basic_analysis_rust(self):
        """Test enhanced basic analysis for Rust."""
        rust_code = """
// This is a Rust file
use std::collections::HashMap;

struct MyStruct {
    value: i32,
}

impl MyStruct {
    fn new() -> Self {
        Self { value: 42 }
    }

    fn get_value(&self) -> i32 {
        self.value
    }
}

fn main() {
    let instance = MyStruct::new();
    println!("Value: {}", instance.get_value());
}
"""

        result = self.analyzer._enhanced_basic_analysis(rust_code, "rust")

        assert result["language"] == "rust"
        assert result["functions"] >= 2  # new, get_value, main
        assert result["classes"] == 1  # MyStruct
        assert result["imports"] == 1  # use statement
        assert result["comments"] == 1  # // This is a Rust file
        assert result["lines_of_code"] > 0

    def test_enhanced_basic_analysis_go(self):
        """Test enhanced basic analysis for Go."""
        go_code = """
// This is a Go file
package main

import (
    "fmt"
    "os"
)

type MyStruct struct {
    Value int
}

func NewMyStruct() *MyStruct {
    return &MyStruct{Value: 42}
}

func (m *MyStruct) GetValue() int {
    return m.Value
}

func main() {
    instance := NewMyStruct()
    fmt.Println("Value:", instance.GetValue())
}
"""

        result = self.analyzer._enhanced_basic_analysis(go_code, "go")

        assert result["language"] == "go"
        assert result["functions"] >= 3  # NewMyStruct, GetValue, main
        assert result["classes"] == 1  # MyStruct
        assert result["imports"] == 1  # import statement
        assert result["comments"] == 1  # // This is a Go file
        assert result["lines_of_code"] > 0

    def test_analyze_file_with_detected_language(self):
        """Test analyze_file with detected language."""
        python_code = """
def hello():
    print("Hello World")

class Test:
    pass
"""

        result = self.analyzer.analyze_file("test.py", python_code)

        assert result["language"] == "python"
        assert result["functions"] == 1
        assert result["classes"] == 1
        assert result["lines_of_code"] > 0

    def test_analyze_file_unknown_extension(self):
        """Test analyze_file with unknown extension."""
        content = "This is just text content"

        result = self.analyzer.analyze_file("file.txt", content)

        assert result["language"] == "unknown"
        assert result["lines_of_code"] > 0


if __name__ == "__main__":
    pytest.main([__file__])
