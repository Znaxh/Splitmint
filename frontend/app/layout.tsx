import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SplitMint - Smart Expense Sharing",
  description: "AI-powered expense sharing platform with smart debt settlement and real-time updates",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
