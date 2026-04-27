# React/ShadCN Migration Guide

## Overview

This guide provides a comprehensive roadmap for migrating the Container Inspection AI from Streamlit to a modern React-based stack using Next.js, shadcn/ui, and TailwindCSS.

---

## 🎯 Target Architecture

### Tech Stack

```
Frontend:
├── Next.js 14 (App Router)
├── React 18
├── TypeScript
├── TailwindCSS
├── shadcn/ui
├── Framer Motion (animations)
├── Lucide React (icons)
├── Recharts (data visualization)
└── TanStack Query (API state management)

Backend:
├── FastAPI (existing - no changes)
└── Python 3.10+

State Management:
├── Zustand (global state)
└── React Context (theme, auth)

Forms & Validation:
├── React Hook Form
└── Zod

Testing:
├── Jest
├── React Testing Library
└── Playwright (E2E)
```

---

## 📁 Proposed Project Structure

```
container-inspection-ai/
├── frontend/
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Home/Dashboard
│   │   ├── detection/
│   │   │   └── page.tsx             # Detection page
│   │   ├── reports/
│   │   │   ├── page.tsx             # Reports list
│   │   │   └── [id]/page.tsx        # Report detail
│   │   ├── analytics/
│   │   │   └── page.tsx             # Analytics dashboard
│   │   └── settings/
│   │       └── page.tsx             # Settings
│   ├── components/
│   │   ├── ui/                      # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── accordion.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── detection/
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── AnnotatedImage.tsx
│   │   │   ├── ScanningAnimation.tsx
│   │   │   └── DetectionResults.tsx
│   │   ├── metrics/
│   │   │   ├── MetricCard.tsx
│   │   │   ├── ConditionBadge.tsx
│   │   │   ├── ConfidenceMeter.tsx
│   │   │   └── StatusIndicator.tsx
│   │   ├── reports/
│   │   │   ├── ReportCard.tsx
│   │   │   ├── DamageTable.tsx
│   │   │   └── DownloadButtons.tsx
│   │   └── analytics/
│   │       ├── DamageChart.tsx
│   │       └── TrendGraph.tsx
│   ├── lib/
│   │   ├── api.ts                   # API client
│   │   ├── utils.ts                 # Utility functions
│   │   └── constants.ts             # Constants
│   ├── hooks/
│   │   ├── useInspection.ts         # Inspection API hook
│   │   ├── useReports.ts            # Reports API hook
│   │   └── useTheme.ts              # Theme hook
│   ├── store/
│   │   └── inspectionStore.ts       # Zustand store
│   ├── types/
│   │   └── index.ts                 # TypeScript types
│   ├── styles/
│   │   └── globals.css              # Global styles
│   ├── public/
│   │   └── assets/
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── tsconfig.json
│   └── package.json
└── backend/                          # Existing FastAPI (unchanged)
```

---

## 🔄 Component Mapping

### Streamlit → React/shadcn

| Streamlit Component | React/shadcn Equivalent | Notes |
|---------------------|-------------------------|-------|
| `st.button()` | `<Button>` from shadcn/ui | Use variants: default, destructive, outline, ghost |
| `st.file_uploader()` | Custom `<FileUploader>` with `react-dropzone` | Drag-and-drop with preview |
| `st.metric()` | Custom `<MetricCard>` | Use Card + custom styling |
| `st.columns()` | Flexbox or Grid | Use Tailwind: `flex gap-4` or `grid grid-cols-3` |
| `st.expander()` | `<Accordion>` from shadcn/ui | Collapsible sections |
| `st.dataframe()` | `<DataTable>` with TanStack Table | Sortable, filterable table |
| `st.progress()` | `<Progress>` from shadcn/ui | Linear progress bar |
| `st.spinner()` | Custom `<LoadingSpinner>` | Use Framer Motion for animation |
| `st.image()` | `<Image>` from Next.js | Optimized image loading |
| `st.download_button()` | `<Button>` with download logic | Use `downloadjs` library |
| `st.success()` | `<Alert>` from shadcn/ui | Use variant="success" |
| `st.error()` | `<Alert>` from shadcn/ui | Use variant="destructive" |
| `st.warning()` | `<Alert>` from shadcn/ui | Use variant="warning" |
| `st.info()` | `<Alert>` from shadcn/ui | Use variant="info" |
| `st.sidebar` | `<Sidebar>` component | Fixed position with animations |

