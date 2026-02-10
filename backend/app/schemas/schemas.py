"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime
from enum import Enum
import uuid


class SplitType(str, Enum):
    """Types of expense splits"""
    EQUAL = "equal"
    CUSTOM = "custom"
    PERCENTAGE = "percentage"


class CategoryEnum(str, Enum):
    """Expense categories"""
    FOOD = "Food"
    TRAVEL = "Travel"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    BILLS = "Bills"
    OTHER = "Other"


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    clerk_user_id: str


class UserResponse(UserBase):
    """Schema for user responses"""
    id: uuid.UUID
    clerk_user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Group Schemas
class GroupCreate(BaseModel):
    """Schema for creating a group"""
    name: str = Field(..., min_length=1, max_length=255)


class GroupMemberAdd(BaseModel):
    """Schema for adding a member to a group"""
    user_id: uuid.UUID


class GroupResponse(BaseModel):
    """Schema for group responses"""
    id: uuid.UUID
    name: str
    created_by: uuid.UUID
    created_at: datetime
    archived_at: Optional[datetime] = None
    member_count: int = 0
    
    class Config:
        from_attributes = True


# Expense Split Schemas
class ExpenseSplitInput(BaseModel):
    """Schema for individual expense split input"""
    user_id: uuid.UUID
    amount: Decimal = Field(..., ge=0, decimal_places=2)


class ExpenseSplitResponse(BaseModel):
    """Schema for expense split responses"""
    id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    user_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# Expense Schemas
class ExpenseCreate(BaseModel):
    """Schema for creating an expense"""
    group_id: uuid.UUID
    paid_by: uuid.UUID
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: str = Field(..., min_length=1)
    category: CategoryEnum = CategoryEnum.OTHER
    expense_date: date
    split_type: SplitType
    participant_ids: List[uuid.UUID] = Field(..., min_items=1, max_items=4)
    custom_amounts: Optional[List[Decimal]] = None
    percentages: Optional[List[Decimal]] = None
    
    @field_validator('participant_ids')
    @classmethod
    def validate_participant_count(cls, v):
        if len(v) > 4:
            raise ValueError('Maximum 4 participants allowed per group')
        return v


class ExpenseResponse(BaseModel):
    """Schema for expense responses"""
    id: uuid.UUID
    group_id: uuid.UUID
    paid_by: uuid.UUID
    amount: Decimal
    description: str
    category: str
    expense_date: date
    created_at: datetime
    payer_name: Optional[str] = None
    splits: List[ExpenseSplitResponse] = []
    
    class Config:
        from_attributes = True


# Settlement Schemas
class SettlementCreate(BaseModel):
    """Schema for creating a settlement"""
    group_id: uuid.UUID
    paid_by: uuid.UUID
    paid_to: uuid.UUID
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    settlement_date: date
    
    @field_validator('paid_to')
    @classmethod
    def validate_different_users(cls, v, info):
        if 'paid_by' in info.data and v == info.data['paid_by']:
            raise ValueError('paid_by and paid_to must be different users')
        return v


class SettlementResponse(BaseModel):
    """Schema for settlement responses"""
    id: uuid.UUID
    group_id: uuid.UUID
    paid_by: uuid.UUID
    paid_to: uuid.UUID
    amount: Decimal
    settlement_date: date
    created_at: datetime
    payer_name: Optional[str] = None
    receiver_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# Balance Schemas
class UserBalance(BaseModel):
    """Schema for user balance in a group"""
    user_id: uuid.UUID
    user_name: str
    balance: Decimal  # Positive = owed to them, Negative = they owe


class BalanceResponse(BaseModel):
    """Schema for group balance response"""
    group_id: uuid.UUID
    balances: List[UserBalance]
    is_zero_sum: bool


class SimplifiedTransaction(BaseModel):
    """Schema for simplified settlement transaction"""
    from_user_id: str
    to_user_id: str
    amount: Decimal
    from_user_name: str
    to_user_name: str


class SimplifyResponse(BaseModel):
    """Schema for debt simplification response"""
    group_id: uuid.UUID
    transactions: List[SimplifiedTransaction]
    total_transactions: int


# AI Parsing Schemas
class ParseExpenseRequest(BaseModel):
    """Schema for AI expense parsing request"""
    text: str = Field(..., min_length=1)
    group_id: uuid.UUID


class ParseExpenseResponse(BaseModel):
    """Schema for AI expense parsing response"""
    amount: Decimal
    description: str
    category: CategoryEnum
    participants: List[str]  # Names
    date: date


# Filter Schemas
class ExpenseFilters(BaseModel):
    """Schema for expense filtering"""
    group_id: uuid.UUID
    participant_id: Optional[uuid.UUID] = None
    category: Optional[CategoryEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
