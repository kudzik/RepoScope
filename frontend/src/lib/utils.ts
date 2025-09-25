import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Mapuje poziom bezpieczeństwa na odpowiednie kolory
 * @param severity - poziom bezpieczeństwa (critical, high, medium, low, safe, issues)
 * @returns obiekt z klasami CSS dla tła, tekstu i border
 */
export function getSeverityColor(severity: string) {
  const normalizedSeverity = severity?.toLowerCase() || 'issues';

  switch (normalizedSeverity) {
    case 'critical':
      return {
        bg: 'bg-red-100 dark:bg-red-900/40',
        text: 'text-red-900 dark:text-red-100',
        border: 'border-red-300 dark:border-red-700',
        badge:
          'bg-red-200 text-red-900 border-red-300 dark:bg-red-800/50 dark:text-red-100 dark:border-red-600',
        icon: 'text-red-600 dark:text-red-400',
        title: '🔴 Critical',
        description: 'Immediate attention required - high security risk',
      };
    case 'high':
      return {
        bg: 'bg-red-50 dark:bg-red-900/20',
        text: 'text-red-800 dark:text-red-200',
        border: 'border-red-200 dark:border-red-800',
        badge:
          'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800',
        icon: 'text-red-500 dark:text-red-400',
        title: '🔴 High',
        description: 'Requires attention soon - significant risk',
      };
    case 'medium':
      return {
        bg: 'bg-orange-50 dark:bg-orange-900/20',
        text: 'text-orange-800 dark:text-orange-200',
        border: 'border-orange-200 dark:border-orange-800',
        badge:
          'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-200 dark:border-orange-800',
        icon: 'text-orange-500 dark:text-orange-400',
        title: '🟠 Medium',
        description: 'Attention needed soon - moderate risk',
      };
    case 'low':
      return {
        bg: 'bg-yellow-50 dark:bg-yellow-900/20',
        text: 'text-yellow-800 dark:text-yellow-200',
        border: 'border-yellow-200 dark:border-yellow-800',
        badge:
          'bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-800',
        icon: 'text-yellow-500 dark:text-yellow-400',
        title: '🟡 Low',
        description: 'Low priority, but requires attention - minimal risk',
      };
    case 'safe':
      return {
        bg: 'bg-green-50 dark:bg-green-900/20',
        text: 'text-green-800 dark:text-green-200',
        border: 'border-green-200 dark:border-green-800',
        badge:
          'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800',
        icon: 'text-green-500 dark:text-green-400',
        title: '🟢 Safe',
        description: 'No security issues - everything is fine',
      };
    case 'issues':
    default:
      return {
        bg: 'bg-gray-50 dark:bg-gray-900/20',
        text: 'text-gray-800 dark:text-gray-200',
        border: 'border-gray-200 dark:border-gray-800',
        badge:
          'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-900/30 dark:text-gray-200 dark:border-gray-800',
        icon: 'text-gray-500 dark:text-gray-400',
        title: '⚪ General',
        description: 'Informational, no urgency - standard information',
      };
  }
}

/**
 * Mapuje poziom jakości kodu na odpowiednie kolory
 * @param quality - poziom jakości (excellent, good, fair, poor, critical)
 * @returns obiekt z klasami CSS dla tła, tekstu i border
 */
