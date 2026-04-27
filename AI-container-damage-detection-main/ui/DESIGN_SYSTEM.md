# Container Inspection AI - Design System

## 🎨 Visual Identity

### Brand Positioning
Enterprise-grade AI logistics platform with industrial sophistication and cutting-edge technology aesthetics.

---

## Color Palette

### Primary Colors
```css
--primary-teal: #00C7B7        /* Main accent, CTAs, highlights */
--primary-teal-dark: #00A89A   /* Hover states */
--primary-teal-light: #1FFFE8  /* Glow effects */

--deep-blue: #0F172A           /* Primary background */
--slate-dark: #1E293B          /* Secondary background */
--slate-medium: #334155        /* Card backgrounds */
--slate-light: #475569         /* Borders, dividers */
```

### Semantic Colors
```css
--success-green: #10B981       /* Healthy condition, success states */
--warning-amber: #F59E0B       /* Moderate damage, warnings */
--danger-red: #EF4444          /* Severe damage, critical alerts */
--info-blue: #3B82F6           /* Information, metadata */

--text-primary: #F8FAFC        /* Main text */
--text-secondary: #CBD5E1      /* Secondary text */
--text-muted: #94A3B8          /* Muted text, labels */
```

### Detection Colors (Bounding Boxes)
```css
--bbox-damage: #EF4444         /* Red - Damage detection */
--bbox-container-id: #10B981   /* Green - Container ID */
--bbox-data-plate: #06B6D4     /* Cyan - Data plate */
--bbox-location: #FFD700       /* Yellow - Location codes */
```

---

## Typography

### Font Families
```css
Primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
Monospace: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace
```

### Type Scale
```css
--text-xs: 0.75rem (12px)      /* Labels, captions */
--text-sm: 0.875rem (14px)     /* Body small, metadata */
--text-base: 1rem (16px)       /* Body text */
--text-lg: 1.125rem (18px)     /* Subheadings */
--text-xl: 1.25rem (20px)      /* Card titles */
--text-2xl: 1.5rem (24px)      /* Section headers */
--text-3xl: 1.875rem (30px)    /* Page titles */
--text-4xl: 2.25rem (36px)     /* Hero text */
```

### Font Weights
```css
--font-normal: 400
--font-medium: 500
--font-semibold: 600
--font-bold: 700
```

---

## Spacing System

```css
--space-1: 0.25rem (4px)
--space-2: 0.5rem (8px)
--space-3: 0.75rem (12px)
--space-4: 1rem (16px)
--space-5: 1.25rem (20px)
--space-6: 1.5rem (24px)
--space-8: 2rem (32px)
--space-10: 2.5rem (40px)
--space-12: 3rem (48px)
--space-16: 4rem (64px)
```

---

## Border Radius

```css
--radius-sm: 8px               /* Small elements, badges */
--radius-md: 12px              /* Buttons, inputs */
--radius-lg: 16px              /* Cards, containers */
--radius-xl: 20px              /* Large cards, modals */
--radius-full: 9999px          /* Pills, avatars */
```

---

## Shadows & Elevation

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3)
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4)
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5)
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6)

