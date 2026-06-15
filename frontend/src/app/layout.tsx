import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import { PlatformProvider } from "@/components/platform-context";
import { PlatformShell } from "@/components/platform-shell";
import { OrganizationProvider } from "@/components/organization-context";

import "@/styles/theme.css";
import "./globals.css";
import "@/styles/legacy-compat.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CamPigen",
  description: "Next.js frontend for CamPigen backend APIs",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body>
        <PlatformProvider>
          <OrganizationProvider>
            <PlatformShell>{children}</PlatformShell>
          </OrganizationProvider>
        </PlatformProvider>
      </body>
    </html>
  );
}