export function getQualityColor(quality: string) {
  const normalizedQuality = quality?.toLowerCase() || 'fair';

  switch (normalizedQuality) {
    case 'excellent':
      return {
        bg: 'bg-green-50 dark:bg-green-900/20',
        text: 'text-green-800 dark:text-green-200',
        border: 'border-green-200 dark:border-green-800',
        badge:
          'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800',
        icon: 'text-green-500 dark:text-green-400',
        title: '🟢 Excellent',
        description: 'Highest code quality - exemplary implementation',
      };
    case 'good':
      return {
        bg: 'bg-blue-50 dark:bg-blue-900/20',
        text: 'text-blue-800 dark:text-blue-200',
        border: 'border-blue-200 dark:border-blue-800',
        badge:
          'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/30 dark:text-blue-200 dark:border-blue-800',
        icon: 'text-blue-500 dark:text-blue-400',
        title: '🔵 Good',
        description: 'Good code quality - solid implementation',
      };
    case 'fair':
      return {
        bg: 'bg-yellow-50 dark:bg-yellow-900/20',
        text: 'text-yellow-800 dark:text-yellow-200',
        border: 'border-yellow-200 dark:border-yellow-800',
        badge:
          'bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-800',
        icon: 'text-yellow-500 dark:text-yellow-400',
        title: '🟡 Fair',
        description: 'Moderate quality - needs improvement',
      };
    case 'poor':
      return {
        bg: 'bg-orange-50 dark:bg-orange-900/20',
        text: 'text-orange-800 dark:text-orange-200',
        border: 'border-orange-200 dark:border-orange-800',
        badge:
          'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-200 dark:border-orange-800',
        icon: 'text-orange-500 dark:text-orange-400',
        title: '🟠 Poor',
        description: 'Poor quality - requires significant improvements',
      };
    case 'critical':
      return {
        bg: 'bg-red-50 dark:bg-red-900/20',
        text: 'text-red-800 dark:text-red-200',
        border: 'border-red-200 dark:border-red-800',
        badge:
          'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800',
        icon: 'text-red-500 dark:text-red-400',
        title: '🔴 Critical',
        description: 'Critical quality - requires immediate attention',
      };
    default:
      return {
        bg: 'bg-gray-50 dark:bg-gray-900/20',
        text: 'text-gray-800 dark:text-gray-200',
        border: 'border-gray-200 dark:border-gray-800',
        badge:
          'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-900/30 dark:text-gray-200 dark:border-gray-800',
        icon: 'text-gray-500 dark:text-gray-400',
        title: '⚪ Unknown',
        description: 'Unknown quality - requires analysis',
      };
  }
}

/**
 * Mapuje poziom pokrycia testów na odpowiednie kolory
 * @param coverage - poziom pokrycia (excellent, good, fair, poor, critical)
 * @returns obiekt z klasami CSS dla tła, tekstu i border
 */
export function getCoverageColor(coverage: string) {
  const normalizedCoverage = coverage?.toLowerCase() || 'fair';

  switch (normalizedCoverage) {
    case 'excellent':
      return {
        bg: 'bg-green-50 dark:bg-green-900/20',
        text: 'text-green-800 dark:text-green-200',
        border: 'border-green-200 dark:border-green-800',
        badge:
          'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800',
        icon: 'text-green-500 dark:text-green-400',
        title: '🟢 Excellent',
        description: 'Coverage >90% - exemplary testing',
      };
    case 'good':
      return {
        bg: 'bg-blue-50 dark:bg-blue-900/20',
        text: 'text-blue-800 dark:text-blue-200',
        border: 'border-blue-200 dark:border-blue-800',
        badge:
          'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/30 dark:text-blue-200 dark:border-blue-800',
        icon: 'text-blue-500 dark:text-blue-400',
        title: '🔵 Good',
        description: 'Coverage 70-90% - solid testing',
      };
    case 'fair':
      return {
        bg: 'bg-yellow-50 dark:bg-yellow-900/20',
        text: 'text-yellow-800 dark:text-yellow-200',
        border: 'border-yellow-200 dark:border-yellow-800',
        badge:
          'bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-800',
        icon: 'text-yellow-500 dark:text-yellow-400',
        title: '🟡 Fair',
        description: 'Coverage 50-70% - needs improvement',
      };
    case 'poor':
      return {
        bg: 'bg-orange-50 dark:bg-orange-900/20',
        text: 'text-orange-800 dark:text-orange-200',
        border: 'border-orange-200 dark:border-orange-800',
        badge:
          'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-200 dark:border-orange-800',
        icon: 'text-orange-500 dark:text-orange-400',
        title: '🟠 Poor',
        description: 'Coverage 30-50% - requires significant improvements',
      };
    case 'critical':
      return {
        bg: 'bg-red-50 dark:bg-red-900/20',
        text: 'text-red-800 dark:text-red-200',
        border: 'border-red-200 dark:border-red-800',
        badge:
          'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800',
        icon: 'text-red-500 dark:text-red-400',
        title: '🔴 Critical',
        description: 'Coverage <30% - requires immediate attention',
      };
    default:
      return {
        bg: 'bg-gray-50 dark:bg-gray-900/20',
        text: 'text-gray-800 dark:text-gray-200',
        border: 'border-gray-200 dark:border-gray-800',
        badge:
          'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-900/30 dark:text-gray-200 dark:border-gray-800',
        icon: 'text-gray-500 dark:text-gray-400',
        title: '⚪ Unknown',
        description: 'Unknown coverage - requires analysis',
      };
  }
}

