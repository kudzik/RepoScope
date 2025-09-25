import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ThemeProvider } from '@/providers/theme-provider';
import { ErrorBoundary } from '@/components/error-boundary';
import { ToastProvider } from '@/components/toast-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'RepoScope - Repository Analysis Tool',
  description: 'Analyze GitHub repositories with AI-powered insights',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className} suppressHydrationWarning>
        <ErrorBoundary>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {children}
            <ToastProvider />
          </ThemeProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}
