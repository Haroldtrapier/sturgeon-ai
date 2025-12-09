// SAM.gov API Integration
// API Documentation: https://open.gsa.gov/api/opportunities-api/

const SAM_API_KEY = process.env.SAM_GOV_API_KEY || '';
const SAM_BASE_URL = 'https://api.sam.gov/opportunities/v2/search';

export interface SamOpportunity {
  noticeId: string;
  title: string;
  solicitationNumber?: string;
  department?: string;
  subTier?: string;
  office?: string;
  postedDate?: string;
  type?: string;
  baseType?: string;
  archiveType?: string;
  archiveDate?: string;
  typeOfSetAsideDescription?: string;
  responseDeadLine?: string;
  naicsCode?: string;
  classificationCode?: string;
  active?: string;
  award?: {
    date?: string;
    number?: string;
    amount?: string;
    awardee?: {
      name?: string;
      duns?: string;
      location?: {
        city?: string;
        state?: string;
      };
    };
  };
  pointOfContact?: Array<{
    type?: string;
    title?: string;
    fullName?: string;
    email?: string;
    phone?: string;
    fax?: string;
  }>;
  description?: string;
  organizationType?: string;
  officeAddress?: {
    city?: string;
    state?: string;
    country?: string;
  };
  placeOfPerformance?: {
    city?: {
      name?: string;
    };
    state?: {
      name?: string;
    };
    country?: {
      name?: string;
    };
  };
  additionalInfoLink?: string;
  uiLink?: string;
  links?: Array<{
    rel?: string;
    href?: string;
  }>;
}

export interface SamSearchResponse {
  totalRecords: number;
  opportunitiesData: SamOpportunity[];
}

/**
 * Search SAM.gov opportunities
 * @param query - Search query string
 * @param limit - Number of results to return (max 1000)
 * @param offset - Pagination offset
 * @param postedFrom - Filter by posted date (YYYY-MM-DD)
 * @param active - Filter active opportunities (yes/no)
 */
export async function searchSamGov(
  query: string,
  limit: number = 10,
  offset: number = 0,
  postedFrom?: string,
  active: string = 'yes'
): Promise<SamSearchResponse> {
  if (!SAM_API_KEY) {
    throw new Error('SAM_GOV_API_KEY environment variable is not set');
  }

  const params = new URLSearchParams({
    api_key: SAM_API_KEY,
    q: query,
    limit: limit.toString(),
    offset: offset.toString(),
  });

  if (postedFrom) {
    params.append('postedFrom', postedFrom);
  }

  if (active) {
    params.append('active', active);
  }

  const url = `${SAM_BASE_URL}?${params.toString()}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`SAM.gov API error (${response.status}): ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('SAM.gov API request failed:', error);
    throw error;
  }
}

/**
 * Get opportunity details by Notice ID
 */
export async function getOpportunityDetails(noticeId: string): Promise<SamOpportunity> {
  if (!SAM_API_KEY) {
    throw new Error('SAM_GOV_API_KEY environment variable is not set');
  }

  const url = `https://api.sam.gov/opportunities/v2/search?api_key=${SAM_API_KEY}&noticeId=${noticeId}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch opportunity details: ${response.status}`);
    }

    const data = await response.json();
    return data.opportunitiesData?.[0] || null;
  } catch (error) {
    console.error('Failed to get opportunity details:', error);
    throw error;
  }
}

/**
 * Format SAM.gov opportunity for display
 */
export function formatSamOpportunity(opp: SamOpportunity) {
  return {
    id: opp.noticeId,
    title: opp.title,
    solicitation: opp.solicitationNumber,
    agency: opp.department || opp.subTier || 'Unknown Agency',
    office: opp.office,
    status: opp.active === 'Yes' ? 'Active' : 'Archived',
    type: opp.type,
    postedDate: opp.postedDate,
    responseDeadline: opp.responseDeadLine,
    naicsCode: opp.naicsCode,
    setAside: opp.typeOfSetAsideDescription,
    description: opp.description,
    pointOfContact: opp.pointOfContact?.[0],
    link: opp.uiLink,
    source: 'SAM.gov',
  };
}
