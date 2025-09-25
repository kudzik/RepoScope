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
  code_structure?: Record<string, unknown>;
  documentation_quality?: Record<string, unknown>;
  test_coverage?: Record<string, unknown>;
  security_issues?: Array<Record<string, unknown>>;
  license_info?: Record<string, unknown>;
  ai_summary?: string;
  analysis_duration?: number;
  error_message?: string;
  result?: AnalysisResult;
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
  test_coverage: TestCoverageMetrics;
  license_info: LicenseInfo;
  metrics: CodeMetrics;
}

export interface CodeQualityMetrics {
  score: number;
  issues: string[];
  recommendations: string[];
  metrics?: {
    maintainability_index: number;
    technical_debt_ratio: number;
    code_duplication: number;
    architecture_score: number;
  };
  patterns?: {
    design_patterns: string[];
    anti_patterns: string[];
    code_smells: string[];
  };
  hotspots?: Array<Record<string, unknown>>;
}

export interface DocumentationMetrics {
  score: number;
  issues: string[];
  recommendations: string[];
  details?: {
    has_readme: boolean;
    has_contributing: boolean;
    has_license: boolean;
    has_api_docs: boolean;
    has_changelog: boolean;
    readme_quality: number;
    comment_coverage: number;
    doc_files: string[];
  };
}

export interface SecurityMetrics {
  score: number;
  vulnerabilities: Array<{
    type: string;
    severity: string;
    description: string;
    file: string;
    line: number;
  }>;
  recommendations: string[];
  summary?: {
    total_issues: number;
    high_severity: number;
    medium_severity: number;
    low_severity: number;
  };
}

export interface TestCoverageMetrics {
  has_tests: boolean;
  coverage_percentage: number;
  test_frameworks: string[];
  test_files: string[];
  test_directories: string[];
  issues: string[];
  recommendations: string[];
}

export interface LicenseInfo {
  license_type: string;
  is_open_source: boolean;
  license_file?: string;
  compatibility: string;
}

export interface CodeMetrics {
  lines_of_code: number;
  files_count: number;
  languages: Record<string, number>;
  complexity: number;
  largest_files: Array<{
    name: string;
    lines: number;
  }>;
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