---

## 🎨 Design System Migration

### TailwindCSS Configuration

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Primary Colors
        'primary-teal': '#00C7B7',
        'primary-teal-dark': '#00A89A',
        'primary-teal-light': '#1FFFE8',
        'deep-blue': '#0F172A',
        'slate-dark': '#1E293B',
        'slate-medium': '#334155',
        'slate-light': '#475569',
        
        // Semantic Colors
        'success-green': '#10B981',  
        'warning-amber': '#F59E0B',
        'danger-red': '#EF4444',
        'info-blue': '#3B82F6',
        
        // Detection Colors
        'bbox-damage': '#EF4444',
        'bbox-container-id': '#10B981',
        'bbox-data-plate': '#06B6D4',
        'bbox-location': '#FFD700',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '20px',
      },
      boxShadow: {
        'glow-teal': '0 0 20px rgba(0, 199, 183, 0.4)',
        'glow-teal-strong': '0 0 30px rgba(0, 199, 183, 0.6)',
      },
      animation: {
        'scan-line': 'scanLine 2s infinite',
        'radar-pulse': 'radarPulse 2s infinite',
        'fade-in-up': 'fadeInUp 0.5s ease-out',
      },
      keyframes: {
        scanLine: {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '50%': { opacity: '1' },
          '100%': { transform: 'translateX(100%)', opacity: '0' },
        },
        radarPulse: {
          '0%': { transform: 'scale(1)', opacity: '0.8' },
          '100%': { transform: 'scale(1.5)', opacity: '0' },
        },
        fadeInUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
```

---

## 🔧 Key Component Examples

### 1. File Uploader Component

```typescript
// components/detection/ImageUploader.tsx
'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface ImageUploaderProps {
  onUpload: (file: File) => void
  isLoading?: boolean
}

export function ImageUploader({ onUpload, isLoading }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setPreview(URL.createObjectURL(file))
      onUpload(file)
    }
  }, [onUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png'] },
    maxFiles: 1,
    disabled: isLoading,
  })

  const clearPreview = () => {
    setPreview(null)
  }

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all",
          "hover:border-primary-teal hover:bg-primary-teal/5",
          isDragActive && "border-primary-teal-light bg-primary-teal/10 shadow-glow-teal",
          isLoading && "opacity-50 cursor-not-allowed",
          "border-slate-light bg-slate-medium"
        )}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 mx-auto mb-4 text-primary-teal" />
        <p className="text-lg font-medium text-gray-200">
          {isDragActive ? 'Drop the image here' : 'Drag & drop or click to upload'}
        </p>
        <p className="text-sm text-gray-400 mt-2">
          Supported formats: JPG, PNG, JPEG (Max 10MB)
        </p>
      </div>

      {preview && (
        <div className="relative rounded-lg overflow-hidden border border-slate-light">
          <img src={preview} alt="Preview" className="w-full h-auto" />
          <Button
            size="icon"
            variant="destructive"
            className="absolute top-2 right-2"
            onClick={clearPreview}
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      )}
    </div>
  )
}
```

### 2. Metric Card Component

```typescript
// components/metrics/MetricCard.tsx
import { LucideIcon } from 'lucide-react'
import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface MetricCardProps {
  label: string
  value: string | number
  icon?: LucideIcon
  color?: 'teal' | 'green' | 'amber' | 'red' | 'blue'
  trend?: {
    value: number
    isPositive: boolean
  }
  className?: string
}

const colorClasses = {
  teal: 'text-primary-teal border-primary-teal',
  green: 'text-success-green border-success-green',
  amber: 'text-warning-amber border-warning-amber',
  red: 'text-danger-red border-danger-red',
  blue: 'text-info-blue border-info-blue',
}

