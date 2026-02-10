# 🚀 SplitMint - Quick Reference

## Start Development

### Backend
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm run dev
```

**Access:**
- App: http://localhost:3000

## Environment Variables

### Backend `.env`
```env
DATABASE_URL=postgresql://user:pass@host:port/db
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your-key
CLERK_SECRET_KEY=sk_test_xxx
GEMINI_API_KEY=your-gemini-key
SECRET_KEY=random-secret
```

### Frontend `.env.local`
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx
```

## Project Files

### Key Backend Files
- `app/main.py` - FastAPI application entry
- `app/models/database.py` - SQLAlchemy models
- `app/services/split_engine.py` - Split algorithms
- `app/services/debt_simplifier.py` - Settlement optimizer
- `app/services/mintsense_ai.py` - AI parsing
- `app/api/expenses.py` - Expense endpoints
- `app/tests/test_balance_engine.py` - Tests

### Key Frontend Files
- `app/page.tsx` - Landing page
- `app/globals.css` - Dark theme styles
- `components/Dashboard.tsx` - Summary cards
- `components/BalanceTable.tsx` - Balance display
- `components/MintSenseInput.tsx` - AI input

## Commands

### Backend
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup_database.py

# Run
uvicorn app.main:app --reload

# Test
pytest app/tests/ -v
pytest app/tests/test_balance_engine.py -v
```

### Frontend
```bash
# Setup
npm install

# Run
npm run dev

# Build
npm run build

# Lint
npm run lint
```

## API Quick Reference

### Create Expense
```bash
POST /api/expenses
{
  "group_id": "uuid",
  "paid_by": "uuid",
  "amount": 120.00,
  "description": "Dinner",
  "category": "Food",
  "expense_date": "2026-02-09",
  "split_type": "equal",
  "participant_ids": ["uuid1", "uuid2"]
}
```

### Parse with AI
```bash
POST /api/expenses/parse
{
  "text": "Paid $120 for dinner with Alice yesterday",
  "group_id": "uuid"
}
```

### Get Balances
```bash
GET /api/expenses/group/{group_id}/balances
```

### Simplify Debts
```bash
GET /api/expenses/group/{group_id}/simplify
```

## Key Features

✅ **Ledger-based** - No static balances, computed dynamically
✅ **AI-powered** - Natural language expense parsing
✅ **Smart splits** - Equal, custom, percentage with perfect rounding
✅ **Debt optimization** - Minimal transactions via graph algorithm
✅ **Race-safe** - Database locking prevents concurrent issues
✅ **Real-time ready** - Supabase integration prepared
✅ **Dark theme** - Modern fintech UI with glassmorphism
✅ **Tested** - Comprehensive unit tests with zero-sum validation

## Next Steps

1. **Get API Keys:**
   - Supabase: https://supabase.com
   - Clerk: https://clerk.com
   - Gemini: https://ai.google.dev

2. **Configure Environment:**
   - Copy `.env.example` files
   - Fill in your API keys

3. **Setup Database:**
   - Run `python backend/setup_database.py`

4. **Start Development:**
   - Backend: `uvicorn app.main:app --reload`
   - Frontend: `npm run dev`

5. **Verify:**
   - Visit http://localhost:3000
   - Check http://localhost:8000/docs

## Documentation

- [README.md](file:///home/anurag/Downloads/Karbon/README.md) - Full documentation
- [SETUP.md](file:///home/anurag/Downloads/Karbon/SETUP.md) - Setup guide
- [walkthrough.md](file:///home/anurag/.gemini/antigravity/brain/2b82010d-7f0c-48cc-a689-393d24340459/walkthrough.md) - Build walkthrough
- [implementation_plan.md](file:///home/anurag/.gemini/antigravity/brain/2b82010d-7f0c-48cc-a689-393d24340459/implementation_plan.md) - Technical plan

---

**Built with 🌿 - Gateway to Karbon**
