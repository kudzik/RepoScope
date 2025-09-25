/**
 * Enhanced API hooks with toast notifications.
 */

import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { apiClient, ApiError } from '@/lib/api-client';
import type { AnalysisResponse } from '@/lib/api-types';

// Generic hook with toast notifications
export function useAsyncOperationWithToast<T extends unknown[], R>(
  operation: (...args: T) => Promise<R>,
  options?: {
    successMessage?: string | ((result: R) => string);
    errorMessage?: string | ((error: Error) => string);
    loadingMessage?: string;
  }
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (...args: T): Promise<R | null> => {
      try {
        setLoading(true);
        setError(null);

        // Show loading toast if message provided
        const loadingToastId = options?.loadingMessage
          ? toast.loading(options.loadingMessage)
          : null;

        const result = await operation(...args);

        // Dismiss loading toast
        if (loadingToastId) {
          toast.dismiss(loadingToastId);
        }

        // Show success toast
        if (options?.successMessage) {
          const message =
            typeof options.successMessage === 'function'
              ? options.successMessage(result)
              : options.successMessage;
          toast.success(message);
        }

        return result;
      } catch (err) {
        const errorMessage =
          err instanceof ApiError
            ? err.message
            : 'An unexpected error occurred';

        setError(errorMessage);

        // Show error toast
        const finalErrorMessage = options?.errorMessage
          ? typeof options.errorMessage === 'function'
            ? options.errorMessage(err as Error)
            : options.errorMessage
          : errorMessage;

        toast.error(finalErrorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [operation, options]
  );

  return { execute, loading, error };
}

// Enhanced hooks with toast notifications
export function useAnalyzeRepositoryWithToast() {
  return useAsyncOperationWithToast(
    apiClient.analyzeRepository.bind(apiClient),
    {
      loadingMessage:
        'Starting repository analysis... This may take up to 2 minutes.',
      successMessage: (result: AnalysisResponse) =>
        `Analysis completed for ${result.repository_url}`,
      errorMessage: (error: Error) => {
        if (error.message.includes('timeout')) {
          return 'Analysis timed out. The repository may be too large or the server is slow. Please try again.';
        }
        return 'Failed to analyze repository. Please check the URL and try again.';
      },
    }
  );
}

export function useGetAnalysesWithToast() {
  return useAsyncOperationWithToast(apiClient.getAnalyses.bind(apiClient), {
    errorMessage: 'Failed to load analyses',
  });
}

export function useDeleteAnalysisWithToast() {
  return useAsyncOperationWithToast(apiClient.deleteAnalysis.bind(apiClient), {
    successMessage: 'Analysis deleted successfully',
    errorMessage: 'Failed to delete analysis',
  });
}

export function useHealthCheckWithToast() {
  return useAsyncOperationWithToast(apiClient.healthCheck.bind(apiClient), {
    successMessage: 'Backend is healthy',
    errorMessage: 'Backend health check failed',
  });
}

// Utility functions for manual toast usage
export const toastUtils = {
  success: (message: string) => toast.success(message),
  error: (message: string) => toast.error(message),
  info: (message: string) => toast.info(message),
  warning: (message: string) => toast.warning(message),
  loading: (message: string) => toast.loading(message),
  promise: <T>(
    promise: Promise<T>,
    messages: {
      loading: string;
      success: string | ((data: T) => string);
      error: string | ((error: unknown) => string);
    }
  ) => toast.promise(promise, messages),
};
