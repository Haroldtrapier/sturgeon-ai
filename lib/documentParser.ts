// Utility: Document Parser
// Parse PDF, DOCX, and other document formats

import pdfParse from 'pdf-parse';
import mammoth from 'mammoth';
import fs from 'fs';

export interface ParsedDocument {
  text: string;
  metadata: {
    pages?: number;
    wordCount: number;
    [key: string]: any;
  };
}

export async function parseDocument(filePath: string, fileType: string): Promise<ParsedDocument> {
  const buffer = fs.readFileSync(filePath);

  if (fileType === 'pdf') {
    const data = await pdfParse(buffer);
    return {
      text: data.text,
      metadata: {
        pages: data.numpages,
        wordCount: data.text.split(/\s+/).length,
        info: data.info
      }
    };
  }

  if (fileType === 'docx' || fileType === 'doc') {
    const result = await mammoth.extractRawText({ buffer });
    return {
      text: result.value,
      metadata: {
        wordCount: result.value.split(/\s+/).length
      }
    };
  }

  if (fileType === 'txt') {
    const text = buffer.toString('utf-8');
    return {
      text,
      metadata: {
        wordCount: text.split(/\s+/).length
      }
    };
  }

  throw new Error(`Unsupported file type: ${fileType}`);
}
