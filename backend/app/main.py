"""
Main FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import expenses, groups, users, settlements

# Create FastAPI app
app = FastAPI(
    title="SplitMint API",
    description="High-performance fintech expense sharing platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(groups.router, prefix="/api/groups", tags=["groups"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
app.include_router(settlements.router, prefix="/api/settlements", tags=["settlements"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SplitMint API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
