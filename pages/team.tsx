import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { TeamWorkspace } from '@/components/team/TeamWorkspace';
import { supabase } from '@/lib/supabase';

export default function TeamPage() {
  const [teamId, setTeamId] = useState<string>('');
  const [members, setMembers] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchTeamData();
  }, []);

  const fetchTeamData = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      // Get user's team
      const { data: membership } = await supabase
        .from('team_members')
        .select('team_id, teams(*)')
        .eq('user_id', user.id)
        .single();

      if (membership) {
        setTeamId(membership.team_id);

        // Get all team members
        const { data: teamMembers } = await supabase
          .from('team_members')
          .select('*, user:auth.users(*)')
          .eq('team_id', membership.team_id);

        setMembers(teamMembers || []);
      }
    } catch (error) {
      console.error('Failed to fetch team data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInvite = async (email: string, role: string) => {
    try {
      // Call invite API endpoint
      const response = await fetch('/api/team/invite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teamId, email, role })
      });

      if (!response.ok) throw new Error('Invite failed');

      await fetchTeamData();
      alert(`Invitation sent to ${email}`);
    } catch (error) {
      console.error('Failed to invite member:', error);
      alert('Failed to send invitation');
    }
  };

  const handleUpdateRole = async (memberId: string, newRole: string) => {
    try {
      const { error } = await supabase
        .from('team_members')
        .update({ role: newRole })
        .eq('id', memberId);

      if (error) throw error;
      await fetchTeamData();
    } catch (error) {
      console.error('Failed to update role:', error);
    }
  };

  const handleRemove = async (memberId: string) => {
    if (!confirm('Are you sure you want to remove this team member?')) return;

    try {
      const { error } = await supabase
        .from('team_members')
        .delete()
        .eq('id', memberId);

      if (error) throw error;
      await fetchTeamData();
    } catch (error) {
      console.error('Failed to remove member:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>Team - Sturgeon AI</title>
      </Head>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Team Management</h1>

          <TeamWorkspace
            teamId={teamId}
            members={members}
            onInvite={handleInvite}
            onUpdateRole={handleUpdateRole}
            onRemove={handleRemove}
          />
        </div>
      </div>
    </>
  );
}
