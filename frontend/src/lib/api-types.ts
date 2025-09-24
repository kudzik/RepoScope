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
  repository_info: RepositoryInfo;
  status: AnalysisStatus;
  created_at: string;
  completed_at?: string;
  code_structure?: any;
  documentation_quality?: any;
  test_coverage?: any;
  security_issues?: any[];
  license_info?: any;
  ai_summary?: string;
  analysis_duration?: number;
  error_message?: string;
}

export interface RepositoryInfo {
  name: string;
  owner: string;
  full_name: string;
  description?: string;
  language?: string;
  stars: number;
  forks: number;
  size: number;
  created_at?: string;
  updated_at?: string;
}

// Legacy types for backward compatibility
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
  analyses: T[];
  total: number;
  page: number;
  page_size: number;
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
