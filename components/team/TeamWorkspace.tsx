import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: 'owner' | 'admin' | 'editor' | 'viewer';
  avatar?: string;
  status: 'active' | 'invited' | 'inactive';
  joinedAt: string;
}

interface TeamWorkspaceProps {
  teamId: string;
  members: TeamMember[];
  onInvite: (email: string, role: string) => Promise<void>;
  onUpdateRole: (memberId: string, newRole: string) => Promise<void>;
  onRemove: (memberId: string) => Promise<void>;
}

export const TeamWorkspace: React.FC<TeamWorkspaceProps> = ({
  teamId,
  members,
  onInvite,
  onUpdateRole,
  onRemove
}) => {
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('editor');
  const [isInviting, setIsInviting] = useState(false);

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteEmail) return;

    setIsInviting(true);
    try {
      await onInvite(inviteEmail, inviteRole);
      setInviteEmail('');
      setInviteRole('editor');
    } catch (error) {
      console.error('Invite failed:', error);
    } finally {
      setIsInviting(false);
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'owner': return 'bg-purple-100 text-purple-700';
      case 'admin': return 'bg-blue-100 text-blue-700';
      case 'editor': return 'bg-green-100 text-green-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="space-y-6">
      {/* Invite Section */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Invite Team Members</h3>
        <form onSubmit={handleInvite} className="flex gap-3">
          <Input
            type="email"
            placeholder="colleague@example.com"
            value={inviteEmail}
            onChange={(e) => setInviteEmail(e.target.value)}
            className="flex-1"
          />
          <select
            value={inviteRole}
            onChange={(e) => setInviteRole(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value="viewer">Viewer</option>
            <option value="editor">Editor</option>
            <option value="admin">Admin</option>
          </select>
          <Button type="submit" disabled={isInviting} variant="primary">
            {isInviting ? 'Sending...' : 'Invite'}
          </Button>
        </form>
      </Card>

      {/* Team Members List */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Team Members ({members.length})</h3>
        <div className="space-y-3">
          {members.map((member) => (
            <div key={member.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-semibold">
                  {member.name.charAt(0).toUpperCase()}
                </div>
                <div>
                  <div className="font-medium text-gray-900">{member.name}</div>
                  <div className="text-sm text-gray-600">{member.email}</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getRoleColor(member.role)}`}>
                  {member.role}
                </span>
                {member.status === 'invited' && (
                  <span className="text-xs text-yellow-600">Pending</span>
                )}
                {member.role !== 'owner' && (
                  <Button
                    onClick={() => onRemove(member.id)}
                    variant="outline"
                    size="sm"
                  >
                    Remove
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Permissions Info */}
      <Card className="p-6 bg-blue-50">
        <h4 className="font-semibold text-blue-900 mb-2">Role Permissions</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li><strong>Owner:</strong> Full access, manage billing and team</li>
          <li><strong>Admin:</strong> Manage team members and all resources</li>
          <li><strong>Editor:</strong> Create and edit proposals and opportunities</li>
          <li><strong>Viewer:</strong> View-only access to all resources</li>
        </ul>
      </Card>
    </div>
  );
};
