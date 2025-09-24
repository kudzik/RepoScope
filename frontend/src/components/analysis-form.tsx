'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { useAnalyzeRepositoryWithToast } from '@/hooks/use-toast-api';
import { useNetworkStatus } from '@/hooks/use-network-status';
import { AnalysisList } from './analysis-list';
import { AnalysisResults } from './analysis-results';
import type { AnalysisResponse } from '@/lib/api-types';

export function AnalysisForm() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisResponse | null>(null);
  const [showList, setShowList] = useState(false);
  const { execute, loading, error } = useAnalyzeRepositoryWithToast();
  const { isOnline } = useNetworkStatus();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!url.trim()) return;

    const analysisResult = await execute(url.trim());
    if (analysisResult) {
      setResult(analysisResult);
      setUrl(''); // Clear form on success
      setShowList(true); // Show analyses list
    }
  };

  const isValidGitHubUrl = (url: string) => {
    return url.match(/^https:\/\/github\.com\/[\w\-\.]+\/[\w\-\.]+\/?$/);
  };

  return (
    <div className="space-y-6">
      <Card className="max-w-sm mx-auto sm:max-w-md md:max-w-lg lg:max-w-xl">
        <CardHeader className="space-y-2">
          <CardTitle className="text-xl sm:text-2xl">
            Analyze Repository
          </CardTitle>
          <CardDescription className="text-sm sm:text-base">
            Enter a GitHub repository URL to get AI-powered insights about code quality,
            documentation, and more.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="repository-url" className="sr-only">
                GitHub Repository URL
              </label>
              <Input
                id="repository-url"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="text-sm sm:text-base"
                aria-describedby="repository-help"
                required
                disabled={loading}
              />
              <div id="repository-help" className="sr-only">
                Enter a valid GitHub repository URL starting with https://github.com/
              </div>

              {url && !isValidGitHubUrl(url) && (
                <p className="text-sm text-destructive">
                  Please enter a valid GitHub repository URL
                </p>
              )}

              {!isOnline && (
                <p className="text-sm text-destructive">
                  No internet connection. Please check your network.
                </p>
              )}
            </div>

            <Button
              type="submit"
              className="w-full text-sm sm:text-base"
              disabled={loading || !url.trim() || !isValidGitHubUrl(url) || !isOnline}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                'Analyze Repository'
              )}
            </Button>
          </form>

          {/* Error display */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Success display */}
          {result && (
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>
                Analysis started successfully! ID: {result.id}
                <br />
                Status: {result.status}
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Show selected analysis results */}
      {selectedAnalysis && (
        <div className="mt-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">Analysis Results</h3>
            <Button
              onClick={() => setSelectedAnalysis(null)}
              variant="outline"
              size="sm"
            >
              Close
            </Button>
          </div>
          <AnalysisResults analysis={selectedAnalysis} />
        </div>
      )}

      {/* Show analyses list */}
      {showList && !selectedAnalysis && (
        <div className="mt-8">
          <AnalysisList onSelectAnalysis={setSelectedAnalysis} />
        </div>
      )}
    </div>
  );
}
