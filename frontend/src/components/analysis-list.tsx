'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  CheckCircle,
  Clock,
  XCircle,
  Trash2,
  ExternalLink,
  RefreshCw,
  AlertCircle,
} from 'lucide-react';
import { useGetAnalysesWithToast, useDeleteAnalysisWithToast } from '@/hooks/use-toast-api';
import type { AnalysisResponse } from '@/lib/api-types';

interface AnalysisListProps {
  onSelectAnalysis?: (analysis: AnalysisResponse) => void;
}

export function AnalysisList({ onSelectAnalysis }: AnalysisListProps) {
  const [page, setPage] = useState(1);
  const [analyses, setAnalyses] = useState<AnalysisResponse[]>([]);
  const { execute: fetchAnalyses, loading, error } = useGetAnalysesWithToast();
  const { execute: deleteAnalysis, loading: deleting } = useDeleteAnalysisWithToast();

  const loadAnalyses = async () => {
    const result = await fetchAnalyses(page, 10);
    if (result && result.analyses) {
      setAnalyses(result.analyses);
    } else {
      setAnalyses([]);
    }
  };

  useEffect(() => {
    loadAnalyses();
  }, [page]);

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this analysis?')) {
      const success = await deleteAnalysis(id);
      if (success !== null) {
        // Refresh the list
        loadAnalyses();
      }
    }
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pl-PL', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getRepoName = (url: string) => {
    const match = url.match(/github\.com\/([^\/]+\/[^\/]+)/);
    return match ? match[1] : url;
  };

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>Failed to load analyses: {error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Recent Analyses</h2>
        <Button onClick={loadAnalyses} disabled={loading} variant="outline" size="sm">
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {loading && analyses.length === 0 ? (
        <div className="text-center py-8">
          <Clock className="h-8 w-8 mx-auto mb-2 animate-pulse" />
          <p className="text-muted-foreground">Loading analyses...</p>
        </div>
      ) : analyses.length === 0 ? (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No analyses found. Start by analyzing a repository above.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {analyses.map(analysis => (
            <Card key={analysis.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(analysis.status)}
                      <CardTitle className="text-lg">
                        {getRepoName(analysis.repository_url)}
                      </CardTitle>
                      <Badge className={getStatusColor(analysis.status)}>{analysis.status}</Badge>
                    </div>
                    <CardDescription>
                      Created: {formatDate(analysis.created_at)}
                      {analysis.completed_at && (
                        <> • Completed: {formatDate(analysis.completed_at)}</>
                      )}
                    </CardDescription>
                  </div>
                  <div className="flex gap-2">
                    {analysis.status === 'completed' && onSelectAnalysis && (
                      <Button
                        onClick={() => onSelectAnalysis(analysis)}
                        variant="outline"
                        size="sm"
                      >
                        <ExternalLink className="h-4 w-4 mr-2" />
                        View
                      </Button>
                    )}
                    <Button
                      onClick={() => handleDelete(analysis.id)}
                      disabled={deleting}
                      variant="outline"
                      size="sm"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>

              {analysis.error_message && (
                <CardContent className="pt-0">
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{analysis.error_message}</AlertDescription>
                  </Alert>
                </CardContent>
              )}

              {analysis.ai_summary && (
                <CardContent className="pt-0">
                  <div className="space-y-2">
                    <h4 className="font-medium text-sm">AI Analysis Summary</h4>
                    <div className="text-sm text-muted-foreground max-h-32 overflow-y-auto bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                      {analysis.ai_summary}
                    </div>
                  </div>
                </CardContent>
              )}

              {analysis.status === 'completed' && analysis.repository_info && (
                <CardContent className="pt-0">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="text-center">
                      <div className="font-medium">Stars</div>
                      <div className="text-2xl font-bold">{analysis.repository_info.stars}</div>
                    </div>
                    <div className="text-center">
                      <div className="font-medium">Forks</div>
                      <div className="text-2xl font-bold">{analysis.repository_info.forks}</div>
                    </div>
                    <div className="text-center">
                      <div className="font-medium">Language</div>
                      <div className="text-sm font-bold">
                        {analysis.repository_info.language || 'N/A'}
                      </div>
                    </div>
                  </div>

                  {/* Show detailed metrics if result is available */}
                  {analysis.result && (
                    <div className="mt-4 pt-4 border-t space-y-4">
                      {/* Main Metrics */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                          <div className="font-medium text-green-600">Code Quality</div>
                          <div className="text-2xl font-bold text-green-700">
                            {analysis.result.code_quality.score}/100
                          </div>
                        </div>
                        <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <div className="font-medium text-blue-600">Documentation</div>
                          <div className="text-2xl font-bold text-blue-700">
                            {analysis.result.documentation.score}/100
                          </div>
                        </div>
                        <div className="text-center p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                          <div className="font-medium text-red-600">Security</div>
                          <div className="text-2xl font-bold text-red-700">
                            {analysis.result.security.score}/100
                          </div>
                        </div>
                        <div className="text-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                          <div className="font-medium text-purple-600">Test Coverage</div>
                          <div className="text-2xl font-bold text-purple-700">
                            {analysis.result.test_coverage.coverage_percentage}%
                          </div>
                        </div>
                      </div>

                      {/* Additional Details */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        {/* Code Quality Details */}
                        {analysis.result.code_quality.issues.length > 0 && (
                          <div className="space-y-2">
                            <h5 className="font-medium text-yellow-600">
                              Code Issues ({analysis.result.code_quality.issues.length})
                            </h5>
                            <div className="max-h-20 overflow-y-auto space-y-1">
                              {analysis.result.code_quality.issues
                                .slice(0, 3)
                                .map((issue: string, index: number) => (
                                  <div key={index} className="text-xs text-muted-foreground">
                                    • {issue}
                                  </div>
                                ))}
                              {analysis.result.code_quality.issues.length > 3 && (
                                <div className="text-xs text-muted-foreground">
                                  ... i {analysis.result.code_quality.issues.length - 3} więcej
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Security Details */}
                        {analysis.result.security.vulnerabilities.length > 0 && (
                          <div className="space-y-2">
                            <h5 className="font-medium text-red-600">
                              Security Issues ({analysis.result.security.vulnerabilities.length})
                            </h5>
                            <div className="max-h-20 overflow-y-auto space-y-1">
                              {analysis.result.security.vulnerabilities
                                .slice(0, 3)
                                .map((vuln: any, index: number) => (
                                  <div key={index} className="text-xs text-muted-foreground">
                                    • {vuln.type} ({vuln.severity})
                                  </div>
                                ))}
                              {analysis.result.security.vulnerabilities.length > 3 && (
                                <div className="text-xs text-muted-foreground">
                                  ... i {analysis.result.security.vulnerabilities.length - 3} więcej
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Test Coverage Details */}
                        {analysis.result.test_coverage.test_frameworks.length > 0 && (
                          <div className="space-y-2">
                            <h5 className="font-medium text-purple-600">Test Frameworks</h5>
                            <div className="flex flex-wrap gap-1">
                              {analysis.result.test_coverage.test_frameworks.map(
                                (framework: string, index: number) => (
                                  <span
                                    key={index}
                                    className="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 px-2 py-1 rounded"
                                  >
                                    {framework}
                                  </span>
                                )
                              )}
                            </div>
                          </div>
                        )}

                        {/* Documentation Details */}
                        {analysis.result.documentation.details && (
                          <div className="space-y-2">
                            <h5 className="font-medium text-blue-600">Documentation Status</h5>
                            <div className="grid grid-cols-2 gap-2 text-xs">
                              <div className="flex items-center gap-1">
                                <span>README:</span>
                                <span
                                  className={
                                    analysis.result.documentation.details.has_readme
                                      ? 'text-green-600'
                                      : 'text-red-600'
                                  }
                                >
                                  {analysis.result.documentation.details.has_readme ? '✓' : '✗'}
                                </span>
                              </div>
                              <div className="flex items-center gap-1">
                                <span>API Docs:</span>
                                <span
                                  className={
                                    analysis.result.documentation.details.has_api_docs
                                      ? 'text-green-600'
                                      : 'text-red-600'
                                  }
                                >
                                  {analysis.result.documentation.details.has_api_docs ? '✓' : '✗'}
                                </span>
                              </div>
                              <div className="flex items-center gap-1">
                                <span>License:</span>
                                <span
                                  className={
                                    analysis.result.documentation.details.has_license
                                      ? 'text-green-600'
                                      : 'text-red-600'
                                  }
                                >
                                  {analysis.result.documentation.details.has_license ? '✓' : '✗'}
                                </span>
                              </div>
                              <div className="flex items-center gap-1">
                                <span>Contributing:</span>
                                <span
                                  className={
                                    analysis.result.documentation.details.has_contributing
                                      ? 'text-green-600'
                                      : 'text-red-600'
                                  }
                                >
                                  {analysis.result.documentation.details.has_contributing
                                    ? '✓'
                                    : '✗'}
                                </span>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
