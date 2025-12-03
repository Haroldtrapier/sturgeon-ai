import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/server/auth';

// Stripe configuration
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
const NEXT_PUBLIC_URL = process.env.NEXT_PUBLIC_URL || 'http://localhost:3000';

// Plan price IDs (replace with your actual Stripe Price IDs)
const PLAN_PRICES = {
  pro: process.env.STRIPE_PRO_PRICE_ID || 'price_pro_monthly',
  enterprise: process.env.STRIPE_ENTERPRISE_PRICE_ID || 'price_enterprise_monthly',
};

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions);
    if (!session?.user?.email) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { plan } = body;

    // Validate plan
    if (!plan || !['pro', 'enterprise'].includes(plan)) {
      return NextResponse.json(
        { error: 'Invalid plan. Must be "pro" or "enterprise"' },
        { status: 400 }
      );
    }

    // Check if Stripe is configured
    if (!STRIPE_SECRET_KEY) {
      console.error('Stripe is not configured. Add STRIPE_SECRET_KEY to environment variables.');

      // Return mock checkout URL for development
      return NextResponse.json({
        success: true,
        url: `${NEXT_PUBLIC_URL}/billing/success?plan=${plan}`,
        message: 'Development mode: Stripe not configured',
      });
    }

    // In production, create actual Stripe checkout session
    // Uncomment and configure when Stripe is set up:
    /*
    const stripe = require('stripe')(STRIPE_SECRET_KEY);

    const checkoutSession = await stripe.checkout.sessions.create({
      customer_email: session.user.email,
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [
        {
          price: PLAN_PRICES[plan],
          quantity: 1,
        },
      ],
      success_url: `${NEXT_PUBLIC_URL}/billing/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${NEXT_PUBLIC_URL}/billing?canceled=true`,
      metadata: {
        userId: session.user.id,
        plan: plan,
      },
    });

    return NextResponse.json({
      success: true,
      url: checkoutSession.url,
    });
    */

    // Development fallback
    return NextResponse.json({
      success: true,
      url: `${NEXT_PUBLIC_URL}/billing/success?plan=${plan}&dev=true`,
      message: 'Development mode: Using mock checkout',
    });

  } catch (error) {
    console.error('Checkout error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to create checkout session',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
