# Container Inspection AI - UI Mockups & Wireframes

## Visual Design Documentation

This document describes the visual layout and design of each page in the Container Inspection AI system.

---

## 🏠 Home / Dashboard Page

### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│  🚢 Container Inspection AI                          [Profile]  │
│  Enterprise-Grade Damage Detection • AI-Powered • Reports       │
├──────────┬──────────────────────────────────────────────────────┤
│          │                                                       │
│  📦      │  ┌─────────────────────────────────────────────┐    │
│  INSPEC  │  │  📤 Upload Container Image                  │    │
│  -TION   │  │  ┌─────────────────────────────────────┐   │    │
│  AI      │  │  │                                       │   │    │
│  v2.0    │  │  │     [Upload Cloud Icon]              │   │    │
│          │  │  │  Drag & drop or click to upload      │   │    │
│  ─────   │  │  │  JPG, PNG, JPEG (Max 10MB)           │   │    │
│          │  │  │                                       │   │    │
│  🎯 Nav  │  │  └─────────────────────────────────────┘   │    │
│  🏠 Home │  │                                              │    │
│  🔍 Det  │  │  [🚀 Run AI Inspection]                     │    │
│  📊 Rep  │  └─────────────────────────────────────────────┘    │
│  📈 Ana  │                                                       │
│  ⚙️ Set  │  ┌──────────┬──────────┬──────────┬──────────┐     │
│          │  │ Total    │ Pending  │ Critical │ Success  │     │
│  ─────   │  │ Scans    │ Review   │ Issues   │ Rate     │     │
│          │  │ 1,247    │ 23       │ 8        │ 94.2%    │     │
│  🎨 Leg  │  └──────────┴──────────┴──────────┴──────────┘     │
│  🔴 Dam  │                                                       │
│  🟢 ID   │  Recent Inspections                                  │
│  🔵 Pla  │  ┌─────────────────────────────────────────────┐    │
│  🟡 Loc  │  │ CPIU1811772  │ Poor    │ ₹45,000 │ 2m ago  │    │
│          │  │ MSCU4567890  │ Good    │ ₹12,000 │ 5m ago  │    │
│  ─────   │  │ TEMU9876543  │ Fair    │ ₹28,000 │ 8m ago  │    │
│          │  └─────────────────────────────────────────────┘    │
│  📡 Sys  │                                                       │
│  ● API   │                                                       │
│  ● AI    │                                                       │
└──────────┴───────────────────────────────────────────────────────┘
```

### Key Elements
- **Hero Section**: Gradient title with tagline
- **Upload Zone**: Dashed border, hover effects, drag-and-drop
- **Metrics Cards**: 4 cards showing key statistics
- **Recent Activity**: Table of latest inspections
- **Sidebar**: Navigation, legend, system status

---

## 🔍 Detection Results Page

### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│  Inspection Results                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              CPIU1811772                                   │ │
│  └───────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────┬──────────────────────┤
│                                          │                      │
│  🖼️ Annotated Detection                 │  📊 Key Metrics     │
│  ┌────────────────────────────────────┐ │                      │
│  │                                    │ │  ┌────────────────┐ │
│  │                                    │ │  │ Overall Cond.  │ │
│  │     [Container Image with          │ │  │     Poor       │ │
│  │      Bounding Boxes]               │ │  └────────────────┘ │
│  │                                    │ │                      │
│  │  🔴 Damage                         │ │  💰 Repair Cost    │
│  │  🟢 Container ID                   │ │     ₹45,000        │
│  │  🔵 Data Plate                     │ │                      │
│  │                                    │ │  AI Confidence     │
│  └────────────────────────────────────┘ │  92% ████████░░    │
│                                          │                      │
│                                          │  ⚠️ DISCARD        │
│                                          │  Structural damage │
│                                          │                      │
│                                          │  📥 Downloads      │
│                                          │  [📄 PDF Report]   │
│                                          │  [📊 Excel]        │
│                                          │  [📋 JSON]         │
└──────────────────────────────────────────┴──────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  🤖 AI Vision Analysis                                          │
│  ┌──────────────┬──────────────┬──────────────┐                │
│  │ Structural   │ GPT-5        │ Safety       │                │
│  │ Integrity    │ Confidence   │ Concerns     │                │
│  │ Compromised  │ 95%          │ ⚠️ 3         │                │
│  └──────────────┴──────────────┴──────────────┘                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────────┐
│  🚨 Safety Concerns          │  🔧 Maintenance Recommendations  │
│  1. Structural frame damage  │  1. Replace door hinges          │
│  2. Compromised seal         │  2. Repair corner post           │
│  3. Rust on floor panels     │  3. Apply anti-corrosion coating │
└──────────────────────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  📦 Container Metadata                                          │
│  ┌──────────────┬──────────────┬──────────────┐                │
│  │ ID: CPIU...  │ Size: 40ft   │ Max Gross:   │                │
│  │ Type: Dry    │ Category: U  │ 30,480 kg    │                │
│  │ Owner: CPIU  │ Integrity:   │ Tare: 3,800  │                │
│  └──────────────┴──────────────┴──────────────┘                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  🔍 Damage Analysis                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Type    │ Severity │ Zone  │ Location │ Confidence │ Cost │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │ Dent    │ Major    │ Door  │ 07       │ 92%        │ 15k  │ │
│  │ Rust    │ Minor    │ Floor │ 12       │ 88%        │ 8k   │ │
│  │ Crack   │ Major    │ Frame │ 03       │ 95%        │ 22k  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Expandable Details for Each Damage]                          │
└─────────────────────────────────────────────────────────────────┘
```

