# 💳 Dual Payment Setup Guide - Stripe & Square

## Overview
Sturgeon AI now supports **both Stripe AND Square** for payment processing. Customers can choose their preferred provider at checkout.

---

## 🚀 Quick Start

### Environment Variables Required

Add these to your Vercel/hosting environment:

```bash
# === STRIPE (Required) ===
STRIPE_SECRET_KEY=sk_test_... # or sk_live_... for production
STRIPE_WEBHOOK_SECRET=whsec_...

# === SQUARE (Optional but Recommended) ===
SQUARE_ACCESS_TOKEN=EAAl...
SQUARE_LOCATION_ID=L...
SQUARE_ENVIRONMENT=sandbox  # or "production"

# === APP CONFIGURATION ===
FRONTEND_URL=https://sturgeon-ai-prod.vercel.app
ENVIRONMENT=development  # or "production"
JWT_SECRET=your-secret-key
```

---

## 📋 Step-by-Step Setup

### 1. Stripe Setup (5 minutes)

#### Get Stripe Credentials:
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
2. Copy your **Secret Key** (starts with `sk_test_` or `sk_live_`)
3. Add to Vercel: `STRIPE_SECRET_KEY=sk_...`

#### Setup Stripe Webhooks:
1. Go to [Stripe Webhooks](https://dashboard.stripe.com/webhooks)
2. Click "Add endpoint"
3. Enter URL: `https://your-domain.com/webhooks/stripe`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. Copy **Signing secret** (starts with `whsec_`)
6. Add to Vercel: `STRIPE_WEBHOOK_SECRET=whsec_...`

---

### 2. Square Setup (5 minutes)

#### Get Square Credentials:
1. Go to [Square Developer Dashboard](https://developer.squareup.com/apps)
2. Create or select your app
3. Go to **"Credentials"** tab

#### For Testing (Sandbox):
4. Switch to **"Sandbox"** tab
5. Copy **Sandbox Access Token** (starts with `EAAl`)
6. Copy **Sandbox Test Location** ID (starts with `L`)
7. Add to Vercel:
   ```bash
   SQUARE_ACCESS_TOKEN=EAAl...
   SQUARE_LOCATION_ID=L...
   SQUARE_ENVIRONMENT=sandbox
   ```

#### For Production:
4. Switch to **"Production"** tab
5. Copy **Production Access Token**
6. Copy **Production Location** ID
7. Update Vercel:
   ```bash
   SQUARE_ACCESS_TOKEN=EAAl...  # Production token
   SQUARE_LOCATION_ID=L...       # Production location
   SQUARE_ENVIRONMENT=production
   ```

#### Setup Square Webhooks:
1. In Square Developer Dashboard → **Webhooks**
2. Add endpoint: `https://your-domain.com/webhooks/square`
3. Subscribe to: `payment.created`, `payment.updated`

---

## 🧪 Testing

### Test Cards - Stripe (Sandbox/Test Mode):
```
Visa: 4242 4242 4242 4242
Mastercard: 5555 5555 5555 4444
Amex: 3782 822463 10005

CVV: Any 3 digits
Expiry: Any future date
ZIP: Any 5 digits
```

### Test Cards - Square (Sandbox):
```
Visa: 4111 1111 1111 1111
Mastercard: 5105 1051 0510 5100
Discover: 6011 0000 0000 0004

CVV: Any 3 digits
Expiry: Any future date
ZIP: Any valid ZIP
```

---

## 🔌 API Endpoints

### Get Available Plans
```bash
GET /payment/plans

Response:
{
  "plans": {
    "pro": {
      "name": "Sturgeon AI Pro",
      "price": 29.00,
      "currency": "USD",
      "interval": "month",
      "features": [...]
    },
    "enterprise": {...}
  }
}
```

### Create Checkout Session
```bash
POST /payments/create-checkout
Headers: Authorization: Bearer <JWT_TOKEN>
Body:
{
  "plan": "pro",  # or "enterprise"
  "provider": "stripe",  # or "square"
  "success_url": "https://your-domain.com/success" # optional
  "cancel_url": "https://your-domain.com/cancel"   # optional
}

Response:
{
  "provider": "stripe",
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_..."
}
```

---

## 🎯 Frontend Integration Example

```typescript
// Create checkout session
const createCheckout = async (plan: 'pro' | 'enterprise', provider: 'stripe' | 'square') => {
  const response = await fetch('/payments/create-checkout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${userToken}`
    },
    body: JSON.stringify({
      plan,
      provider,
      success_url: window.location.origin + '/success',
      cancel_url: window.location.origin + '/pricing'
    })
  });

  const { checkout_url } = await response.json();

  // Redirect to checkout
  window.location.href = checkout_url;
};

// Usage
<button onClick={() => createCheckout('pro', 'stripe')}>
  Pay with Stripe
</button>
<button onClick={() => createCheckout('pro', 'square')}>
  Pay with Square
</button>
```

---

## 🔒 Security Features

✅ **Rate Limiting**: 20 requests/minute on payment endpoints
✅ **JWT Authentication**: All payment endpoints require valid JWT
✅ **Webhook Validation**: Stripe signatures verified
✅ **HTTPS Only**: All payment data encrypted in transit
✅ **PCI Compliant**: No card data touches your servers

---

## 🐛 Troubleshooting

### "Square payment provider not configured"
- **Cause**: Missing `SQUARE_ACCESS_TOKEN` environment variable
- **Fix**: Add Square credentials to Vercel or disable Square provider

### "Stripe error: No such price"
- **Cause**: Price not created in Stripe Dashboard
- **Fix**: We create prices on-the-fly, check `STRIPE_SECRET_KEY` is correct

### "Invalid location_id"
- **Cause**: Wrong Square Location ID
- **Fix**: Get Location ID from Square Dashboard → Locations

### Webhook not receiving events
- **Cause**: Webhook URL not configured or incorrect
- **Fix**: Verify webhook URLs in Stripe/Square dashboards match your domain

---

## 📊 Monitoring

Check payment provider status:
```bash
GET /

Response:
{
  "message": "Sturgeon AI API",
  "status": "online",
  "payment_providers": {
    "stripe": true,
    "square": true
  }
}
```

---

## 🚀 Go Live Checklist

- [ ] Switch Stripe from test to live keys (`sk_live_...`)
- [ ] Switch Square from sandbox to production
- [ ] Update webhook URLs to production domain
- [ ] Test one real $1 transaction on each provider
- [ ] Verify webhooks are working in production
- [ ] Monitor first 10 transactions closely

---

## 💡 Pro Tips

1. **Start with Sandbox**: Test everything in sandbox/test mode first
2. **One Provider**: You can start with just Stripe, add Square later
3. **Webhooks Are Critical**: Without webhooks, subscriptions won't update properly
4. **Test Failed Payments**: Use Stripe test cards that decline to test error handling
5. **Monitor Logs**: Check Vercel/server logs for webhook delivery issues

---

## 📞 Support

- Stripe Support: https://support.stripe.com
- Square Support: https://squareup.com/help
- Sturgeon AI Issues: GitHub Issues

---

**Ready to accept payments! 🎉**
