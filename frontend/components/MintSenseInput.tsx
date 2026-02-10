'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';

interface MintSenseInputProps {
    groupId: string;
    onParse?: (parsedData: any) => void;
}

export function MintSenseInput({ groupId, onParse }: MintSenseInputProps) {
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleParse = async () => {
        if (!input.trim()) return;

        setIsLoading(true);
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/expenses/parse`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: input,
                    groupId
                }),
            });

            if (response.ok) {
                const parsed = await response.json();
                onParse?.(parsed);
                setInput('');
            }
        } catch (error) {
            console.error('Failed to parse expense:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleParse();
        }
    };

    return (
        <div className="relative">
            <motion.div
                className="relative"
                whileFocus={{ scale: 1.01 }}
            >
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Try: 'Paid $120 for dinner with Alice and Bob yesterday'"
                    className="w-full px-6 py-4 pr-32 bg-bg-secondary border border-glass-border rounded-full
                     focus:border-electric-mint focus:outline-none transition-colors text-white
                     placeholder:text-slate-grey"
                    disabled={isLoading}
                />

                <motion.button
                    onClick={handleParse}
                    disabled={isLoading || !input.trim()}
                    className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 
                     bg-electric-mint text-charcoal font-semibold rounded-full
                     hover:bg-accent-hover transition-colors disabled:opacity-50
                     disabled:cursor-not-allowed flex items-center gap-2"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    {isLoading ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                        <Sparkles className="w-4 h-4" />
                    )}
                    <span>{isLoading ? 'Parsing...' : 'Parse'}</span>
                </motion.button>
            </motion.div>

            <div className="mt-3 flex items-center gap-2 text-sm text-slate-grey">
                <Sparkles className="w-4 h-4" />
                <span>Powered by MintSense AI</span>
            </div>
        </div>
    );
}
