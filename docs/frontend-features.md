# Frontend Features - Finance Tracker MVP (24-Hour Assignment)

## 🔐 Authentication
- **Google OAuth Login**: Simple Google sign-in button
  - Redirect to dashboard after successful login
  - Store JWT token securely
  - Auto-redirect to login if token expired

## 🏠 Landing Page
- **Hero Section**: Clean design with app value proposition
- **Feature Highlights**: 3-4 key features with icons
- **Call-to-Action**: "Sign in with Google" button
- **Responsive Design**: Mobile-friendly layout

## 📊 Dashboard
- **Financial Summary Cards**:
  - Total Income (current month)
  - Total Expenses (current month)
  - Net Balance (income - expenses)
  - Daily Budget Remaining
- **Quick Actions**:
  - Add Income button
  - Add Expense button
  - Upload Receipt button (bonus)
- **Recent Transactions**: Last 5 transactions with quick edit
- **Daily Report Card**: AI-generated daily spending insights with recommendations

## 💳 Transaction Management
- **Add Transaction Form**:
  - Amount input (required)
  - Type: Income/Expense radio buttons
  - Category: Dropdown (for expenses only)
  - Description: Text input
  - Date: Date picker (default: today)
- **Transaction List**:
  - Simple table/card view
  - Filter by date range
  - Filter by category
  - Edit/delete actions
  - Pagination (20 items per page)
- **Receipt Upload** (Bonus):
  - Camera/file upload
  - Show OCR results for editing
  - Auto-fill form with extracted data

## 🎯 Goals Management
- **Goals List**: Display all user goals with progress bars
- **Add Goal Form**:
  - Goal title
  - Target amount
  - Deadline date
  - Current amount (auto-calculated from transactions)
- **Goal Progress**: Visual progress indicators
- **Daily Savings Calculator**: Show how much to save daily to reach goals

## 📈 Simple Analytics
- **Daily Report**: AI-generated daily spending insights
  - Today's spending summary
  - Budget vs actual spending
  - Category breakdown for today
  - AI recommendations for tomorrow
  - Spending pattern analysis
- **Monthly Overview**:
  - Income vs Expenses bar chart
  - Category breakdown pie chart
  - Monthly trend line chart
- **Budget Tracking**:
  - Daily budget calculation
  - Spending by preferred days
  - Budget vs actual spending

## 🎨 UI/UX (Clean & Simple)
- **Modern Design**: Clean, minimal interface
- **Responsive Layout**: Works on mobile and desktop
- **Color Coding**:
  - Green for income
  - Red for expenses
  - Blue for goals
- **Loading States**: Simple spinners for API calls
- **Error Handling**: Toast notifications for errors

## 📱 Core Pages Structure
1. **Landing Page** (`/`)
   - Hero section
   - Sign in with Google

2. **Dashboard** (`/dashboard`)
   - Summary cards
   - Quick actions
   - Recent transactions

3. **Transactions** (`/transactions`)
   - Add transaction form
   - Transaction list with filters
   - Edit/delete functionality

4. **Goals** (`/goals`)
   - Goals list
   - Add goal form
   - Progress tracking

5. **Analytics** (`/analytics`)
   - Daily spending report
   - Monthly reports
   - Category breakdown
   - Budget tracking

6. **Profile** (`/profile`)
   - User info from Google
   - Monthly income setting
   - Preferred spending days
   - Daily budget multiplier

## 🔧 Technical Implementation
- **React**: Frontend framework
- **React Router**: Navigation
- **Axios**: API calls
- **Chart.js/Recharts**: Simple charts
- **Tailwind CSS**: Styling
- **React Hook Form**: Form handling
- **React Query**: API state management

## 📊 Daily Budget Formula
```javascript
// Simple calculation
const dailyBudget = (monthlyIncome - totalGoalContributions) / daysInMonth;

// Adjust for preferred spending days
const adjustedBudget = preferredSpendingDay ? 
  dailyBudget * dailyBudgetMultiplier : 
  dailyBudget * (1 - (dailyBudgetMultiplier - 1) / 7);
```

## 🤖 AI Integration Points
- **Transaction Categorization**: Send description to AI, get category from enum
- **Daily Reports**: AI-generated daily spending insights and recommendations
  - Analyze spending vs budget
  - Identify patterns (overspending categories, timing)
  - Provide actionable recommendations for tomorrow
  - Compare with user's goals and preferred spending days
- **Monthly Reports**: AI-generated monthly summaries
- **Receipt OCR**: Extract amount and description from images

## ✅ MVP Success Criteria
1. ✅ Google OAuth authentication
2. ✅ Add/edit/delete transactions
3. ✅ List transactions with date filtering
4. ✅ Basic charts (category breakdown, monthly trends)
5. ✅ Goals management with progress tracking
6. ✅ Daily budget calculation
7. ✅ Receipt OCR (bonus feature)
8. ✅ Responsive design
9. ✅ Clean, professional UI