"""
Settlement API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
import uuid

from app.core.database import get_db
from app.models.database import Settlement, Group, GroupMember, User
from app.schemas.schemas import SettlementCreate, SettlementResponse

router = APIRouter()


@router.post("/", response_model=SettlementResponse, status_code=status.HTTP_201_CREATED)
async def create_settlement(
    settlement_data: SettlementCreate,
    db: Session = Depends(get_db)
):
    """
    Record a settlement (payment between group members).
    """
    # Verify group exists
    group = db.query(Group).filter(Group.id == settlement_data.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Verify both users are members
    payer_member = db.query(GroupMember).filter(
        and_(
            GroupMember.group_id == settlement_data.group_id,
            GroupMember.user_id == settlement_data.paid_by
        )
    ).first()
    
    receiver_member = db.query(GroupMember).filter(
        and_(
            GroupMember.group_id == settlement_data.group_id,
            GroupMember.user_id == settlement_data.paid_to
        )
    ).first()
    
    if not payer_member or not receiver_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both users must be members of the group"
        )
    
    # Create settlement
    db_settlement = Settlement(
        group_id=settlement_data.group_id,
        paid_by=settlement_data.paid_by,
        paid_to=settlement_data.paid_to,
        amount=settlement_data.amount,
        settlement_date=settlement_data.settlement_date
    )
    
    db.add(db_settlement)
    db.commit()
    db.refresh(db_settlement)
    
    # Get user names
    payer = db.query(User).filter(User.id == db_settlement.paid_by).first()
    receiver = db.query(User).filter(User.id == db_settlement.paid_to).first()
    
    return SettlementResponse(
        id=db_settlement.id,
        group_id=db_settlement.group_id,
        paid_by=db_settlement.paid_by,
        paid_to=db_settlement.paid_to,
        amount=db_settlement.amount,
        settlement_date=db_settlement.settlement_date,
        created_at=db_settlement.created_at,
        payer_name=payer.name if payer else None,
        receiver_name=receiver.name if receiver else None
    )


@router.get("/group/{group_id}", response_model=List[SettlementResponse])
async def get_group_settlements(group_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get all settlements for a group.
    """
    settlements = db.query(Settlement).filter(
        Settlement.group_id == group_id
    ).order_by(Settlement.settlement_date.desc()).all()
    
    result = []
    for settlement in settlements:
        payer = db.query(User).filter(User.id == settlement.paid_by).first()
        receiver = db.query(User).filter(User.id == settlement.paid_to).first()
        
        result.append(SettlementResponse(
            id=settlement.id,
            group_id=settlement.group_id,
            paid_by=settlement.paid_by,
            paid_to=settlement.paid_to,
            amount=settlement.amount,
            settlement_date=settlement.settlement_date,
            created_at=settlement.created_at,
            payer_name=payer.name if payer else None,
            receiver_name=receiver.name if receiver else None
        ))
    
    return result
