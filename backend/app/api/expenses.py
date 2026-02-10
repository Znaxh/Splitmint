"""
Expense API endpoints with race condition handling.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import uuid
from decimal import Decimal
from datetime import date

from app.core.database import get_db
from app.models.database import Expense, ExpenseSplit, Group, User, GroupMember
from app.schemas.schemas import (
    ExpenseCreate, ExpenseResponse, ExpenseSplitResponse,
    ParseExpenseRequest, ParseExpenseResponse, ExpenseFilters,
    BalanceResponse, UserBalance, SimplifyResponse, SimplifiedTransaction
)
from app.services.split_engine import create_splits, SplitType
from app.services.debt_simplifier import calculate_group_balances, simplify_debts
from app.services.mintsense_ai import parse_expense_text

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new expense with atomic transaction.
    Handles race conditions with database-level locking.
    """
    try:
        # Start transaction
        # Verify group exists and lock it
        group = db.query(Group).filter(
            Group.id == expense_data.group_id
        ).with_for_update().first()
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        
        # Verify payer is a member
        payer_membership = db.query(GroupMember).filter(
            and_(
                GroupMember.group_id == expense_data.group_id,
                GroupMember.user_id == expense_data.paid_by
            )
        ).first()
        
        if not payer_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payer must be a member of the group"
            )
        
        # Verify all participants are members
        for participant_id in expense_data.participant_ids:
            membership = db.query(GroupMember).filter(
                and_(
                    GroupMember.group_id == expense_data.group_id,
                    GroupMember.user_id == participant_id
                )
            ).first()
            
            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Participant {participant_id} is not a member of the group"
                )
        
        # Create expense splits using split engine
        splits_map = create_splits(
            amount=expense_data.amount,
            split_type=SplitType(expense_data.split_type),
            participant_ids=[str(pid) for pid in expense_data.participant_ids],
            custom_amounts=expense_data.custom_amounts,
            percentages=expense_data.percentages
        )
        
        # Create expense
        db_expense = Expense(
            group_id=expense_data.group_id,
            paid_by=expense_data.paid_by,
            amount=expense_data.amount,
            description=expense_data.description,
            category=expense_data.category.value,
            expense_date=expense_data.expense_date
        )
        db.add(db_expense)
        db.flush()
        
        # Create expense splits
        for user_id_str, split_amount in splits_map.items():
            db_split = ExpenseSplit(
                expense_id=db_expense.id,
                user_id=uuid.UUID(user_id_str),
                amount=split_amount
            )
            db.add(db_split)
        
        db.commit()
        db.refresh(db_expense)
        
        # Fetch payer name and splits for response
        payer = db.query(User).filter(User.id == db_expense.paid_by).first()
        splits = db.query(ExpenseSplit).filter(
            ExpenseSplit.expense_id == db_expense.id
        ).all()
        
        split_responses = []
        for split in splits:
            user = db.query(User).filter(User.id == split.user_id).first()
            split_responses.append(ExpenseSplitResponse(
                id=split.id,
                user_id=split.user_id,
                amount=split.amount,
                user_name=user.name if user else None
            ))
        
        return ExpenseResponse(
            id=db_expense.id,
            group_id=db_expense.group_id,
            paid_by=db_expense.paid_by,
            amount=db_expense.amount,
            description=db_expense.description,
            category=db_expense.category,
            expense_date=db_expense.expense_date,
            created_at=db_expense.created_at,
            payer_name=payer.name if payer else None,
            splits=split_responses
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create expense: {str(e)}"
        )


@router.post("/parse", response_model=ParseExpenseResponse)
async def parse_expense(
    parse_request: ParseExpenseRequest,
    db: Session = Depends(get_db)
):
    """
    Parse natural language expense using MintSense AI.
    """
    # Get group members
    members = db.query(User).join(GroupMember).filter(
        GroupMember.group_id == parse_request.group_id
    ).all()
    
    if not members:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found or has no members"
        )
    
    member_data = [{"name": m.name, "id": str(m.id)} for m in members]
    
    try:
        parsed = await parse_expense_text(parse_request.text, member_data)
        
        return ParseExpenseResponse(
            amount=parsed.amount,
            description=parsed.description,
            category=parsed.category,
            participants=parsed.participants,
            date=date.fromisoformat(parsed.date)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse expense: {str(e)}"
        )


