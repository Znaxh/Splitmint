'use client';

import { motion } from 'framer-motion';
import { ArrowUp, ArrowDown } from 'lucide-react';

interface Balance {
    userId: string;
    userName: string;
    balance: number;
}

export function BalanceTable({ balances }: { balances: Balance[] }) {
    return (
        <div className="glass-card p-6 rounded-2xl">
            <h2 className="text-xl font-semibold mb-6">Group Balances</h2>

            <div className="space-y-4">
                {balances.map((balance) => (
                    <motion.div
                        key={balance.userId}
                        className="flex items-center justify-between p-4 bg-bg-secondary rounded-lg hover:bg-bg-tertiary transition-colors"
                        whileHover={{ scale: 1.02 }}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                    >
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-electric-mint bg-opacity-20 rounded-full flex items-center justify-center">
                                <span className="text-electric-mint font-semibold">
                                    {balance.userName.charAt(0).toUpperCase()}
                                </span>
                            </div>
                            <span className="font-medium">{balance.userName}</span>
                        </div>

                        <div className="flex items-center gap-2">
                            {balance.balance > 0 ? (
                                <>
                                    <span className="text-success font-semibold">
                                        +${Math.abs(balance.balance).toFixed(2)}
                                    </span>
                                    <ArrowUp className="w-5 h-5 text-success" />
                                </>
                            ) : balance.balance < 0 ? (
                                <>
                                    <span className="text-warning font-semibold">
                                        ${Math.abs(balance.balance).toFixed(2)}
                                    </span>
                                    <ArrowDown className="w-5 h-5 text-warning" />
                                </>
                            ) : (
                                <span className="text-slate-grey">Settled</span>
                            )}
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