### Visual Features
- **Split Layout**: 2:1 ratio (image:metrics)
- **Color-Coded Badges**: Condition status with matching borders
- **Progress Bars**: Animated confidence meters
- **Expandable Sections**: Accordion for detailed damage info
- **Download Buttons**: Prominent, icon-enhanced

---

## 📊 Reports List Page

### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Inspection Reports                        [Search] [Filter] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  CPIU1811772          Poor        ₹45,000      2m ago      │ │
│  │  [View Report] [Download]                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MSCU4567890          Good        ₹12,000      5m ago      │ │
│  │  [View Report] [Download]                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  TEMU9876543          Fair        ₹28,000      8m ago      │ │
│  │  [View Report] [Download]                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Load More]                                  Page 1 of 25      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 Analytics Dashboard

### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│  📈 Analytics Dashboard                      [Last 30 Days ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┬──────────┬──────────┬──────────┐                 │
│  │ Total    │ Avg Cost │ Critical │ Success  │                 │
│  │ Scans    │ per Scan │ Rate     │ Rate     │                 │
│  │ 1,247    │ ₹18,500  │ 6.4%     │ 94.2%    │                 │
│  └──────────┴──────────┴──────────┴──────────┘                 │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Inspections Over Time                                     │ │
│  │  [Line Chart showing daily inspection volume]             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────┬──────────────────────────────┐   │
│  │  Damage Type Distribution│  Condition Breakdown         │   │
│  │  [Pie Chart]             │  [Bar Chart]                 │   │
│  └──────────────────────────┴──────────────────────────────┘   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Cost Analysis                                             │ │
│  │  [Stacked Bar Chart showing cost by damage type]          │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Usage Guide

### Condition Status
- **Excellent**: `#10B981` (Green) - Solid border, light background
- **Good**: `#34D399` (Light Green)
- **Fair**: `#F59E0B` (Amber)
- **Poor**: `#FB923C` (Orange)
- **Critical**: `#EF4444` (Red) - Pulsing animation

### Detection Bounding Boxes
- **Damage**: `#EF4444` (Red) - Thick border (3px)
- **Container ID**: `#10B981` (Green) - Medium border (2px)
- **Data Plate**: `#06B6D4` (Cyan) - Medium border (2px)
- **Location Codes**: `#FFD700` (Yellow) - Thin border (1px)

