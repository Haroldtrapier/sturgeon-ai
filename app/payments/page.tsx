'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface PricePlan {
  id: string;
  name: 'Free' | 'Pro' | 'Enterprise';
  price: number;
  priceId: string; // Stripe Price ID
  features: string[];
  popular?: boolean;
  buttonLabel: string;
}

const pricingPlans: PricePlan[] = [
  {
    id: 'free',
    name: 'Free',
    price: 0,
    priceId: '', // No Stripe ID for free plan
    features: [
      '100 queries/month',
      'Basic analytics',
      'Community support',
      'Standard models',
    ],
    buttonLabel: 'Current Plan',
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 29,
    priceId: 'price_1ProExamplePriceID', // Replace with real Stripe Price ID
    features: [
      'Unlimited queries',
      'Advanced analytics',
      'Priority support',
      'Advanced models',
      'Custom integrations',
    ],
    popular: true,
    buttonLabel: 'Upgrade to Pro',
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 99,
    priceId: 'price_1EnterpriseExamplePriceID', // Replace with real Stripe Price ID
    features: [
      'Unlimited everything',
      'Dedicated support',
      'Custom models',
      'Private instances',
      'SLA guarantee',
      'On-premise deployment',
    ],
    buttonLabel: 'Contact Sales',
  },
];

export default function PaymentsPage() {
  const router = useRouter();
  const [currentPlan, setCurrentPlan] = useState<string>('free');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          router.push('/login');
          return;
        }

        const response = await fetch('/api/payments/subscription', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setCurrentPlan(data.plan || 'free');
        }
      } catch (err) {
        console.error('Failed to fetch subscription:', err);
      }
    };

    fetchSubscription();
  }, [router]);

  const handleUpgrade = async (priceId: string, planId: string) => {
    if (planId === 'free') {
      return; // Already on free plan
    }

    if (planId === 'enterprise') {
      // Redirect to contact page or open email
      window.location.href = 'mailto:sales@sturgeon-ai.com?subject=Enterprise%20Plan%20Inquiry';
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('auth_token');

      if (!token) {
        router.push('/login');
        return;
      }

      // Create Stripe checkout session
      const response = await fetch('/api/payments/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ priceId }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to create checkout session');
      }

      const data = await response.json();

      // Redirect to Stripe Checkout
      if (data.checkoutUrl) {
        window.location.href = data.checkoutUrl;
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800">Choose Your Plan</h1>
          <p className="text-xl text-gray-600 mt-4">
            Upgrade to unlock more features and capabilities
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-8 max-w-2xl mx-auto">
            {error}
          </div>
        )}

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {pricingPlans.map((plan) => (
            <div
              key={plan.id}
              className={`bg-white rounded-xl shadow-lg p-8 ${
                plan.popular ? 'ring-2 ring-blue-500 relative' : ''
              }`}
            >
              {plan.popular && (
                <span className="absolute top-0 right-6 transform translate-y-1/2 bg-blue-600 text-white px-4 py-1 text-sm font-medium rounded-full">
                  Popular
                </span>
              )}

              <h3 className="text-2xl font-bold text-gray-800">{plan.name}</h3>
              <div className="mt-4">
                <span className="text-4xl font-bold text-gray-800">
$p{plan.price}</span>
                <span className="text-gray-600">/month</span>
              </div>

              <ul className="mt-6 space-y-3">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center gap-2">
                    <span className="text-green-500">✅</span>
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleUpgrade(plan.priceId, plan.id)}
                disabled={isLoading || currentPlan === plan.id}
                className={`w-full mt-8 py-3 px-6 rounded-lg font-medium transition ${
                  currentPlan === plan.id
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : plan.popular
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-gray-800 hover:bg-gray-900 text-white'
                }`}
              >
                {currentPlan === plan.id ? 'Current Plan' : plan.buttonLabel}
              </button>
            </div>
          ))}
        </div>

        {/* FAQ or Additional Info */}
        <div className="text-center mt-16">
          <p className="text-gray-600">
            All plans include 30-day money-back guarantee. No questions asked.
          </p>
          <a href="/help" className="text-blue-600 hover:text-blue-500 mt-4 inline-block">
            Need help choosing? Contact support
          </a>
        </div>
      </div>
    </div>
  );
}