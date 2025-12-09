import { NextRequest, NextResponse } from 'next/server';
import { routeToAgent } from '@/lib/agents';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, context } = body;

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    const response = await routeToAgent(message, context);

    return NextResponse.json({
      success: true,
      ...response
    });
  } catch (error: any) {
    console.error('AI Chat error:', error);
    return NextResponse.json(
      { 
        error: error.message || 'Failed to process message',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined
      },
      { status: 500 }
    );
  }
}
