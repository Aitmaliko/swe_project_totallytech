// import { useEffect, useState } from 'react';
// import { Link } from 'react-router-dom';
// import { ordersAPI, productsAPI, linksAPI, complaintsAPI } from '../api';

// interface Stats {
//   totalOrders: number;
//   pendingOrders: number;
//   totalProducts: number;
//   activeLinks: number;
//   openComplaints: number;
// }

// export default function Dashboard() {
//   const [stats, setStats] = useState<Stats>({
//     totalOrders: 0,
//     pendingOrders: 0,
//     totalProducts: 0,
//     activeLinks: 0,
//     openComplaints: 0,
//   });
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     loadStats();
//   }, []);

//   const loadStats = async () => {
//     try {
//       const [orders, products, links, complaints] = await Promise.all([
//         ordersAPI.getMyOrders(),
//         productsAPI.getMyProducts(),
//         linksAPI.getMyLinks(),
//         complaintsAPI.getOpenComplaints(),
//       ]);

//       setStats({
//         totalOrders: orders.data.length,
//         pendingOrders: orders.data.filter((o: any) => o.status === 'pending').length,
//         totalProducts: products.data.length,
//         activeLinks: links.data.filter((l: any) => l.status === 'accepted').length,
//         openComplaints: complaints.data.length,
//       });
//     } catch (error) {
//       console.error('Failed to load stats:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   if (loading) {
//     return (
//       <div className="flex items-center justify-center h-64">
//         <div className="text-xl">Loading...</div>
//       </div>
//     );
//   }

//   return (
//     <div className="p-6">
//       <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
//         <StatCard
//           title="Total Orders"
//           value={stats.totalOrders}
//           subtitle={`${stats.pendingOrders} pending`}
//           link="/orders"
//         />
//         <StatCard
//           title="Products"
//           value={stats.totalProducts}
//           link="/products"
//         />
//         <StatCard
//           title="Active Links"
//           value={stats.activeLinks}
//           link="/links"
//         />
//         <StatCard
//           title="Open Complaints"
//           value={stats.openComplaints}
//           link="/complaints"
//         />
//       </div>

//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         <QuickActions />
//         <RecentActivity />
//       </div>
//     </div>
//   );
// }

// function StatCard({ title, value, subtitle, link }: any) {
//   return (
//     <Link
//       to={link}
//       className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
//     >
//       <h3 className="text-gray-500 text-sm font-medium mb-2">{title}</h3>
//       <p className="text-3xl font-bold mb-1">{value}</p>
//       {subtitle && <p className="text-sm text-gray-600">{subtitle}</p>}
//     </Link>
//   );
// }

// function QuickActions() {
//   return (
//     <div className="bg-white p-6 rounded-lg shadow">
//       <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
//       <div className="space-y-2">
//         <Link
//           to="/products"
//           className="block w-full text-left px-4 py-2 bg-blue-50 hover:bg-blue-100 rounded"
//         >
//           Add New Product
//         </Link>
//         <Link
//           to="/staff"
//           className="block w-full text-left px-4 py-2 bg-blue-50 hover:bg-blue-100 rounded"
//         >
//           Add Staff Member
//         </Link>
//         <Link
//           to="/orders"
//           className="block w-full text-left px-4 py-2 bg-blue-50 hover:bg-blue-100 rounded"
//         >
//           View Pending Orders
//         </Link>
//       </div>
//     </div>
//   );
// }

// function RecentActivity() {
//   return (
//     <div className="bg-white p-6 rounded-lg shadow">
//       <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
//       <div className="space-y-3">
//         <div className="text-sm text-gray-600">No recent activity</div>
//       </div>
//     </div>
//   );
// }


// import { useEffect, useState } from 'react'; 
// import { Link } from 'react-router-dom';
// import { ordersAPI, productsAPI, linksAPI, complaintsAPI } from '../api';

// interface Stats {
//   totalOrders: number;
//   pendingOrders: number;
//   totalProducts: number;
//   activeLinks: number;
//   openComplaints: number;
// }

