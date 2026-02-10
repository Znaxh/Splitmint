# SplitMint 🌿

**Gateway to Karbon** — A high-performance fintech expense sharing platform with AI-powered parsing, smart debt settlement, and real-time updates.

![SplitMint](https://img.shields.io/badge/SplitMint-v1.0.0-00FFAB?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

## 🚀 Features

- **MintSense AI** — Natural language expense parsing using Gemini
- **Smart Splits** — Equal, custom amounts, or percentages with penny-perfect accuracy
- **Debt Simplification** — Minimize transactions with graph-theory algorithm
- **Real-time Updates** — Instant balance sync across all devices via Supabase
- **Ledger-based** — Immutable transaction history, balances computed dynamically
- **Race Condition Safe** — Database-level locking for concurrent operations
- **Dark Theme UI** — Modern fintech design with glassmorphism and animations

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Framer Motion
- Clerk (Authentication)
- Supabase (Realtime)

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL (via Supabase)
- SQLAlchemy ORM
- Pydantic validation
- Google Gemini AI

### Key Design Principles

1. **Ledger-based Accounting** — No static balance columns. Balances computed from SUM of expenses and settlements.
2. **ACID Transactions** — Database-level locks prevent race conditions.
3. **Zero-Sum Invariant** — All splits and balances must sum to zero (±1¢ tolerance).
4. **Banker's Rounding** — Ensures perfect penny distribution.

## 📦 Installation

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL database (Supabase account)
- Clerk account
- Gemini API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required environment variables:**
```env
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
CLERK_SECRET_KEY=your-clerk-secret-key
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-jwt-secret-key
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template  
cp .env.local.example .env.local

# Edit .env.local with your credentials
nano .env.local
```

**Required environment variables:**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
```

### Database Setup

1. Create a Supabase project
2. Run the database schema:

```sql
-- Create tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- See backend/app/models/database.py for full schema
```

Or use Alembic migrations:

```bash
cd backend
alembic upgrade head
```

## 🚀 Running Locally

### Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Backend will run at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run at: `http://localhost:3000`

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest app/tests/ -v
```

**Critical tests:**
- Zero-sum validation for all splits
- Debt simplification correctness
- Race condition handling

### Run specific test suites:

```bash
# Balance engine tests only
pytest app/tests/test_balance_engine.py -v

# Zero-sum invariant tests
pytest app/tests/test_balance_engine.py::TestZeroSumInvariant -v
```

## 📝 API Documentation

### Key Endpoints

**Expenses:**
- `POST /api/expenses` — Create expense with splits
- `POST /api/expenses/parse` — AI-powered natural language parsing
- `GET /api/expenses/group/{group_id}` — List expenses with filters
- `GET /api/expenses/group/{group_id}/balances` — Real-time balances
- `GET /api/expenses/group/{group_id}/simplify` — Optimal settlement plan

**Groups:**
- `POST /api/groups` — Create group (max 4 members)
- `POST /api/groups/{group_id}/members` — Add member
- `GET /api/groups/user/{clerk_user_id}` — List user's groups

**Settlements:**
- `POST /api/settlements` — Record payment between members
- `GET /api/settlements/group/{group_id}` — List settlements

## 🎨 UI Components

### Landing Page
- Hero section with animated background
- Feature grid with glassmorphism cards
- Responsive design

### Dashboard
- Summary cards (Total Spent, You Owe, Owed to You)
- Real-time balance updates
- Framer Motion animations

### MintSense AI Input
- Natural language expense entry
- Example: "Paid $120 for dinner with Alice yesterday"
- Auto-parsing with visual feedback

## 🔐 Security

- **Clerk Authentication** — Industry-standard auth
- **Database-level Locking** — Prevents race conditions
- **Input Validation** — Pydantic (backend) + Zod (frontend)
- **SQL Injection Protection** — SQLAlchemy ORM
- **CORS Configuration** — Restricted origins

## 🚢 Deployment

### Frontend (Vercel)

```bash
cd frontend
vercel --prod
```

### Backend

**Option 1: Railway**
```bash
railway up
```

**Option 2: Render**
- Connect GitHub repo
- Set environment variables
- Deploy

**Option 3: Fly.io**
```bash
fly deploy
```

### Environment Variables

Set all required environment variables in your deployment platform.

## 🧮 Core Algorithms

### Equal Split with Banker's Rounding

```python
def split_equal(amount: Decimal, num_participants: int) -> List[Decimal]:
    base = (amount / num_participants).quantize(Decimal('0.01'), ROUND_HALF_EVEN)
    splits = [base] * num_participants
    
    # Distribute pennies to ensure exact sum
    diff = amount - sum(splits)
    for i in range(abs(int(diff * 100))):
        splits[i] += Decimal('0.01') if diff > 0 else Decimal('-0.01')
    
    return splits
```

### Debt Simplification

Uses greedy algorithm to match largest creditor with largest debtor:
1. Separate users into debtors (negative balance) and creditors (positive balance)
2. Sort both by magnitude
3. Match iteratively, creating minimal transactions

**Complexity:** O(n log n) where n = number of participants

## 📊 Database Design

### Ledger-based Approach

**Traditional (DON'T DO):**
```
users: { id, name, balance }  ❌ Static balance
```

**SplitMint (CORRECT):**
```
expenses: { paid_by, amount }
expense_splits: { user_id, amount }
settlements: { paid_by, paid_to, amount }

Balance = SUM(paid) - SUM(owed) + SUM(received) - SUM(settled)  ✅
```

**Benefits:**
- Complete audit trail
- Impossible to have inconsistent state
- Easy to verify zero-sum property

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with ❤️ as a gateway to Karbon
- Inspired by modern fintech platforms
- Powered by cutting-edge AI and real-time tech

---

**Made with 🌿 by the SplitMint Team**
# Splitmint
# Splitmint
