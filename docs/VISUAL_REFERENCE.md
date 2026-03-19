# 🎨 Quick Visual Reference - Pastel UI Theme

## Color Palette Swatches

### Primary Colors
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ #FAFAF9     │  │ #FFFFFF     │  │ #F5E6D3     │
│ Warm White  │  │ Pure White  │  │ Soft Beige  │
│ Background  │  │ Surface     │  │ Accent      │
└─────────────┘  └─────────────┘  └─────────────┘

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ #FFB380     │  │ #1A1A1A     │  │ #6B6B6B     │
│ Pastel Org  │  │ Soft Black  │  │ Gray        │
│ Primary     │  │ Text        │  │ Text        │
└─────────────┘  └─────────────┘  └─────────────┘
```

### Status Colors
```
Success: #88D8B7 (Pastel Green)   ██████
Warning: #FFCC80 (Pastel Amber)   ██████
Error:   #FFABAB (Pastel Red)     ██████
Info:    #A2D2FF (Pastel Blue)    ██████
```

---

## Button Styles

### Primary Button
```css
Background: #FFB380 (Pastel Orange)
Color: #1A1A1A (Soft Black)
Border: None
Radius: 10px
Shadow: Soft
Hover: Lift -2px + Darken
```

### Secondary Button
```css
Background: #F5E6D3 (Soft Beige)
Color: #1A1A1A
Border: None
Radius: 10px
```

### Outline Button
```css
Background: Transparent
Border: 1.5px solid #E5E5E5
Color: #1A1A1A
Radius: 10px
Hover: Fill with beige
```

---

## Card Design

```
┌────────────────────────────────────┐
│  Card Title (16px, Bold)          │
│  ─────────────────────────────    │
│  Content text (14px, Gray)        │
│  More content here...             │
│                                   │
│  [Action Button]  [Secondary]     │
└────────────────────────────────────┘

Background: #FFFFFF
Border: 1px solid #F0F0F0
Radius: 14px
Shadow: 0 4px 6px rgba(0,0,0,0.06)
Hover: Lift -2px + Enhanced Shadow
```

---

## Score Badges

```
Excellent (80-100):
┌──────────┐
│   95     │  Background: rgba(136,216,183,0.15)
│ Excellent│  Color: #059669
└──────────┘  Border: 1px solid rgba(136,216,183,0.3)

Good (60-79):
┌──────────┐
│   72     │  Background: rgba(162,210,255,0.15)
│   Good   │  Color: #2563EB
└──────────┘  Border: 1px solid rgba(162,210,255,0.3)

Fair (40-59):
┌──────────┐
│   52     │  Background: rgba(255,204,128,0.15)
│   Fair   │  Color: #D97706
└──────────┘  Border: 1px solid rgba(255,204,128,0.3)

Poor (0-39):
┌──────────┐
│   28     │  Background: rgba(255,171,171,0.15)
│   Poor   │  Color: #DC2626
└──────────┘  Border: 1px solid rgba(255,171,171,0.3)
```

---

## Form Controls

### Input Field
```
┌────────────────────────────┐
│ Placeholder text (gray)    │
└────────────────────────────┘

Normal State:
Background: #FFFFFF
Border: 1.5px solid #F0F0F0
Radius: 10px

Focus State:
Border: 1.5px solid #FFB380
Shadow: 0 0 0 3px rgba(255,179,128,0.15)
```

### Range Slider
```
○────────────────○────────○
0                50      100

Track: #F5E6D3 (Beige)
Thumb: #FFB380 (Orange) 18px circle
Hover: Thumb scales to 1.1x
```

---

## Typography Scale

```
H1: 2.5rem (40px) - Page titles
H2: 2rem (32px)   - Section headers
H3: 1.5rem (24px) - Card titles
H4: 1.25rem (20px) - Subheaders
H5: 1.125rem (18px) - Small headers
H6: 1rem (16px)   - Labels

Body: 0.9375rem (15px)
Small: 0.875rem (14px)
Tiny: 0.8125rem (13px)
```

---

## Spacing System

```
xs:  4px   (tight)
sm:  8px   (compact)
md:  16px  (default)
lg:  24px  (spacious)
xl:  32px  (wide)
```

---

## Border Radius

```
sm:  6px   (slight round)
md:  10px  (moderate)
lg:  14px  (rounded)
xl:  20px  (very round)
```

---

## Shadows

```
Small:
0 1px 2px rgba(0,0,0,0.04)

Medium:
0 4px 6px rgba(0,0,0,0.06)

Large:
0 10px 15px rgba(0,0,0,0.08)

Extra Large:
0 20px 25px rgba(0,0,0,0.1)
```

---

## Animations

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
Duration: 0.4s
Timing: ease-out
```

### Slide Up
```css
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
Duration: 0.5s
Timing: cubic-bezier(0.4, 0, 0.2, 1)
```

### Pulse
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0.5; }
}
Duration: 2s
Timing: infinite
```

---

## Layout Examples

### 3-Column Dashboard
```
┌─────────┬──────────────────┬─────────────┐
│ Vehicle │     2D Map       │  Station    │
│Controls │  (Leaflet)       │ Recommend   │
│         │                  │             │
│ 380px   │    Flexible      │   420px     │
└─────────┴──────────────────┴─────────────┘
```

### Card Grid
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Card 1  │  │  Card 2  │  │  Card 3  │
│          │  │          │  │          │
└──────────┘  └──────────┘  └──────────┘
   350px         350px         350px
```

---

## Component Hierarchy

```
App
├── Navbar (White, blur, border-bottom)
├── Main Content
│   ├── Vehicle Controls Panel (White, shadow)
│   ├── Smart Map (Leaflet with custom markers)
│   └── Station Recommender (White, scrollable)
│       └── Station Cards (White, border, hover lift)
│           ├── Score Badge (Color-coded)
│           ├── Metrics Grid (3 columns)
│           ├── Details (2 columns)
│           ├── ML Insights (Blue background)
│           └── Action Buttons (Select, Navigate)
```

---

## Usage Examples

### Button in JSX
```jsx
<button 
  className="btn btn-primary"
  style={{
    background: 'var(--accent-primary)',
    color: 'var(--text-primary)',
    fontWeight: 600,
    padding: '12px 20px',
    borderRadius: '10px',
    border: 'none',
    boxShadow: 'var(--shadow-sm)',
    transition: 'all 0.3s ease'
  }}
>
  Click Me
</button>
```

### Card in JSX
```jsx
<div 
  className="card"
  style={{
    background: 'var(--bg-secondary)',
    border: '1px solid var(--border-light)',
    borderRadius: 'var(--radius-lg)',
    padding: 'var(--spacing-lg)',
    boxShadow: 'var(--shadow-sm)',
    transition: 'all var(--transition-base)'
  }}
>
  Card Content
</div>
```

---

## Quick Reference Table

| Element | Property | Value |
|---------|----------|-------|
| Primary Color | Hex | #FFB380 |
| Background | Hex | #FAFAF9 |
| Text Primary | Hex | #1A1A1A |
| Border Radius (md) | px | 10px |
| Border Radius (lg) | px | 14px |
| Shadow (md) | CSS | 0 4px 6px rgba(0,0,0,0.06) |
| Transition | CSS | all 0.3s ease |
| Font Family | - | 'Inter', sans-serif |
| Button Hover | Transform | translateY(-2px) |
| Card Hover | Transform | translateY(-2px) |

---

**Keep this guide handy for consistent UI implementation!** 🎨✨