// export default function Dashboard() {
//   const [stats, setStats] = useState<Stats>({
//     totalOrders: 0,
//     pendingOrders: 0,
//     totalProducts: 0,
//     activeLinks: 0,
//     openComplaints: 0,
//   });
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     loadStats();
//   }, []);

//   const loadStats = async () => {
//     try {
//       const [orders, products, links, complaints] = await Promise.all([
//         ordersAPI.getMyOrders(),
//         productsAPI.getMyProducts(),
//         linksAPI.getMyLinks(),
//         complaintsAPI.getOpenComplaints(),
//       ]);

//       setStats({
//         totalOrders: orders.data.length,
//         pendingOrders: orders.data.filter((o: any) => o.status === 'pending').length,
//         totalProducts: products.data.length,
//         activeLinks: links.data.filter((l: any) => l.status === 'accepted').length,
//         openComplaints: complaints.data.length,
//       });
//     } catch (error) {
//       console.error('Failed to load stats:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   if (loading) {
//     return (
//       <div className="flex items-center justify-center h-64">
//         <div className="text-xl">Loading...</div>
//       </div>
//     );
//   }

//   return (
//     <div className="p-6">
//       <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

//       {/* LIGHT BROWN STAT CARDS */}
//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
//         <StatCard
//           title="Total Orders"
//           value={stats.totalOrders}
//           subtitle={`${stats.pendingOrders} pending`}
//           link="/orders"
//         />
//         <StatCard
//           title="Products"
//           value={stats.totalProducts}
//           link="/products"
//         />
//         <StatCard
//           title="Active Links"
//           value={stats.activeLinks}
//           link="/links"
//         />
//         <StatCard
//           title="Open Complaints"
//           value={stats.openComplaints}
//           link="/complaints"
//         />
//       </div>

//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         <QuickActions />
//         {/* <RecentActivity /> */}
//       </div>
//     </div>
//   );
// }

// // function StatCard({ title, value, subtitle, link }: any) {
// //   return (
// //     <Link
// //       to={link}
// //       className="bg-amber-50 p-6 rounded-lg shadow hover:bg-amber-100 transition"
// //     >
// //       <h3 className="text-gray-600 text-sm font-medium mb-2">{title}</h3>
// //       <p className="text-3xl font-bold mb-1">{value}</p>
// //       {subtitle && <p className="text-sm text-gray-700">{subtitle}</p>}
// //     </Link>
// //   );
// // }


// // function QuickActions() {
// //   return (
// //     <div className="bg-amber-50 p-6 rounded-lg shadow">
// //       <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
// //       <div className="space-y-2">

// //         {/* PURPLE BUTTONS */}
// //         <Link
// //           to="/products"
// //           className="block w-full text-left px-4 py-2 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded"
// //         >
// //           Add New Product
// //         </Link>

// //         <Link
// //           to="/staff"
// //           className="block w-full text-left px-4 py-2 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded"
// //         >
// //           Add Staff Member
// //         </Link>

// //         <Link
// //           to="/orders"
// //           className="block w-full text-left px-4 py-2 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded"
// //         >
// //           View Pending Orders
// //         </Link>

// //       </div>
// //     </div>
// //   );
// // }

// // function RecentActivity() {
// //   return (
// //     <div className="bg-amber-50 p-6 rounded-lg shadow">
// //       <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
// //       <div className="space-y-3">
// //         <div className="text-sm text-gray-700">No recent activity</div>
// //       </div>
// //     </div>
// //   );
// // }

// function StatCard({ title, value, subtitle, link }: any) {
//   return (
//     <Link
//       to={link}
//       className="bg-rose-200 p-6 rounded-lg shadow hover:bg-rose-300 transition"
//     >
//       <h3 className="text-gray-700 text-sm font-medium mb-2">{title}</h3>
//       <p className="text-3xl font-bold mb-1">{value}</p>
//       {subtitle && <p className="text-sm text-gray-800">{subtitle}</p>}
//     </Link>
//   );
// }
// function QuickActions() {
//   return (
//     <div className="bg-rose-200 p-6 rounded-lg shadow hover:bg-rose-300 transition">
//       <h2 className="text-xl font-bold mb-4 text-gray-800">Quick Actions</h2>
//       <div className="space-y-2">

