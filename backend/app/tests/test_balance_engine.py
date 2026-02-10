"""
Unit tests for balance engine and split algorithms.
Ensures zero-sum accuracy and proper rounding.
"""
import pytest
from decimal import Decimal
from app.services.split_engine import split_equal, split_custom, split_percentage, create_splits, SplitType
from app.services.debt_simplifier import simplify_debts, calculate_group_balances, verify_zero_sum


class TestSplitEngine:
    """Tests for split engine"""
    
    def test_equal_split_zero_sum(self):
        """Ensure equal splits sum exactly to original amount."""
        amount = Decimal('100.00')
        splits = split_equal(amount, 3)
        
        assert sum(splits) == amount
        assert len(splits) == 3
    
    def test_equal_split_with_remainder(self):
        """Test rounding with uneven division."""
        amount = Decimal('10.00')
        splits = split_equal(amount, 3)
        
        # 10 / 3 = 3.33, 3.33, 3.34
        assert sum(splits) == amount
        assert splits == [Decimal('3.34'), Decimal('3.33'), Decimal('3.33')]
    
    def test_equal_split_large_amount(self):
        """Test with large amounts."""
        amount = Decimal('1234.56')
        splits = split_equal(amount, 7)
        
        assert sum(splits) == amount
        # Each should be around 176.37
        for split in splits:
            assert split > Decimal('176.00')
            assert split < Decimal('177.00')
    
    def test_custom_split_valid(self):
        """Test valid custom split."""
        amount = Decimal('100.00')
        custom = [Decimal('50.00'), Decimal('30.00'), Decimal('20.00')]
        
        result = split_custom(amount, custom)
        assert result == custom
        assert sum(result) == amount
    
    def test_custom_split_invalid_sum(self):
        """Test custom split with incorrect sum."""
        amount = Decimal('100.00')
        custom = [Decimal('50.00'), Decimal('30.00'), Decimal('15.00')]  # Sums to 95
        
        with pytest.raises(ValueError, match="do not sum to total amount"):
            split_custom(amount, custom)
    
    def test_percentage_split(self):
        """Test percentage-based split."""
        amount = Decimal('100.00')
        percentages = [Decimal('50.00'), Decimal('30.00'), Decimal('20.00')]
        
        splits = split_percentage(amount, percentages)
        
        assert sum(splits) == amount
        assert splits[0] == Decimal('50.00')
        assert splits[1] == Decimal('30.00')
        assert splits[2] == Decimal('20.00')
    
    def test_percentage_split_with_rounding(self):
        """Test percentage split with rounding."""
        amount = Decimal('100.00')
        percentages = [Decimal('33.33'), Decimal('33.33'), Decimal('33.34')]
        
        splits = split_percentage(amount, percentages)
        
        assert sum(splits) == amount
    
    def test_create_splits_equal(self):
        """Test create_splits with equal type."""
        splits = create_splits(
            amount=Decimal('99.99'),
            split_type=SplitType.EQUAL,
            participant_ids=['user1', 'user2', 'user3']
        )
        
        assert len(splits) == 3
        assert sum(splits.values()) == Decimal('99.99')


