import { NextRequest, NextResponse } from 'next/server';
import { supabaseClient as supabase } from '@/lib/supabaseClient';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/server/auth';

export async function POST(request: NextRequest) {
  try {
    // Get authenticated user
    const session = await getServerSession(authOptions);
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();

    // Validate required fields
    const { title, source, externalId, status } = body;
    if (!title || !source || !externalId) {
      return NextResponse.json(
        { error: 'Missing required fields: title, source, externalId' },
        { status: 400 }
      );
    }

    // Check if opportunity already exists for this user
    const { data: existing } = await supabase
      .from('opportunities')
      .select('id')
      .eq('user_id', session.user.id)
      .eq('external_id', externalId)
      .single();

    if (existing) {
      return NextResponse.json(
        { error: 'Opportunity already saved' },
        { status: 409 }
      );
    }

    // Save to Supabase
    const { data, error } = await supabase
      .from('opportunities')
      .insert([{
        user_id: session.user.id,
        title,
        agency: body.agency || null,
        source,
        external_id: externalId,
        status: status || 'watchlist',
        metadata: body.metadata || {},
        created_at: new Date().toISOString(),
      }])
      .select()
      .single();

    if (error) {
      console.error('Supabase error:', error);
      throw error;
    }

    return NextResponse.json({
      success: true,
      data,
      message: 'Opportunity saved successfully',
    });
  } catch (error) {
    console.error('Error saving opportunity:', error);
    return NextResponse.json(
      { 
        error: 'Failed to save opportunity',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// GET endpoint to list saved opportunities
export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { data, error } = await supabase
      .from('opportunities')
      .select('*')
      .eq('user_id', session.user.id)
      .order('created_at', { ascending: false });

    if (error) throw error;

    return NextResponse.json({
      success: true,
      data,
    });
  } catch (error) {
    console.error('Error fetching opportunities:', error);
    return NextResponse.json(
      { error: 'Failed to fetch opportunities' },
      { status: 500 }
    );
  }
}
