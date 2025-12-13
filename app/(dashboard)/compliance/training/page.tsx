'use client';

import { useState } from 'react';
import { BookOpen, Play, Award } from 'lucide-react';

export default function ComplianceTrainingPage() {
  const [courses] = useState([
    { id: '1', title: 'FAR Part 15: Contracting by Negotiation', duration: '2 hours', progress: 75, status: 'In Progress' },
    { id: '2', title: 'DFARS Cybersecurity Requirements', duration: '1.5 hours', progress: 100, status: 'Completed' },
  ]);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Compliance Training</h1>
      <p className="text-slate-600 mb-8">Master FAR, DFARS, and federal contracting regulations</p>

      <div className="space-y-6">
        {courses.map((course) => (
          <div key={course.id} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold mb-2">{course.title}</h3>
            <p className="text-sm text-slate-600 mb-4">{course.duration}</p>
            <div className="h-2 bg-slate-200 rounded-full mb-4">
              <div className="h-full bg-blue-600 rounded-full" style={{ width: `${course.progress}%` }} />
            </div>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center gap-2">
              <Play className="w-4 h-4" />
              {course.status === 'Not Started' ? 'Start' : 'Continue'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
