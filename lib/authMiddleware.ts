// Utility: Auth Middleware
import { NextApiRequest, NextApiResponse } from 'next';
import { supabaseAdmin } from './supabase';

export interface AuthenticatedRequest extends NextApiRequest {
  user: {
    id: string;
    email: string;
    [key: string]: any;
  };
}

export async function requireAuth(
  req: NextApiRequest,
  res: NextApiResponse
): Promise<AuthenticatedRequest | null> {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    res.status(401).json({ error: 'Unauthorized - No token provided' });
    return null;
  }

  const token = authHeader.replace('Bearer ', '');

  try {
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(token);

    if (error || !user) {
      res.status(401).json({ error: 'Unauthorized - Invalid token' });
      return null;
    }

    (req as AuthenticatedRequest).user = user;
    return req as AuthenticatedRequest;
  } catch (error) {
    res.status(401).json({ error: 'Unauthorized - Authentication failed' });
    return null;
  }
}
