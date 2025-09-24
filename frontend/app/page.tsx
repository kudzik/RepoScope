import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ThemeToggle } from '@/components/theme-toggle';
import { ResponsiveTest } from '@/components/responsive-test';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header with theme toggle */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center justify-end px-4">
          <ThemeToggle />
        </div>
      </header>

      {/* Main content */}
      <div className="container mx-auto px-4 py-8 sm:py-12 md:py-16">
        <div className="text-center space-y-6">
          {/* Hero section */}
          <div className="space-y-4">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl md:text-5xl lg:text-6xl">
              RepoScope
            </h1>
            <p className="text-base text-gray-600 dark:text-gray-300 sm:text-lg md:text-xl lg:text-2xl max-w-2xl mx-auto">
              Repository Analysis Tool powered by AI
            </p>
          </div>

          {/* Main card */}
          <Card className="max-w-sm mx-auto sm:max-w-md md:max-w-lg lg:max-w-xl">
            <CardHeader className="space-y-2">
              <CardTitle className="text-xl sm:text-2xl">Analyze Repository</CardTitle>
              <CardDescription className="text-sm sm:text-base">
                Enter a GitHub repository URL to get AI-powered insights about code quality,
                documentation, and more.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Input
                  placeholder="https://github.com/username/repository"
                  className="text-sm sm:text-base"
                />
                <Button className="w-full text-sm sm:text-base">Analyze Repository</Button>
              </div>
            </CardContent>
          </Card>

          {/* Features section */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mt-12 max-w-4xl mx-auto">
            <Card className="p-4 sm:p-6">
              <CardContent className="pt-0">
                <h3 className="font-semibold text-sm sm:text-base mb-2">Code Quality</h3>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  Analyze code structure, patterns, and best practices
                </p>
              </CardContent>
            </Card>

            <Card className="p-4 sm:p-6">
              <CardContent className="pt-0">
                <h3 className="font-semibold text-sm sm:text-base mb-2">Documentation</h3>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  Evaluate README, API docs, and code comments
                </p>
              </CardContent>
            </Card>

            <Card className="p-4 sm:p-6 sm:col-span-2 lg:col-span-1">
              <CardContent className="pt-0">
                <h3 className="font-semibold text-sm sm:text-base mb-2">Security</h3>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  Identify potential security risks and vulnerabilities
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Responsive test section */}
          <div className="mt-16">
            <ResponsiveTest />
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-sm text-muted-foreground">
            <p>© 2024 RepoScope. Built with Next.js, Tailwind CSS, and shadcn/ui.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
