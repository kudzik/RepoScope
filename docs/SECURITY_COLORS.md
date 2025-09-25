# 🎨 System kolorów dla bezpieczeństwa RepoScope

## 📋 Przegląd

System kolorów dla poziomów bezpieczeństwa w RepoScope został zaimplementowany zgodnie z najlepszymi praktykami UX/UI, zapewniając intuicyjne rozpoznawanie priorytetów problemów bezpieczeństwa.

## 🎯 Poziomy bezpieczeństwa i kolory

### 🔴 Critical (Krytyczne) - Czerwony

- **Kolor tła**: `bg-red-100 dark:bg-red-900/40`
- **Kolor tekstu**: `text-red-900 dark:text-red-100`
- **Kolor ramki**: `border-red-300 dark:border-red-700`
- **Badge**: `bg-red-200 text-red-900 border-red-300 dark:bg-red-800/50 dark:text-red-100 dark:border-red-600`
- **Tytuł**: 🔴 Critical
- **Opis**: Immediate attention required - high security risk

### 🔴 High (Wysokie) - Czerwony

- **Kolor tła**: `bg-red-50 dark:bg-red-900/20`
- **Kolor tekstu**: `text-red-800 dark:text-red-200`
- **Kolor ramki**: `border-red-200 dark:border-red-800`
- **Badge**: `bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800`
- **Tytuł**: 🔴 High
- **Opis**: Requires attention soon - significant risk

### 🟠 Medium (Średnie) - Pomarańczowy

- **Kolor tła**: `bg-orange-50 dark:bg-orange-900/20`
- **Kolor tekstu**: `text-orange-800 dark:text-orange-200`
- **Kolor ramki**: `border-orange-200 dark:border-orange-800`
- **Badge**: `bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-200 dark:border-orange-800`
- **Tytuł**: 🟠 Medium
- **Opis**: Attention needed soon - moderate risk

### 🟡 Low (Niskie) - Żółty

- **Kolor tła**: `bg-yellow-50 dark:bg-yellow-900/20`
- **Kolor tekstu**: `text-yellow-800 dark:text-yellow-200`
- **Kolor ramki**: `border-yellow-200 dark:border-yellow-800`
- **Badge**: `bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-800`
- **Tytuł**: 🟡 Low
- **Opis**: Low priority, but requires attention - minimal risk

### 🟢 Safe (Bezpieczne) - Zielony

- **Kolor tła**: `bg-green-50 dark:bg-green-900/20`
- **Kolor tekstu**: `text-green-800 dark:text-green-200`
- **Kolor ramki**: `border-green-200 dark:border-green-800`
- **Badge**: `bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800`
- **Tytuł**: 🟢 Safe
- **Opis**: No security issues - everything is fine

### ⚪ Issues (Ogólne) - Szary

- **Kolor tła**: `bg-gray-50 dark:bg-gray-900/20`
- **Kolor tekstu**: `text-gray-800 dark:text-gray-200`
- **Kolor ramki**: `border-gray-200 dark:border-gray-800`
- **Badge**: `bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-900/30 dark:text-gray-200 dark:border-gray-800`
- **Tytuł**: ⚪ General
- **Opis**: Informational, no urgency - standard information

## 🛠️ Implementacja

### Funkcje kolorów

#### `getSeverityColor` - Poziomy bezpieczeństwa

```typescript
export function getSeverityColor(severity: string) {
  const normalizedSeverity = severity?.toLowerCase() || "issues";

  switch (normalizedSeverity) {
    case "critical":
      return {
        bg: "bg-red-100 dark:bg-red-900/40",
        text: "text-red-900 dark:text-red-100",
        border: "border-red-300 dark:border-red-700",
        badge:
          "bg-red-200 text-red-900 border-red-300 dark:bg-red-800/50 dark:text-red-100 dark:border-red-600",
        icon: "text-red-600 dark:text-red-400",
        title: "🔴 Krytyczne",
        description: "Natychmiastowa uwaga wymagana - wysokie ryzyko bezpieczeństwa",
      };
    case "high":
      return {
        bg: "bg-red-50 dark:bg-red-900/20",
        text: "text-red-800 dark:text-red-200",
        border: "border-red-200 dark:border-red-800",
        badge:
          "bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800",
        icon: "text-red-500 dark:text-red-400",
        title: "🔴 Wysokie",
        description: "Wymaga uwagi w najbliższym czasie - znaczące ryzyko",
      };
    // ... inne poziomy
  }
}
```

#### `getQualityColor` - Poziomy jakości kodu