--glow-teal: 0 0 20px rgba(0, 199, 183, 0.4)
--glow-teal-strong: 0 0 30px rgba(0, 199, 183, 0.6)
```

---

## UI Components

### 1. Navigation Bar
- **Height**: 64px
- **Background**: Deep blue with subtle gradient
- **Logo**: Left-aligned, 40px height
- **Elements**: Status indicator, user profile (right)
- **Border**: 1px bottom border with teal accent

### 2. Sidebar
- **Width**: 280px (collapsed: 64px)
- **Background**: Slate dark
- **Items**: Icon + label, hover state with teal accent
- **Active state**: Teal left border + background highlight

### 3. Cards
- **Background**: Slate medium with subtle gradient
- **Border**: 1px solid slate light
- **Radius**: 16px
- **Padding**: 24px
- **Hover**: Lift effect (translateY -2px) + shadow increase

### 4. Buttons

#### Primary (CTA)
- Background: Teal gradient
- Text: White, semibold
- Radius: 12px
- Padding: 12px 24px
- Hover: Glow effect + slight scale

#### Secondary
- Background: Transparent
- Border: 1px teal
- Text: Teal
- Hover: Teal background (10% opacity)

#### Danger
- Background: Danger red
- Text: White
- Hover: Darker red

### 5. Upload Zone
- **Style**: Dashed border (2px), teal color
- **State - Default**: Subtle pulse animation
- **State - Hover**: Solid border, background teal (5% opacity)
- **State - Drag**: Strong glow, background teal (10% opacity)
- **Icon**: Upload cloud, 48px, animated on hover

### 6. Progress Indicators

#### Scanning Animation
- Horizontal sweep with teal gradient
- Radar pulse effect
- Percentage counter with smooth counting animation

#### Confidence Meter
- Circular progress ring
- Color: Green (>80%), Amber (50-80%), Red (<50%)
- Animated fill on load

### 7. Condition Badge
- **Excellent**: Green background, dark green text
- **Good**: Light green background
- **Fair**: Amber background
- **Poor**: Orange background
- **Critical**: Red background
- **Radius**: Full (pill shape)
- **Padding**: 6px 16px

### 8. Data Display

#### Metrics Card
- Large number (text-3xl, bold)
- Label below (text-sm, muted)
- Icon (top-right, teal)
- Background: Gradient overlay

#### Table
- Header: Slate dark, text uppercase, text-xs
- Rows: Alternating background (subtle)
- Hover: Teal highlight (5% opacity)
- Border: None (use spacing)

---

## Animations & Transitions

### Timing Functions
```css
--ease-smooth: cubic-bezier(0.4, 0.0, 0.2, 1)
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55)
--ease-in-out: cubic-bezier(0.4, 0.0, 0.6, 1)
```

### Durations
```css
--duration-fast: 150ms
--duration-normal: 300ms
--duration-slow: 500ms
```

### Key Animations

#### 1. Scan Line (AI Processing)
```css
@keyframes scanLine {
  0% { transform: translateX(-100%); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateX(100%); opacity: 0; }
}
Duration: 2s, infinite
```

#### 2. Radar Pulse
```css
@keyframes radarPulse {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}
Duration: 2s, infinite
```

#### 3. Fade In Up
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
Duration: 500ms
```

#### 4. Success Checkmark
```css
@keyframes checkmark {
  0% { stroke-dashoffset: 100; }
  100% { stroke-dashoffset: 0; }
}
Duration: 600ms
```

#### 5. Number Counter
Smooth counting animation using JavaScript
Duration: 1000ms with easeOutExpo

---

## Micro-interactions

### Hover States
- **Cards**: Lift 2px, increase shadow
- **Buttons**: Scale 1.02, add glow
- **Icons**: Rotate 5deg or scale 1.1
- **Links**: Underline slide-in from left

### Click/Active States
- **Buttons**: Scale 0.98, reduce shadow
- **Cards**: Brief flash of teal border
- **Checkboxes**: Bounce animation

### Loading States
- **Skeleton**: Shimmer effect (gradient sweep)
- **Spinner**: Rotating teal ring
- **Progress**: Smooth width transition

---

## Layout Patterns

### Dashboard Grid
```
┌─────────────────────────────────────────┐
│  Navigation Bar (64px)                  │
├──────┬──────────────────────────────────┤
│      │  Main Content Area               │
│ Side │  ┌────────────┬────────────┐     │
│ bar  │  │  Card 1    │  Card 2    │     │
│ 280  │  └────────────┴────────────┘     │
│ px   │  ┌──────────────────────────┐    │
│      │  │  Detection Area          │    │
│      │  └──────────────────────────┘    │
└──────┴──────────────────────────────────┘
```

### Detection View (2-Column)
```
┌─────────────────────┬──────────────┐
│                     │  Metrics     │
│  Annotated Image    │  ┌────────┐  │
│  (Large)            │  │ Metric │  │
│                     │  └────────┘  │
│                     │  Downloads   │
│                     │  Legend      │
└─────────────────────┴──────────────┘
```

---

## Iconography

### Icon Library
**Lucide Icons** (consistent, modern, 24px default)

