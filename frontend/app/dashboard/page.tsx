'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Users, Sparkles, TrendingDown } from 'lucide-react';
import Link from 'next/link';
import { Dashboard } from '@/components/Dashboard';
import { BalanceTable } from '@/components/BalanceTable';
import { MintSenseInput } from '@/components/MintSenseInput';
import { ExpenseList } from '@/components/ExpenseList';

// Mock data for development
const MOCK_GROUP_ID = '123e4567-e89b-12d3-a456-426614174000';
const MOCK_USER_ID = '123e4567-e89b-12d3-a456-426614174001';

const MOCK_EXPENSES = [
    {
        id: '1',
        group_id: MOCK_GROUP_ID,
        paid_by: MOCK_USER_ID,
        amount: 120.50,
        description: 'Dinner at Italian Restaurant',
        category: 'Food',
        expense_date: '2026-02-09',
        created_at: '2026-02-09T19:30:00Z',
        payer_name: 'You',
        splits: [
            { id: '1a', user_id: MOCK_USER_ID, amount: 40.17, user_name: 'You' },
            { id: '1b', user_id: '2', amount: 40.17, user_name: 'Alice' },
            { id: '1c', user_id: '3', amount: 40.16, user_name: 'Bob' }
        ]
    },
    {
        id: '2',
        group_id: MOCK_GROUP_ID,
        paid_by: '2',
        amount: 45.00,
        description: 'Uber to Airport',
        category: 'Transport',
        expense_date: '2026-02-08',
        created_at: '2026-02-08T14:20:00Z',
        payer_name: 'Alice',
        splits: [
            { id: '2a', user_id: MOCK_USER_ID, amount: 15.00, user_name: 'You' },
            { id: '2b', user_id: '2', amount: 15.00, user_name: 'Alice' },
            { id: '2c', user_id: '3', amount: 15.00, user_name: 'Bob' }
        ]
    },
    {
        id: '3',
        group_id: MOCK_GROUP_ID,
        paid_by: '3',
        amount: 85.75,
        description: 'Movie Night Tickets',
        category: 'Entertainment',
        expense_date: '2026-02-07',
        created_at: '2026-02-07T20:15:00Z',
        payer_name: 'Bob',
        splits: [
            { id: '3a', user_id: MOCK_USER_ID, amount: 28.58, user_name: 'You' },
            { id: '3b', user_id: '2', amount: 28.58, user_name: 'Alice' },
            { id: '3c', user_id: '3', amount: 28.59, user_name: 'Bob' }
        ]
    },
    {
        id: '4',
        group_id: MOCK_GROUP_ID,
        paid_by: MOCK_USER_ID,
        amount: 200.00,
        description: 'Grocery Shopping',
        category: 'Shopping',
        expense_date: '2026-02-06',
        created_at: '2026-02-06T11:00:00Z',
        payer_name: 'You',
        splits: [
            { id: '4a', user_id: MOCK_USER_ID, amount: 66.67, user_name: 'You' },
            { id: '4b', user_id: '2', amount: 66.67, user_name: 'Alice' },
            { id: '4c', user_id: '3', amount: 66.66, user_name: 'Bob' }
        ]
    }
];

const MOCK_BALANCES = [
    { userId: MOCK_USER_ID, userName: 'You', balance: 76.92 },
    { userId: '2', userName: 'Alice', balance: -23.08 },
    { userId: '3', userName: 'Bob', balance: -53.84 }
];

const MOCK_SETTLEMENTS = [
    { from_user_name: 'Bob', to_user_name: 'You', amount: 53.84 },
    { from_user_name: 'Alice', to_user_name: 'You', amount: 23.08 }
];