### Interactive States
- **Hover**: Lift 4px, increase shadow, border glow
- **Active**: Scale 0.98, reduce shadow
- **Focus**: 2px teal outline with 4px offset
- **Disabled**: 50% opacity, no pointer events

---

## 🎬 Animation Specifications

### Page Load
- **Duration**: 500ms
- **Easing**: ease-out
- **Effect**: Fade in + slide up 20px

### Scanning Animation
- **Duration**: 2s (infinite loop)
- **Effect**: Horizontal sweep with gradient
- **Colors**: Teal to light teal gradient

### Metric Cards
- **Hover**: 300ms transform + shadow
- **Number Counter**: 1s with easeOutExpo
- **Entry**: Staggered fade-in (100ms delay each)

### Progress Bars
- **Fill Animation**: 1s ease-out
- **Color Transition**: Smooth gradient based on value

### Success/Error States
- **Success**: Checkmark with scale + rotate animation (600ms)
- **Error**: Shake animation (400ms)
- **Toast**: Slide in from right (300ms)

---

## 📱 Responsive Breakpoints

### Mobile (< 640px)
- Single column layout
- Sidebar collapses to hamburger menu
- Metrics stack vertically
- Reduced padding (16px → 12px)
- Font sizes reduced by 10%

### Tablet (640px - 1024px)
- 2-column layout for metrics
- Sidebar remains visible
- Image and metrics stack vertically
- Touch-friendly targets (min 44px)

### Desktop (> 1024px)
- Full 3-column layouts
- Sidebar fixed at 280px
- Optimal spacing and typography
- Hover effects enabled

### Wide (> 1536px)
- Max content width: 1400px
- Increased spacing
- Larger images and charts

---

## 🎯 Accessibility Features

### Keyboard Navigation
- Tab order follows visual flow
- Skip links for main content
- Escape closes modals
- Arrow keys for navigation

### Screen Readers
- Semantic HTML (header, nav, main, section)
- ARIA labels on icons
- Status announcements for dynamic content
- Alt text for all images

### Visual
- Minimum 7:1 contrast ratio (AAA)
- Focus indicators always visible
- No color-only information
- Scalable text (rem units)

### Motion
- Respect `prefers-reduced-motion`
- Disable animations if requested
- Provide static alternatives

---

## 🖼️ Icon Usage

### Navigation
- 🏠 Home
- 🔍 Detection
- 📊 Reports
- 📈 Analytics
- ⚙️ Settings

### Actions
- 📤 Upload
- 🚀 Run Inspection
- 📥 Download
- 🔄 Refresh
- ❌ Close

### Status
- ✅ Success
- ⚠️ Warning
- ❌ Error
- ℹ️ Info
- 🔴 Critical

### Detection
- 🔴 Damage
- 🟢 Container ID
- 🔵 Data Plate
- 🟡 Location Code

---

## 💡 Design Principles

1. **Clarity**: Information hierarchy is clear and logical
2. **Efficiency**: Minimize clicks to complete tasks
3. **Feedback**: Immediate visual response to all actions
4. **Consistency**: Patterns repeat throughout the app
5. **Accessibility**: Usable by everyone, everywhere
6. **Performance**: Fast load times, smooth animations
7. **Delight**: Subtle animations enhance experience

---

## 🎨 Typography Scale

```
Hero Title:     2.5rem (40px) - Bold
Page Title:     2rem (32px) - Bold
Section Header: 1.5rem (24px) - Semibold
Card Title:     1.25rem (20px) - Semibold
Body Large:     1.125rem (18px) - Regular
Body:           1rem (16px) - Regular
Body Small:     0.875rem (14px) - Regular
Caption:        0.75rem (12px) - Medium
```

---

## 📐 Spacing System

```
Micro:   4px  - Icon padding, tight spacing
Small:   8px  - Element spacing
Medium:  16px - Card padding, section spacing
Large:   24px - Component spacing
XLarge:  32px - Section gaps
XXLarge: 48px - Page sections
```

---

This mockup documentation provides a complete visual reference for implementing the Container Inspection AI interface. All measurements, colors, and interactions are specified for consistent implementation across the application.
