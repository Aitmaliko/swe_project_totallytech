import { useEffect, useState } from 'react';
import { ordersAPI } from '../api';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const response = await ordersAPI.getMyOrders();
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to load orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (orderId: number, status: string) => {
    try {
      await ordersAPI.updateOrderStatus(orderId, status);
      loadOrders();
    } catch (error) {
      console.error('Failed to update order:', error);
    }
  };

  const filteredOrders = filter === 'all'
    ? orders
    : orders.filter((o: any) => o.status === filter);

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Orders</h1>

      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded ${
            filter === 'all' ? 'bg-purple-600 text-white' : 'bg-gray-200'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('pending')}
          className={`px-4 py-2 rounded ${
            filter === 'pending' ? 'bg-purple-600 text-white' : 'bg-gray-200'
          }`}
        >
          Pending
        </button>
        <button
          onClick={() => setFilter('accepted')}
          className={`px-4 py-2 rounded ${
            filter === 'accepted' ? 'bg-purple-600 text-white' : 'bg-gray-200'
          }`}
        >
          Accepted
        </button>
      </div>

      <div className="space-y-4">
        {filteredOrders.map((order: any) => (
          <div key={order.id} className="bg-white p-6 rounded-lg shadow">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold">Order #{order.id}</h3>
                <p className="text-gray-600">Total: ${order.total_amount}</p>
                <p className="text-sm text-gray-500">
                  {new Date(order.created_at).toLocaleString()}
                </p>
              </div>
              <span
                className={`px-3 py-1 rounded text-sm ${
                  order.status === 'pending'
                    ? 'bg-yellow-100 text-yellow-800'
                    : order.status === 'accepted'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {order.status}
              </span>
            </div>

            <div className="mb-4">
              <h4 className="font-medium mb-2">Items:</h4>
              {order.items.map((item: any) => (
                <div key={item.id} className="text-sm text-gray-600">
                  Product #{item.product_id} - Qty: {item.quantity} - $
                  {item.total_price}
                </div>
              ))}
            </div>

            {order.status === 'pending' && (
              <div className="flex gap-2">
                <button
                  onClick={() => handleStatusUpdate(order.id, 'accepted')}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Accept
                </button>
                <button
                  onClick={() => handleStatusUpdate(order.id, 'rejected')}
                  className="px-4 py-2 bg-red-600 text-red rounded hover:bg-red-700"
                >
                  Reject
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