@router.get("/group/{group_id}", response_model=List[ExpenseResponse])
async def get_group_expenses(
    group_id: uuid.UUID,
    participant_id: Optional[uuid.UUID] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get expenses for a group with optional filters.
    """
    query = db.query(Expense).filter(Expense.group_id == group_id)
    
    # Apply filters
    if participant_id:
        # Filter by expenses where user is either payer or split participant
        query = query.join(ExpenseSplit).filter(
            or_(
                Expense.paid_by == participant_id,
                ExpenseSplit.user_id == participant_id
            )
        )
    
    if category:
        query = query.filter(Expense.category == category)
    
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)
    
    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    
    expenses = query.order_by(Expense.expense_date.desc()).all()
    
    # Build responses with payer names and splits
    result = []
    for expense in expenses:
        payer = db.query(User).filter(User.id == expense.paid_by).first()
        splits = db.query(ExpenseSplit).filter(
            ExpenseSplit.expense_id == expense.id
        ).all()
        
        split_responses = []
        for split in splits:
            user = db.query(User).filter(User.id == split.user_id).first()
            split_responses.append(ExpenseSplitResponse(
                id=split.id,
                user_id=split.user_id,
                amount=split.amount,
                user_name=user.name if user else None
            ))
        
        result.append(ExpenseResponse(
            id=expense.id,
            group_id=expense.group_id,
            paid_by=expense.paid_by,
            amount=expense.amount,
            description=expense.description,
            category=expense.category,
            expense_date=expense.expense_date,
            created_at=expense.created_at,
            payer_name=payer.name if payer else None,
            splits=split_responses
        ))
    
    return result


@router.get("/group/{group_id}/balances", response_model=BalanceResponse)
async def get_group_balances(group_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Calculate real-time balances for all members in a group.
    """
    # Get all expenses
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    expense_data = []
    
    for expense in expenses:
        splits = db.query(ExpenseSplit).filter(
            ExpenseSplit.expense_id == expense.id
        ).all()
        
        expense_data.append({
            'paid_by': str(expense.paid_by),
            'amount': float(expense.amount),
            'splits': [
                {'user_id': str(s.user_id), 'amount': float(s.amount)}
                for s in splits
            ]
        })
    
    # Get all settlements (will implement later)
    settlements = []
    
    # Calculate balances
    balances = calculate_group_balances(expense_data, settlements)
    
    # Get user names
    user_balances = []
    for user_id, balance in balances.items():
        user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if user:
            user_balances.append(UserBalance(
                user_id=uuid.UUID(user_id),
                user_name=user.name or user.email,
                balance=balance
            ))
    
    # Check zero-sum property
    from app.services.debt_simplifier import verify_zero_sum
    is_zero_sum = verify_zero_sum(balances)
    
    return BalanceResponse(
        group_id=group_id,
        balances=user_balances,
        is_zero_sum=is_zero_sum
    )


@router.get("/group/{group_id}/simplify", response_model=SimplifyResponse)
async def simplify_group_debts(group_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get optimal settlement transactions to balance all debts.
    """
    # Get current balances
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    expense_data = []
    
    for expense in expenses:
        splits = db.query(ExpenseSplit).filter(
            ExpenseSplit.expense_id == expense.id
        ).all()
        
        expense_data.append({
            'paid_by': str(expense.paid_by),
            'amount': float(expense.amount),
            'splits': [
                {'user_id': str(s.user_id), 'amount': float(s.amount)}
                for s in splits
            ]
        })
    
    balances = calculate_group_balances(expense_data, [])
    
    # Simplify debts
    transactions = simplify_debts(balances)
    
    # Build response with user names
    transaction_responses = []
    for from_id, to_id, amount in transactions:
        from_user = db.query(User).filter(User.id == uuid.UUID(from_id)).first()
        to_user = db.query(User).filter(User.id == uuid.UUID(to_id)).first()
        
        transaction_responses.append(SimplifiedTransaction(
            from_user_id=from_id,
            to_user_id=to_id,
            amount=amount,
            from_user_name=from_user.name if from_user else "Unknown",
            to_user_name=to_user.name if to_user else "Unknown"
        ))
    
    return SimplifyResponse(
        group_id=group_id,
        transactions=transaction_responses,
        total_transactions=len(transaction_responses)
    )
