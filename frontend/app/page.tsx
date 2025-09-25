'use client';

import { Card, CardContent } from '@/components/ui/card';
import { ThemeToggle } from '@/components/theme-toggle';
import { AnalysisForm } from '@/components/analysis-form';
import { AnalysisResults } from '@/components/analysis-results';
import { AnalysisList } from '@/components/analysis-list';
import { LoadingOverlay } from '@/components/loading-overlay';
import { useState } from 'react';
import type { AnalysisResponse } from '@/lib/api-types';

export default function Home() {
  const [selectedAnalysis, setSelectedAnalysis] =
    useState<AnalysisResponse | null>(null);
  const [showList, setShowList] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const handleAnalysisStart = () => {
    setIsAnalyzing(true);
    setAnalysisError(null);
  };

  const handleAnalysisComplete = (analysis: AnalysisResponse) => {
    setSelectedAnalysis(analysis);
    setShowList(true);
    setIsAnalyzing(false);
  };

  const handleAnalysisError = (error: string) => {
    setAnalysisError(error);
    setIsAnalyzing(false);
  };

  const handleBackToForm = () => {
    setSelectedAnalysis(null);
    setShowList(false);
    setAnalysisError(null);
  };

  return (
    <>
      {/* Skip link for accessibility */}
      <a href="#main-content" className="skip-link">
        Przejdź do głównej treści
      </a>

      <main
        id="main-content"
        className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800"
        role="main"
        aria-label="Repository Analysis Tool"
      >
        {/* Header with theme toggle */}
        <header
          className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
          role="banner"
        >
          <div className="container flex h-14 items-center justify-between px-4">
            <div className="flex items-center gap-4">
              <h1 className="text-lg font-semibold">RepoScope</h1>
              {selectedAnalysis && (
                <button
                  onClick={handleBackToForm}
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  ← Back to Analysis
                </button>
              )}
            </div>
            <ThemeToggle />
          </div>
        </header>

        {/* Main content */}
        <div className="container mx-auto px-4 py-6 sm:py-8 md:py-12 lg:py-16">
          {!selectedAnalysis ? (
            <div className="text-center space-y-6">
              {/* Hero section */}
              <section className="space-y-4" aria-labelledby="hero-title">
                <h2
                  id="hero-title"
                  className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl"
                >
                  RepoScope
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-300 sm:text-base md:text-lg lg:text-xl xl:text-2xl max-w-2xl mx-auto">
                  Repository Analysis Tool powered by AI
                </p>
              </section>

              {/* Analysis Form */}
              <section aria-labelledby="analyze-title">
                <AnalysisForm
                  onAnalysisComplete={handleAnalysisComplete}
                  onAnalysisStart={handleAnalysisStart}
                  onAnalysisError={handleAnalysisError}
                />
              </section>

              {/* Features section */}
              <section
                aria-labelledby="features-title"
                className="mt-8 sm:mt-12"
              >
                <h3 id="features-title" className="sr-only">
                  Key Features
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-5xl mx-auto">
                  <Card className="p-4 sm:p-6">
                    <CardContent className="pt-0">
                      <h4 className="font-semibold text-sm sm:text-base mb-2">
                        Code Quality
                      </h4>
                      <p className="text-xs sm:text-sm text-muted-foreground">
                        Analyze code structure, patterns, and best practices
                      </p>
                    </CardContent>
                  </Card>

                  <Card className="p-4 sm:p-6">
                    <CardContent className="pt-0">
                      <h4 className="font-semibold text-sm sm:text-base mb-2">
                        Documentation
                      </h4>
                      <p className="text-xs sm:text-sm text-muted-foreground">
                        Evaluate README, API docs, and code comments
                      </p>
                    </CardContent>
                  </Card>

                  <Card className="p-4 sm:p-6 sm:col-span-2 lg:col-span-1">
                    <CardContent className="pt-0">
                      <h4 className="font-semibold text-sm sm:text-base mb-2">
                        Security
                      </h4>
                      <p className="text-xs sm:text-sm text-muted-foreground">
                        Identify potential security risks and vulnerabilities
                      </p>
                    </CardContent>
                  </Card>
                </div>
              </section>
            </div>
          ) : (
            /* Analysis Results */
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold mb-2">Analysis Results</h2>
                <p className="text-muted-foreground">
                  Repository: {selectedAnalysis.repository_info.full_name}
                </p>
              </div>
              <AnalysisResults analysis={selectedAnalysis} />
            </div>
          )}

          {/* Show analyses list when available */}
          {showList && !selectedAnalysis && (
            <div className="mt-8">
              <AnalysisList onSelectAnalysis={setSelectedAnalysis} />
            </div>
          )}

          {/* Loading overlay */}
          {isAnalyzing && (
            <LoadingOverlay
              message="Analyzing repository... This may take up to 2 minutes."
              progress={undefined}
            />
          )}

          {/* Error display */}
          {analysisError && (
            <div className="fixed bottom-4 right-4 z-50">
              <Card className="border-destructive bg-destructive/10">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-2 bg-destructive rounded-full" />
                    <p className="text-sm text-destructive font-medium">
                      {analysisError}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        {/* Footer */}
        <footer
          className="border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
          role="contentinfo"
        >
          <div className="container mx-auto px-4 py-6">
            <div className="text-center text-sm text-muted-foreground">
              <p>
                © 2024 RepoScope. Built with Next.js, Tailwind CSS, and
                shadcn/ui.
              </p>
            </div>
          </div>
        </footer>
      </main>
    </>
  );
}
