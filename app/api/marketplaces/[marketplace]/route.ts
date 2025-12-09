import { NextRequest, NextResponse } from 'next/server';
import { searchSamGov, formatSamOpportunity } from '@/lib/integrations/samgov';

// Real SAM.gov integration
async function searchSAM(query: string) {
  try {
    // Search last 30 days of active opportunities
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const postedFrom = thirtyDaysAgo.toISOString().split('T')[0];

    const response = await searchSamGov(query, 25, 0, postedFrom, 'yes');

    // Format opportunities for frontend
    const formatted = response.opportunitiesData?.map(formatSamOpportunity) || [];

    return {
      results: formatted,
      total: response.totalRecords || 0,
      source: 'SAM.gov'
    };
  } catch (error: any) {
    console.error('SAM.gov search error:', error);
    throw new Error(`SAM.gov API error: ${error.message}`);
  }
}

// USASpending.gov integration (optional - can add later)
async function searchGovSpend(query: string) {
  // TODO: Implement USASpending.gov API integration
  return {
    results: [],
    total: 0,
    source: 'USASpending.gov',
    message: 'USASpending.gov integration coming soon'
  };
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
    let data;
    switch (marketplace.toLowerCase()) {
      case 'sam':
      case 'samgov':
        data = await searchSAM(query);
        break;
      case 'govspend':
      case 'usaspending':
        data = await searchGovSpend(query);
        break;
      default:
        return NextResponse.json(
          { error: `Unknown marketplace: ${marketplace}. Supported: sam, govspend` },
          { status: 400 }
        );
    }

    return NextResponse.json({
      success: true,
      ...data,
      marketplace,
      query,
    });
  } catch (error: any) {
    console.error('Marketplace search error:', error);
    return NextResponse.json(
      { 
        error: error.message || 'Failed to search marketplace',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined
      },
      { status: 500 }
    );
  }
}
