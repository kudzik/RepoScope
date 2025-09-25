/**
 * React hooks for API operations with loading states and error handling.
 */

import { useState, useCallback } from 'react';
import { apiClient, ApiError } from '@/lib/api-client';
// import type { AnalysisResponse, PaginatedResponse } from '@/lib/api-types';

// Generic hook for async operations
export function useAsyncOperation<T extends unknown[], R>(
  operation: (...args: T) => Promise<R>
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (...args: T): Promise<R | null> => {
      try {
        setLoading(true);
        setError(null);
        const result = await operation(...args);
        return result;
      } catch (err) {
        const errorMessage =
          err instanceof ApiError
            ? err.message
            : 'An unexpected error occurred';
        setError(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [operation]
  );

  return { execute, loading, error };
}

// Hook for repository analysis
export function useAnalyzeRepository() {
  return useAsyncOperation(apiClient.analyzeRepository.bind(apiClient));
}

// Hook for getting analyses list
export function useGetAnalyses() {
  return useAsyncOperation(apiClient.getAnalyses.bind(apiClient));
}

// Hook for getting single analysis
export function useGetAnalysis() {
  return useAsyncOperation(apiClient.getAnalysis.bind(apiClient));
}

// Hook for deleting analysis
export function useDeleteAnalysis() {
  return useAsyncOperation(apiClient.deleteAnalysis.bind(apiClient));
}

// Hook for health check
export function useHealthCheck() {
  return useAsyncOperation(apiClient.healthCheck.bind(apiClient));
}
