'use client';

import { motion } from 'framer-motion';

interface SummaryCardProps {
    title: string;
    amount: number;
    icon: string;
    trend?: string;
    variant?: 'default' | 'success' | 'warning';
}

export function SummaryCard({ title, amount, icon, trend, variant = 'default' }: SummaryCardProps) {
    const variantColors = {
        default: 'text-electric-mint',
        success: 'text-success',
        warning: 'text-warning'
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.3 }}
            className="glass-card p-6 rounded-2xl cursor-pointer"
        >
            <div className="flex items-center justify-between mb-4">
                <span className="text-4xl">{icon}</span>
                {trend && (
                    <motion.span
                        className="text-sm text-electric-mint"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                    >
                        {trend}
                    </motion.span>
                )}
            </div>
            <h3 className="text-slate-grey text-sm font-medium mb-2">{title}</h3>
            <p className={`text-3xl font-bold ${variantColors[variant]}`}>
                ${Math.abs(amount).toFixed(2)}
            </p>
        </motion.div>
    );
}

export function Dashboard({ totalSpent = 0, youOwe = 0, owedToYou = 0 }: {
    totalSpent?: number;
    youOwe?: number;
    owedToYou?: number;
}) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <SummaryCard
                title="Total Spent"
                amount={totalSpent}
                icon="💸"
                trend="+12%"
            />
            <SummaryCard
                title="You Owe"
                amount={youOwe}
                icon="📤"
                variant="warning"
            />
            <SummaryCard
                title="Owed to You"
                amount={owedToYou}
                icon="📥"
                variant="success"
            />
        </div>
    );
}
