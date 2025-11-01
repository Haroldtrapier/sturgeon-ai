import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sturgeon AI - Government Contracting Platform",
  description: "AI-powered government contracting and grant management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
