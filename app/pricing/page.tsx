'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { APIClient } from '@/lib/api';

export default function PricingPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubscribe = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/signup');
        return;
      }
      const { url } = await APIClient.createCheckout();
      window.location.href = url;
    } catch (err) {
      console.error('Checkout failed:', err);
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-gray-600">Choose the plan that's right for you</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Free Plan */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Free</h3>
            <p className="text-4xl font-bold text-gray-900 mb-6">
              $0<span className="text-lg text-gray-600">/month</span>
            </p>
            <ul className="space-y-4 mb-8">
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Basic contract search</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Up to 10 searches per month</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Email support</span>
              </li>
            </ul>
            <a
              href="/signup"
              className="block w-full py-3 px-6 text-center bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
            >
              Get Started
            </a>
          </div>

          {/* Pro Plan */}
          <div className="bg-blue-600 text-white rounded-lg shadow-lg p-8 relative">
            <div className="absolute top-0 right-0 bg-yellow-400 text-gray-900 px-3 py-1 rounded-bl-lg rounded-tr-lg text-sm font-bold">
              POPULAR
            </div>
            <h3 className="text-2xl font-bold mb-4">Pro</h3>
            <p className="text-4xl font-bold mb-6">
              $29<span className="text-lg opacity-80">/month</span>
            </p>
            <ul className="space-y-4 mb-8">
              <li className="flex items-start">
                <svg className="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Unlimited contract searches</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>AI-powered proposal assistance</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Advanced analytics</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Priority support</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Export to PDF</span>
              </li>
            </ul>
            <button
              onClick={handleSubscribe}
              disabled={loading}
              className="block w-full py-3 px-6 text-center bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition font-semibold disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Subscribe Now'}
            </button>
          </div>
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-600">
            All plans include access to our government contract database and basic AI features.
          </p>
        </div>
      </div>
    </div>
  );
}