export default function DashboardPage() {
    const [expenses, setExpenses] = useState(MOCK_EXPENSES);
    const [showSettlements, setShowSettlements] = useState(false);

    // Calculate summary stats from expenses
    const totalSpent = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const youOwe = MOCK_BALANCES.find(b => b.userId === MOCK_USER_ID)?.balance || 0;
    const youOweAmount = youOwe < 0 ? Math.abs(youOwe) : 0;
    const owedToYou = youOwe > 0 ? youOwe : 0;

    const handleParse = (parsedData: any) => {
        console.log('Parsed expense:', parsedData);
        // In production, this would create the expense via API
        // For now, just log it
    };

    return (
        <div className="min-h-screen bg-charcoal">
            {/* Header */}
            <header className="border-b border-glass-border bg-bg-primary sticky top-0 z-50 backdrop-blur-lg">
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <Link
                                href="/"
                                className="text-slate-grey hover:text-electric-mint transition-colors"
                            >
                                <ArrowLeft className="w-5 h-5" />
                            </Link>
                            <div>
                                <h1 className="text-2xl font-bold">
                                    <span className="text-electric-mint">Split</span>
                                    <span>Mint</span>
                                </h1>
                                <p className="text-sm text-slate-grey">Dashboard</p>
                            </div>
                        </div>
                        <div className="glass-card px-4 py-2 rounded-full flex items-center gap-2">
                            <Users className="w-4 h-4 text-electric-mint" />
                            <span className="text-sm font-medium">Weekend Trip Group</span>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
                {/* MintSense AI Input */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <MintSenseInput
                        groupId={MOCK_GROUP_ID}
                        onParse={handleParse}
                    />
                </motion.div>

                {/* Summary Cards */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <Dashboard
                        totalSpent={totalSpent}
                        youOwe={youOweAmount}
                        owedToYou={owedToYou}
                    />
                </motion.div>

                {/* Two Column Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left Column - Expense List */}
                    <motion.div
                        className="lg:col-span-2"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <ExpenseList expenses={expenses} />
                    </motion.div>

                    {/* Right Column - Balances */}
                    <motion.div
                        className="space-y-6"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        {/* Balance Table */}
                        <BalanceTable balances={MOCK_BALANCES} />

                        {/* Settle Up Card */}
                        <div className="glass-card p-6 rounded-2xl">
                            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                <TrendingDown className="w-5 h-5 text-electric-mint" />
                                Settle Up
                            </h2>
                            <p className="text-slate-grey text-sm mb-4">
                                Minimize transactions with our smart algorithm
                            </p>

                            <button
                                onClick={() => setShowSettlements(!showSettlements)}
                                className="w-full btn-primary flex items-center justify-center gap-2"
                            >
                                <Sparkles className="w-4 h-4" />
                                {showSettlements ? 'Hide' : 'Show'} Settlement Plan
                            </button>

                            {showSettlements && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    className="mt-4 space-y-3"
                                >
                                    {MOCK_SETTLEMENTS.map((settlement, index) => (
                                        <div
                                            key={index}
                                            className="bg-bg-secondary p-4 rounded-lg border border-glass-border"
                                        >
                                            <div className="text-sm">
                                                <span className="font-semibold text-warning">
                                                    {settlement.from_user_name}
                                                </span>
                                                <span className="text-slate-grey mx-2">→</span>
                                                <span className="font-semibold text-success">
                                                    {settlement.to_user_name}
                                                </span>
                                            </div>
                                            <div className="text-xl font-bold text-electric-mint mt-1">
                                                ${settlement.amount.toFixed(2)}
                                            </div>
                                        </div>
                                    ))}
                                    <div className="text-xs text-slate-grey text-center pt-2 border-t border-glass-border">
                                        {MOCK_SETTLEMENTS.length} transaction{MOCK_SETTLEMENTS.length !== 1 ? 's' : ''} to settle all debts
                                    </div>
                                </motion.div>
                            )}
                        </div>
                    </motion.div>
                </div>

                {/* Info Banner */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    className="glass-card p-4 rounded-xl border-electric-mint border-opacity-30"
                >
                    <div className="flex items-start gap-3">
                        <Sparkles className="w-5 h-5 text-electric-mint flex-shrink-0 mt-0.5" />
                        <div>
                            <h3 className="font-semibold text-white mb-1">Demo Mode</h3>
                            <p className="text-sm text-slate-grey">
                                You're viewing mock data. Configure Clerk authentication and Supabase
                                to connect to your real database and enable all features including AI expense parsing.
                            </p>
                        </div>
                    </div>
                </motion.div>
            </main>
        </div>
    );
}