//         <Link
//           to="/products"
//           className="block w-full text-left px-4 py-2 bg-stone-100 hover:bg-stone-200 text-gray-800 rounded"
      
//         >
//           Add New Product
//         </Link>

//         <Link
//           to="/staff"
//           className="block w-full text-left px-4 py-2 bg-stone-100 hover:bg-stone-200 text-gray-800 rounded"
        
//         >
//           Add Staff Member
//         </Link>

//         <Link
//           to="/orders"
//           className="block w-full text-left px-4 py-2 bg-stone-100 hover:bg-stone-200 text-gray-800 rounded"
        
//         >
//           View Pending Orders
//         </Link>

//       </div>
//     </div>
//   );
// }













import { useEffect, useState } from 'react'; 
import { Link } from 'react-router-dom';
import { ordersAPI, productsAPI, linksAPI, complaintsAPI } from '../api';

interface Stats {
  totalOrders: number;
  pendingOrders: number;
  totalProducts: number;
  activeLinks: number;
  openComplaints: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats>({
    totalOrders: 0,
    pendingOrders: 0,
    totalProducts: 0,
    activeLinks: 0,
    openComplaints: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [orders, products, links, complaints] = await Promise.all([
        ordersAPI.getMyOrders(),
        productsAPI.getMyProducts(),
        linksAPI.getMyLinks(),
        complaintsAPI.getOpenComplaints(),
      ]);

      setStats({
        totalOrders: orders.data.length,
        pendingOrders: orders.data.filter((o: any) => o.status === 'pending').length,
        totalProducts: products.data.length,
        activeLinks: links.data.filter((l: any) => l.status === 'accepted').length,
        openComplaints: complaints.data.length,
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      {/* LEFT: all stats in one vertical column, RIGHT: Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT COLUMN */}
        <div className="space-y-6">
          <StatCard
            title="Total Orders"
            value={stats.totalOrders}
            subtitle={`${stats.pendingOrders} pending`}
            link="/orders"
          />
          <StatCard
            title="Products"
            value={stats.totalProducts}
            link="/products"
          />
          <StatCard
            title="Active Links"
            value={stats.activeLinks}
            link="/links"
          />
          <StatCard
            title="Open Complaints"
            value={stats.openComplaints}
            link="/complaints"
          />
        </div>

        {/* RIGHT COLUMN */}
        <QuickActions />
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, link }: any) {
  return (
    <Link
      to={link}
      className="block w-full bg-purple-200 p-6 rounded-lg shadow hover:bg-purple-300 transition"
    >
      <h3 className="text-gray-700 text-sm font-medium mb-2">{title}</h3>
      <p className="text-3xl font-bold mb-1">{value}</p>
      {subtitle && <p className="text-sm text-gray-800">{subtitle}</p>}
    </Link>
  );
}


function QuickActions() {
  return (
      <div className="self-start bg-purple-200 p-6 rounded-lg shadow hover:bg-purple-300 transition">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Quick Actions</h2>
      <div className="space-y-2">
        <Link
          to="/products"
          className="block w-full text-left px-4 py-2 bg-stone-100 hover:bg-stone-200 text-gray-800 rounded"
        >
          Add New Product
        </Link>

        <Link
          to="/staff"
          className="block w-full text-left px-4 py-2 bg-stone-100 hover:bg-stone-200 text-gray-800 rounded"
        >
          Add Staff Member
        </Link>

        <Link
          to="/orders"
          className="block w-full text-left px-4 py-2 bg-stone-100 hover:bg-stone-200 text-gray-800 rounded"
        >
          View Pending Orders
        </Link>
      </div>
    </div>
  );
}

















// function RecentActivity() {
//   return (
//     <div className="bg-rose-200 p-6 rounded-lg shadow">
//       <h2 className="text-xl font-bold mb-4 text-gray-800">Recent Activity</h2>
//       <div className="space-y-3">
//         <div className="text-sm text-gray-800">No recent activity</div>
//       </div>
//     </div>
//   );
// }

