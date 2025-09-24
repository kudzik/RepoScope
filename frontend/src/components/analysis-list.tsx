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
  AlertCircle
} from 'lucide-react';
import { useGetAnalyses, useDeleteAnalysis } from '@/hooks/use-api';
import type { AnalysisResponse } from '@/lib/api-types';

interface AnalysisListProps {
  onSelectAnalysis?: (analysis: AnalysisResponse) => void;
}

export function AnalysisList({ onSelectAnalysis }: AnalysisListProps) {
  const [page, setPage] = useState(1);
  const [analyses, setAnalyses] = useState<AnalysisResponse[]>([]);
  const { execute: fetchAnalyses, loading, error } = useGetAnalyses();
  const { execute: deleteAnalysis, loading: deleting } = useDeleteAnalysis();

  const loadAnalyses = async () => {
    const result = await fetchAnalyses(page, 10);
    if (result) {
      setAnalyses(result.items);
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
        <AlertDescription>
          Failed to load analyses: {error}
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Recent Analyses</h2>
        <Button
          onClick={loadAnalyses}
          disabled={loading}
          variant="outline"
          size="sm"
        >
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
          {analyses.map((analysis) => (
            <Card key={analysis.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(analysis.status)}
                      <CardTitle className="text-lg">
                        {getRepoName(analysis.repository_url)}
                      </CardTitle>
                      <Badge className={getStatusColor(analysis.status)}>
                        {analysis.status}
                      </Badge>
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
                    <AlertDescription>
                      {analysis.error_message}
                    </AlertDescription>
                  </Alert>
                </CardContent>
              )}

              {analysis.result && (
                <CardContent className="pt-0">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="text-center">
                      <div className="font-medium">Code Quality</div>
                      <div className="text-2xl font-bold">
                        {analysis.result.code_quality.score}
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="font-medium">Documentation</div>
                      <div className="text-2xl font-bold">
                        {analysis.result.documentation.score}
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="font-medium">Security</div>
                      <div className="text-2xl font-bold">
                        {analysis.result.security.score}
                      </div>
                    </div>
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
