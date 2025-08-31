# sidemoney Frontend (v0)

Environment variables required:

- NEXT_PUBLIC_API_BASE_URL (e.g., http://localhost:8000)
- NEXT_PUBLIC_GOOGLE_CLIENT_ID (Google Identity Services OAuth client ID)

Features:

- Google sign-in -> exchanges id_token at /auth/google, stores JWT in localStorage
- Authenticated dashboard with:
  - Daily budget and report cards (/analytics/daily-budget, /analytics/daily-report)
  - Transactions list with filters and pagination (/transactions)
  - Create transaction form (/transactions)
  - Goals CRUD (/goals)
  - OCR receipt upload (/ai/ocr/process -> /transactions/bulk)
  - AI analyze action (/ai/analyze)
- Settings page to update profile (/user/profile)

Design:

- Colors (5 total): Blue (#1E40AF), Emerald (#10B981), White (#FFFFFF), Light Gray (#F7F7F9), Charcoal (#111827)
- Fonts: Geist Sans (default in project)
- No gradients, mobile-first, shadcn/ui components, Recharts for charts
