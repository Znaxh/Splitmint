'use client';

import { motion } from 'framer-motion';
import { Calendar, User, TrendingUp } from 'lucide-react';

interface ExpenseSplit {
    id: string;
    user_id: string;
    amount: number;
    user_name?: string;
}

interface Expense {
    id: string;
    group_id: string;
    paid_by: string;
    amount: number;
    description: string;
    category: string;
    expense_date: string;
    created_at: string;
    payer_name?: string;
    splits: ExpenseSplit[];
}

const categoryEmojis: { [key: string]: string } = {
    'food': '🍕',
    'transport': '🚗',
    'entertainment': '🎬',
    'utilities': '💡',
    'shopping': '🛍️',
    'other': '📦'
};

const categoryColors: { [key: string]: string } = {
    'food': 'text-orange-400',
    'transport': 'text-blue-400',
    'entertainment': 'text-purple-400',
    'utilities': 'text-yellow-400',
    'shopping': 'text-pink-400',
    'other': 'text-slate-400'
};

export function ExpenseList({ expenses }: { expenses: Expense[] }) {
    if (expenses.length === 0) {
        return (
            <div className="glass-card p-8 rounded-2xl text-center">
                <div className="text-6xl mb-4">💸</div>
                <h3 className="text-xl font-semibold mb-2">No expenses yet</h3>
                <p className="text-slate-grey">
                    Add your first expense using MintSense AI above
                </p>
            </div>
        );
    }

    return (
        <div className="glass-card p-6 rounded-2xl">
            <h2 className="text-xl font-semibold mb-6">Recent Expenses</h2>

            <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                {expenses.map((expense, index) => (
                    <motion.div
                        key={expense.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className="bg-bg-secondary rounded-xl p-4 hover:bg-bg-tertiary transition-colors"
                    >
                        {/* Header */}
                        <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center gap-3">
                                <div className={`text-3xl ${categoryColors[expense.category.toLowerCase()] || categoryColors.other}`}>
                                    {categoryEmojis[expense.category.toLowerCase()] || categoryEmojis.other}
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white">
                                        {expense.description}
                                    </h4>
                                    <div className="flex items-center gap-2 text-sm text-slate-grey mt-1">
                                        <User className="w-3 h-3" />
                                        <span>Paid by {expense.payer_name || 'Unknown'}</span>
                                    </div>
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="text-xl font-bold text-electric-mint">
                                    ${expense.amount.toFixed(2)}
                                </div>
                                <div className="flex items-center gap-1 text-xs text-slate-grey mt-1">
                                    <Calendar className="w-3 h-3" />
                                    {new Date(expense.expense_date).toLocaleDateString('en-US', {
                                        month: 'short',
                                        day: 'numeric'
                                    })}
                                </div>
                            </div>
                        </div>

                        {/* Splits */}
                        {expense.splits && expense.splits.length > 0 && (
                            <div className="border-t border-glass-border pt-3 mt-3">
                                <div className="text-xs text-slate-grey mb-2">Split between:</div>
                                <div className="flex flex-wrap gap-2">
                                    {expense.splits.map((split) => (
                                        <div
                                            key={split.id}
                                            className="flex items-center gap-1 bg-bg-tertiary px-3 py-1 rounded-full text-sm"
                                        >
                                            <span className="text-white">
                                                {split.user_name || 'User'}
                                            </span>
                                            <span className="text-slate-grey">•</span>
                                            <span className="text-electric-mint font-medium">
                                                ${split.amount.toFixed(2)}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
