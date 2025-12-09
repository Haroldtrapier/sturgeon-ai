// Background Worker: Document Parser
// Run this as a separate service or serverless function

import { createClient } from '@supabase/supabase-js';
import { parseDocument } from '@/lib/documentParser';
import OpenAI from 'openai';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

interface DocumentJob {
  id: string;
  s3_key: string;
  file_type: string;
  name: string;
}

export async function processDocument(job: DocumentJob) {
  console.log(`Processing document: ${job.name}`);

  try {
    // Update status to processing
    await supabase
      .from('documents')
      .update({ status: 'processing' })
      .eq('id', job.id);

    // Download file from Supabase Storage
    const { data: fileData, error: downloadError } = await supabase.storage
      .from('documents')
      .download(job.s3_key);

    if (downloadError) throw downloadError;

    // Convert blob to buffer
    const arrayBuffer = await fileData.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // Write to temp file
    const fs = require('fs');
    const tempPath = `/tmp/${job.id}.${job.file_type}`;
    fs.writeFileSync(tempPath, buffer);

    // Parse document
    const parsed = await parseDocument(tempPath, job.file_type);

    // Extract key information using AI
    const analysis = await analyzeDocument(parsed.text);

    // Update database
    await supabase
      .from('documents')
      .update({
        status: 'completed',
        parsed_content: parsed.text,
        extracted_data: {
          ...parsed.metadata,
          ...analysis
        }
      })
      .eq('id', job.id);

    // Clean up
    fs.unlinkSync(tempPath);

    console.log(`Document processed successfully: ${job.name}`);
    return { success: true };
  } catch (error) {
    console.error(`Failed to process document ${job.name}:`, error);

    // Update status to failed
    await supabase
      .from('documents')
      .update({
        status: 'failed',
        metadata: { error: (error as Error).message }
      })
      .eq('id', job.id);

    return { success: false, error: (error as Error).message };
  }
}

async function analyzeDocument(text: string) {
  try {
    const prompt = `Analyze this document and extract:
1. Document type (contract, proposal, grant, report, etc.)
2. Key entities (organizations, people, dates, amounts)
3. Main topics/themes
4. Important deadlines or dates
5. Action items or requirements

Document text:
${text.substring(0, 6000)}

Respond in JSON format with keys: documentType, entities, topics, deadlines, requirements`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        {
          role: 'system',
          content: 'You are a document analysis expert. Extract structured information from documents.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.2
    });

    return JSON.parse(completion.choices[0].message.content || '{}');
  } catch (error) {
    console.error('AI analysis failed:', error);
    return {};
  }
}

// Worker loop - polls for pending documents
export async function startWorker() {
  console.log('Document parser worker started');

  while (true) {
    try {
      // Find documents with status 'uploaded'
      const { data: pendingDocs } = await supabase
        .from('documents')
        .select('*')
        .eq('status', 'uploaded')
        .limit(5);

      if (pendingDocs && pendingDocs.length > 0) {
        console.log(`Found ${pendingDocs.length} documents to process`);

        // Process in parallel
        await Promise.all(
          pendingDocs.map(doc => processDocument(doc))
        );
      }

      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, 10000)); // 10 seconds
    } catch (error) {
      console.error('Worker error:', error);
      await new Promise(resolve => setTimeout(resolve, 30000)); // Wait longer on error
    }
  }
}

// Run worker if executed directly
if (require.main === module) {
  startWorker();
}
