"""
Group API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.core.database import get_db
from app.models.database import Group, GroupMember, User
from app.schemas.schemas import GroupCreate, GroupResponse, GroupMemberAdd

router = APIRouter()


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group: GroupCreate,
    creator_clerk_id: str,
    db: Session = Depends(get_db)
):
    """
    Create a new expense group.
    """
    # Get creator user
    creator = db.query(User).filter(User.clerk_user_id == creator_clerk_id).first()
    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator user not found"
        )
    
    # Create group
    db_group = Group(
        name=group.name,
        created_by=creator.id
    )
    db.add(db_group)
    db.flush()
    
    # Add creator as first member
    db_member = GroupMember(
        group_id=db_group.id,
        user_id=creator.id
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_group)
    
    return {
        **db_group.__dict__,
        "member_count": 1
    }


@router.post("/{group_id}/members", status_code=status.HTTP_201_CREATED)
async def add_group_member(
    group_id: uuid.UUID,
    member: GroupMemberAdd,
    db: Session = Depends(get_db)
):
    """
    Add a member to a group.
    Enforces max 4 participants.
    """
    # Check group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check member limit
    current_members = db.query(GroupMember).filter(GroupMember.group_id == group_id).count()
    if current_members >= 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group already has maximum of 4 members"
        )
    
    # Check user exists
    user = db.query(User).filter(User.id == member.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already a member
    existing = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == member.user_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this group"
        )
    
    # Add member
    db_member = GroupMember(
        group_id=group_id,
        user_id=member.user_id
    )
    db.add(db_member)
    db.commit()
    
    return {"message": "Member added successfully"}


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(group_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get group details.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    member_count = db.query(GroupMember).filter(GroupMember.group_id == group_id).count()
    
    return {
        **group.__dict__,
        "member_count": member_count
    }


@router.get("/user/{clerk_user_id}", response_model=List[GroupResponse])
async def get_user_groups(clerk_user_id: str, db: Session = Depends(get_db)):
    """
    Get all groups for a user.
    """
    # Get user
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get groups where user is a member
    group_ids = db.query(GroupMember.group_id).filter(
        GroupMember.user_id == user.id
    ).all()
    
    group_ids = [gid[0] for gid in group_ids]
    
    groups = db.query(Group).filter(
        Group.id.in_(group_ids),
        Group.archived_at.is_(None)
    ).all()
    
    # Add member counts
    result = []
    for group in groups:
        member_count = db.query(GroupMember).filter(
            GroupMember.group_id == group.id
        ).count()
        result.append({
            **group.__dict__,
            "member_count": member_count
        })
    
    return result
