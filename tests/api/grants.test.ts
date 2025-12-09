// Example API Test
// tests/api/grants.test.ts

import { createMocks } from 'node-mocks-http';
import handler from '@/pages/api/grants/search';

describe('/api/grants/search', () => {
  it('returns grants successfully', async () => {
    const { req, res } = createMocks({
      method: 'POST',
      body: {
        keyword: 'research'
      }
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    const data = JSON.parse(res._getData());
    expect(data).toHaveProperty('grants');
    expect(Array.isArray(data.grants)).toBe(true);
  });

  it('handles empty search', async () => {
    const { req, res } = createMocks({
      method: 'POST',
      body: {}
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(200);
  });

  it('rejects non-POST requests', async () => {
    const { req, res } = createMocks({
      method: 'GET'
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(405);
  });
});
