'use client';

import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import type { AnalysisResponse } from '@/lib/api-types';
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

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

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
            <Badge className={getStatusColor(analysis.status)}>{analysis.status}</Badge>
          </div>
          <CardDescription>Repository: {analysis.repository_url}</CardDescription>
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
              <Badge className={getStatusColor(analysis.status)}>{analysis.status}</Badge>
            </div>
            <div className="text-sm text-muted-foreground">
              Duration:{' '}
              {analysis.analysis_duration ? `${Math.round(analysis.analysis_duration)}s` : 'N/A'}
            </div>
          </div>
          <CardDescription>Repository: {analysis.repository_url}</CardDescription>
        </CardHeader>
        <CardContent>
          {/* Repository Info */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="flex items-center gap-2">
              <Star className="h-4 w-4 text-yellow-500" />
              <span className="text-sm">{analysis.repository_info.stars} stars</span>
            </div>
            <div className="flex items-center gap-2">
              <GitFork className="h-4 w-4 text-blue-500" />
              <span className="text-sm">{analysis.repository_info.forks} forks</span>
            </div>
            <div className="flex items-center gap-2">
              <FileCode className="h-4 w-4 text-green-500" />
              <span className="text-sm">{analysis.repository_info.language || 'Unknown'}</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-purple-500" />
              <span className="text-sm">
                {analysis.repository_info.updated_at
                  ? new Date(analysis.repository_info.updated_at).toLocaleDateString()
                  : 'N/A'}
              </span>
            </div>
          </div>

          {/* AI Summary */}
          <div className="space-y-2">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <Zap className="h-4 w-4 text-blue-500" />
              AI Analysis Summary
            </h4>
            <p className="text-sm text-muted-foreground whitespace-pre-wrap">
              {analysis.ai_summary || 'No AI summary available'}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Main Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Code Quality */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Code className="h-4 w-4" />
              <CardTitle className="text-sm">Code Quality</CardTitle>
            </div>
            <CardDescription className="text-xs">
              Overall code maintainability, complexity, and technical debt assessment
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
              <Progress value={safeNumber(result.code_quality?.score, 0)} className="h-2" />
              {result.code_quality?.metrics && (
                <div className="text-xs text-muted-foreground space-y-1">
                  <div
                    className="cursor-help"
                    title="Maintainability Index: Measures how easy the code is to understand and modify. Higher values (80+) indicate excellent maintainability, while lower values (below 40) suggest significant maintenance challenges."
                  >
                    Maintainability:{' '}
                    {safeNumber(result.code_quality.metrics.maintainability_index, 0).toFixed(2)}
                  </div>
                  <div
                    className="cursor-help"
                    title="Technical Debt Ratio: Percentage of code that needs refactoring or improvement. Lower values (below 30%) are better, while higher values (above 70%) indicate significant technical debt."
                  >
                    Technical Debt:{' '}
                    {safeNumber(result.code_quality.metrics.technical_debt_ratio, 0).toFixed(2)}%
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Documentation */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              <CardTitle className="text-sm">Documentation</CardTitle>
            </div>
            <CardDescription className="text-xs">
              Quality and completeness of project documentation and code comments
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
              <Progress value={safeNumber(result.documentation?.score, 0)} className="h-2" />
              {result.documentation?.details && (
                <div className="text-xs text-muted-foreground space-y-1">
                  <div
                    className="cursor-help flex items-center gap-1"
                    title="README file: Essential project documentation that explains what the project does, how to install and use it."
                  >
                    <span>README:</span>
                    <span
                      className={
                        result.documentation.details.has_readme ? 'text-green-600' : 'text-red-600'
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
                      {safeNumber(result.documentation.details.comment_coverage, 0).toFixed(1)}%
                    </span>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Security */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Shield className="h-4 w-4" />
              <CardTitle className="text-sm">Security</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">{safeNumber(result.security?.score, 0)}</span>
                <span className={`text-sm ${getScoreColor(safeNumber(result.security?.score, 0))}`}>
                  /100
                </span>
              </div>
              <Progress value={safeNumber(result.security?.score, 0)} className="h-2" />
              {result.security?.summary && (
                <div className="text-xs text-muted-foreground space-y-1">
                  <div>Issues: {safeNumber(result.security.summary.total_issues, 0)}</div>
                  <div>High: {safeNumber(result.security.summary.high_severity, 0)}</div>
                  <div>Medium: {safeNumber(result.security.summary.medium_severity, 0)}</div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Test Coverage */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <TestTube className="h-4 w-4" />
              <CardTitle className="text-sm">Test Coverage</CardTitle>
            </div>
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
              />
              <div className="text-xs text-muted-foreground space-y-1">
                <div>Has Tests: {result.test_coverage?.has_tests ? '✓' : '✗'}</div>
                <div>Frameworks: {safeArray(result.test_coverage?.test_frameworks).length}</div>
                <div>Files: {safeArray(result.test_coverage?.test_files).length}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Code Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Code Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="space-y-4">
              <h4 className="font-medium text-sm">Basic Metrics</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Lines of Code:</span>
                  <span className="font-mono">
                    {safeNumber(result.metrics?.lines_of_code, 0).toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Files:</span>
                  <span className="font-mono">{safeNumber(result.metrics?.files_count, 0)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Complexity:</span>
                  <span className="font-mono">{safeNumber(result.metrics?.complexity, 0)}</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-medium text-sm">Languages</h4>
              <div className="space-y-2">
                {Object.entries(safeObject(result.metrics?.languages)).map(([lang, percentage]) => (
                  <div key={lang} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span>{safeString(lang)}</span>
                      <span>{safeNumber(percentage, 0)}%</span>
                    </div>
                    <Progress value={safeNumber(percentage, 0)} className="h-1" />
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-medium text-sm">Largest Files</h4>
              <div className="space-y-1 text-sm">
                {safeArray(result.metrics?.largest_files).map((file, index: number) => {
                  const fileObj = file as Record<string, unknown>;
                  return (
                    <div key={index} className="flex justify-between">
                      <span className="truncate">{safeString(fileObj?.name, 'Unknown')}</span>
                      <span className="text-muted-foreground">
                        {safeNumber(fileObj?.lines, 0)} lines
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Detailed Analysis Results */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Code Quality Details */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Code className="h-5 w-5" />
              Code Quality Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {Array.isArray(result.code_quality.issues) && result.code_quality.issues.length > 0 && (
              <div>
                <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-500" />
                  Issues Found ({result.code_quality.issues.length})
                </h4>
                <ul className="space-y-1 text-sm max-h-32 overflow-y-auto">
                  {result.code_quality.issues.map((issue: string, index: number) => (
                    <li key={index} className="text-muted-foreground">
                      • {typeof issue === 'string' ? issue : String(issue)}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {Array.isArray(result.code_quality.recommendations) &&
              result.code_quality.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                    <Target className="h-4 w-4 text-green-500" />
                    Recommendations ({result.code_quality.recommendations.length})
                  </h4>
                  <ul className="space-y-1 text-sm max-h-32 overflow-y-auto">
                    {result.code_quality.recommendations.map((rec: string, index: number) => (
                      <li key={index} className="text-muted-foreground">
                        • {typeof rec === 'string' ? rec : String(rec)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

            {result.code_quality.patterns && (
              <div>
                <h4 className="font-medium text-sm mb-2">Code Patterns</h4>
                <div className="space-y-2 text-sm">
                  {Array.isArray(result.code_quality.patterns.design_patterns) &&
                    result.code_quality.patterns.design_patterns.length > 0 && (
                      <div>
                        <span className="text-green-600">Design Patterns: </span>
                        <span>{result.code_quality.patterns.design_patterns.join(', ')}</span>
                      </div>
                    )}
                  {Array.isArray(result.code_quality.patterns.anti_patterns) &&
                    result.code_quality.patterns.anti_patterns.length > 0 && (
                      <div>
                        <span className="text-red-600">Anti-patterns: </span>
                        <span>{result.code_quality.patterns.anti_patterns.join(', ')}</span>
                      </div>
                    )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Security & Documentation Details */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Security & Documentation
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {Array.isArray(result.security.vulnerabilities) &&
              result.security.vulnerabilities.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                    <AlertCircle className="h-4 w-4 text-red-500" />
                    Security Vulnerabilities ({result.security.vulnerabilities.length})
                  </h4>
                  <div className="space-y-2 max-h-32 overflow-y-auto">
                    {result.security.vulnerabilities.map((vuln, index: number) => (
                      <div key={index} className="text-sm p-2 bg-red-50 dark:bg-red-900/20 rounded">
                        <div className="flex justify-between items-start">
                          <span className="font-medium">{vuln?.type || 'Unknown'}</span>
                          <Badge variant={vuln?.severity === 'high' ? 'destructive' : 'secondary'}>
                            {vuln?.severity || 'Unknown'}
                          </Badge>
                        </div>
                        <p className="text-muted-foreground text-xs mt-1">
                          {vuln?.description || 'No description'}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          File: {vuln?.file || 'Unknown'}:{vuln?.line || 'Unknown'}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            {Array.isArray(result.security.recommendations) &&
              result.security.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                    <Info className="h-4 w-4 text-blue-500" />
                    Security Recommendations
                  </h4>
                  <ul className="space-y-1 text-sm max-h-24 overflow-y-auto">
                    {result.security.recommendations.map((rec: string, index: number) => (
                      <li key={index} className="text-muted-foreground">
                        • {typeof rec === 'string' ? rec : String(rec)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

            {result.documentation.details && (
              <div>
                <h4 className="font-medium text-sm mb-2">Documentation Details</h4>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div
                    className="flex items-center gap-2 cursor-help"
                    title="README file: Essential project documentation that explains what the project does, how to install and use it."
                  >
                    <span>README:</span>
                    <span
                      className={
                        result.documentation.details.has_readme ? 'text-green-600' : 'text-red-600'
                      }
                    >
                      {result.documentation.details.has_readme ? '✓' : '✗'}
                    </span>
                  </div>
                  <div
                    className="flex items-center gap-2 cursor-help"
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
                    className="flex items-center gap-2 cursor-help"
                    title="License file: Legal document that specifies the terms under which the software can be used."
                  >
                    <span>License:</span>
                    <span
                      className={
                        result.documentation.details.has_license ? 'text-green-600' : 'text-red-600'
                      }
                    >
                      {result.documentation.details.has_license ? '✓' : '✗'}
                    </span>
                  </div>
                  <div
                    className="flex items-center gap-2 cursor-help"
                    title="Contributing guidelines: Instructions for developers on how to contribute to the project."
                  >
                    <span>Contributing:</span>
                    <span
                      className={
                        result.documentation.details.has_contributing
                          ? 'text-green-600'
                          : 'text-red-600'
                      }
                    >
                      {result.documentation.details.has_contributing ? '✓' : '✗'}
                    </span>
                  </div>
                </div>
                {result.documentation.details.comment_coverage !== undefined && (
                  <div className="mt-3">
                    <div
                      className="flex items-center justify-between text-sm cursor-help"
                      title="Comment Coverage: Percentage of code lines that contain comments. Higher values indicate better code documentation."
                    >
                      <span>Comment Coverage:</span>
                      <span className="font-mono">
                        {result.documentation.details.comment_coverage.toFixed(1)}%
                      </span>
                    </div>
                    <Progress
                      value={result.documentation.details.comment_coverage}
                      className="h-1 mt-1"
                    />
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

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
                <span className="font-mono">{result.test_coverage.coverage_percentage}%</span>
              </div>
              <Progress value={result.test_coverage.coverage_percentage} className="h-2" />
            </div>

            {Array.isArray(result.test_coverage.test_frameworks) &&
              result.test_coverage.test_frameworks.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2">Test Frameworks</h4>
                  <div className="flex flex-wrap gap-1">
                    {result.test_coverage.test_frameworks.map(
                      (framework: string, index: number) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {typeof framework === 'string' ? framework : String(framework)}
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
                    {result.test_coverage.issues.map((issue: string, index: number) => (
                      <li key={index} className="text-muted-foreground">
                        • {typeof issue === 'string' ? issue : String(issue)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

            {Array.isArray(result.test_coverage.recommendations) &&
              result.test_coverage.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-sm mb-2">Test Recommendations</h4>
                  <ul className="space-y-1 text-sm max-h-24 overflow-y-auto">
                    {result.test_coverage.recommendations.map((rec: string, index: number) => (
                      <li key={index} className="text-muted-foreground">
                        • {typeof rec === 'string' ? rec : String(rec)}
                      </li>
                    ))}
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
                <span className="font-mono">{result.license_info.license_type}</span>
              </div>
              <div className="flex justify-between">
                <span>Open Source:</span>
                <span
                  className={result.license_info.is_open_source ? 'text-green-600' : 'text-red-600'}
                >
                  {result.license_info.is_open_source ? '✓ Yes' : '✗ No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Compatibility:</span>
                <span className="font-mono">{result.license_info.compatibility}</span>
              </div>
              {result.license_info.license_file && (
                <div className="flex justify-between">
                  <span>License File:</span>
                  <span className="font-mono text-sm">{result.license_info.license_file}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
