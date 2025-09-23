import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">RepoScope</h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">Repository Analysis Tool</p>
          <Card className="max-w-md mx-auto">
            <CardHeader>
              <CardTitle>shadcn/ui Test</CardTitle>
              <CardDescription>
                This page uses shadcn/ui components with Tailwind CSS.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input placeholder="Enter repository URL..." />
              <Button className="w-full">Analyze Repository</Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
