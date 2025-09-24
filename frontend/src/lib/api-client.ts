/**
 * API Client for RepoScope backend communication.
 * Handles all HTTP requests to the FastAPI backend.
 */

import { env } from './env';
import type {
  // AnalysisRequest,
  AnalysisResponse,
  PaginatedResponse,
  HealthResponse,
} from './api-types';

// API Client class
export class ApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor() {
    this.baseUrl = env.API_URL;
    this.timeout = env.API_TIMEOUT;
  }

  /**
   * Make HTTP request with error handling and retry logic
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    retries: number = 3
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    // Add timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    config.signal = controller.signal;

    try {
      const response = await fetch(url, config);
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          response.status,
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
          errorData
        );
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof ApiError) {
        // Retry on server errors (5xx) or timeout (408)
        if (retries > 0 && (error.status >= 500 || error.status === 408)) {
          console.log(`Retrying request (${4 - retries}/3)...`);
          await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries))); // Exponential backoff
          return this.request(endpoint, options, retries - 1);
        }
        throw error;
      }

      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new ApiError(408, 'Request timeout - analysis may take longer than expected');
        }
        throw new ApiError(0, `Network error: ${error.message}`);
      }

      throw new ApiError(0, 'Unknown error occurred');
    }
  }

  /**
   * Start repository analysis
   */
  async analyzeRepository(repositoryUrl: string): Promise<AnalysisResponse> {
    return this.request<AnalysisResponse>('/analysis/', {
      method: 'POST',
      body: JSON.stringify({ repository_url: repositoryUrl }),
    });
  }

  /**
   * Get list of analyses with pagination
   */
  async getAnalyses(
    page: number = 1,
    size: number = 10
  ): Promise<PaginatedResponse<AnalysisResponse>> {
    return this.request<PaginatedResponse<AnalysisResponse>>(
      `/analysis/?page=${page}&size=${size}`
    );
  }

  /**
   * Get single analysis by ID
   */
  async getAnalysis(id: string): Promise<AnalysisResponse> {
    return this.request<AnalysisResponse>(`/analysis/${id}/`);
  }

  /**
   * Delete analysis by ID
   */
  async deleteAnalysis(id: string): Promise<void> {
    await this.request<void>(`/analysis/${id}/`, {
      method: 'DELETE',
    });
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }
}

// Custom error class for API errors
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }

  get isNetworkError(): boolean {
    return this.status === 0;
  }

  get isTimeout(): boolean {
    return this.status === 408;
  }

  get isClientError(): boolean {
    return this.status >= 400 && this.status < 500;
  }

  get isServerError(): boolean {
    return this.status >= 500;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
