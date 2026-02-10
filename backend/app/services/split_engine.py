"""
Split engine - handles equal, custom, and percentage-based splits.
Uses Banker's Rounding to handle uneven cents.
"""
from decimal import Decimal, ROUND_HALF_EVEN
from typing import List, Dict
from enum import Enum


class SplitType(str, Enum):
    """Types of expense splits"""
    EQUAL = "equal"
    CUSTOM = "custom"
    PERCENTAGE = "percentage"


def split_equal(amount: Decimal, num_participants: int) -> List[Decimal]:
    """
    Split amount equally using Banker's Rounding.
    Ensures sum of splits exactly equals original amount.
    
    Args:
        amount: Total amount to split
        num_participants: Number of people splitting the expense
        
    Returns:
        List of split amounts that sum exactly to original amount
        
    Example:
        >>> split_equal(Decimal('10.00'), 3)
        [Decimal('3.33'), Decimal('3.33'), Decimal('3.34')]
    """
    if num_participants <= 0:
        raise ValueError("Number of participants must be positive")
    
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    # Calculate base split with Banker's rounding
    base = (amount / num_participants).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
    splits = [base] * num_participants
    
    # Calculate rounding difference
    total = sum(splits)
    diff = amount - total
    
    # Distribute pennies to first n participants
    if diff != 0:
        adjustment = Decimal('0.01') if diff > 0 else Decimal('-0.01')
        num_adjustments = abs(int(diff * 100))
        
        for i in range(num_adjustments):
            splits[i] += adjustment
    
    return splits


def split_custom(amount: Decimal, custom_amounts: List[Decimal]) -> List[Decimal]:
    """
    Validate custom split amounts.
    
    Args:
        amount: Total amount
        custom_amounts: List of custom amounts for each participant
        
    Returns:
        Validated custom amounts
        
    Raises:
        ValueError: If custom amounts don't sum to total
    """
    total = sum(custom_amounts)
    
    if total != amount:
        raise ValueError(
            f"Custom amounts ({total}) do not sum to total amount ({amount}). "
            f"Difference: {amount - total}"
        )
    
    for amt in custom_amounts:
        if amt < 0:
            raise ValueError("Custom amounts cannot be negative")
    
    return custom_amounts


def split_percentage(amount: Decimal, percentages: List[Decimal]) -> List[Decimal]:
    """
    Split based on percentages with rounding adjustment.
    
    Args:
        amount: Total amount to split
        percentages: List of percentages (should sum to 100)
        
    Returns:
        List of split amounts that sum exactly to original amount
        
    Example:
        >>> split_percentage(Decimal('100.00'), [Decimal('33.33'), Decimal('33.33'), Decimal('33.34')])
        [Decimal('33.33'), Decimal('33.33'), Decimal('33.34')]
    """
    total_percentage = sum(percentages)
    
    # Allow small rounding errors (within 0.01%)
    if abs(total_percentage - Decimal('100.00')) > Decimal('0.01'):
        raise ValueError(
            f"Percentages must sum to 100. Got: {total_percentage}"
        )
    
    # Calculate amounts
    splits = []
    for pct in percentages:
        if pct < 0:
            raise ValueError("Percentages cannot be negative")
        
        split_amount = (amount * pct / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        splits.append(split_amount)
    
    # Adjust for rounding errors
    total = sum(splits)
    diff = amount - total
    
    if diff != 0:
        # Add adjustment to the largest split
        max_idx = splits.index(max(splits))
        splits[max_idx] += diff
    
    return splits


def create_splits(
    amount: Decimal,
    split_type: SplitType,
    participant_ids: List[str],
    custom_amounts: List[Decimal] = None,
    percentages: List[Decimal] = None
) -> Dict[str, Decimal]:
    """
    Create expense splits based on split type.
    
    Args:
        amount: Total expense amount
        split_type: Type of split (equal, custom, or percentage)
        participant_ids: List of user IDs
        custom_amounts: Custom amounts for each participant (if split_type is CUSTOM)
        percentages: Percentages for each participant (if split_type is PERCENTAGE)
        
    Returns:
        Dictionary mapping user_id to split amount
    """
    num_participants = len(participant_ids)
    
    if num_participants == 0:
        raise ValueError("At least one participant required")
    
    if split_type == SplitType.EQUAL:
        split_amounts = split_equal(amount, num_participants)
    
    elif split_type == SplitType.CUSTOM:
        if not custom_amounts or len(custom_amounts) != num_participants:
            raise ValueError("Custom amounts must be provided for all participants")
        split_amounts = split_custom(amount, custom_amounts)
    
    elif split_type == SplitType.PERCENTAGE:
        if not percentages or len(percentages) != num_participants:
            raise ValueError("Percentages must be provided for all participants")
        split_amounts = split_percentage(amount, percentages)
    
    else:
        raise ValueError(f"Invalid split type: {split_type}")
    
    # Create mapping of user_id to amount
    return {
        user_id: split_amount
        for user_id, split_amount in zip(participant_ids, split_amounts)
    }
