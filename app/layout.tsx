import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sturgeon AI - Government Contracting",
  description: "AI-powered government contracting platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
