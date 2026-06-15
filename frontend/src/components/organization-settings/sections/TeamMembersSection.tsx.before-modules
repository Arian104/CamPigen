"use client";

import { Plus, Trash2 } from "lucide-react";
import { Member } from "../types";

export function TeamMembersSection({
  members,
  newMemberEmail,
  setNewMemberEmail,
  newMemberRole,
  setNewMemberRole,
  addMember,
  updateMember,
  removeMember,
}: {
  members: Member[];
  newMemberEmail: string;
  setNewMemberEmail: (value: string) => void;
  newMemberRole: string;
  setNewMemberRole: (value: string) => void;
  addMember: () => void;
  updateMember: (memberId: string, role: string) => void;
  removeMember: (memberId: string) => void;
}) {
  return (
    <div>
      <h2>Team Members</h2>

      <div className="memberAddBox">
        <input
          placeholder="User email"
          value={newMemberEmail}
          onChange={(e) => setNewMemberEmail(e.target.value)}
        />

        <select value={newMemberRole} onChange={(e) => setNewMemberRole(e.target.value)}>
          <option value="admin">Admin</option>
          <option value="manager">Manager</option>
          <option value="marketer">Marketer</option>
          <option value="analyst">Analyst</option>
          <option value="viewer">Viewer</option>
        </select>

        <button type="button" className="buttonLink" onClick={addMember}>
          <Plus size={16} />
          Add Member
        </button>
      </div>

      <div className="tableWrap">
        <table className="dataTable">
          <thead>
            <tr>
              <th>User</th>
              <th>Role</th>
              <th>Status</th>
              <th />
            </tr>
          </thead>

          <tbody>
            {members.map((member) => (
              <tr key={member.id}>
                <td>
                  <strong>
                    {member.first_name || member.last_name
                      ? `${member.first_name} ${member.last_name}`
                      : member.email}
                  </strong>
                  <span>{member.email}</span>
                </td>

                <td>
                  <select
                    value={member.role}
                    disabled={member.role === "owner"}
                    onChange={(e) => updateMember(member.id, e.target.value)}
                  >
                    <option value="owner">Owner</option>
                    <option value="admin">Admin</option>
                    <option value="manager">Manager</option>
                    <option value="marketer">Marketer</option>
                    <option value="analyst">Analyst</option>
                    <option value="viewer">Viewer</option>
                  </select>
                </td>

                <td>{member.status}</td>

                <td>
                  <button type="button" className="dangerIconButton" onClick={() => removeMember(member.id)}>
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
