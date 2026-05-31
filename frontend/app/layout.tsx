import type { Metadata } from "next";
import { Navigation } from "@/components/Navigation";
import "./globals.css";

export const metadata: Metadata = {
  title: "routAIne",
  description: "AI-powered adaptive planner and scheduler",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <Navigation />
        <main style={{ padding: "1.25rem" }}>{children}</main>
      </body>
    </html>
  );
}
