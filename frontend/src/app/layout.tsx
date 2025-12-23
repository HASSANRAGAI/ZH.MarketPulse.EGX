import type { Metadata } from "next";
import "./globals.scss";
import "@syncfusion/ej2-base/styles/material3-dark.css";
import "@syncfusion/ej2-react-layouts/styles/material3-dark.css";
import "@syncfusion/ej2-react-navigations/styles/material3-dark.css";
import "@syncfusion/ej2-react-dropdowns/styles/material3-dark.css";
import SyncfusionLicense from "../components/SyncfusionLicense";

export const metadata: Metadata = {
  title: "Market Pulse EGX",
  description: "Egyptian Stock Exchange Market Pulse Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <SyncfusionLicense />
        {children}
      </body>
    </html>
  );
}
