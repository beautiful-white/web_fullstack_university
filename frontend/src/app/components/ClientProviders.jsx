"use client";
import React, { useEffect } from 'react';
import { useAuth } from '@/shared/store';

export default function ClientProviders({ children }) {
  const initialize = useAuth(state => state.initialize);
  
  useEffect(() => {
    initialize();
  }, [initialize]);

  return (
    <>
      {children}
    </>
  );
} 