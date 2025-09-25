# Contributing to RepoScope

Thank you for your interest in contributing to RepoScope! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Provide detailed reproduction steps
- Include system information and error logs
- Check existing issues before creating new ones

### Suggesting Features

- Open a feature request issue
- Describe the use case and benefits
- Consider implementation complexity
- Discuss with maintainers before starting work

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+ (backend)
- Node.js 18+ (frontend)
- Git
- Code editor with TypeScript support

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Full Stack Development

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

## 📝 Code Style Guidelines

### Python (Backend)

- **Formatter**: Black
- **Linter**: Flake8
- **Type Hints**: Required for all functions
- **Docstrings**: Google-style documentation

```python
def analyze_repository(repo_url: str, depth: str = "standard") -> AnalysisResult:
    """
    Analyze a GitHub repository for code quality and metrics.

    Args:
        repo_url: GitHub repository URL
        depth: Analysis depth level

    Returns:
        AnalysisResult: Comprehensive analysis results

    Raises:
        RepositoryError: If repository cannot be accessed
        AnalysisError: If analysis fails
    """
    # Implementation here
    pass
```

### TypeScript (Frontend)

- **Formatter**: Prettier
- **Linter**: ESLint
- **Components**: Functional components with hooks
- **Styling**: Tailwind CSS

```typescript
interface ComponentProps {
  title: string;
  data: AnalysisData;
  onUpdate?: (data: AnalysisData) => void;
}

const Component: React.FC<ComponentProps> = ({ title, data, onUpdate }) => {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold">{title}</h2>
      {/* Component content */}
    </div>
  );
};
```

## 🧪 Testing Requirements

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v --cov=services
```

**Test Categories:**

- Unit tests for individual functions
- Integration tests for API endpoints
- Language detection tests
- Analysis engine tests

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

**Test Categories:**

- Component unit tests
- API integration tests
- User interaction tests
- Visual regression tests

### Test Coverage

- **Minimum**: 80% code coverage
- **New Features**: 100% coverage required
- **Critical Paths**: Comprehensive testing

## 📋 Pull Request Process

### Before Submitting

1. **Fork and Clone**: Fork the repository and clone locally
2. **Create Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature or fix
4. **Add Tests**: Include tests for new functionality
5. **Update Docs**: Update documentation as needed
6. **Test Locally**: Ensure all tests pass

### PR Requirements

- **Clear Title**: Descriptive title explaining the change
- **Description**: Detailed description of changes and motivation
- **Tests**: All tests must pass
- **Documentation**: Update relevant documentation
- **Screenshots**: For UI changes, include before/after screenshots

### PR Template

```markdown
## Description

Brief description of changes and motivation.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🎯 Contribution Areas

### High Priority

- **Language Support**: Add support for new programming languages
- **Performance**: Optimize analysis speed and memory usage
- **UI/UX**: Improve user interface and experience
- **Documentation**: Enhance documentation and examples

### Medium Priority

- **API Features**: Add new analysis endpoints
- **Visualization**: Improve charts and graphs
- **Accessibility**: Enhance accessibility features
- **Internationalization**: Add multi-language support

### Low Priority

- **Themes**: Add new UI themes
- **Integrations**: Third-party service integrations
- **Advanced Features**: Complex analysis features
- **Optimization**: Performance micro-optimizations

## 🐛 Bug Reports

### Required Information

- **Environment**: OS, Python/Node versions
- **Steps**: Detailed reproduction steps
- **Expected**: What should happen
- **Actual**: What actually happens
- **Logs**: Relevant error logs and stack traces

### Bug Report Template

```markdown
## Bug Description

Brief description of the bug.

## Environment

- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.0]
- Node: [e.g., 18.0.0]

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Screenshots

If applicable, add screenshots.

## Additional Context

Any other context about the problem.
```

## 🚀 Feature Requests

### Feature Request Template

```markdown
## Feature Description

Brief description of the feature.

## Use Case

Describe the use case and benefits.

## Proposed Solution

How you think this should be implemented.

## Alternatives

Any alternative solutions you've considered.

## Additional Context

Any other context or screenshots.
```

## 📚 Documentation

### Documentation Standards

- **README**: Keep main README updated
- **API Docs**: Update API documentation for new endpoints
- **Code Comments**: Add comments for complex logic
- **Examples**: Provide usage examples

### Documentation Types

- **User Documentation**: How to use the application
- **Developer Documentation**: How to contribute and develop
- **API Documentation**: Endpoint specifications
- **Architecture Documentation**: System design and components

## 🔧 Development Tools

### Recommended Tools

- **IDE**: VS Code with Python and TypeScript extensions
- **Git**: Use conventional commit messages
- **Testing**: pytest (Python), Jest (JavaScript)
- **Linting**: Black, Flake8 (Python), ESLint (TypeScript)

### VS Code Extensions

- Python
- TypeScript and JavaScript
- Tailwind CSS IntelliSense
- GitLens
- Prettier
- ESLint

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Pull Requests**: Code review and feedback

### Code Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Manual Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: Maintainer approval required
5. **Merge**: Changes merged to main branch

## 🎉 Recognition

### Contributor Recognition

- **Contributors**: Listed in README
- **Special Thanks**: Notable contributions highlighted
- **Maintainers**: Long-term contributors may become maintainers

### Contribution Types

- **Code**: Bug fixes, features, improvements
- **Documentation**: README, API docs, examples
- **Testing**: Test cases, bug reports
- **Community**: Help others, answer questions

## 📄 License

By contributing to RepoScope, you agree that your contributions will be licensed under the MIT License.

## 👨‍💻 Author

**Artur Kud** - kudzik@outlook.com

## 🙏 Thank You

Thank you for contributing to RepoScope! Your contributions help make the project better for everyone.

---

For questions or clarifications, please contact Artur Kud at kudzik@outlook.com or open an issue on GitHub.
