'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export function ResponsiveTest() {
  return (
    <div className="p-4 space-y-4">
      <h2 className="text-2xl font-bold text-center mb-6">Responsive Design Test</h2>

      {/* Breakpoint indicators */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <Card className="bg-blue-100 dark:bg-blue-900">
          <CardHeader>
            <CardTitle className="text-sm">Mobile First</CardTitle>
            <CardDescription className="text-xs">Base styles for mobile devices</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-xs space-y-1">
              <div className="block sm:hidden">📱 Mobile (default)</div>
              <div className="hidden sm:block lg:hidden">📱 Small (sm: 640px+)</div>
              <div className="hidden lg:block xl:hidden">💻 Large (lg: 1024px+)</div>
              <div className="hidden xl:block">🖥️ Extra Large (xl: 1280px+)</div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-green-100 dark:bg-green-900">
          <CardHeader>
            <CardTitle className="text-sm">Typography Scale</CardTitle>
            <CardDescription className="text-xs">Responsive text sizing</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <h3 className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-bold">
                Responsive Heading
              </h3>
              <p className="text-xs sm:text-sm md:text-base lg:text-lg">
                This text scales with screen size
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-100 dark:bg-purple-900">
          <CardHeader>
            <CardTitle className="text-sm">Grid Layout</CardTitle>
            <CardDescription className="text-xs">Responsive grid system</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              <div className="bg-white dark:bg-gray-800 p-2 rounded text-xs">Item 1</div>
              <div className="bg-white dark:bg-gray-800 p-2 rounded text-xs">Item 2</div>
              <div className="bg-white dark:bg-gray-800 p-2 rounded text-xs">Item 3</div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-orange-100 dark:bg-orange-900">
          <CardHeader>
            <CardTitle className="text-sm">Spacing</CardTitle>
            <CardDescription className="text-xs">Responsive spacing</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="p-2 sm:p-4 lg:p-6 bg-white dark:bg-gray-800 rounded text-xs">
              Padding: 2 (8px) → 4 (16px) → 6 (24px)
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Container width test */}
      <Card className="w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto">
        <CardHeader>
          <CardTitle className="text-center">Container Width Test</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-sm">
            <p>This container adapts to screen size:</p>
            <p className="mt-2 text-xs">
              Mobile: 320px → Small: 384px → Medium: 448px → Large: 512px → XL: 576px
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
