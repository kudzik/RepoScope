'use client';

import { Progress } from '@/components/ui/progress';
import { METRIC_COLORS } from '@/lib/color-system';
import { TYPOGRAPHY } from '@/lib/layout-config';

interface QualityMetricsProps {
  metrics: {
    maintainability_index?: number;
    technical_debt_ratio?: number;
    code_duplication?: number;
    test_coverage?: number;
  };
  architectureScore?: number;
  overallScore?: number;
  issuesCount?: number;
  recommendationsCount?: number;
}

export function QualityMetrics({
  metrics,
  architectureScore = 0,
  overallScore = 0,
  issuesCount = 0,
  recommendationsCount = 0,
}: QualityMetricsProps) {
  const metricItems = [
    {
      key: 'maintainability',
      label: 'Maintainability',
      value: metrics.maintainability_index || 0,
      max: 100,
      unit: '/100',
      color: METRIC_COLORS.maintainability,
      title:
        'Code maintainability index (0-100) based on complexity, documentation, and structure',
    },
    {
      key: 'technicalDebt',
      label: 'Tech Debt',
      value: metrics.technical_debt_ratio || 0,
      max: 100,
      unit: '%',
      color: METRIC_COLORS.technicalDebt,
      title:
        'Technical debt ratio indicating code quality issues that need to be addressed',
    },
    {
      key: 'duplication',
      label: 'Duplication',
      value: metrics.code_duplication || 0,
      max: 100,
      unit: '%',
      color: METRIC_COLORS.duplication,
      title:
        'Percentage of duplicated code that could be refactored for better maintainability',
    },
    {
      key: 'architecture',
      label: 'Architecture',
      value: architectureScore,
      max: 100,
      unit: '/100',
      color: METRIC_COLORS.architecture,
      title:
        'Architecture quality score (0-100) based on design patterns, modularity, and code organization',
    },
    {
      key: 'testCoverage',
      label: 'Test Coverage',
      value: metrics.test_coverage || 0,
      max: 100,
      unit: '%',
      color: METRIC_COLORS.testCoverage,
      title:
        'Percentage of code covered by automated tests, indicating code reliability and quality',
    },
    {
      key: 'overall',
      label: 'Overall Score',
      value: overallScore,
      max: 100,
      unit: '/100',
      color: METRIC_COLORS.lines,
      title:
        'Overall code quality score (0-100) combining all quality metrics and analysis results',
    },
    {
      key: 'issues',
      label: 'Issues Found',
      value: issuesCount,
      unit: '',
      color: METRIC_COLORS.issues,
      title:
        'Number of code quality issues, bugs, and potential problems identified during analysis',
    },
    {
      key: 'recommendations',
      label: 'Recommendations',
      value: recommendationsCount,
      unit: '',
      color: METRIC_COLORS.recommendations,
      title:
        'Number of improvement suggestions and best practices recommendations for the codebase',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {metricItems.map(metric => (
        <div key={metric.key} className="space-y-4">
          <h4 className={TYPOGRAPHY.title.metric}>{metric.label}</h4>
          <div className="space-y-3 text-sm">
            <div
              className={`flex justify-between items-center p-3 bg-${metric.color}-50 dark:bg-${metric.color}-950/20 rounded-lg border cursor-help`}
              title={metric.title}
            >
              <div className="flex items-center gap-2">
                <div
                  className={`w-3 h-3 rounded-full bg-${metric.color}-500`}
                />
                <span>{metric.label}:</span>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`font-mono font-semibold text-${metric.color}-700 dark:text-${metric.color}-300`}
                >
                  {typeof metric.value === 'number'
                    ? metric.value.toFixed(metric.unit.includes('%') ? 1 : 0)
                    : metric.value}
                  {metric.unit}
                </span>
                {metric.max && typeof metric.value === 'number' && (
                  <Progress value={metric.value} className="w-16 h-2" />
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
