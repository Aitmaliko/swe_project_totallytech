import { useEffect, useState } from 'react';
import { complaintsAPI } from '../api';

interface Complaint {
  id: number;
  order_id: number;
  link_id: number;
  created_by_id: number;
  assigned_to_id: number | null;
  title: string;
  description: string;
  status: string;
  priority: string;
  resolution_notes: string | null;
  created_at: string;
  resolved_at: string | null;
}

export default function Complaints() {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedComplaint, setSelectedComplaint] = useState<Complaint | null>(null);

  useEffect(() => {
    loadComplaints();
  }, []);

  const loadComplaints = async () => {
    try {
      const response = await complaintsAPI.getOpenComplaints();
      setComplaints(response.data);
    } catch (error) {
      console.error('Failed to load complaints:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResolveComplaint = async (complaintId: number, resolutionNotes: string) => {
    try {
      await complaintsAPI.updateComplaint(complaintId, {
        status: 'resolved',
        resolution_notes: resolutionNotes,
      });
      await loadComplaints();
      setSelectedComplaint(null);
      alert('Complaint resolved successfully');
    } catch (error) {
      console.error('Failed to resolve complaint:', error);
      alert('Failed to resolve complaint');
    }
  };

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Complaints</h1>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Order ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Priority
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Created At
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {complaints.map((complaint) => (
              <tr key={complaint.id}>
                <td className="px-6 py-4 whitespace-nowrap">{complaint.order_id}</td>
                <td className="px-6 py-4">{complaint.title}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs rounded ${
                      complaint.priority === 'high'
                        ? 'bg-red-100 text-red-800'
                        : complaint.priority === 'normal'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {complaint.priority}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs rounded ${
                      complaint.status === 'open'
                        ? 'text-purple-600 hover:text-purple-900'
                        : complaint.status === 'in_progress'
                        ? 'bg-yellow-100 text-yellow-800'
                        : complaint.status === 'escalated'
                        ? 'bg-orange-100 text-orange-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {complaint.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(complaint.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  <button
                    onClick={() => setSelectedComplaint(complaint)}
                    className="text-purple-600 hover:text-purple-900"
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedComplaint && (
        <ComplaintModal
          complaint={selectedComplaint}
          onClose={() => setSelectedComplaint(null)}
          onResolve={handleResolveComplaint}
        />
      )}
    </div>
  );
}

function ComplaintModal({ complaint, onClose, onResolve }: any) {
  const [resolutionNotes, setResolutionNotes] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onResolve(complaint.id, resolutionNotes);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
        <h2 className="text-2xl font-bold mb-4">Complaint Details</h2>

        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Order ID</label>
            <p className="mt-1">{complaint.order_id}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Title</label>
            <p className="mt-1">{complaint.title}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <p className="mt-1">{complaint.description}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Priority</label>
            <p className="mt-1">{complaint.priority}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Status</label>
            <p className="mt-1">{complaint.status}</p>
          </div>
        </div>

        {complaint.status !== 'resolved' && complaint.status !== 'closed' && (
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Resolution Notes</label>
              <textarea
                required
                value={resolutionNotes}
                onChange={(e) => setResolutionNotes(e.target.value)}
                className="w-full border rounded px-3 py-2"
                rows={4}
                placeholder="Enter resolution notes..."
              />
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
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Resolve Complaint
              </button>
            </div>
          </form>
        )}

        {(complaint.status === 'resolved' || complaint.status === 'closed') && (
          <div className="flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 border rounded hover:bg-gray-100"
            >
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
