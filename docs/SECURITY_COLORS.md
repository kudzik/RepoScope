# 🎨 System kolorów dla bezpieczeństwa RepoScope

## 📋 Przegląd

System kolorów dla poziomów bezpieczeństwa w RepoScope został zaimplementowany zgodnie z najlepszymi praktykami UX/UI, zapewniając intuicyjne rozpoznawanie priorytetów problemów bezpieczeństwa.

## 🎯 Poziomy bezpieczeństwa i kolory

### 🔴 High (Wysoki) - Czerwony

- **Kolor tła**: `bg-red-50 dark:bg-red-900/20`
- **Kolor tekstu**: `text-red-800 dark:text-red-200`
- **Kolor ramki**: `border-red-200 dark:border-red-800`
- **Badge**: `bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800`

### 🟠 Medium (Średni) - Pomarańczowy

- **Kolor tła**: `bg-orange-50 dark:bg-orange-900/20`
- **Kolor tekstu**: `text-orange-800 dark:text-orange-200`
- **Kolor ramki**: `border-orange-200 dark:border-orange-800`
- **Badge**: `bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-200 dark:border-orange-800`

### 🟡 Low (Niski) - Żółty

- **Kolor tła**: `bg-yellow-50 dark:bg-yellow-900/20`
- **Kolor tekstu**: `text-yellow-800 dark:text-yellow-200`
- **Kolor ramki**: `border-yellow-200 dark:border-yellow-800`
- **Badge**: `bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-200 dark:border-yellow-800`

### ⚪ Issues (Ogólne) - Biały/Szary

- **Kolor tła**: `bg-gray-50 dark:bg-gray-900/20`
- **Kolor tekstu**: `text-gray-800 dark:text-gray-200`
- **Kolor ramki**: `border-gray-200 dark:border-gray-800`
- **Badge**: `bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-900/30 dark:text-gray-200 dark:border-gray-800`

## 🛠️ Implementacja

### Funkcja `getSeverityColor`

```typescript
export function getSeverityColor(severity: string) {
  const normalizedSeverity = severity?.toLowerCase() || "issues";

  switch (normalizedSeverity) {
    case "high":
      return {
        bg: "bg-red-50 dark:bg-red-900/20",
        text: "text-red-800 dark:text-red-200",
        border: "border-red-200 dark:border-red-800",
        badge:
          "bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-200 dark:border-red-800",
      };
    // ... inne poziomy
  }
}
```

### Użycie w komponentach

```tsx
// W analysis-results.tsx
const severityColors = getSeverityColor(vuln?.severity || "issues");
<div className={`text-sm p-2 ${severityColors.bg} ${severityColors.border} border rounded`}>
  <span className={`font-medium ${severityColors.text}`}>{vuln?.type || "Unknown"}</span>
  <Badge className={severityColors.badge}>{vuln?.severity || "Unknown"}</Badge>
</div>;

// W analysis-list.tsx
const severityColors = getSeverityColor(vuln.severity);
<span className={`px-2 py-1 rounded text-xs font-medium ${severityColors.badge}`}>
  {vuln.severity}
</span>;
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