class TestDebtSimplifier:
    """Tests for debt simplification algorithm"""
    
    def test_simple_debt_simplification(self):
        """Test basic debt simplification."""
        balances = {
            'Alice': Decimal('50.00'),   # Owed 50
            'Bob': Decimal('-30.00'),    # Owes 30
            'Charlie': Decimal('-20.00'), # Owes 20
        }
        
        transactions = simplify_debts(balances)
        
        # Should need only 2 transactions
        assert len(transactions) <= 2
        
        # Verify correctness
        final_balances = balances.copy()
        for from_user, to_user, amount in transactions:
            final_balances[from_user] += amount
            final_balances[to_user] -= amount
        
        for balance in final_balances.values():
            assert abs(balance) < Decimal('0.01')
    
    def test_complex_debt_simplification(self):
        """Test complex multi-person debt scenario."""
        balances = {
            'A': Decimal('100.00'),
            'B': Decimal('-50.00'),
            'C': Decimal('-30.00'),
            'D': Decimal('-20.00'),
        }
        
        transactions = simplify_debts(balances)
        
        # Should minimize transactions (at most 3)
        assert len(transactions) <= 3
        
        # Verify zero-sum after settlements
        final_balances = balances.copy()
        for from_user, to_user, amount in transactions:
            final_balances[from_user] += amount
            final_balances[to_user] -= amount
        
        for balance in final_balances.values():
            assert abs(balance) < Decimal('0.01')
    
    def test_already_balanced(self):
        """Test when all balances are already zero."""
        balances = {
            'A': Decimal('0.00'),
            'B': Decimal('0.00'),
            'C': Decimal('0.00'),
        }
        
        transactions = simplify_debts(balances)
        
        # Should need no transactions
        assert len(transactions) == 0
    
    def test_calculate_group_balances(self):
        """Test group balance calculation."""
        expenses = [
            {
                'paid_by': 'alice',
                'amount': 100.00,
                'splits': [
                    {'user_id': 'alice', 'amount': 50.00},
                    {'user_id': 'bob', 'amount': 50.00},
                ]
            }
        ]
        
        balances = calculate_group_balances(expenses, [])
        
        # Alice paid 100, owes 50 -> balance = +50
        # Bob paid 0, owes 50 -> balance = -50
        assert balances['alice'] == Decimal('50.00')
        assert balances['bob'] == Decimal('-50.00')
    
    def test_verify_zero_sum_valid(self):
        """Test zero-sum verification with valid balances."""
        balances = {
            'Alice': Decimal('50.00'),
            'Bob': Decimal('-30.00'),
            'Charlie': Decimal('-20.00'),
        }
        
        assert verify_zero_sum(balances) is True
    
    def test_verify_zero_sum_invalid(self):
        """Test zero-sum verification with invalid balances."""
        balances = {
            'Alice': Decimal('50.00'),
            'Bob': Decimal('-30.00'),
            # Missing Charlie's -20, doesn't sum to zero
        }
        
        assert verify_zero_sum(balances) is False
    
    def test_complex_expense_scenario(self):
        """Test realistic multi-expense scenario."""
        expenses = [
            # Alice pays 120 for dinner, split 3 ways
            {
                'paid_by': 'alice',
                'amount': 120.00,
                'splits': [
                    {'user_id': 'alice', 'amount': 40.00},
                    {'user_id': 'bob', 'amount': 40.00},
                    {'user_id': 'charlie', 'amount': 40.00},
                ]
            },
            # Bob pays 60 for movie, split 2 ways
            {
                'paid_by': 'bob',
                'amount': 60.00,
                'splits': [
                    {'user_id': 'bob', 'amount': 30.00},
                    {'user_id': 'charlie', 'amount': 30.00},
                ]
            },
        ]
        
        balances = calculate_group_balances(expenses, [])
        
        # Alice: paid 120, owes 40 = +80
        # Bob: paid 60, owes 70 = -10
        # Charlie: paid 0, owes 70 = -70
        assert balances['alice'] == Decimal('80.00')
        assert balances['bob'] == Decimal('-10.00')
        assert balances['charlie'] == Decimal('-70.00')
        assert verify_zero_sum(balances)


class TestZeroSumInvariant:
    """Critical tests for zero-sum property"""
    
    def test_equal_split_always_zero_sum(self):
        """Test that equal splits always maintain zero-sum."""
        test_cases = [
            (Decimal('100.00'), 3),
            (Decimal('99.99'), 4),
            (Decimal('1000.01'), 7),
            (Decimal('0.01'), 2),
        ]
        
        for amount, num_people in test_cases:
            splits = split_equal(amount, num_people)
            assert sum(splits) == amount, f"Failed for {amount} / {num_people}"
    
    def test_percentage_split_always_zero_sum(self):
        """Test that percentage splits maintain zero-sum."""
        amount = Decimal('1234.56')
        percentages = [Decimal('25.00'), Decimal('25.00'), Decimal('25.00'), Decimal('25.00')]
        
        splits = split_percentage(amount, percentages)
        assert sum(splits) == amount
