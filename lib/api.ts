// Call Next.js API routes instead of external backend
const API_BASE_URL = '/api'; // Internal Next.js API routes

export class APIClient {
  private static getHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  static async register(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }
    return response.json();
  }

  static async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
  }

  static async getProfile() {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch profile');
    }
    return response.json();
  }

  static async createCheckout() {
    const response = await fetch(`${API_BASE_URL}/payments/create-checkout`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to create checkout');
    }
    return response.json();
  }

  static logout() {
    localStorage.removeItem('token');
  }
}

// API Response helper functions for server-side routes
import { NextResponse } from 'next/server';

export function createSuccessResponse(data: any, message?: string) {
  return {
    success: true,
    data,
    message,
  };
}

export function createErrorResponse(message: string, status: number = 500) {
  return NextResponse.json(
    {
      success: false,
      error: message,
    },
    { status }
  );
}

export function setAuthCookie(response: NextResponse, token: string, refreshToken: string) {
  // Set access token cookie
  response.cookies.set('access_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 15, // 15 minutes
    path: '/',
  });

  // Set refresh token cookie
  response.cookies.set('refresh_token', refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
    path: '/',
  });
}

export function clearAuthCookies(response: NextResponse) {
  response.cookies.delete('access_token');
  response.cookies.delete('refresh_token');
}
