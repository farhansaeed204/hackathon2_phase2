'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated by checking for token in localStorage
    const token = localStorage.getItem('auth-token');
    
    // If user is authenticated, redirect to tasks page
    if (token) {
      router.push('/tasks');
    } else {
      // If not authenticated, redirect to login page
      router.push('/login');
    }
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="text-center">
        <p>Redirecting...</p>
      </div>
    </div>
  );
}
