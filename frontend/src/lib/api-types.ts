/**
 * Shared TypeScript types for API communication.
 * These types should match the Pydantic schemas in the backend.
 */

// Base types
export type AnalysisStatus = 'pending' | 'processing' | 'completed' | 'failed';

// Request types
export interface AnalysisRequest {
  repository_url: string;
}

// Response types
export interface AnalysisResponse {
  id: string;
  repository_url: string;
  status: AnalysisStatus;
  created_at: string;
  completed_at?: string;
  result?: AnalysisResult;
  error_message?: string;
}

export interface AnalysisResult {
  summary: string;
  code_quality: CodeQualityMetrics;
  documentation: DocumentationMetrics;
  security: SecurityMetrics;
  metrics: CodeMetrics;
}

export interface CodeQualityMetrics {
  score: number;
  issues: string[];
  recommendations: string[];
}

export interface DocumentationMetrics {
  score: number;
  has_readme: boolean;
  has_api_docs: boolean;
  coverage: number;
}

export interface SecurityMetrics {
  score: number;
  vulnerabilities: string[];
  recommendations: string[];
}

export interface CodeMetrics {
  lines_of_code: number;
  files_count: number;
  languages: Record<string, number>;
  complexity: number;
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Error types
export interface ApiErrorResponse {
  detail: string;
  status_code?: number;
}

// Health check
export interface HealthResponse {
  status: string;
  service: string;
}
