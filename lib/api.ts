import { verifyToken, extractTokenFromHeader } from './auth';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

/**
 * Create a success response
 */
export function createSuccessResponse<T>(data: T, message?: string): ApiResponse<T> {
  return {
    success: true,
    data,
    message,
  };
}

/**
 * Create an error response
 */
export function createErrorResponse(error: string, statusCode: number = 400): Response {
  return new Response(
    JSON.stringify({
      success: false,
      error,
    }),
    {
      status: statusCode,
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
}

/**
 * Authenticate a request using JWT token
 */
export function authenticateRequest(request: Request) {
  const authHeader = request.headers.get('authorization');
  const token = extractTokenFromHeader(authHeader);

  if (!token) {
    return {
      success: false,
      error: 'No token provided',
    };
  }

  const user = verifyToken(token);

  if (!user) {
    return {
      success: false,
      error: 'Invalid or expired token',
    };
  }

  return {
    success: true,
    user,
  };
}

/**
 * Handle API errors consistently
 */
export function handleApiError(error: any): Response {
  console.error('API Error:', error);

  // Handle Supabase errors
  if (error?.message) {
    return createErrorResponse(error.message, 400);
  }

  // Handle Stripe errors
  if (error?.type?.startsWith('Stripe')) {
    return createErrorResponse(error.message || 'Payment error occurred', 400);
  }

  // Generic error
  return createErrorResponse('An unexpected error occurred', 500);
}

/**
 * Validate required fields in a request body
 */
export function validateRequiredFields(body: any, requiredFields: string[]): { valid: boolean; missing?: string[] } {
  const missing = requiredFields.filter((field) => !body[field]);

  if (missing.length > 0) {
    return {
      valid: false,
      missing,
    };
  }

  return { valid: true };
}

/**
 * Set secure cookie with JWT token
 */
export function setAuthCookie(response: Response, token: string, refreshToken: string): void {
  // Set access token cookie (15 minutes)
  response.headers.append(
    'Set-Cookie',
    `auth_token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=900; Path=/`
  );

  // Set refresh token cookie (7 days)
  response.headers.append(
    'Set-Cookie',
    `refresh_token=${refreshToken}; HttpOnly; Secure; SameSite=Strict; Max-Age=604800; Path=/api/auth`
  );
}

/**
 * Clear auth cookies (for logout)
 */
export function clearAuthCookies(response: Response): void {
  response.headers.append(
    'Set-Cookie',
    `auth_token=; HttpOnly; Secure; SameSite=Strict; Max-Age=0; Path=/`
  );
  response.headers.append(
    'Set-Cookie',
    `refresh_token=; HttpOnly; Secure; SameSite=Strict; Max-Age=0; Path=/api/auth`
  );
}

/**
 * Rate limit helper (simple in-memory implementation)
 * NOTE: For production, use a proper rate limiting service like Upstash Rate Limit
 */
const rateLimitCache = new Map<string, { count: number; reset: number }>();

export function checkRateLimit(identifier: string, limit: number = 100, windowMs: number = 60000): boolean {
  const now = Date.now();
  const record = rateLimitCache.get(identifier);

  if (!record || now > record.reset) {
    rateLimitCache.set(identifier, {
      count: 1,
      reset: now + windowMs,
    });
    return true;
  }

  if (record.count >= limit) {
    return false;
  }

  record.count++;
  return true;
}