```typescript
export function getQualityColor(quality: string) {
  const normalizedQuality = quality?.toLowerCase() || "fair";

  switch (normalizedQuality) {
    case "excellent":
      return {
        bg: "bg-green-50 dark:bg-green-900/20",
        text: "text-green-800 dark:text-green-200",
        border: "border-green-200 dark:border-green-800",
        badge:
          "bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800",
        icon: "text-green-500 dark:text-green-400",
        title: "🟢 Doskonała",
        description: "Najwyższa jakość kodu - wzorowa implementacja",
      };
    // ... inne poziomy
  }
}
```

#### `getCoverageColor` - Poziomy pokrycia testów

```typescript
export function getCoverageColor(coverage: string) {
  const normalizedCoverage = coverage?.toLowerCase() || "fair";

  switch (normalizedCoverage) {
    case "excellent":
      return {
        bg: "bg-green-50 dark:bg-green-900/20",
        text: "text-green-800 dark:text-green-200",
        border: "border-green-200 dark:border-green-800",
        badge:
          "bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800",
        icon: "text-green-500 dark:text-green-400",
        title: "🟢 Doskonałe",
        description: "Pokrycie >90% - wzorowe testowanie",
      };
    // ... inne poziomy
  }
}
```

#### `getDocumentationColor` - Poziomy dokumentacji

```typescript
export function getDocumentationColor(documentation: string) {
  const normalizedDoc = documentation?.toLowerCase() || "fair";

  switch (normalizedDoc) {
    case "excellent":
      return {
        bg: "bg-green-50 dark:bg-green-900/20",
        text: "text-green-800 dark:text-green-200",
        border: "border-green-200 dark:border-green-800",
        badge:
          "bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-200 dark:border-green-800",
        icon: "text-green-500 dark:text-green-400",
        title: "🟢 Doskonała",
        description: "Wzorowa dokumentacja - kompletna i aktualna",
      };
    // ... inne poziomy
  }
}
```

#### Funkcje pomocnicze

```typescript
// Mapuje wynik liczbowy na poziom jakości
export function getScoreLevel(
  score: number,
  type: "security" | "quality" | "coverage" | "documentation" = "quality"
): string {
  if (score >= 90) return "excellent";
  if (score >= 80) return "good";
  if (score >= 60) return "fair";
  if (score >= 40) return "poor";
  return "critical";
}

// Mapuje wynik liczbowy na kolor dla progress bar
export function getScoreColor(score: number): string {
  if (score >= 80) return "text-green-600 dark:text-green-400";
  if (score >= 60) return "text-yellow-600 dark:text-yellow-400";
  if (score >= 40) return "text-orange-600 dark:text-orange-400";
  return "text-red-600 dark:text-red-400";
}

// Mapuje wynik liczbowy na kolor tła dla progress bar
export function getScoreBgColor(score: number): string {
  if (score >= 80) return "bg-green-500";
  if (score >= 60) return "bg-yellow-500";
  if (score >= 40) return "bg-orange-500";
  return "bg-red-500";
}
```

### Użycie w komponentach

#### Analysis Results - Pełne karty z poziomami jakości

```tsx
// W analysis-results.tsx - Code Quality
{
  (() => {
    const qualityLevel = getScoreLevel(safeNumber(result.code_quality?.score, 0), "quality");
    const qualityColors = getQualityColor(qualityLevel);
    return (
      <div className={`text-xs p-2 rounded ${qualityColors.bg} ${qualityColors.border} border`}>
        <div className="flex items-center gap-2">
          <span className={`font-medium ${qualityColors.text}`}>{qualityColors.title}</span>
          <Badge className={qualityColors.badge}>{qualityLevel}</Badge>
        </div>
        <p className={`text-xs mt-1 ${qualityColors.text}`}>{qualityColors.description}</p>
      </div>
    );
  })();
}

// Security
{
  (() => {
    const securityLevel = getScoreLevel(safeNumber(result.security?.score, 0), "security");
    const securityColors = getSeverityColor(securityLevel);
    return (
      <div className={`text-xs p-2 rounded ${securityColors.bg} ${securityColors.border} border`}>
        <div className="flex items-center gap-2">
          <span className={`font-medium ${securityColors.text}`}>{securityColors.title}</span>
          <Badge className={securityColors.badge}>{securityLevel}</Badge>
        </div>
        <p className={`text-xs mt-1 ${securityColors.text}`}>{securityColors.description}</p>
      </div>
    );
  })();
}

// Test Coverage
{
  (() => {
    const coverageLevel = getScoreLevel(
      safeNumber(result.test_coverage?.coverage_percentage, 0),
      "coverage"
    );
    const coverageColors = getCoverageColor(coverageLevel);
    return (
      <div className={`text-xs p-2 rounded ${coverageColors.bg} ${coverageColors.border} border`}>
        <div className="flex items-center gap-2">
          <span className={`font-medium ${coverageColors.text}`}>{coverageColors.title}</span>
          <Badge className={coverageColors.badge}>{coverageLevel}</Badge>
        </div>
        <p className={`text-xs mt-1 ${coverageColors.text}`}>{coverageColors.description}</p>
      </div>
    );
  })();
}

// Documentation
{
  (() => {
    const docLevel = getScoreLevel(safeNumber(result.documentation?.score, 0), "documentation");
    const docColors = getDocumentationColor(docLevel);
    return (
      <div className={`text-xs p-2 rounded ${docColors.bg} ${docColors.border} border`}>
        <div className="flex items-center gap-2">
          <span className={`font-medium ${docColors.text}`}>{docColors.title}</span>
          <Badge className={docColors.badge}>{docLevel}</Badge>
        </div>
        <p className={`text-xs mt-1 ${docColors.text}`}>{docColors.description}</p>
      </div>
    );
  })();
}
```

