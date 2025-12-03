import { NextRequest, NextResponse } from 'next/server';

// Mock data generator for different marketplaces
function generateMockResults(marketplace: string, query: string) {
  const agencies = [
    'Department of Defense',
    'Department of Homeland Security',
    'Department of Veterans Affairs',
    'General Services Administration',
    'Department of Energy',
    'NASA',
  ];

  const statuses = ['Active', 'Pre-Solicitation', 'Award Pending', 'Archived'];

  return Array.from({ length: 5 }, (_, i) => ({
    id: `${marketplace}-${Date.now()}-${i}`,
    title: `${query} - ${marketplace.toUpperCase()} Opportunity ${i + 1}`,
    agency: agencies[Math.floor(Math.random() * agencies.length)],
    status: statuses[Math.floor(Math.random() * statuses.length)],
    source: marketplace,
  }));
}

// TODO: Implement real API integrations
async function searchSAM(query: string) {
  return generateMockResults('sam', query);
}

async function searchGovWin(query: string) {
  return generateMockResults('govwin', query);
}

async function searchGovSpend(query: string) {
  return generateMockResults('govspend', query);
}

async function searchUnison(query: string) {
  return generateMockResults('unison', query);
}

export async function GET(
  request: NextRequest,
  { params }: { params: { marketplace: string } }
) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('q');

    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter "q" is required' },
        { status: 400 }
      );
    }

    const { marketplace } = params;

    // Route to appropriate search function
    let results;
    switch (marketplace.toLowerCase()) {
      case 'sam':
        results = await searchSAM(query);
        break;
      case 'govwin':
        results = await searchGovWin(query);
        break;
      case 'govspend':
        results = await searchGovSpend(query);
        break;
      case 'unison':
        results = await searchUnison(query);
        break;
      default:
        return NextResponse.json(
          { error: `Unknown marketplace: ${marketplace}` },
          { status: 400 }
        );
    }

    return NextResponse.json({
      success: true,
      results,
      marketplace,
      query,
    });
  } catch (error) {
    console.error('Marketplace search error:', error);
    return NextResponse.json(
      { error: 'Failed to search marketplace' },
      { status: 500 }
    );
  }
}
