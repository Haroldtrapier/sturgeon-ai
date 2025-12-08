# Components

## ResetPasswordForm

A simple React component for resetting user passwords using Supabase authentication.

### Usage

```tsx
import ResetPasswordForm from '@/components/ResetPasswordForm';

export default function MyPage() {
  return <ResetPasswordForm />;
}
```

### Features

- Client-side React component with Next.js App Router support
- Integrates with Supabase authentication
- Simple error handling and display
- Automatic redirect to login page on success
- Styled using CSS classes defined in `app/globals.css`

### Dependencies

- `@supabase/supabase-js` - Supabase JavaScript client
- `next/navigation` - Next.js navigation hooks
- `react` - React hooks (useState)

### Notes

- This component assumes that the Supabase session is already established (e.g., via a password reset token from an email link)
- For a more complete implementation with session handling from email tokens, see `/app/reset-password/page.tsx`
- The component uses the Supabase client from `/lib/supabaseClient.ts`
