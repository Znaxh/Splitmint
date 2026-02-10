"""
Debt simplification algorithm.
Finds minimal set of transactions to settle all debts using greedy approach.
"""
from decimal import Decimal
from typing import List, Dict, Tuple


def simplify_debts(balances: Dict[str, Decimal]) -> List[Tuple[str, str, Decimal]]:
    """
    Find minimal set of transactions to settle all debts.
    Uses greedy algorithm: match highest creditor with highest debtor.
    
    The algorithm works by:
    1. Separating users into debtors (negative balance) and creditors (positive balance)
    2. Sorting both lists by magnitude
    3. Matching the largest debtor with the largest creditor repeatedly
    
    Args:
        balances: Dictionary mapping user_id to their balance
                 Positive = owed money, Negative = owes money
    
    Returns:
        List of tuples (from_user, to_user, amount) representing optimal settlements
        
    Example:
        >>> balances = {
        ...     'Alice': Decimal('50.00'),   # Owed 50
        ...     'Bob': Decimal('-30.00'),    # Owes 30
        ...     'Charlie': Decimal('-20.00'), # Owes 20
        ... }
        >>> simplify_debts(balances)
        [('Bob', 'Alice', Decimal('30.00')), ('Charlie', 'Alice', Decimal('20.00'))]
    """
    # Filter out zero balances and separate into debtors and creditors
    debtors = [(user, abs(balance)) for user, balance in balances.items() if balance < -Decimal('0.01')]
    creditors = [(user, balance) for user, balance in balances.items() if balance > Decimal('0.01')]
    
    # Sort debtors by amount owed (largest first)
    debtors.sort(key=lambda x: x[1], reverse=True)
    # Sort creditors by amount owed (largest first)
    creditors.sort(key=lambda x: x[1], reverse=True)
    
    transactions = []
    i, j = 0, 0
    
    # Current debt and credit being processed
    current_debt = debtors[i][1] if debtors else Decimal('0')
    current_credit = creditors[j][1] if creditors else Decimal('0')
    
    while i < len(debtors) and j < len(creditors):
        debtor, _ = debtors[i]
        creditor, _ = creditors[j]
        
        # Settle the minimum of current debt and credit
        settlement_amount = min(current_debt, current_credit)
        
        transactions.append((debtor, creditor, settlement_amount))
        
        # Update remaining amounts
        current_debt -= settlement_amount
        current_credit -= settlement_amount
        
        # Move to next debtor if current debt is settled
        if current_debt < Decimal('0.01'):
            i += 1
            if i < len(debtors):
                current_debt = debtors[i][1]
        
        # Move to next creditor if current credit is settled
        if current_credit < Decimal('0.01'):
            j += 1
            if j < len(creditors):
                current_credit = creditors[j][1]
    
    return transactions


def calculate_group_balances(
    expenses: List[Dict],
    settlements: List[Dict]
) -> Dict[str, Decimal]:
    """
    Calculate current balances for all users in a group.
    
    Balance calculation:
    - For each user: amount_paid - amount_owed + settlements_received - settlements_made
    
    Args:
        expenses: List of expense dicts with 'paid_by', 'splits' (list of {user_id, amount})
        settlements: List of settlement dicts with 'paid_by', 'paid_to', 'amount'
    
    Returns:
        Dictionary mapping user_id to their current balance
    """
    balances: Dict[str, Decimal] = {}
    
    # Process expenses
    for expense in expenses:
        payer_id = expense['paid_by']
        total_amount = expense['amount']
        
        # Payer gets credited for the full amount
        balances[payer_id] = balances.get(payer_id, Decimal('0')) + Decimal(str(total_amount))
        
        # Each participant gets debited for their split
        for split in expense['splits']:
            user_id = split['user_id']
            split_amount = Decimal(str(split['amount']))
            balances[user_id] = balances.get(user_id, Decimal('0')) - split_amount
    
    # Process settlements
    for settlement in settlements:
        paid_by = settlement['paid_by']
        paid_to = settlement['paid_to']
        amount = Decimal(str(settlement['amount']))
        
        # Payer loses the settlement amount
        balances[paid_by] = balances.get(paid_by, Decimal('0')) - amount
        # Receiver gains the settlement amount
        balances[paid_to] = balances.get(paid_to, Decimal('0')) + amount
    
    return balances


def verify_zero_sum(balances: Dict[str, Decimal], tolerance: Decimal = Decimal('0.01')) -> bool:
    """
    Verify that all balances sum to zero (within tolerance).
    This is a critical invariant that should always hold.
    
    Args:
        balances: Dictionary of user balances
        tolerance: Acceptable rounding error
        
    Returns:
        True if sum is within tolerance of zero
    """
    total = sum(balances.values())
    return abs(total) <= tolerance
