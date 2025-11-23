import { useEffect, useState } from 'react';
import { linksAPI } from '../api';

interface Link {
  id: number;
  consumer_id: number;
  supplier_id: number;
  consumer_name?: string;
  supplier_name?: string;
  status: string;
  requested_at: string;
  responded_at: string | null;
  notes: string | null;
}

export default function Links() {
  const [links, setLinks] = useState<Link[]>([]);
  const [pendingLinks, setPendingLinks] = useState<Link[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'pending'>('all');

  useEffect(() => {
    loadLinks();
  }, []);

  const loadLinks = async () => {
    try {
      const [allLinks, pending] = await Promise.all([
        linksAPI.getMyLinks(),
        linksAPI.getPendingLinks(),
      ]);
      console.log('All Links received:', allLinks.data);
      console.log('Pending Links received:', pending.data);
      setLinks(allLinks.data);
      setPendingLinks(pending.data);
    } catch (error) {
      console.error('Failed to load links:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateLink = async (linkId: number, status: string) => {
    try {
      await linksAPI.updateLinkStatus(linkId, status);
      await loadLinks();
      alert(`Link ${status} successfully`);
    } catch (error) {
      console.error('Failed to update link:', error);
      alert('Failed to update link');
    }
  };

  const handleBlockLink = async (linkId: number) => {
    if (!confirm('Are you sure you want to block this link?')) return;

    try {
      await linksAPI.blockLink(linkId);
      await loadLinks();
      alert('Link blocked successfully');
    } catch (error) {
      console.error('Failed to block link:', error);
      alert('Failed to block link');
    }
  };

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  const displayLinks = activeTab === 'pending' ? pendingLinks : links;
  
  console.log('Active Tab:', activeTab);
  console.log('Display Links:', displayLinks);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Consumer Links</h1>

      <div className="mb-6 border-b">
        <div className="flex space-x-4">
          <button
            onClick={() => setActiveTab('all')}
            className={`pb-2 px-1 ${
              activeTab === 'all'
                ? 'border-b-2 border-purple-600 text-purple-600'
                : 'text-gray-500'
            }`}
          >
            All Links ({links.length})
          </button>
          <button
            onClick={() => setActiveTab('pending')}
            className={`pb-2 px-1 ${
              activeTab === 'pending'
                ? 'border-b-2 border-purple-600 text-purple-600'
                : 'text-gray-500'
            }`}
          >
            Pending ({pendingLinks.length})
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Consumer
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Supplier
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Requested At
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Notes
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {displayLinks.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                  <div className="text-lg mb-2">No links</div>
                  <div className="text-sm">
                    {activeTab === 'pending' 
                      ? 'You have no link requests from consumers'
                      : 'Wait for consumer to send a link.'}
                  </div>
                </td>
              </tr>
            ) : (
              displayLinks.map((link) => (
              <tr key={link.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {link.consumer_name || `Consumer #${link.consumer_id}`}
                  </div>
                  <div className="text-xs text-gray-500">ID: {link.consumer_id}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {link.supplier_name || `Supplier #${link.supplier_id}`}
                  </div>
                  <div className="text-xs text-gray-500">ID: {link.supplier_id}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs rounded ${
                      link.status === 'ACCEPTED' || link.status === 'accepted'
                        ? 'bg-green-100 text-green-800'
                        : link.status === 'PENDING' || link.status === 'pending'
                        ? 'bg-yellow-100 text-yellow-800'
                        : link.status === 'BLOCKED' || link.status === 'blocked'
                        ? 'bg-red-100 text-red-800'
                        : link.status === 'REJECTED' || link.status === 'rejected'
                        ? 'bg-gray-100 text-gray-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {link.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(link.requested_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4">{link.notes || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right space-x-2">
                  {link.status === 'pending' && (
                    <>
                      <button
                        onClick={() => handleUpdateLink(link.id, 'accepted')}
                        className="text-green-600 hover:text-green-900"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => handleUpdateLink(link.id, 'rejected')}
                        className="text-red-600 hover:text-red-900"
                      >
                        Reject
                      </button>
                    </>
                  )}
                  {link.status === 'accepted' && (
                    <button
                      onClick={() => handleBlockLink(link.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Block
                    </button>
                  )}
                </td>
              </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
