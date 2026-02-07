const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export interface LoginResponse {
  success: boolean;
  token?: string;
  error?: string;
  user?: {
    id: string;
    email: string;
    name?: string;
  };
}

export interface SignupResponse {
  success: boolean;
  token?: string;
  error?: string;
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store the token in localStorage
      localStorage.setItem('auth-token', data.token);

      // Set the auth token cookie
      document.cookie = `auth-token=${data.token}; path=/;`;

      return {
        success: true,
        token: data.token,
        user: data.user,
      };
    } else {
      return {
        success: false,
        error: data.detail || 'Login failed',
      };
    }
  } catch (error) {
    console.error('Login error:', error);
    return {
      success: false,
      error: 'Network error or server unavailable',
    };
  }
};

export const signup = async (email: string, password: string, name?: string): Promise<SignupResponse> => {
  try {
    const response = await fetch(`${BACKEND_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store the token in localStorage
      localStorage.setItem('auth-token', data.token);

      // Set the auth token cookie
      document.cookie = `auth-token=${data.token}; path=/;`;

      return {
        success: true,
        token: data.token,
      };
    } else {
      return {
        success: false,
        error: data.detail || 'Signup failed',
      };
    }
  } catch (error) {
    console.error('Signup error:', error);
    return {
      success: false,
      error: 'Network error or server unavailable',
    };
  }
};

export const logout = async (): Promise<boolean> => {
  try {
    // Remove the token from localStorage
    localStorage.removeItem('auth-token');

    // Remove the auth token cookie if it exists
    document.cookie = 'auth-token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

    return true;
  } catch (error) {
    console.error('Logout error:', error);
    return false;
  }
};

// Function to get the current user from the stored token
export const getCurrentUser = async (): Promise<any> => {
  const token = localStorage.getItem('auth-token');
  
  if (!token) {
    return null;
  }

  try {
    const response = await fetch(`${BACKEND_URL}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      return await response.json();
    } else {
      return null;
    }
  } catch (error) {
    console.error('Get current user error:', error);
    return null;
  }
};