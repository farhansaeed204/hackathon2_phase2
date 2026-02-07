'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

// Custom hook for handling API responses and errors
export const useApiErrorHandler = () => {
  const router = useRouter();

  const handleApiError = (error: any, customMessage?: string) => {
    console.error('API Error:', error);

    // Handle different types of errors
    if (error.status === 401) {
      // Unauthorized - JWT token expired or invalid
      toast.error('Session expired. Redirecting to login...');
      // Clear any stored tokens
      localStorage.removeItem('auth-token');
      // Redirect to login after a short delay
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else if (error.status === 404) {
      // Resource not found
      toast.error(error.message || 'Resource not found');
    } else if (error.status >= 500) {
      // Server error
      toast.error(customMessage || 'Server error. Please try again later.');
    } else {
      // Other client errors
      toast.error(error.message || customMessage || 'An error occurred');
    }
  };

  return { handleApiError };
};

// Higher-order component for protecting routes
export function withAuthProtection<T extends object>(
  WrappedComponent: React.ComponentType<T>
): React.FC<T> {
  const AuthenticatedComponent: React.FC<T> = (props) => {
    const router = useRouter();

    useEffect(() => {
      // Check if user is authenticated
      const token = localStorage.getItem('auth-token');
      if (!token) {
        // Redirect to login if not authenticated
        router.push('/login');
      }
    }, [router]);

    return React.createElement(WrappedComponent, props);
  };

  return AuthenticatedComponent;
}