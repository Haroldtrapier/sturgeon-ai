'use client';

import { useState } from 'react';
import { Bell, Mail, Smartphone, Clock, Settings } from 'lucide-react';

export default function AlertsPage() {
  const [alerts] = useState([
    {
      id: '1',
      type: 'New Match',
      title: 'High-value cybersecurity contract matches your profile',
      time: '2 hours ago',
      read: false,
    },
    {
      id: '2',
      type: 'Deadline Warning',
      title: 'Proposal deadline in 3 days: DOD IT Services',
      time: '5 hours ago',
      read: false,
    },
    {
      id: '3',
      type: 'Watchlist Update',
      title: '3 new opportunities matching "Cloud Infrastructure"',
      time: '1 day ago',
      read: true,
    },
  ]);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Alerts & Notifications</h1>
        <p className="text-slate-600">Stay updated on opportunities and deadlines</p>
      </div>

      {/* Alert Settings */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Notification Preferences</h3>
        <div className="grid grid-cols-3 gap-6">
          <div className="flex items-center gap-3">
            <input type="checkbox" id="email" defaultChecked className="w-5 h-5" />
            <label htmlFor="email" className="flex items-center gap-2 text-slate-700">
              <Mail className="w-5 h-5" />
              Email Notifications
            </label>
          </div>
          <div className="flex items-center gap-3">
            <input type="checkbox" id="push" defaultChecked className="w-5 h-5" />
            <label htmlFor="push" className="flex items-center gap-2 text-slate-700">
              <Smartphone className="w-5 h-5" />
              Push Notifications
            </label>
          </div>
          <div className="flex items-center gap-3">
            <input type="checkbox" id="daily" className="w-5 h-5" />
            <label htmlFor="daily" className="flex items-center gap-2 text-slate-700">
              <Clock className="w-5 h-5" />
              Daily Digest
            </label>
          </div>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-3">
        {alerts.map((alert) => (
          <div
            key={alert.id}
            className={`bg-white rounded-lg shadow p-4 border-l-4 ${
              alert.read ? 'border-slate-300' : 'border-blue-600'
            }`}
          >
            <div className="flex items-start gap-4">
              <Bell className={`w-5 h-5 mt-1 ${alert.read ? 'text-slate-400' : 'text-blue-600'}`} />
              <div className="flex-1">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className={`font-semibold ${alert.read ? 'text-slate-700' : 'text-slate-900'}`}>
                      {alert.title}
                    </p>
                    <p className="text-sm text-slate-500 mt-1">
                      {alert.type} • {alert.time}
                    </p>
                  </div>
                  {!alert.read && (
                    <button className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
                      View
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
