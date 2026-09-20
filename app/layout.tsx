import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '5OS Excel',
  description: 'Oefenportaal rekenblad — Sint-Michiel',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="nl">
      <body>{children}</body>
    </html>
  );
}
