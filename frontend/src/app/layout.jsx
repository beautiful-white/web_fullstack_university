import React from 'react';
import ClientProviders from './components/ClientProviders';
import Navigation from './components/Navigation';
import "./globals.css";

export const metadata = {
  title: "Ресторанный сервис",
  description: "Сервис для бронирования столиков в ресторанах",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body>
        <ClientProviders>
          <Navigation />
          <main>
            {children}
          </main>
        </ClientProviders>
      </body>
    </html>
  );
}