#### Analysis List - Kompaktowe wyświetlanie

```tsx
// W analysis-list.tsx - Security vulnerabilities
{
  analysis.result.security.vulnerabilities
    .slice(0, 3)
    .map((vuln: { type: string; severity: string }, index: number) => {
      const severityColors = getSeverityColor(vuln.severity);
      return (
        <div key={index} className="flex items-center gap-2 text-xs">
          <span className={`px-2 py-1 rounded text-xs font-medium ${severityColors.badge}`}>
            {vuln.severity}
          </span>
          <span className="text-muted-foreground">{vuln.type}</span>
        </div>
      );
    });
}
```

#### Progress Bars z kolorami

```tsx
// Progress bars z dynamicznymi kolorami
<Progress
  value={safeNumber(result.code_quality?.score, 0)}
  className="h-2"
  style={{
    '--progress-background': getScoreBgColor(safeNumber(result.code_quality?.score, 0))
  } as React.CSSProperties}
/>

// Score colors
<span className={`text-sm ${getScoreColor(safeNumber(result.code_quality?.score, 0))}`}>
  /100
</span>
```

## 🎨 Zasady projektowe

### Dostępność (Accessibility)

- Wszystkie kolory spełniają standardy kontrastu WCAG 2.1 AA
- Obsługa trybu ciemnego z odpowiednimi kolorami
- Intuicyjne rozpoznawanie priorytetów przez użytkowników

### Spójność wizualna

- Jednolite zastosowanie kolorów w całej aplikacji
- Zgodność z systemem designu Tailwind CSS
- Responsywne zachowanie na różnych urządzeniach

### Semantyka kolorów

- **Czerwony**: Natychmiastowa uwaga wymagana
- **Pomarańczowy**: Uwaga w najbliższym czasie
- **Żółty**: Niska priorytet, ale wymaga uwagi
- **Szary**: Informacyjny, bez pilności

## 📱 Obsługa trybu ciemnego

Wszystkie kolory zostały zaprojektowane z myślą o trybie ciemnym:

- Automatyczne przełączanie między jasnym a ciemnym motywem
- Zachowanie czytelności w obu trybach
- Spójne doświadczenie użytkownika

## 🔄 Rozszerzalność

System jest łatwo rozszerzalny o nowe poziomy bezpieczeństwa:

```typescript
case 'critical':
  return {
    bg: 'bg-red-100 dark:bg-red-900/40',
    text: 'text-red-900 dark:text-red-100',
    border: 'border-red-300 dark:border-red-700',
    badge: 'bg-red-200 text-red-900 border-red-300 dark:bg-red-800/50 dark:text-red-100 dark:border-red-600',
  };
```

## ✅ Testowanie

System kolorów został przetestowany pod kątem:

- ✅ Kompilacji TypeScript
- ✅ Lintingu ESLint/Prettier
- ✅ Buildu produkcyjnego Next.js
- ✅ Responsywności na różnych urządzeniach
- ✅ Dostępności w trybie jasnym i ciemnym

## 📝 Changelog

### v1.0.0 (2024-01-XX)

- ✅ Dodano funkcję `getSeverityColor` do `utils.ts`
- ✅ Zaktualizowano `analysis-results.tsx` z kolorami bezpieczeństwa
- ✅ Zaktualizowano `analysis-list.tsx` z kolorami bezpieczeństwa
- ✅ Dodano obsługę trybu ciemnego
- ✅ Zapewniono zgodność z WCAG 2.1 AA
- ✅ Przetestowano build produkcyjny
