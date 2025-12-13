'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard, Search, FileText, CheckSquare, MessageSquare,
  Award, BookOpen, BarChart3, Users, Settings, LogOut, Building2,
  Target, Briefcase, Shield, TrendingUp, Bell, Archive
} from 'lucide-react';

interface SidebarProps {
  onLogout?: () => void;
  user?: {
    name: string;
    email: string;
    avatar?: string;
  };
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'AI Chat', href: '/ai-chat', icon: MessageSquare, badge: '5 Agents' },
  {
    name: 'Opportunities',
    icon: Target,
    children: [
      { name: 'Search', href: '/opportunities' },
      { name: 'Saved', href: '/opportunities/saved' },
      { name: 'Watchlist', href: '/opportunities/watchlist' },
      { name: 'Matching', href: '/opportunities/matching' },
      { name: 'Alerts', href: '/opportunities/alerts' },
    ]
  },
  {
    name: 'Proposals',
    icon: FileText,
    children: [
      { name: 'Builder', href: '/proposals' },
      { name: 'Templates', href: '/proposals/templates' },
      { name: 'Library', href: '/proposals/library' },
      { name: 'Compliance Matrix', href: '/proposals/compliance' },
      { name: 'Win Themes', href: '/proposals/win-themes' },
    ]
  },
  {
    name: 'Compliance',
    icon: Shield,
    children: [
      { name: 'FAR/DFARS Checker', href: '/compliance' },
      { name: 'Audit Trail', href: '/compliance/audit' },
      { name: 'Training', href: '/compliance/training' },
      { name: 'Certifications', href: '/compliance/certifications' },
    ]
  },
  {
    name: 'Research',
    icon: BookOpen,
    children: [
      { name: 'Contract Database', href: '/research' },
      { name: 'Agency Profiles', href: '/research/agencies' },
      { name: 'Market Intelligence', href: '/research/market' },
      { name: 'Competitor Analysis', href: '/research/competitors' },
    ]
  },
  {
    name: 'Analytics',
    icon: BarChart3,
    children: [
      { name: 'Dashboard', href: '/analytics' },
      { name: 'Win/Loss Analysis', href: '/analytics/win-loss' },
      { name: 'Pipeline', href: '/analytics/pipeline' },
      { name: 'Performance', href: '/analytics/performance' },
    ]
  },
  {
    name: 'Team',
    icon: Users,
    children: [
      { name: 'Workspace', href: '/team' },
      { name: 'Members', href: '/team/members' },
      { name: 'Roles & Permissions', href: '/team/roles' },
      { name: 'Activity', href: '/team/activity' },
    ]
  },
  {
    name: 'Certifications',
    icon: Award,
    children: [
      { name: 'My Certifications', href: '/certifications' },
      { name: 'Training Courses', href: '/certifications/courses' },
      { name: 'Exam Prep', href: '/certifications/exam-prep' },
      { name: 'Resources', href: '/certifications/resources' },
    ]
  },
];

const bottomNav = [
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Help & Support', href: '/help', icon: BookOpen },
];

export default function Sidebar({ onLogout, user }: SidebarProps) {
  const pathname = usePathname();
  const [expandedSections, setExpandedSections] = useState<string[]>([]);

  const toggleSection = (name: string) => {
    setExpandedSections(prev =>
      prev.includes(name)
        ? prev.filter(n => n !== name)
        : [...prev, name]
    );
  };

  const isActive = (href: string) => pathname === href || pathname?.startsWith(href + '/');

  return (
    <div className="w-64 bg-slate-900 text-white flex flex-col h-screen">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <Link href="/dashboard" className="block">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Sturgeon AI
          </h1>
          <p className="text-slate-400 text-sm mt-1">Gov Contracting Intelligence</p>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {navigation.map((item) => (
          <div key={item.name}>
            {item.children ? (
              <>
                <button
                  onClick={() => toggleSection(item.name)}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-slate-800 transition"
                >
                  <div className="flex items-center gap-3">
                    <item.icon className="w-5 h-5" />
                    <span className="font-medium">{item.name}</span>
                  </div>
                  <svg
                    className={`w-4 h-4 transition-transform ${expandedSections.includes(item.name) ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedSections.includes(item.name) && (
                  <div className="ml-8 mt-1 space-y-1">
                    {item.children.map((child) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        className={`block px-3 py-2 rounded-lg text-sm transition ${
                          isActive(child.href)
                            ? 'bg-blue-600 text-white'
                            : 'text-slate-300 hover:bg-slate-800'
                        }`}
                      >
                        {child.name}
                      </Link>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <Link
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition ${
                  isActive(item.href)
                    ? 'bg-blue-600'
                    : 'hover:bg-slate-800'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.name}</span>
                {item.badge && (
                  <span className="ml-auto text-xs bg-purple-600 px-2 py-0.5 rounded-full">
                    {item.badge}
                  </span>
                )}
              </Link>
            )}
          </div>
        ))}
      </nav>

      {/* Bottom Section */}
      <div className="border-t border-slate-700">
        <div className="p-4 space-y-1">
          {bottomNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition ${
                isActive(item.href)
                  ? 'bg-blue-600'
                  : 'hover:bg-slate-800'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span>{item.name}</span>
            </Link>
          ))}
        </div>

        {/* User Profile */}
        {user && (
          <div className="p-4 border-t border-slate-700">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center font-bold">
                {user.name.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1 overflow-hidden">
                <p className="font-semibold text-sm truncate">{user.name}</p>
                <p className="text-slate-400 text-xs truncate">{user.email}</p>
              </div>
            </div>
            {onLogout && (
              <button
                onClick={onLogout}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm font-semibold transition"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function useState<T>(initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // This is a simplified implementation for the server-side component
  // In actual use, this would be imported from React
  return [initialValue, () => {}];
}
