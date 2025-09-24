'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  CheckCircle,
  Clock,
  AlertTriangle,
  XCircle,
  Code,
  FileText,
  Shield,
  BarChart3
} from 'lucide-react';
import type { AnalysisResponse, AnalysisResult } from '@/lib/api-types';

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

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <CardTitle>Analysis Complete</CardTitle>
            <Badge className={getStatusColor(analysis.status)}>
              {analysis.status}
            </Badge>
          </div>
          <CardDescription>
            Repository: {analysis.repository_url}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm">{result.summary}</p>
        </CardContent>
      </Card>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Code Quality */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Code className="h-4 w-4" />
              <CardTitle className="text-sm">Code Quality</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {result.code_quality.score}
                </span>
                <span className={`text-sm ${getScoreColor(result.code_quality.score)}`}>
                  /100
                </span>
              </div>
              <Progress value={result.code_quality.score} className="h-2" />
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
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold">
                  {result.documentation.score}
                </span>
                <span className={`text-sm ${getScoreColor(result.documentation.score)}`}>
                  /100
                </span>
              </div>
              <Progress value={result.documentation.score} className="h-2" />
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
                <span className="text-2xl font-bold">
                  {result.security.score}
                </span>
                <span className={`text-sm ${getScoreColor(result.security.score)}`}>
                  /100
                </span>
              </div>
              <Progress value={result.security.score} className="h-2" />
            </div>
          </CardContent>
        </Card>

        {/* Code Metrics */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              <CardTitle className="text-sm">Code Metrics</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Lines:</span>
                <span>{result.metrics.lines_of_code.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span>Files:</span>
                <span>{result.metrics.files_count}</span>
              </div>
              <div className="flex justify-between">
                <span>Complexity:</span>
                <span>{result.metrics.complexity}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Results */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Issues & Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Issues & Recommendations</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {result.code_quality.issues.length > 0 && (
              <div>
                <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-500" />
                  Code Quality Issues
                </h4>
                <ul className="space-y-1 text-sm">
                  {result.code_quality.issues.map((issue, index) => (
                    <li key={index} className="text-muted-foreground">
                      • {issue}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.code_quality.recommendations.length > 0 && (
              <div>
                <h4 className="font-medium text-sm mb-2">Recommendations</h4>
                <ul className="space-y-1 text-sm">
                  {result.code_quality.recommendations.map((rec, index) => (
                    <li key={index} className="text-muted-foreground">
                      • {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Security & Languages */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Security & Languages</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {result.security.vulnerabilities.length > 0 && (
              <div>
                <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                  <Shield className="h-4 w-4 text-red-500" />
                  Security Issues
                </h4>
                <ul className="space-y-1 text-sm">
                  {result.security.vulnerabilities.map((vuln, index) => (
                    <li key={index} className="text-muted-foreground">
                      • {vuln}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div>
              <h4 className="font-medium text-sm mb-2">Languages</h4>
              <div className="space-y-2">
                {Object.entries(result.metrics.languages).map(([lang, percentage]) => (
                  <div key={lang} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span>{lang}</span>
                      <span>{percentage}%</span>
                    </div>
                    <Progress value={percentage} className="h-1" />
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
