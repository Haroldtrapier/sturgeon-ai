import React, { useState, useCallback } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

interface UploadedDocument {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadedAt: string;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  parsedData?: any;
}

interface DocumentUploaderProps {
  onUpload: (file: File) => Promise<UploadedDocument>;
  onDelete: (docId: string) => void;
  acceptedTypes?: string[];
  maxSizeMB?: number;
}

export const DocumentUploader: React.FC<DocumentUploaderProps> = ({
  onUpload,
  onDelete,
  acceptedTypes = ['.pdf', '.docx', '.doc', '.txt'],
  maxSizeMB = 10
}) => {
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    await handleFiles(files);
  }, []);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      await handleFiles(files);
    }
  };

  const handleFiles = async (files: File[]) => {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;

    for (const file of files) {
      if (file.size > maxSizeBytes) {
        alert(`File ${file.name} exceeds ${maxSizeMB}MB limit`);
        continue;
      }

      // Add to list with uploading status
      const tempDoc: UploadedDocument = {
        id: `temp-${Date.now()}`,
        name: file.name,
        size: file.size,
        type: file.type,
        uploadedAt: new Date().toISOString(),
        status: 'uploading'
      };
      setDocuments(prev => [...prev, tempDoc]);

      try {
        const uploadedDoc = await onUpload(file);
        setDocuments(prev => prev.map(doc => 
          doc.id === tempDoc.id ? uploadedDoc : doc
        ));
      } catch (error) {
        setDocuments(prev => prev.map(doc => 
          doc.id === tempDoc.id ? { ...doc, status: 'failed' as const } : doc
        ));
      }
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600';
      case 'failed': return 'text-red-600';
      case 'processing': return 'text-yellow-600';
      default: return 'text-blue-600';
    }
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <Card
        className={`p-8 border-2 border-dashed transition-colors ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="text-center">
          <div className="text-4xl mb-4">📁</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Drop files here or click to upload
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            Accepted formats: {acceptedTypes.join(', ')} (max {maxSizeMB}MB)
          </p>
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept={acceptedTypes.join(',')}
            multiple
            onChange={handleFileSelect}
          />
          <label htmlFor="file-upload">
            <Button as="span" variant="primary">
              Select Files
            </Button>
          </label>
        </div>
      </Card>

      {/* Documents List */}
      {documents.length > 0 && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Uploaded Documents</h3>
          <div className="space-y-3">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{doc.name}</div>
                  <div className="flex items-center gap-3 text-sm text-gray-600 mt-1">
                    <span>{formatFileSize(doc.size)}</span>
                    <span className={getStatusColor(doc.status)}>
                      {doc.status}
                    </span>
                  </div>
                </div>
                <Button
                  onClick={() => {
                    onDelete(doc.id);
                    setDocuments(prev => prev.filter(d => d.id !== doc.id));
                  }}
                  variant="outline"
                  size="sm"
                >
                  Delete
                </Button>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};
