# RepoScope Frontend

Modern React-based frontend for repository analysis with AI-powered insights.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   └── globals.css        # Global styles
│   ├── components/            # React components
│   │   ├── analysis-results.tsx # Main analysis display
│   │   ├── api-debug.tsx      # API debugging tools
│   │   └── ui/                # shadcn/ui components
│   ├── lib/                   # Utilities
│   │   └── api-types.ts       # TypeScript interfaces
│   └── styles/                # Additional styles
├── public/                    # Static assets
├── .env.local                 # Environment variables
└── package.json               # Dependencies
```

## 🎨 UI Components

### Main Components

#### Analysis Results (`analysis-results.tsx`)

The main component displaying comprehensive analysis results:

- **Code Metrics Panel**: Basic metrics, quality metrics, and additional metrics
- **Languages Section**: Color-coded language distribution with percentage bars
- **Largest Files**: Top 5 largest files with language indicators
- **Interactive Tooltips**: Hover explanations for all metrics

#### API Debug (`api-debug.tsx`)

Development tool for API monitoring and debugging:

- **Endpoint Testing**: Test all API endpoints
- **Health Monitoring**: System resource monitoring
- **Performance Metrics**: Request duration and success rates

### UI Features

#### Responsive Design

- **Desktop**: 4-column layout for metrics
- **Tablet**: 2-column layout
- **Mobile**: Single column layout

#### Theme Support

- **Light Theme**: Clean, professional appearance
- **Dark Theme**: Modern dark mode
- **System Theme**: Automatic theme switching

#### Interactive Elements

- **Tooltips**: Hover explanations for all metrics
- **Progress Bars**: Visual representation of percentages
- **Color Coding**: Consistent color scheme
- **Loading States**: Smooth loading animations

## 🔧 Configuration

### Environment Variables (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RepoScope
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### API Configuration

The frontend connects to the backend API using the configured URL. All API calls are made to the backend service for analysis processing.

## 🎯 Key Features

### Code Metrics Display

#### Basic Metrics

- **Lines of Code**: Total repository lines with tooltip
- **Files**: Source code file count
- **Complexity**: Cyclomatic complexity score
- **Avg File Size**: Average lines per file

#### Quality Metrics

- **Maintainability**: Code maintainability index (0-100)
- **Tech Debt**: Technical debt ratio with progress bar
- **Duplication**: Code duplication percentage
- **Architecture**: Architecture quality score

#### Additional Metrics

- **Overall Score**: Combined quality score
- **Test Coverage**: Code coverage percentage
- **Issues Found**: Number of identified problems
- **Recommendations**: Improvement suggestions count

### Language Analysis

#### Language Distribution

- **Color-coded Bar**: Visual percentage distribution
- **Language Details**: Files, lines, and percentages
- **Progress Bars**: Individual language progress
- **Sorting**: Unknown languages always last

#### Language Colors

Consistent color scheme for all supported languages:

- Python: Blue (#3776ab)
- JavaScript: Yellow (#f7df1e)
- TypeScript: Blue (#3178c6)
- Java: Orange (#f89820)
- C++: Blue (#00599c)
- And 15+ more languages

### File Analysis

#### Largest Files

- **Top 5 Files**: Largest files with line counts
- **Language Indicators**: Color-coded language dots
- **File Names**: Clean file name display
- **Line Counts**: Formatted line numbers

## 🛠️ Development

### Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Linting
npm run lint

# Formatting
npm run format
```

### Code Style

- **ESLint**: Code linting with Next.js rules
- **Prettier**: Code formatting
- **TypeScript**: Type safety
- **Functional Components**: React hooks pattern

### Component Guidelines

#### Component Structure

```typescript
interface ComponentProps {
  // Props interface
}

const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Component logic
  return (
    <div>
      {/* JSX content */}
    </div>
  );
};

export default Component;
```

#### Styling Guidelines

- **Tailwind CSS**: Utility-first approach
- **shadcn/ui**: Pre-built components
- **Responsive Design**: Mobile-first approach
- **Accessibility**: ARIA labels and keyboard navigation

## 🧪 Testing

### Test Setup

```bash
# Run tests
npm test

# Test coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

### Testing Strategy

- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **E2E Tests**: Full user workflow testing
- **Visual Tests**: UI component testing

## 🎨 Design System

### Color Palette

- **Primary**: Blue shades for main actions
- **Success**: Green for positive metrics
- **Warning**: Yellow/Orange for caution
- **Error**: Red for issues and problems
- **Info**: Cyan/Teal for information

### Typography

- **Font**: Inter (system font fallback)
- **Headings**: Bold, clear hierarchy
- **Body**: Readable, accessible sizing
- **Code**: Monospace for technical content

### Spacing

- **Consistent**: 4px base unit
- **Responsive**: Adaptive spacing
- **Visual Hierarchy**: Clear content separation

## 🚀 Performance

### Optimization Features

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js image optimization
- **Bundle Analysis**: Webpack bundle analyzer
- **Lazy Loading**: Component lazy loading

### Performance Metrics

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3.5s

## 🔧 Troubleshooting

### Common Issues

#### Build Errors

```bash
# Clear cache and reinstall
rm -rf .next node_modules
npm install
npm run build
```

#### API Connection Issues

1. Verify backend is running on port 8000
2. Check `.env.local` configuration
3. Test API endpoints manually
4. Review browser console for errors

#### Styling Issues

```bash
# Format code
npm run format

# Check for linting errors
npm run lint
```

### Debug Tools

- **API Debug Component**: Built-in API testing
- **Browser DevTools**: React DevTools extension
- **Network Tab**: API request monitoring
- **Console Logs**: Error tracking and debugging

## 📱 Browser Support

### Supported Browsers

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

### Mobile Support

- **iOS Safari**: 14+
- **Chrome Mobile**: 90+
- **Samsung Internet**: 13+

## 🚀 Deployment

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Environment Configuration

```env
# Production environment
NEXT_PUBLIC_API_URL=https://api.reposcope.dev
NEXT_PUBLIC_APP_NAME=RepoScope
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Deployment Platforms

- **Vercel**: Recommended for Next.js
- **Netlify**: Static site deployment
- **Docker**: Containerized deployment
- **AWS**: Cloud deployment

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

### Code Requirements

- **TypeScript**: All components must be typed
- **Testing**: New features require tests
- **Documentation**: Update README as needed
- **Styling**: Follow Tailwind CSS patterns

---

For more information, see the main [README.md](../README.md) file.
