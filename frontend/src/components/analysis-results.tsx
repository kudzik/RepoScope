'use client';

import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import type { AnalysisResponse } from '@/lib/api-types';
import {
  getCoverageColor,
  getDocumentationColor,
  getQualityColor,
  getScoreBgColor,
  getScoreColor,
  getScoreLevel,
  getSeverityColor,
} from '@/lib/utils';
import {
  AlertCircle,
  AlertTriangle,
  BarChart3,
  Calendar,
  CheckCircle,
  Clock,
  Code,
  FileCheck,
  FileCode,
  FileText,
  GitFork,
  Info,
  Shield,
  Star,
  Target,
  TestTube,
  XCircle,
  Zap,
} from 'lucide-react';

interface AnalysisResultsProps {
  analysis: AnalysisResponse;
}

export function AnalysisResults({ analysis }: AnalysisResultsProps) {
  const getLanguageColor = (language: string): string => {
    const colors: Record<string, string> = {
      // Popular languages with GitHub-style colors
      python: '#3776ab',
      javascript: '#f7df1e',
      typescript: '#3178c6',
      java: '#f89820',
      cpp: '#00599c',
      c: '#a8b9cc',
      rust: '#dea584',
      go: '#00add8',
      php: '#777bb4',
      ruby: '#cc342d',
      csharp: '#239120',
      swift: '#fa7343',
      kotlin: '#7f52ff',
      scala: '#dc322f',
      shell: '#89e051',
      bash: '#89e051',
      powershell: '#012456',
      dockerfile: '#2496ed',
      cmake: '#064f8c',
      makefile: '#427819',
      html: '#e34c26',
      css: '#1572b6',
      sql: '#336791',
      r: '#276dc3',
      matlab: '#e16737',
      perl: '#39457e',
      lua: '#000080',
      vim: '#019733',
      elisp: '#c065db',
      // Special cases
      unknown: '#6b7280', // Gray for unknown
    };

    return colors[language.toLowerCase()] || '#6b7280';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'processing':
        return <Clock className="h-4 w-4 text-blue-500 animate-pulse" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'processing':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  // Usunięto lokalną funkcję getScoreColor - używamy importowanej z utils

  // Safe number formatting
  const safeNumber = (value: unknown, defaultValue: number = 0): number => {
    if (typeof value === 'number' && !isNaN(value)) return value;
    return defaultValue;
  };

  // Safe string formatting
  const safeString = (value: unknown, defaultValue: string = 'N/A'): string => {
    if (typeof value === 'string') return value;
    return defaultValue;
  };

  // Safe array check
  const safeArray = (value: unknown): unknown[] => {
    return Array.isArray(value) ? value : [];
  };

  // Safe object check
  const safeObject = (value: unknown): Record<string, unknown> => {
    return value && typeof value === 'object' && !Array.isArray(value)
      ? (value as Record<string, unknown>)
      : {};
  };

  if (analysis.status === 'failed') {
    return (
      <Alert variant="destructive">
        <XCircle className="h-4 w-4" />
        <AlertDescription>
          Analysis failed: {analysis.error_message || 'Unknown error occurred'}
        </AlertDescription>
      </Alert>
    );
  }

  if (analysis.status !== 'completed' || !analysis.result) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            {getStatusIcon(analysis.status)}
            <CardTitle className="text-lg">Analysis Status</CardTitle>
            <Badge className={getStatusColor(analysis.status)}>
              {analysis.status}
            </Badge>
          </div>
          <CardDescription>
            Repository: {analysis.repository_url}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {analysis.status === 'processing' && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">
                Analysis is in progress. This may take a few minutes...
              </p>
              <Progress value={undefined} className="w-full" />
            </div>
          )}
        </CardContent>
      </Card>
    );
  }

  const result = analysis.result;
  if (!result) {
    return (
      <Alert variant="destructive">
        <XCircle className="h-4 w-4" />
        <AlertDescription>No analysis results available</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Repository Info */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <CardTitle>Analysis Complete</CardTitle>
              <Badge className={getStatusColor(analysis.status)}>
                {analysis.status}
              </Badge>
            </div>
            <div className="text-sm text-muted-foreground">
              Duration:{' '}
              {analysis.analysis_duration
                ? `${Math.round(analysis.analysis_duration)}s`
                : 'N/A'}
            </div>
          </div>
          <CardDescription>
            Repository: {analysis.repository_url}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Repository Info */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="flex items-center gap-2">
              <Star className="h-4 w-4 text-yellow-500" />
              <span className="text-sm">
                {analysis.repository_info.stars} stars
              </span>
            </div>
            <div className="flex items-center gap-2">
              <GitFork className="h-4 w-4 text-blue-500" />
              <span className="text-sm">
                {analysis.repository_info.forks} forks
              </span>
            </div>
            <div className="flex items-center gap-2">
              <FileCode className="h-4 w-4 text-green-500" />
              <span className="text-sm">
                {analysis.repository_info.language || 'Unknown'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-purple-500" />
              <span className="text-sm">
                {analysis.repository_info.updated_at
                  ? new Date(
                      analysis.repository_info.updated_at
                    ).toLocaleDateString()
                  : 'N/A'}
              </span>
            </div>
          </div>

          {/* AI Summary */}
          <div className="space-y-3">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <Zap className="h-4 w-4 text-blue-500" />
              AI Analysis Summary
            </h4>
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <div className="text-sm leading-relaxed whitespace-pre-wrap">
                  {analysis.ai_summary || 'No AI summary available'}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Code Quality */}
        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Code className="h-5 w-5 text-blue-500" />
              <CardTitle className="text-base">Code Quality</CardTitle>
            </div>
            <CardDescription className="text-sm">
              Overall code maintainability, complexity, and technical debt
              assessment
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {safeNumber(result.code_quality?.score, 0)}
                </span>
                <span
                  className={`text-sm ${getScoreColor(safeNumber(result.code_quality?.score, 0))}`}
                >
                  /100
                </span>
              </div>
              <Progress
                value={safeNumber(result.code_quality?.score, 0)}
                className="h-2"
                style={
                  {
                    '--progress-background': getScoreBgColor(
                      safeNumber(result.code_quality?.score, 0)
                    ),
                  } as React.CSSProperties
                }
              />
              {(() => {
                const qualityLevel = getScoreLevel(
                  safeNumber(result.code_quality?.score, 0),
                  'quality'
                );
                const qualityColors = getQualityColor(qualityLevel);
                return (
                  <div
                    className={`text-xs p-2 rounded ${qualityColors.bg} ${qualityColors.border} border`}
                  >
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${qualityColors.text}`}>
                        {qualityColors.title}
                      </span>
                      <Badge className={qualityColors.badge}>
                        {qualityLevel}
                      </Badge>
                    </div>
                    <p className={`text-xs mt-1 ${qualityColors.text}`}>
                      {qualityColors.description}
                    </p>
                  </div>
                );
              })()}
              {result.code_quality?.metrics && (
                <div className="text-xs text-muted-foreground space-y-1">
                  <div
                    className="cursor-help"
                    title="Maintainability Index: Measures how easy the code is to understand and modify. Higher values (80+) indicate excellent maintainability, while lower values (below 40) suggest significant maintenance challenges."
                  >
                    Maintainability:{' '}
                    {safeNumber(
                      result.code_quality.metrics.maintainability_index,
                      0
                    ).toFixed(2)}
                  </div>
                  <div
                    className="cursor-help"
                    title="Technical Debt Ratio: Percentage of code that needs refactoring or improvement. Lower values (below 30%) are better, while higher values (above 70%) indicate significant technical debt."
                  >
                    Technical Debt:{' '}
                    {safeNumber(
                      result.code_quality.metrics.technical_debt_ratio,
                      0
                    ).toFixed(2)}
                    %
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Documentation */}
        <Card className="border-l-4 border-l-purple-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-purple-500" />
              <CardTitle className="text-base">Documentation</CardTitle>
            </div>
            <CardDescription className="text-sm">
              Quality and completeness of project documentation and code
              comments
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {safeNumber(result.documentation?.score, 0)}
                </span>
                <span
                  className={`text-sm ${getScoreColor(safeNumber(result.documentation?.score, 0))}`}
                >
                  /100
                </span>
              </div>
              <Progress
                value={safeNumber(result.documentation?.score, 0)}
                className="h-2"
                style={
                  {
                    '--progress-background': getScoreBgColor(
                      safeNumber(result.documentation?.score, 0)
                    ),
                  } as React.CSSProperties
                }
              />
              {(() => {
                const docLevel = getScoreLevel(
                  safeNumber(result.documentation?.score, 0),
                  'documentation'
                );
                const docColors = getDocumentationColor(docLevel);
                return (
                  <div
                    className={`text-xs p-2 rounded ${docColors.bg} ${docColors.border} border`}
                  >
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${docColors.text}`}>
                        {docColors.title}
                      </span>
                      <Badge className={docColors.badge}>{docLevel}</Badge>
                    </div>
                    <p className={`text-xs mt-1 ${docColors.text}`}>
                      {docColors.description}
                    </p>
                  </div>
                );
              })()}
              {result.documentation?.details && (
                <div className="text-xs text-muted-foreground space-y-1">
                  <div
                    className="cursor-help flex items-center gap-1"
                    title="README file: Essential project documentation that explains what the project does, how to install and use it."
                  >
                    <span>README:</span>
                    <span
                      className={
                        result.documentation.details.has_readme
                          ? 'text-green-600'
                          : 'text-red-600'
                      }
                    >
                      {result.documentation.details.has_readme ? '✓' : '✗'}
                    </span>
                  </div>
                  <div
                    className="cursor-help flex items-center gap-1"
                    title="API Documentation: Documentation for application programming interfaces and endpoints."
                  >
                    <span>API Docs:</span>
                    <span
                      className={
                        result.documentation.details.has_api_docs
                          ? 'text-green-600'
                          : 'text-red-600'
                      }
                    >
                      {result.documentation.details.has_api_docs ? '✓' : '✗'}
                    </span>
                  </div>
                  <div
                    className="cursor-help flex items-center gap-1"
                    title="Comment Coverage: Percentage of code lines that contain comments. Higher values indicate better code documentation."
                  >
                    <span>Comments:</span>
                    <span className="font-mono">
                      {safeNumber(
                        result.documentation.details.comment_coverage,
                        0
                      ).toFixed(1)}
                      %
                    </span>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Security */}
        <Card className="border-l-4 border-l-red-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-red-500" />
              <CardTitle className="text-base">Security</CardTitle>
            </div>
            <CardDescription className="text-sm">
              Security vulnerabilities, hardcoded secrets, and security best
              practices
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {safeNumber(result.security?.score, 0)}
                </span>
                <span
                  className={`text-sm ${getScoreColor(safeNumber(result.security?.score, 0))}`}
                >
                  /100
                </span>
              </div>
              <Progress
                value={safeNumber(result.security?.score, 0)}
                className="h-2"
                style={
                  {
                    '--progress-background': getScoreBgColor(
                      safeNumber(result.security?.score, 0)
                    ),
                  } as React.CSSProperties
                }
              />
              {(() => {
                const securityLevel = getScoreLevel(
                  safeNumber(result.security?.score, 0),
                  'security'
                );
                const securityColors = getSeverityColor(securityLevel);
                return (
                  <div
                    className={`text-xs p-2 rounded ${securityColors.bg} ${securityColors.border} border`}
                  >
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${securityColors.text}`}>
                        {securityColors.title}
                      </span>
                      <Badge className={securityColors.badge}>
                        {securityLevel}
                      </Badge>
                    </div>
                    <p className={`text-xs mt-1 ${securityColors.text}`}>
                      {securityColors.description}
                    </p>
                  </div>
                );
              })()}
              <div className="text-xs text-muted-foreground space-y-1">
                <div
                  className="cursor-help flex items-center gap-1"
                  title="Total security issues found in the repository. This includes all severity levels (high, medium, low)."
                >
                  <span>Issues:</span>
                  <span className="font-mono">
                    {safeNumber(result.security?.summary?.total_issues, 0)}
                  </span>
                </div>
                <div
                  className="cursor-help flex items-center gap-1"
                  title="High severity security issues that require immediate attention. These are critical vulnerabilities that should be fixed as soon as possible."
                >
                  <span>High:</span>
                  <span className="font-mono">
                    {safeNumber(result.security?.summary?.high_severity, 0)}
                  </span>
                </div>
                <div
                  className="cursor-help flex items-center gap-1"
                  title="Medium severity security issues that should be addressed. These are important security concerns that should be fixed in the near future."
                >
                  <span>Medium:</span>
                  <span className="font-mono">
                    {safeNumber(result.security?.summary?.medium_severity, 0)}
                  </span>
                </div>
                <div
                  className="cursor-help flex items-center gap-1"
                  title="Low severity security issues that can be addressed when convenient. These are minor security concerns that can be fixed during regular maintenance."
                >
                  <span>Low:</span>
                  <span className="font-mono">
                    {safeNumber(result.security?.summary?.low_severity, 0)}
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Test Coverage */}
        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <TestTube className="h-5 w-5 text-green-500" />
              <CardTitle className="text-base">Test Coverage</CardTitle>
            </div>
            <CardDescription className="text-sm">
              Test coverage percentage, frameworks used, and testing quality
              metrics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {safeNumber(result.test_coverage?.coverage_percentage, 0)}%
                </span>
                <span
                  className={`text-sm ${getScoreColor(safeNumber(result.test_coverage?.coverage_percentage, 0))}`}
                >
                  coverage
                </span>
              </div>
              <Progress
                value={safeNumber(result.test_coverage?.coverage_percentage, 0)}
                className="h-2"
                style={
                  {
                    '--progress-background': getScoreBgColor(
                      safeNumber(result.test_coverage?.coverage_percentage, 0)
                    ),
                  } as React.CSSProperties
                }
              />
              {(() => {
                const coverageLevel = getScoreLevel(
                  safeNumber(result.test_coverage?.coverage_percentage, 0),
                  'coverage'
                );
                const coverageColors = getCoverageColor(coverageLevel);
                return (
                  <div
                    className={`text-xs p-2 rounded ${coverageColors.bg} ${coverageColors.border} border`}
                  >
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${coverageColors.text}`}>
                        {coverageColors.title}
                      </span>
                      <Badge className={coverageColors.badge}>
                        {coverageLevel}
                      </Badge>
                    </div>
                    <p className={`text-xs mt-1 ${coverageColors.text}`}>
                      {coverageColors.description}
                    </p>
                  </div>
                );
              })()}
              <div className="text-xs text-muted-foreground space-y-1">
                <div
                  className="cursor-help flex items-center gap-1"
                  title="Whether the project has any test files. Tests are essential for code quality and reliability."
                >
                  <span>Has Tests:</span>
                  <span
                    className={
                      result.test_coverage?.has_tests
                        ? 'text-green-600'
                        : 'text-red-600'
                    }
                  >
                    {result.test_coverage?.has_tests ? '✓' : '✗'}
                  </span>
                </div>
                <div
                  className="cursor-help flex items-center gap-1"
                  title="Number of testing frameworks detected in the project (e.g., Jest, Mocha, Pytest, etc.). More frameworks may indicate better testing coverage."
                >
                  <span>Frameworks:</span>
                  <span className="font-mono">
                    {safeArray(result.test_coverage?.test_frameworks).length}
                  </span>
                </div>
                <div
                  className="cursor-help flex items-center gap-1"
                  title="Total number of test files found in the project. More test files generally indicate better test coverage."
                >
                  <span>Files:</span>
                  <span className="font-mono">
                    {safeArray(result.test_coverage?.test_files).length}
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Code Metrics */}
      <Card className="border-l-4 border-l-indigo-500">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-3">
            <BarChart3 className="h-6 w-6 text-indigo-500" />
            Code Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-8">
            {/* Top Row - Languages and Largest Files */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Languages */}
              <div className="space-y-4">
                <h4 className="font-semibold text-base flex items-center gap-2">
                  <Code className="h-4 w-4 text-blue-500" />
                  Languages
                </h4>
                <div className="space-y-2">
                  {Object.entries(safeObject(result.metrics?.languages))
                    .length > 0 ? (
                    (() => {
                      // Sort languages: unknown last, others by percentage
                      const languages = Object.entries(
                        safeObject(result.metrics?.languages)
                      );
                      const sortedLanguages = languages.sort(
                        ([aName, aData], [bName, bData]) => {
                          if (aName === 'unknown') return 1;
                          if (bName === 'unknown') return -1;
                          const aLines = safeNumber(
                            (aData as Record<string, unknown>)?.lines,
                            0
                          );
                          const bLines = safeNumber(
                            (bData as Record<string, unknown>)?.lines,
                            0
                          );
                          return bLines - aLines;
                        }
                      );

                      // Calculate total lines for percentage
                      const totalLines = safeNumber(
                        result.metrics?.lines_of_code,
                        1
                      );

                      return (
                        <>
                          {/* Language Distribution Bar */}
                          <div className="mb-4">
                            <div className="flex h-4 rounded-lg overflow-hidden border">
                              {sortedLanguages.map(([lang, langData]) => {
                                const langInfo = langData as Record<
                                  string,
                                  unknown
                                >;
                                const lines = safeNumber(langInfo?.lines, 0);
                                const percentage =
                                  totalLines > 0
                                    ? (lines / totalLines) * 100
                                    : 0;
                                const color = getLanguageColor(lang);

                                return (
                                  <div
                                    key={lang}
                                    className="flex items-center justify-center text-xs font-medium text-white"
                                    style={{
                                      width: `${percentage}%`,
                                      backgroundColor: color,
                                      minWidth: percentage > 0 ? '20px' : '0px',
                                    }}
                                    title={`${lang}: ${percentage.toFixed(1)}%`}
                                  >
                                    {percentage > 5 && (
                                      <span className="truncate px-1">
                                        {percentage.toFixed(0)}%
                                      </span>
                                    )}
                                  </div>
                                );
                              })}
                            </div>
                          </div>

                          {/* Language Details */}
                          {sortedLanguages.map(([lang, langData]) => {
                            const langInfo = langData as Record<
                              string,
                              unknown
                            >;
                            const files = safeNumber(langInfo?.files, 0);
                            const lines = safeNumber(langInfo?.lines, 0);
                            const percentage =
                              totalLines > 0 ? (lines / totalLines) * 100 : 0;
                            const color = getLanguageColor(lang);

                            return (
                              <div key={lang} className="space-y-1">
                                <div className="flex justify-between text-sm">
                                  <div className="flex items-center gap-2">
                                    <div
                                      className="w-3 h-3 rounded-full"
                                      style={{ backgroundColor: color }}
                                    />
                                    <span className="capitalize font-medium">
                                      {safeString(lang)}
                                    </span>
                                  </div>
                                  <span className="text-xs text-muted-foreground font-mono">
                                    {percentage.toFixed(1)}%
                                  </span>
                                </div>
                                <div className="flex justify-between text-xs text-muted-foreground">
                                  <span>{files} files</span>
                                  <span>{lines.toLocaleString()} lines</span>
                                </div>
                                <Progress
                                  value={percentage}
                                  className="h-1"
                                  style={
                                    {
                                      '--progress-background': color + '20',
                                    } as React.CSSProperties
                                  }
                                />
                              </div>
                            );
                          })}
                        </>
                      );
                    })()
                  ) : (
                    <div className="text-sm text-muted-foreground text-center py-4">
                      No language data available
                    </div>
                  )}
                </div>
              </div>

              {/* Largest Files */}
              <div className="space-y-4">
                <h4 className="font-semibold text-base flex items-center gap-2">
                  <FileCode className="h-4 w-4 text-green-500" />
                  Largest Files
                </h4>
                <div className="space-y-2">
                  {safeArray(analysis.code_structure?.largest_files)
                    .slice(0, 5)
                    .map((file, index: number) => {
                      const fileObj = file as Record<string, unknown>;
                      const fileName = safeString(fileObj?.path, 'Unknown');
                      const lines = safeNumber(fileObj?.lines, 0);
                      const language = safeString(fileObj?.language, '');
                      const color = getLanguageColor(language);

                      return (
                        <div
                          key={index}
                          className="flex justify-between items-center p-3 bg-muted/20 rounded-lg border"
                        >
                          <div className="flex items-center gap-3 flex-1 min-w-0">
                            <div
                              className="w-3 h-3 rounded-full flex-shrink-0"
                              style={{ backgroundColor: color }}
                            />
                            <div className="flex-1 min-w-0">
                              <div className="truncate font-medium text-sm">
                                {fileName.split('/').pop()}
                              </div>
                              {language && (
                                <div className="text-xs text-muted-foreground capitalize">
                                  {language}
                                </div>
                              )}
                            </div>
                          </div>
                          <div className="text-right flex-shrink-0">
                            <div className="font-mono font-semibold text-sm">
                              {lines.toLocaleString()}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              lines
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  {safeArray(analysis.code_structure?.largest_files).length ===
                    0 && (
                    <div className="text-sm text-muted-foreground text-center py-4">
                      No file data available
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Bottom Row - Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Basic Metrics */}
              <div className="space-y-4">
                <h4 className="font-medium text-sm">Basic Metrics</h4>
                <div className="space-y-3 text-sm">
                  <div
                    className="flex justify-between items-center p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border"
                    title="Total number of lines of code in the repository, including comments and blank lines"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-blue-500" />
                      <span>Lines of Code:</span>
                    </div>
                    <span className="font-mono font-semibold text-blue-700 dark:text-blue-300">
                      {safeNumber(
                        analysis.code_structure?.total_lines,
                        0
                      ).toLocaleString()}
                    </span>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border"
                    title="Total number of source code files in the repository"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-green-500" />
                      <span>Files:</span>
                    </div>
                    <span className="font-mono font-semibold text-green-700 dark:text-green-300">
                      {safeNumber(analysis.code_structure?.total_files, 0)}
                    </span>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-orange-50 dark:bg-orange-950/20 rounded-lg border"
                    title="Cyclomatic complexity score indicating code complexity and maintainability"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-orange-500" />
                      <span>Complexity:</span>
                    </div>
                    <span className="font-mono font-semibold text-orange-700 dark:text-orange-300">
                      {safeNumber(
                        analysis.code_structure?.complexity_score,
                        0
                      ).toFixed(2)}
                    </span>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-purple-50 dark:bg-purple-950/20 rounded-lg border"
                    title="Average number of lines per file, calculated as total lines divided by number of files"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-purple-500" />
                      <span>Avg File Size:</span>
                    </div>
                    <span className="font-mono font-semibold text-purple-700 dark:text-purple-300">
                      {safeNumber(analysis.code_structure?.total_files, 0) > 0
                        ? Math.round(
                            safeNumber(
                              analysis.code_structure?.total_lines,
                              0
                            ) /
                              safeNumber(
                                analysis.code_structure?.total_files,
                                1
                              )
                          )
                        : 0}{' '}
                      lines
                    </span>
                  </div>
                </div>
              </div>

              {/* Quality Metrics */}
              <div className="space-y-4">
                <h4 className="font-medium text-sm">Quality Metrics</h4>
                <div className="space-y-3 text-sm">
                  <div
                    className="flex justify-between items-center p-3 bg-emerald-50 dark:bg-emerald-950/20 rounded-lg border"
                    title="Code maintainability index (0-100) based on complexity, documentation, and structure"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-emerald-500" />
                      <span>Maintainability:</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-emerald-700 dark:text-emerald-300">
                        {safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.maintainability_index,
                          0
                        ).toFixed(1)}
                        /100
                      </span>
                      <Progress
                        value={safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.maintainability_index,
                          0
                        )}
                        className="w-16 h-2"
                      />
                    </div>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-red-50 dark:bg-red-950/20 rounded-lg border"
                    title="Technical debt ratio indicating code quality issues that need to be addressed"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-500" />
                      <span>Tech Debt:</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-red-700 dark:text-red-300">
                        {safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.technical_debt_ratio,
                          0
                        ).toFixed(1)}
                        %
                      </span>
                      <Progress
                        value={safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.technical_debt_ratio,
                          0
                        )}
                        className="w-16 h-2"
                      />
                    </div>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-yellow-50 dark:bg-yellow-950/20 rounded-lg border"
                    title="Percentage of duplicated code that could be refactored for better maintainability"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-yellow-500" />
                      <span>Duplication:</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-yellow-700 dark:text-yellow-300">
                        {safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.code_duplication,
                          0
                        ).toFixed(1)}
                        %
                      </span>
                      <Progress
                        value={safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.code_duplication,
                          0
                        )}
                        className="w-16 h-2"
                      />
                    </div>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-indigo-50 dark:bg-indigo-950/20 rounded-lg border"
                    title="Architecture quality score (0-100) based on design patterns, modularity, and code organization"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-indigo-500" />
                      <span>Architecture:</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-indigo-700 dark:text-indigo-300">
                        {safeNumber(
                          analysis.code_structure?.architecture_score,
                          0
                        ).toFixed(1)}
                        /100
                      </span>
                      <Progress
                        value={safeNumber(
                          analysis.code_structure?.architecture_score,
                          0
                        )}
                        className="w-16 h-2"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Additional Metrics */}
              <div className="space-y-4">
                <h4 className="font-medium text-sm">Additional Metrics</h4>
                <div className="space-y-3 text-sm">
                  <div
                    className="flex justify-between items-center p-3 bg-cyan-50 dark:bg-cyan-950/20 rounded-lg border"
                    title="Overall code quality score (0-100) combining all quality metrics and analysis results"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-cyan-500" />
                      <span>Overall Score:</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-cyan-700 dark:text-cyan-300">
                        {safeNumber(analysis.code_structure?.score, 0)}/100
                      </span>
                      <Progress
                        value={safeNumber(analysis.code_structure?.score, 0)}
                        className="w-16 h-2"
                      />
                    </div>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-teal-50 dark:bg-teal-950/20 rounded-lg border"
                    title="Percentage of code covered by automated tests, indicating code reliability and quality"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-teal-500" />
                      <span>Test Coverage:</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-semibold text-teal-700 dark:text-teal-300">
                        {safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.test_coverage,
                          0
                        ).toFixed(1)}
                        %
                      </span>
                      <Progress
                        value={safeNumber(
                          (
                            analysis.code_structure?.quality_metrics as Record<
                              string,
                              unknown
                            >
                          )?.test_coverage,
                          0
                        )}
                        className="w-16 h-2"
                      />
                    </div>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-rose-50 dark:bg-rose-950/20 rounded-lg border"
                    title="Number of code quality issues, bugs, and potential problems identified during analysis"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-rose-500" />
                      <span>Issues Found:</span>
                    </div>
                    <span className="font-mono font-semibold text-rose-700 dark:text-rose-300">
                      {safeArray(analysis.code_structure?.issues).length}
                    </span>
                  </div>
                  <div
                    className="flex justify-between items-center p-3 bg-lime-50 dark:bg-lime-950/20 rounded-lg border"
                    title="Number of improvement suggestions and best practices recommendations for the codebase"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-lime-500" />
                      <span>Recommendations:</span>
                    </div>
                    <span className="font-mono font-semibold text-lime-700 dark:text-lime-300">
                      {
                        safeArray(analysis.code_structure?.recommendations)
                          .length
                      }
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Code Quality Analysis - Full Width */}
      <Card className="border-l-4 border-l-orange-500">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-3">
            <Code className="h-6 w-6 text-orange-500" />
            Code Quality Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Issues Column */}
            <div className="space-y-4">
              <h4 className="font-semibold text-base mb-3 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-yellow-500" />
                Issues Found ({result.code_quality.issues?.length || 0})
              </h4>
              {Array.isArray(result.code_quality.issues) &&
              result.code_quality.issues.length > 0 ? (
                <div className="space-y-2 max-h-64 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
                  {result.code_quality.issues.map(
                    (issue: string, index: number) => (
                      <div
                        key={index}
                        className="text-sm p-2 bg-yellow-50 dark:bg-yellow-950/20 rounded-lg border"
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-yellow-500" />
                          <span className="text-yellow-700 dark:text-yellow-300">
                            {typeof issue === 'string' ? issue : String(issue)}
                          </span>
                        </div>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <div className="text-sm text-muted-foreground p-4 bg-muted/20 rounded-lg border">
                  No issues found
                </div>
              )}
            </div>

            {/* Recommendations Column */}
            <div className="space-y-4">
              <h4 className="font-semibold text-base mb-3 flex items-center gap-2">
                <Target className="h-5 w-5 text-green-500" />
                Code Quality Recommendations (
                {result.code_quality.recommendations?.length || 0})
              </h4>
              {Array.isArray(result.code_quality.recommendations) &&
              result.code_quality.recommendations.length > 0 ? (
                <div className="space-y-2 max-h-64 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
                  {result.code_quality.recommendations.map(
                    (rec: string, index: number) => (
                      <div
                        key={index}
                        className="text-sm p-2 bg-blue-50 dark:bg-blue-950/20 rounded-lg border"
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-blue-500" />
                          <span className="text-blue-700 dark:text-blue-300">
                            {typeof rec === 'string' ? rec : String(rec)}
                          </span>
                        </div>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <div className="text-sm text-muted-foreground p-4 bg-muted/20 rounded-lg border">
                  No recommendations available
                </div>
              )}
            </div>

            {/* Patterns Column */}
            <div className="space-y-4">
              <h4 className="font-semibold text-base mb-3 flex items-center gap-2">
                <Code className="h-5 w-5 text-purple-500" />
                Code Patterns
              </h4>
              {result.code_quality.patterns && (
                <div className="space-y-2 text-sm max-h-32 overflow-y-auto">
                  {Array.isArray(
                    result.code_quality.patterns.design_patterns
                  ) &&
                    result.code_quality.patterns.design_patterns.length > 0 && (
                      <div>
                        <span className="text-green-600">
                          Design Patterns:{' '}
                        </span>
                        <div className="space-y-1">
                          {(() => {
                            // Group design patterns by pattern name
                            const groupedPatterns =
                              result.code_quality.patterns.design_patterns.reduce(
                                (
                                  acc: Record<
                                    string,
                                    (string | Record<string, unknown>)[]
                                  >,
                                  pattern: string | Record<string, unknown>
                                ) => {
                                  const patternName: string =
                                    typeof pattern === 'string'
                                      ? pattern
                                      : String(
                                          (pattern as Record<string, unknown>)
                                            .pattern ||
                                            (pattern as Record<string, unknown>)
                                              .name ||
                                            'Unknown Pattern'
                                        );

                                  if (!acc[patternName]) {
                                    acc[patternName] = [];
                                  }
                                  acc[patternName].push(pattern);
                                  return acc;
                                },
                                {}
                              );

                            return Object.entries(groupedPatterns).map(
                              ([patternName, patterns]) => (
                                <div
                                  key={patternName}
                                  className="text-sm p-2 bg-green-50 dark:bg-green-950/20 rounded-lg border"
                                >
                                  <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-green-500" />
                                    <span className="font-medium text-green-700 dark:text-green-300">
                                      {patternName}
                                    </span>
                                    <span className="text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-2 py-1 rounded-full">
                                      {patterns.length} occurrence
                                      {patterns.length > 1 ? 's' : ''}
                                    </span>
                                  </div>
                                  {patterns.length <= 3 && (
                                    <div className="ml-4 mt-1 space-y-1">
                                      {patterns.map((pattern, index) => {
                                        if (typeof pattern === 'string')
                                          return null;

                                        const patternObj = pattern as Record<
                                          string,
                                          unknown
                                        >;
                                        const file = patternObj.file as
                                          | string
                                          | undefined;
                                        const line = patternObj.line as
                                          | number
                                          | undefined;

                                        return (
                                          <div
                                            key={index}
                                            className="text-xs text-muted-foreground"
                                          >
                                            📁 {String(file)}
                                            {line && `:${String(line)}`}
                                          </div>
                                        );
                                      })}
                                    </div>
                                  )}
                                  {patterns.length > 3 && (
                                    <div className="ml-4 mt-1 text-xs text-muted-foreground">
                                      📁 Found in {patterns.length} locations
                                    </div>
                                  )}
                                </div>
                              )
                            );
                          })()}
                        </div>
                      </div>
                    )}
                  {Array.isArray(result.code_quality.patterns.anti_patterns) &&
                    result.code_quality.patterns.anti_patterns.length > 0 && (
                      <div>
                        <span className="text-red-600">Anti-patterns: </span>
                        <div className="space-y-1">
                          {(() => {
                            // Group anti-patterns by pattern name
                            const groupedPatterns =
                              result.code_quality.patterns.anti_patterns.reduce(
                                (
                                  acc: Record<
                                    string,
                                    (string | Record<string, unknown>)[]
                                  >,
                                  pattern: string | Record<string, unknown>
                                ) => {
                                  const patternName: string =
                                    typeof pattern === 'string'
                                      ? pattern
                                      : String(
                                          (pattern as Record<string, unknown>)
                                            .pattern ||
                                            (pattern as Record<string, unknown>)
                                              .name ||
                                            'Unknown Pattern'
                                        );

                                  if (!acc[patternName]) {
                                    acc[patternName] = [];
                                  }
                                  acc[patternName].push(pattern);
                                  return acc;
                                },
                                {}
                              );

                            return Object.entries(groupedPatterns).map(
                              ([patternName, patterns]) => (
                                <div
                                  key={patternName}
                                  className="text-sm p-2 bg-red-50 dark:bg-red-950/20 rounded-lg border"
                                >
                                  <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-red-500" />
                                    <span className="font-medium text-red-700 dark:text-red-300">
                                      {patternName}
                                    </span>
                                    <span className="text-xs bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 px-2 py-1 rounded-full">
                                      {patterns.length} occurrence
                                      {patterns.length > 1 ? 's' : ''}
                                    </span>
                                  </div>
                                  {patterns.length <= 3 && (
                                    <div className="ml-4 mt-1 space-y-1">
                                      {patterns.map((pattern, index) => {
                                        if (typeof pattern === 'string')
                                          return null;

                                        const patternObj = pattern as Record<
                                          string,
                                          unknown
                                        >;
                                        const file = patternObj.file as
                                          | string
                                          | undefined;
                                        const line = patternObj.line as
                                          | number
                                          | undefined;

                                        return (
                                          <div
                                            key={index}
                                            className="text-xs text-muted-foreground"
                                          >
                                            📁 {String(file)}
                                            {line && `:${String(line)}`}
                                          </div>
                                        );
                                      })}
                                    </div>
                                  )}
                                  {patterns.length > 3 && (
                                    <div className="ml-4 mt-1 text-xs text-muted-foreground">
                                      📁 Found in {patterns.length} locations
                                    </div>
                                  )}
                                </div>
                              )
                            );
                          })()}
                        </div>
                      </div>
                    )}
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security & Documentation Details */}
      <Card className="border-l-4 border-l-cyan-500">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-3">
            <Shield className="h-6 w-6 text-cyan-500" />
            Security & Documentation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Security Vulnerabilities */}
            <div className="space-y-4">
              <h4 className="font-semibold text-base mb-3 flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-red-500" />
                Security Vulnerabilities (
                {result.security.vulnerabilities?.length || 0})
              </h4>
              {Array.isArray(result.security.vulnerabilities) &&
              result.security.vulnerabilities.length > 0 ? (
                <div className="space-y-2 max-h-64 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
                  {result.security.vulnerabilities.map(
                    (vuln, index: number) => {
                      const severityColors = getSeverityColor(
                        vuln?.severity || 'issues'
                      );
                      return (
                        <div
                          key={index}
                          className={`text-sm p-2 ${severityColors.bg} ${severityColors.border} border rounded`}
                        >
                          <div className="flex justify-between items-start">
                            <span
                              className={`font-medium ${severityColors.text}`}
                            >
                              {vuln?.type || 'Unknown'}
                            </span>
                            <Badge className={severityColors.badge}>
                              {vuln?.severity || 'Unknown'}
                            </Badge>
                          </div>
                          <p className="text-muted-foreground text-xs mt-1">
                            {vuln?.description || 'No description'}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            File: {vuln?.file || 'Unknown'}:
                            {vuln?.line || 'Unknown'}
                          </p>
                        </div>
                      );
                    }
                  )}
                </div>
              ) : (
                <div className="text-sm text-muted-foreground p-4 bg-muted/20 rounded-lg border">
                  No security vulnerabilities found
                </div>
              )}
            </div>

            {/* Security Recommendations */}
            <div className="space-y-4">
              <h4 className="font-semibold text-base mb-3 flex items-center gap-2">
                <Info className="h-5 w-5 text-blue-500" />
                Security Recommendations (
                {result.security.recommendations?.length || 0})
              </h4>
              {Array.isArray(result.security.recommendations) &&
              result.security.recommendations.length > 0 ? (
                <div className="space-y-2 max-h-64 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
                  {result.security.recommendations.map(
                    (rec: string, index: number) => (
                      <div
                        key={index}
                        className="text-sm p-2 bg-blue-50 dark:bg-blue-950/20 rounded-lg border"
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-blue-500" />
                          <span className="text-blue-700 dark:text-blue-300">
                            {typeof rec === 'string' ? rec : String(rec)}
                          </span>
                        </div>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <div className="text-sm text-muted-foreground p-4 bg-muted/20 rounded-lg border">
                  No security recommendations available
                </div>
              )}
            </div>

            {/* Documentation Details */}
            <div className="space-y-4">
              <h4 className="font-semibold text-base mb-3 flex items-center gap-2">
                <FileText className="h-5 w-5 text-green-500" />
                Documentation Status
              </h4>
              {result.documentation.details ? (
                <div className="space-y-3">
                  {/* Documentation Files */}
                  <div className="space-y-2">
                    <div
                      className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border cursor-help"
                      title="README file: Essential project documentation that explains what the project does, how to install and use it."
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-green-500" />
                        <span>README:</span>
                      </div>
                      <span
                        className={
                          result.documentation.details.has_readme
                            ? 'text-green-600 font-semibold'
                            : 'text-red-600 font-semibold'
                        }
                      >
                        {result.documentation.details.has_readme ? '✓' : '✗'}
                      </span>
                    </div>
                    <div
                      className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border cursor-help"
                      title="API Documentation: Documentation for application programming interfaces and endpoints."
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-blue-500" />
                        <span>API Docs:</span>
                      </div>
                      <span
                        className={
                          result.documentation.details.has_api_docs
                            ? 'text-green-600 font-semibold'
                            : 'text-red-600 font-semibold'
                        }
                      >
                        {result.documentation.details.has_api_docs ? '✓' : '✗'}
                      </span>
                    </div>
                    <div
                      className="flex items-center justify-between p-3 bg-purple-50 dark:bg-purple-950/20 rounded-lg border cursor-help"
                      title="License file: Legal document that specifies the terms under which the software can be used."
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-purple-500" />
                        <span>License:</span>
                      </div>
                      <span
                        className={
                          result.documentation.details.has_license
                            ? 'text-green-600 font-semibold'
                            : 'text-red-600 font-semibold'
                        }
                      >
                        {result.documentation.details.has_license ? '✓' : '✗'}
                      </span>
                    </div>
                    <div
                      className="flex items-center justify-between p-3 bg-orange-50 dark:bg-orange-950/20 rounded-lg border cursor-help"
                      title="Contributing guidelines: Instructions for developers on how to contribute to the project."
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-orange-500" />
                        <span>Contributing:</span>
                      </div>
                      <span
                        className={
                          result.documentation.details.has_contributing
                            ? 'text-green-600 font-semibold'
                            : 'text-red-600 font-semibold'
                        }
                      >
                        {result.documentation.details.has_contributing
                          ? '✓'
                          : '✗'}
                      </span>
                    </div>
                  </div>

                  {/* Comment Coverage */}
                  {result.documentation.details.comment_coverage !==
                    undefined && (
                    <div className="p-3 bg-gray-50 dark:bg-gray-950/20 rounded-lg border">
                      <div
                        className="flex items-center justify-between text-sm cursor-help"
                        title="Comment Coverage: Percentage of code lines that contain comments. Higher values indicate better code documentation."
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-gray-500" />
                          <span>Comment Coverage:</span>
                        </div>
                        <span className="font-mono font-semibold">
                          {safeNumber(
                            result.documentation.details.comment_coverage
                          ).toFixed(1)}
                          %
                        </span>
                      </div>
                      <Progress
                        value={result.documentation.details.comment_coverage}
                        className="h-2 mt-2"
                      />
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-sm text-muted-foreground p-4 bg-muted/20 rounded-lg border">
                  No documentation details available
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Test Coverage & License Info */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Test Coverage Details */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <TestTube className="h-5 w-5" />
              Test Coverage Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Coverage Percentage:</span>
                <span className="font-mono">
                  {result.test_coverage.coverage_percentage}%
                </span>
              </div>
              <Progress
                value={result.test_coverage.coverage_percentage}
                className="h-2"
              />
            </div>

            {Array.isArray(result.test_coverage.test_frameworks) &&
              result.test_coverage.test_frameworks.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2">Test Frameworks</h4>
                  <div className="flex flex-wrap gap-1">
                    {result.test_coverage.test_frameworks.map(
                      (framework: string, index: number) => (
                        <Badge
                          key={index}
                          variant="outline"
                          className="text-xs"
                        >
                          {typeof framework === 'string'
                            ? framework
                            : String(framework)}
                        </Badge>
                      )
                    )}
                  </div>
                </div>
              )}

            {Array.isArray(result.test_coverage.issues) &&
              result.test_coverage.issues.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2">Test Issues</h4>
                  <ul className="space-y-1 text-sm max-h-24 overflow-y-auto">
                    {result.test_coverage.issues.map(
                      (issue: string, index: number) => (
                        <li key={index} className="text-muted-foreground">
                          • {typeof issue === 'string' ? issue : String(issue)}
                        </li>
                      )
                    )}
                  </ul>
                </div>
              )}

            {Array.isArray(result.test_coverage.recommendations) &&
              result.test_coverage.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2">
                    Test Recommendations
                  </h4>
                  <ul className="space-y-1 text-sm max-h-24 overflow-y-auto">
                    {result.test_coverage.recommendations.map(
                      (rec: string, index: number) => (
                        <li key={index} className="text-muted-foreground">
                          • {typeof rec === 'string' ? rec : String(rec)}
                        </li>
                      )
                    )}
                  </ul>
                </div>
              )}
          </CardContent>
        </Card>

        {/* License Information */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <FileCheck className="h-5 w-5" />
              License Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>License Type:</span>
                <span className="font-mono">
                  {result.license_info.license_type}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Open Source:</span>
                <span
                  className={
                    result.license_info.is_open_source
                      ? 'text-green-600'
                      : 'text-red-600'
                  }
                >
                  {result.license_info.is_open_source ? '✓ Yes' : '✗ No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Compatibility:</span>
                <span className="font-mono">
                  {result.license_info.compatibility}
                </span>
              </div>
              {result.license_info.license_file && (
                <div className="flex justify-between">
                  <span>License File:</span>
                  <span className="font-mono text-sm">
                    {result.license_info.license_file}
                  </span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
