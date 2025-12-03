import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/server/auth';

// GET - Fetch user profile
export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { data: profile, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('user_id', session.user.id)
      .single();

    if (error && error.code !== 'PGRST116') {
      // PGRST116 is "not found" error, which is okay for first-time users
      console.error('Error fetching profile:', error);
      throw error;
    }

    return NextResponse.json({
      success: true,
      profile: profile || null,
    });
  } catch (error) {
    console.error('Error fetching profile:', error);
    return NextResponse.json(
      { error: 'Failed to fetch profile' },
      { status: 500 }
    );
  }
}

// POST - Update/create user profile
export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();

    // Validate required fields
    if (!body.companyName || body.companyName.trim() === '') {
      return NextResponse.json(
        { error: 'Company name is required' },
        { status: 400 }
      );
    }

    // Prepare profile data
    const profileData = {
      user_id: session.user.id,
      company_name: body.companyName,
      naics_codes: body.naicsCodes || [],
      psc_codes: body.pscCodes || [],
      cage_code: body.cageCode || null,
      duns: body.duns || null,
      capabilities_summary: body.capabilitiesSummary || null,
      certifications: body.certifications || [],
      phone: body.phone || null,
      website: body.website || null,
      updated_at: new Date().toISOString(),
    };

    // Upsert profile (insert or update)
    const { data, error } = await supabase
      .from('profiles')
      .upsert(profileData, {
        onConflict: 'user_id',
      })
      .select()
      .single();

    if (error) {
      console.error('Error upserting profile:', error);
      throw error;
    }

    return NextResponse.json({
      success: true,
      profile: data,
      message: 'Profile saved successfully',
    });
  } catch (error) {
    console.error('Error saving profile:', error);
    return NextResponse.json(
      {
        error: 'Failed to save profile',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