export function MetricCard({
  label,
  value,
  icon: Icon,
  color = 'teal',
  trend,
  className,
}: MetricCardProps) {
  return (
    <Card
      className={cn(
        "p-6 bg-gradient-to-br from-slate-medium to-slate-dark",
        "border transition-all duration-300 hover:scale-105 hover:shadow-xl",
        colorClasses[color],
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-xs uppercase tracking-wider text-gray-400">
            {label}
          </p>
          <p className={cn("text-3xl font-bold", colorClasses[color])}>
            {value}
          </p>
          {trend && (
            <p className={cn(
              "text-sm font-medium",
              trend.isPositive ? "text-success-green" : "text-danger-red"
            )}>
              {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
            </p>
          )}
        </div>
        {Icon && (
          <Icon className={cn("w-8 h-8", colorClasses[color])} />
        )}
      </div>
    </Card>
  )
}
```

### 3. Scanning Animation Component

```typescript
// components/detection/ScanningAnimation.tsx
'use client'

import { motion } from 'framer-motion'
import { Radar } from 'lucide-react'

interface ScanningAnimationProps {
  message?: string
}

export function ScanningAnimation({ message = 'AI Scanning in Progress...' }: ScanningAnimationProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-primary-teal/5 border border-primary-teal rounded-xl">
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 360],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      >
        <Radar className="w-16 h-16 text-primary-teal" />
      </motion.div>
      
      <h3 className="text-xl font-semibold text-primary-teal mt-4">
        {message}
      </h3>
      
      <p className="text-gray-400 text-sm mt-2">
        Analyzing container with GPT-5 Vision
      </p>
      
      <div className="w-full h-1 bg-slate-dark rounded-full mt-6 overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-primary-teal to-primary-teal-light"
          animate={{
            x: ['-100%', '100%'],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      </div>
    </div>
  )
}
```

### 4. API Hook Example

```typescript
// hooks/useInspection.ts
import { useMutation } from '@tanstack/react-query'
import { inspectContainer } from '@/lib/api'
import type { InspectionReport } from '@/types'

export function useInspection() {
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      return inspectContainer(formData)
    },
    onSuccess: (data: InspectionReport) => {
      console.log('Inspection complete:', data)
    },
    onError: (error) => {
      console.error('Inspection failed:', error)
    },
  })
}
```

### 5. API Client

```typescript
// lib/api.ts
import axios from 'axios'
import type { InspectionReport } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function inspectContainer(formData: FormData): Promise<InspectionReport> {
  const { data } = await apiClient.post('/inspect', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return data
}

export async function getReport(reportId: string): Promise<InspectionReport> {
  const { data } = await apiClient.get(`/report/${reportId}`)
  return data
}

export async function downloadReport(reportId: string, format: 'pdf' | 'excel' | 'json') {
  const { data } = await apiClient.get(`/download/${reportId}/${format}`, {
    responseType: 'blob',
  })
  return data
}
```

---

## 🚀 Migration Steps

### Phase 1: Setup (Week 1)

1. **Initialize Next.js Project**
   ```bash
   npx create-next-app@latest container-inspection-ai --typescript --tailwind --app
   cd container-inspection-ai
   ```

2. **Install Dependencies**
   ```bash
   npm install @tanstack/react-query zustand framer-motion lucide-react
   npm install react-dropzone recharts downloadjs
   npm install -D @types/node
   ```

3. **Setup shadcn/ui**
   ```bash
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add button card alert accordion progress dialog
   ```

4. **Configure Tailwind** (use config from above)

### Phase 2: Core Components (Week 2)

1. Create layout components (Navbar, Sidebar, Footer)
2. Build UI components (Button, Card, etc. via shadcn)
3. Implement file uploader
4. Create metric cards and status indicators

### Phase 3: Detection Flow (Week 3)

1. Build detection page
2. Implement image upload and preview
3. Add scanning animation
4. Create results display
5. Integrate with FastAPI backend

### Phase 4: Reports & Analytics (Week 4)

1. Build reports list page
2. Create report detail view
3. Implement damage table
4. Add download functionality
5. Build analytics dashboard with charts

### Phase 5: Polish & Testing (Week 5)

1. Add animations with Framer Motion
2. Implement error handling
3. Add loading states
4. Write unit tests
5. E2E testing with Playwright
6. Performance optimization

### Phase 6: Deployment (Week 6)

1. Setup environment variables
2. Configure production build
3. Deploy frontend (Vercel/Netlify)
4. Ensure backend connectivity
5. Setup monitoring and analytics

---

## 📊 Advantages of React Migration

### Performance
- **Faster Initial Load**: Code splitting and lazy loading
- **Better Caching**: Service workers and static generation
- **Optimized Images**: Next.js Image component
- **Reduced Bundle Size**: Tree shaking and minification

### Developer Experience
- **Type Safety**: Full TypeScript support
- **Better Tooling**: ESLint, Prettier, VS Code integration
- **Component Reusability**: Modular architecture
- **Hot Module Replacement**: Instant feedback during development

### User Experience
- **Smoother Animations**: Framer Motion for 60fps animations
- **Better Responsiveness**: Optimistic UI updates
- **Offline Support**: Progressive Web App capabilities
- **SEO Friendly**: Server-side rendering

### Scalability
- **Easier Testing**: Component-level testing
- **Better State Management**: Zustand/Redux
- **API Abstraction**: TanStack Query for caching
- **Modular Architecture**: Easy to add features

---

## 🔐 Security Considerations

1. **API Authentication**: Implement JWT tokens
2. **File Upload Validation**: Client and server-side
3. **CORS Configuration**: Proper origin whitelisting
4. **Environment Variables**: Never expose secrets
5. **Content Security Policy**: Prevent XSS attacks
6. **Rate Limiting**: Protect API endpoints

---

## 📈 Performance Targets

- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Lighthouse Score**: > 90
- **Bundle Size**: < 200KB (gzipped)
- **API Response Time**: < 500ms (excluding AI processing)

---

## 🧪 Testing Strategy

### Unit Tests
```typescript
// __tests__/components/MetricCard.test.tsx
import { render, screen } from '@testing-library/react'
import { MetricCard } from '@/components/metrics/MetricCard'

describe('MetricCard', () => {
  it('renders metric value correctly', () => {
    render(<MetricCard label="Confidence" value="95%" />)
    expect(screen.getByText('95%')).toBeInTheDocument()
  })
})
```

### E2E Tests
```typescript
// e2e/inspection.spec.ts
import { test, expect } from '@playwright/test'

test('complete inspection flow', async ({ page }) => {
  await page.goto('/')
  await page.setInputFiles('input[type="file"]', 'test-container.jpg')
  await page.click('button:has-text("Run AI Inspection")')
  await expect(page.locator('text=Analysis Complete')).toBeVisible()
})
```

---

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [TailwindCSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion)
- [TanStack Query](https://tanstack.com/query)
- [React Hook Form](https://react-hook-form.com)

---

## 🎯 Success Metrics

- [ ] All Streamlit features replicated
- [ ] Performance improvements (2x faster load time)
- [ ] Better mobile responsiveness
- [ ] Improved accessibility (WCAG AA)
- [ ] 90+ Lighthouse score
- [ ] Zero critical bugs in production
- [ ] Positive user feedback

---

## 💡 Future Enhancements

1. **Real-time Collaboration**: Multiple users viewing same inspection
2. **Historical Analytics**: Trend analysis over time
3. **Mobile App**: React Native version
4. **Batch Processing**: Upload multiple containers
5. **AI Model Comparison**: A/B testing different models
6. **Custom Dashboards**: User-configurable views
7. **Export Templates**: Customizable report formats
8. **Integration APIs**: Webhooks for external systems

---

## 🤝 Conclusion

Migrating to React/Next.js will provide:
- ✅ Better performance and user experience
- ✅ Improved developer productivity
- ✅ Enhanced scalability and maintainability
- ✅ Modern, future-proof architecture
- ✅ Superior animation and interaction capabilities

The migration is estimated to take **6 weeks** with a team of 2-3 developers.

**Recommended Timeline**: Start after current Streamlit version is stable and has been validated by users.
