const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

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

  static async login(email: string, password: string)) {
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