### Key Icons
- **Upload**: Upload Cloud
- **Scan**: Radar / Scan Line
- **Damage**: Alert Triangle
- **Success**: Check Circle
- **Download**: Download
- **Report**: File Text
- **Analytics**: Bar Chart
- **Settings**: Settings
- **Container**: Package
- **Location**: Map Pin

### Icon Usage
- Always pair with text labels
- Use consistent sizing (16px, 20px, 24px)
- Apply teal color for active/primary actions
- Muted color for secondary actions

---

## Accessibility

### Contrast Ratios
- Text on background: Minimum 7:1 (AAA)
- Interactive elements: Minimum 4.5:1 (AA)
- Teal on dark: 4.8:1 ✓

### Focus States
- 2px solid teal outline
- 4px offset for visibility
- Never remove focus indicators

### Keyboard Navigation
- Logical tab order
- Skip links for main content
- Escape to close modals

### Screen Readers
- Semantic HTML elements
- ARIA labels for icons
- Status announcements for dynamic content

---

## Responsive Breakpoints

```css
--mobile: 640px
--tablet: 768px
--desktop: 1024px
--wide: 1280px
--ultrawide: 1536px
```

### Mobile Adaptations
- Sidebar collapses to hamburger menu
- 2-column layouts become single column
- Reduce padding and font sizes
- Touch-friendly targets (min 44px)

---

## Motion Design Principles

1. **Purposeful**: Every animation serves a function
2. **Subtle**: Don't distract from content
3. **Fast**: Keep under 500ms for UI feedback
4. **Consistent**: Same timing and easing throughout
5. **Respectful**: Honor prefers-reduced-motion

---

## Component States

### Interactive Elements
1. **Default**: Base styling
2. **Hover**: Visual feedback (scale, glow, color shift)
3. **Active/Pressed**: Depressed appearance
4. **Focus**: Clear outline for keyboard users
5. **Disabled**: Reduced opacity (0.5), no pointer events
6. **Loading**: Spinner or skeleton

### Data States
1. **Empty**: Placeholder with helpful message
2. **Loading**: Skeleton or spinner
3. **Error**: Red accent, error icon, retry action
4. **Success**: Green accent, checkmark, confirmation
5. **Partial**: Warning state with amber accent

---

## Best Practices

### Performance
- Use CSS transforms over position changes
- Leverage GPU acceleration (transform, opacity)
- Lazy load images and heavy components
- Debounce expensive operations

### Consistency
- Use design tokens (CSS variables)
- Follow established patterns
- Maintain visual hierarchy
- Keep spacing rhythm consistent

### User Experience
- Provide immediate feedback
- Show progress for long operations
- Use optimistic UI updates
- Clear error messages with recovery actions

---

## Migration to React/ShadCN

### Component Mapping

| Streamlit | React/ShadCN |
|-----------|--------------|
| st.button | `<Button>` from shadcn/ui |
| st.metric | Custom `<MetricCard>` component |
| st.file_uploader | `<FileUpload>` with dropzone |
| st.columns | Flexbox or Grid layout |
| st.expander | `<Accordion>` from shadcn/ui |
| st.dataframe | `<DataTable>` with TanStack Table |
| st.progress | `<Progress>` from shadcn/ui |

### Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Styling**: TailwindCSS + CSS Variables
- **Components**: shadcn/ui
- **Icons**: Lucide React
- **Charts**: Recharts or Chart.js
- **State**: Zustand or React Context
- **Forms**: React Hook Form + Zod
- **API**: TanStack Query (React Query)

### Advantages
- Better performance and SEO
- More control over animations
- Easier state management
- Superior developer experience
- Production-ready components
- Type safety with TypeScript

---

## Design Inspiration Sources

1. **Tesla Vehicle Diagnostics**: Clean metrics, real-time status
2. **Azure Cognitive Services**: Professional AI interface
3. **IBM Maximo**: Industrial strength, data-dense
4. **Vercel Dashboard**: Modern, fast, delightful
5. **Linear App**: Smooth animations, keyboard-first

---

## Version History

- **v1.0** (2025-10-07): Initial design system
  - Dark mode theme
  - Teal accent color scheme
  - Component library defined
  - Animation guidelines established
