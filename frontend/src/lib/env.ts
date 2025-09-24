/**
 * Environment variables configuration for RepoScope frontend.
 * Validates and exports environment variables with proper types.
 */

// Validate required environment variables
const requiredEnvVars = {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
} as const;

// Check for missing required variables
const missingVars = Object.entries(requiredEnvVars)
  .filter(([, value]) => !value)
  .map(([key]) => key);

if (missingVars.length > 0) {
  throw new Error(
    `Missing required environment variables: ${missingVars.join(', ')}\n` +
      'Please check your .env.local file.'
  );
}

// Export validated environment variables
export const env = {
  // API Configuration
  API_URL: requiredEnvVars.NEXT_PUBLIC_API_URL!,
  API_TIMEOUT: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '120000', 10), // 2 minutes

  // Supabase Configuration (optional for now)
  SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
  SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',

  // SuperTokens Configuration (optional for now)
  SUPERTOKENS_WEBSITE_DOMAIN: process.env.NEXT_PUBLIC_SUPERTOKENS_WEBSITE_DOMAIN || '',
  SUPERTOKENS_API_DOMAIN: process.env.NEXT_PUBLIC_SUPERTOKENS_API_DOMAIN || '',

  // Application Settings
  APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'RepoScope',
  APP_VERSION: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  ENVIRONMENT: process.env.NEXT_PUBLIC_ENVIRONMENT || 'development',

  // Analytics & Monitoring (optional for now)
  SENTRY_DSN: process.env.NEXT_PUBLIC_SENTRY_DSN || '',
  HIGHLIGHT_PROJECT_ID: process.env.NEXT_PUBLIC_HIGHLIGHT_PROJECT_ID || '',
} as const;

// Type for environment variables
export type Environment = typeof env;
