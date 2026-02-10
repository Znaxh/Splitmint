# SplitMint Setup Guide

## Quick Start

Follow these steps to get SplitMint running locally in under 10 minutes.

### Step 1: Clone and Navigate

```bash
cd /home/anurag/Downloads/Karbon
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Backend Environment

Create `.env` file in `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

**Supabase Setup:**
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your project URL and anon key from Settings > API
4. Copy the Database URL from Settings > Database

**Clerk Setup:**
1. Go to [clerk.com](https://clerk.com)
2. Create a new application
3. Get your Secret Key from API Keys

**Gemini API:**
1. Go to [ai.google.dev](https://ai.google.dev)
2. Get your API key

**Update `.env`:**
```env
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_ANON_KEY=[your-anon-key]
SUPABASE_SERVICE_KEY=[your-service-key]
CLERK_SECRET_KEY=sk_test_[your-key]
GEMINI_API_KEY=[your-gemini-key]
SECRET_KEY=[generate-random-string]
ALLOWED_ORIGINS=http://localhost:3000
```

### Step 4: Setup Database

```bash
# Still in backend/ with venv activated
python setup_database.py
```

### Step 5: Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend is now running at `http://localhost:8000`

Test it: Open `http://localhost:8000/docs` to see API documentation

### Step 6: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd /home/anurag/Downloads/Karbon/frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://[project-ref].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[your-anon-key]
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_[your-key]
```

### Step 7: Start Frontend

```bash
npm run dev
```

Frontend is now running at `http://localhost:3000`

## ✅ Verification

1. **Backend**: Visit `http://localhost:8000/health` — should see `{"status":"healthy"}`
2. **Frontend**: Visit `http://localhost:3000` — should see the landing page
3. **API Docs**: Visit `http://localhost:8000/docs` — interactive API documentation

## 🧪 Run Tests

```bash
# Backend tests
cd backend
pytest app/tests/ -v
```

## 🚀 Next Steps

1. **Create a user** via the frontend signup
2. **Create a group** (max 4 members)
3. **Add an expense** using MintSense AI:
   - "Paid $120 for dinner with Alice and Bob yesterday"
4. **View balances** in real-time
5. **Get settlement suggestions** to minimize transactions

## 💡 Tips

- Keep both terminals open (one for backend, one for frontend)
- Backend auto-reloads on code changes
- Frontend has hot-reload enabled
- Check browser console for any errors
- Check terminal logs for backend errors

## 🐛 Common Issues

### Port Already in Use

If port 8000 or 3000 is already in use:

```bash
# Backend: Use different port
uvicorn app.main:app --reload --port 8001

# Update frontend .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

### Database Connection Error

Make sure your Supabase `DATABASE_URL` matches this format:
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Import Errors (Backend)

Make sure virtual environment is activated:
```bash
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs
- **README**: See main README.md for full documentation
- **Architecture**: See implementation_plan.md for technical details

---

**Happy coding! 🌿**
