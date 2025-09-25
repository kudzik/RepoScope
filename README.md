# RepoScope - Repository Analysis Tool

RepoScope is an AI-powered repository analysis tool that provides comprehensive insights into code quality, documentation, and architecture of GitHub repositories.

## 🚀 Features

### Code Analysis

- **Language Detection**: Automatic detection of programming languages with color-coded visualization
- **Code Metrics**: Lines of code, file count, complexity analysis, and average file size
- **Quality Metrics**: Maintainability index, technical debt ratio, code duplication, and architecture score
- **File Analysis**: Largest files identification with language detection

### AI-Powered Insights

- **Code Quality Assessment**: Comprehensive analysis of code structure and patterns
- **Security Analysis**: Identification of potential security risks and vulnerabilities
- **Documentation Evaluation**: Assessment of README, API docs, and code comments
- **Recommendations**: AI-generated suggestions for code improvements

### Visual Dashboard

- **Interactive Charts**: Color-coded language distribution with percentage bars
- **Progress Indicators**: Visual representation of quality metrics
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark/Light Theme**: Automatic theme switching based on system preferences

## 🛠️ Technology Stack

### Frontend

- **Next.js 15.5.4** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI component library
- **Lucide React** - Beautiful icons

### Backend

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Tree-sitter** - Language parsing (optional, with fallback)
- **aiohttp** - Asynchronous HTTP client
- **psutil** - System resource monitoring

### Analysis Engine

- **Heuristic Analysis** - Pattern-based code analysis
- **Language Detection** - File extension and content-based detection
- **Complexity Calculation** - Cyclomatic complexity scoring
- **Quality Metrics** - Comprehensive code quality assessment

## 📦 Installation

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

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

### Docker Setup (Optional)

```bash
docker-compose up -d
```

## 🚀 Quick Start

1. **Start the Backend**

   ```bash
   cd backend
   python main.py
   ```

   Backend will be available at `http://localhost:8000`

2. **Start the Frontend**

   ```bash
   cd frontend
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

3. **Analyze a Repository**
   - Open `http://localhost:3000` in your browser
   - Enter a GitHub repository URL (e.g., `https://github.com/microsoft/vscode`)
   - Click "Analyze Repository"
   - View comprehensive analysis results

## 📊 API Documentation

### Endpoints

#### `GET /`

- **Description**: API health check
- **Response**: `{"message": "RepoScope API is running!", "version": "1.0.0"}`

#### `POST /analysis/`

- **Description**: Analyze a GitHub repository
- **Request Body**:
  ```json
  {
    "repository_url": "https://github.com/username/repository",
    "include_ai_summary": true,
    "analysis_depth": "standard"
  }
  ```
- **Response**: Comprehensive analysis results

#### `GET /health`

- **Description**: Detailed health check with system information
- **Response**: System status, process info, and resource usage

### Analysis Parameters

#### `analysis_depth`

- **`quick`**: Fast analysis for large repositories (recommended for >10MB)
- **`standard`**: Comprehensive analysis with all metrics
- **`deep`**: Detailed analysis with advanced insights

#### `include_ai_summary`

- **`true`**: Include AI-generated summary and recommendations
- **`false`**: Basic metrics only (faster processing)

## 🔧 Configuration

### Environment Variables

#### Frontend (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RepoScope
NEXT_PUBLIC_APP_VERSION=1.0.0
```

#### Backend

```env
# Optional: Custom configuration
MAX_REPOSITORY_SIZE_MB=50
ANALYSIS_TIMEOUT_SECONDS=120
CACHE_TTL_HOURS=24
```

## 📈 Metrics Explained

### Basic Metrics

- **Lines of Code**: Total lines including comments and blank lines
- **Files**: Number of source code files
- **Complexity**: Cyclomatic complexity score (lower is better)
- **Avg File Size**: Average lines per file

### Quality Metrics

- **Maintainability** (0-100): Code maintainability index
- **Tech Debt** (0-100%): Technical debt ratio
- **Duplication** (0-100%): Code duplication percentage
- **Architecture** (0-100): Architecture quality score

### Additional Metrics

- **Overall Score** (0-100): Combined quality score
- **Test Coverage** (0-100%): Code coverage by tests
- **Issues Found**: Number of identified problems
- **Recommendations**: Number of improvement suggestions

## 🎨 UI Components

### Code Metrics Panel

- **Languages**: Color-coded distribution with percentage bars
- **Largest Files**: Top 5 largest files with language indicators
- **Basic Metrics**: Core repository statistics
- **Quality Metrics**: Code quality assessment with progress bars
- **Additional Metrics**: Extended analysis results

### Interactive Features

- **Tooltips**: Hover explanations for all metrics
- **Progress Bars**: Visual representation of percentages
- **Color Coding**: Consistent color scheme across components
- **Responsive Layout**: Adaptive design for all screen sizes

## 🔍 Language Support

### Supported Languages

- **Primary**: Python, JavaScript, TypeScript, Java, C++, Rust, Go
- **Secondary**: PHP, Ruby, C#, Swift, Kotlin, Scala
- **Scripts**: Shell, Bash, PowerShell
- **Config**: Dockerfile, CMake, Makefile, HTML, CSS, SQL
- **Special**: R, MATLAB, Perl, Lua, Vim, Emacs Lisp

### Language Detection

- **File Extensions**: Primary detection method
- **Special Files**: CMakeLists.txt, Dockerfile, Makefile
- **Content Analysis**: Heuristic-based detection for edge cases
- **Fallback**: Enhanced basic analysis when Tree-sitter unavailable

## 🚨 Error Handling

### API Monitoring

- **Request Logging**: All API requests logged with duration
- **Timeout Handling**: 120-second timeout for analysis requests
- **Error Recovery**: Graceful fallback for parsing failures
- **Resource Monitoring**: CPU and memory usage tracking

### Repository Size Control

- **Size Limits**: Automatic rejection of oversized repositories
- **GitHub API**: Repository size checking before analysis
- **Popularity Limits**: Protection against very popular repositories
- **Cache Management**: Intelligent caching for repeated requests

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Test Coverage

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Language Detection**: Comprehensive language detection tests
- **API Tests**: Backend endpoint testing

## 📝 Development

### Project Structure

```
RepoScope/
├── backend/
│   ├── api/                 # FastAPI endpoints
│   ├── services/           # Business logic
│   ├── schemas/            # Pydantic models
│   ├── middleware/         # API monitoring
│   ├── tests/              # Backend tests
│   └── main.py             # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── lib/           # Utilities
│   │   └── app/           # Next.js app router
│   └── package.json       # Dependencies
└── README.md              # This file
```

### Code Style

- **Python**: Black formatter, Flake8 linter
- **TypeScript**: ESLint, Prettier
- **React**: Functional components with hooks
- **API**: RESTful design with proper HTTP status codes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style and patterns
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tree-sitter** for language parsing capabilities
- **FastAPI** for the excellent Python web framework
- **Next.js** for the powerful React framework
- **Tailwind CSS** for the utility-first CSS approach
- **shadcn/ui** for the beautiful component library

## 📞 Support

For support, email support@reposcope.dev or create an issue on GitHub.

---

**RepoScope** - Analyze repositories with AI-powered insights 🚀
