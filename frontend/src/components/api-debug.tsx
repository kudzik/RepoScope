'use client';

import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, CheckCircle, Clock, RefreshCw, XCircle } from 'lucide-react';
import { useCallback, useEffect, useState } from 'react';

interface APIStatus {
  endpoint: string;
  status: number | string;
  duration: number;
  success: boolean;
  response?: string;
  error?: string;
}

interface SystemInfo {
  cpu_percent: number;
  memory: {
    total: number;
    available: number;
    percent: number;
  };
  process: {
    pid: number;
    memory_rss: number;
    memory_vms: number;
    cpu_percent: number;
  };
}

interface HealthResponse {
  status: string;
  service: string;
  uptime_seconds: number;
  timestamp: number;
  system?: SystemInfo;
  process?: {
    pid: number;
    memory_rss: number;
    memory_vms: number;
    cpu_percent: number;
  };
  error?: string;
}

export default function APIDebug() {
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<APIStatus[]>([]);
  const [healthInfo, setHealthInfo] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const testEndpoint = async (endpoint: string, timeout: number = 10000) => {
    const startTime = Date.now();

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        signal: controller.signal,
        method: endpoint === '/analysis/' ? 'GET' : 'GET',
      });

      clearTimeout(timeoutId);
      const duration = Date.now() - startTime;

      const data = await response.text();

      return {
        endpoint,
        status: response.status,
        duration,
        success: response.ok,
        response: data.length > 200 ? data.substring(0, 200) + '...' : data,
      };
    } catch (err) {
      const duration = Date.now() - startTime;
      return {
        endpoint,
        status: 'error',
        duration,
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      };
    }
  };

  const runTests = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    const results: APIStatus[] = [];

    try {
      // Test health endpoint
      const healthResult = await testEndpoint('/health', 5000);
      results.push(healthResult);

      // Test root endpoint
      const rootResult = await testEndpoint('/', 5000);
      results.push(rootResult);

      // Test analysis endpoint
      const analysisResult = await testEndpoint('/analysis/', 10000);
      results.push(analysisResult);

      // Test detailed health
      const detailedHealthResult = await testEndpoint(
        '/health/detailed',
        10000
      );
      results.push(detailedHealthResult);

      setApiStatus(results);

      // Parse detailed health if available
      if (detailedHealthResult.success && detailedHealthResult.response) {
        try {
          const healthData = JSON.parse(detailedHealthResult.response);
          setHealthInfo(healthData);
        } catch (e) {
          console.warn('Could not parse health data:', e);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const formatBytes = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDuration = (ms: number) => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const getStatusIcon = (status: APIStatus) => {
    if (status.success) {
      return <CheckCircle className="h-4 w-4 text-green-500" />;
    } else if (status.status === 'error') {
      return <XCircle className="h-4 w-4 text-red-500" />;
    } else {
      return <Clock className="h-4 w-4 text-yellow-500" />;
    }
  };

  const getStatusBadge = (status: APIStatus) => {
    if (status.success) {
      return (
        <Badge variant="default" className="bg-green-500">
          OK
        </Badge>
      );
    } else if (status.status === 'error') {
      return <Badge variant="destructive">Error</Badge>;
    } else {
      return <Badge variant="secondary">Unknown</Badge>;
    }
  };

  useEffect(() => {
    runTests();
  }, [runTests]);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            API Debug Monitor
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2 mb-4">
            <Button
              onClick={runTests}
              disabled={isLoading}
              className="flex items-center gap-2"
            >
              <RefreshCw
                className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`}
              />
              {isLoading ? 'Testing...' : 'Run Tests'}
            </Button>
          </div>

          {error && (
            <Alert className="mb-4">
              <XCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-4">
            {apiStatus.map((status, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(status)}
                    <span className="font-mono text-sm">{status.endpoint}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getStatusBadge(status)}
                    <span className="text-sm text-muted-foreground">
                      {formatDuration(status.duration)}
                    </span>
                  </div>
                </div>

                {status.error && (
                  <div className="text-sm text-red-600 mb-2">
                    Error: {status.error}
                  </div>
                )}

                {status.response && (
                  <details className="text-xs">
                    <summary className="cursor-pointer text-muted-foreground">
                      Response ({status.response.length} chars)
                    </summary>
                    <pre className="mt-2 p-2 bg-muted rounded text-xs overflow-auto max-h-32">
                      {status.response}
                    </pre>
                  </details>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {healthInfo && (
        <Card>
          <CardHeader>
            <CardTitle>System Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold mb-2">Service Info</h4>
                <div className="space-y-1 text-sm">
                  <div>
                    Status: <Badge variant="default">{healthInfo.status}</Badge>
                  </div>
                  <div>Service: {healthInfo.service}</div>
                  <div>Uptime: {healthInfo.uptime_seconds?.toFixed(1)}s</div>
                </div>
              </div>

              {healthInfo.system && (
                <div>
                  <h4 className="font-semibold mb-2">System Resources</h4>
                  <div className="space-y-1 text-sm">
                    <div>CPU: {healthInfo.system.cpu_percent}%</div>
                    <div>Memory: {healthInfo.system.memory.percent}%</div>
                    <div>
                      Available:{' '}
                      {formatBytes(healthInfo.system.memory.available)}
                    </div>
                  </div>
                </div>
              )}

              {healthInfo.process && (
                <div>
                  <h4 className="font-semibold mb-2">Process Info</h4>
                  <div className="space-y-1 text-sm">
                    <div>PID: {healthInfo.process.pid}</div>
                    <div>
                      Memory RSS: {formatBytes(healthInfo.process.memory_rss)}
                    </div>
                    <div>
                      Memory VMS: {formatBytes(healthInfo.process.memory_vms)}
                    </div>
                    <div>CPU: {healthInfo.process.cpu_percent}%</div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