/**
 * Mapuje poziom dokumentacji na odpowiednie kolory
 * @param documentation - poziom dokumentacji (excellent, good, fair, poor, critical)
 * @returns obiekt z klasami CSS dla tła, tekstu i border
 */
export function getDocumentationColor(documentation: string) {
  const normalizedDoc = documentation?.toLowerCase() || 'fair';

  switch (normalizedDoc) {
    case 'excellent':
      return {
        bg: 'bg-green-50 dark:bg-green-900/20',
        text: 'text-green-800 dark:text-green-200',
        border: 'border-green-200 dark:border-green-800',
        badge:
          'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800',
        icon: 'text-green-500 dark:text-green-400',
        title: '🟢 Excellent',
        description: 'Exemplary documentation - complete and up-to-date',
      };
    case 'good':
      return {
        bg: 'bg-blue-50 dark:bg-blue-900/20',
        text: 'text-blue-800 dark:text-blue-200',
        border: 'border-blue-200 dark:border-blue-800',
        badge:
          'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/30 dark:text-blue-200 dark:border-blue-800',
        icon: 'text-blue-500 dark:text-blue-400',
        title: '🔵 Good',
        description: 'Good documentation - solid and useful',
      };
    case 'fair':
      return {
        bg: 'bg-yellow-50 dark:bg-yellow-900/20',
        text: 'text-yellow-800 dark:text-yellow-200',
        border: 'border-yellow-200 dark:border-yellow-800',
        badge:
          'bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-800',
        icon: 'text-yellow-500 dark:text-yellow-400',
        title: '🟡 Fair',
        description: 'Moderate documentation - needs improvement',
      };
    case 'poor':
      return {
        bg: 'bg-orange-50 dark:bg-orange-900/20',
        text: 'text-orange-800 dark:text-orange-200',
        border: 'border-orange-200 dark:border-orange-800',
        badge:
          'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-200 dark:border-orange-800',
        icon: 'text-orange-500 dark:text-orange-400',
        title: '🟠 Poor',
        description: 'Poor documentation - requires significant improvements',
      };
    case 'critical':
      return {
        bg: 'bg-red-50 dark:bg-red-900/20',
        text: 'text-red-800 dark:text-red-200',
        border: 'border-red-200 dark:border-red-800',
        badge:
          'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800',
        icon: 'text-red-500 dark:text-red-400',
        title: '🔴 Critical',
        description: 'No documentation - requires immediate attention',
      };
    default:
      return {
        bg: 'bg-gray-50 dark:bg-gray-900/20',
        text: 'text-gray-800 dark:text-gray-200',
        border: 'border-gray-200 dark:border-gray-800',
        badge:
          'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-900/30 dark:text-gray-200 dark:border-gray-800',
        icon: 'text-gray-500 dark:text-gray-400',
        title: '⚪ Unknown',
        description: 'Unknown documentation - requires analysis',
      };
  }
}

/**
 * Mapuje wynik liczbowy na poziom jakości
 * @param score - wynik liczbowy (0-100)
 * @param type - typ metryki (security, quality, coverage, documentation)
 * @returns poziom jakości
 */
export function getScoreLevel(
  score: number,
  _type: 'security' | 'quality' | 'coverage' | 'documentation' = 'quality'
): string {
  if (score >= 90) return 'excellent';
  if (score >= 80) return 'good';
  if (score >= 60) return 'fair';
  if (score >= 40) return 'poor';
  return 'critical';
}

/**
 * Mapuje wynik liczbowy na kolor dla progress bar
 * @param score - wynik liczbowy (0-100)
 * @returns klasa CSS dla koloru
 */
export function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600 dark:text-green-400';
  if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
  if (score >= 40) return 'text-orange-600 dark:text-orange-400';
  return 'text-red-600 dark:text-red-400';
}

/**
 * Mapuje wynik liczbowy na kolor tła dla progress bar
 * @param score - wynik liczbowy (0-100)
 * @returns klasa CSS dla koloru tła
 */
export function getScoreBgColor(score: number): string {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  if (score >= 40) return 'bg-orange-500';
  return 'bg-red-500';
}
