import React from 'react';
import "./globals.css";

export const metadata = {
  title: "Ресторанный сервис",
  description: "Сервис для бронирования столиков в ресторанах",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body>
        {children}
      </body>
    </html>
  );
}
