import { useEffect, useState } from 'react';
import { authAPI } from '../api';
import { useAuthStore } from '../store';

interface StaffMember {
  id: number;
  email: string;
  full_name: string;
  phone: string;
  role: string;
  is_active: boolean;
}

export default function Staff() {
  const [staff, setStaff] = useState<StaffMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const { user } = useAuthStore();

  // Only Owner can access this page
  const isOwner = user?.role === 'owner';

  useEffect(() => {
    if (isOwner) {
      loadStaff();
    }
  }, [isOwner]);

  const loadStaff = async () => {
    try {
      const response = await authAPI.getStaff();
      setStaff(response.data);
    } catch (error) {
      console.error('Failed to load staff:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteStaff = async (staffId: number) => {
    if (!confirm('Are you sure you want to delete this staff member?')) return;

    try {
      await authAPI.deleteStaff(staffId);
      await loadStaff();
      alert('Staff member deleted successfully');
    } catch (error) {
      console.error('Failed to delete staff:', error);
      alert('Failed to delete staff member');
    }
  };

  if (!isOwner) {
    return (
      <div className="p-6">
        <div className="bg-red-100 text-red-800 p-4 rounded">
          Only Owner can access staff management.
        </div>
      </div>
    );
  }

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Staff Management</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Add Staff Member
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Phone
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {staff.map((member) => (
              <tr key={member.id}>
                <td className="px-6 py-4 whitespace-nowrap">{member.full_name}</td>
                <td className="px-6 py-4 whitespace-nowrap">{member.email}</td>
                <td className="px-6 py-4 whitespace-nowrap">{member.phone}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs rounded bg-purple-100 text-purple-800">
                    {member.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs rounded ${
                      member.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {member.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  <button
                    onClick={() => handleDeleteStaff(member.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showCreateModal && (
        <CreateStaffModal
          onClose={() => setShowCreateModal(false)}
          onCreated={() => {
            setShowCreateModal(false);
            loadStaff();
          }}
        />
      )}
    </div>
  );
}

function CreateStaffModal({ onClose, onCreated }: any) {
  const [formData, setFormData] = useState({
    email: '',
    phone: '',
    full_name: '',
    password: '',
    role: 'manager',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await authAPI.createStaff(formData);
      alert('Staff member created successfully');
      onCreated();
    } catch (error: any) {
      console.error('Failed to create staff:', error);
      alert(error.response?.data?.detail || 'Failed to create staff member');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Add Staff Member</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Full Name</label>
            <input
              type="text"
              required
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Phone</label>
            <input
              type="tel"
              required
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Role</label>
            <select
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              className="w-full border rounded px-3 py-2"
            >
              <option value="manager">Manager</option>
              <option value="sales">Sales Representative</option>
            </select>
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded hover:bg-gray-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:bg-gray-400"
            >
              {loading ? 'Creating...' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
