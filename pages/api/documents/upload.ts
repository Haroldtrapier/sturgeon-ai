// API Route: /api/documents/upload
// Handle document upload and parsing

import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';
import formidable from 'formidable';
import fs from 'fs';
import { v4 as uuidv4 } from 'uuid';

export const config = {
  api: {
    bodyParser: false,
  },
};

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const authHeader = req.headers.authorization;

  if (!authHeader) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const token = authHeader.replace('Bearer ', '');
  const { data: { user }, error: authError } = await supabase.auth.getUser(token);

  if (authError || !user) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  try {
    const form = formidable({});
    const [fields, files] = await form.parse(req);

    const file = Array.isArray(files.file) ? files.file[0] : files.file;

    if (!file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Generate unique filename
    const fileExt = file.originalFilename?.split('.').pop() || 'pdf';
    const fileName = `${uuidv4()}.${fileExt}`;
    const filePath = `documents/${user.id}/${fileName}`;

    // Read file
    const fileBuffer = fs.readFileSync(file.filepath);

    // Upload to Supabase Storage
    const { data: uploadData, error: uploadError } = await supabase.storage
      .from('documents')
      .upload(filePath, fileBuffer, {
        contentType: file.mimetype || 'application/pdf',
      });

    if (uploadError) throw uploadError;

    // Get public URL
    const { data: urlData } = supabase.storage
      .from('documents')
      .getPublicUrl(filePath);

    // Create document record
    const { data: document, error: docError } = await supabase
      .from('documents')
      .insert({
        user_id: user.id,
        name: fileName,
        original_name: file.originalFilename || fileName,
        file_type: fileExt,
        file_size: file.size,
        s3_key: filePath,
        s3_url: urlData.publicUrl,
        status: 'processing'
      })
      .select()
      .single();

    if (docError) throw docError;

    // TODO: Trigger document parsing job (queue for background processing)
    // For now, mark as completed
    await supabase
      .from('documents')
      .update({ status: 'completed' })
      .eq('id', document.id);

    // Clean up temp file
    fs.unlinkSync(file.filepath);

    res.status(201).json(document);
  } catch (error) {
    console.error('Document upload error:', error);
    res.status(500).json({ error: 'Failed to upload document' });
  }
}
