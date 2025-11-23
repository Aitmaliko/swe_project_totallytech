import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { useEffect } from 'react';
import { useAuthStore } from './store';
import { authAPI } from './api';

import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Orders from './pages/Orders';
import Links from './pages/Links';
// import Suppliers from './pages/Suppliers';
import Complaints from './pages/Complaints';
import Staff from './pages/Staff';
// import Messages from './pages/Messages';

function App() {
  const { isAuthenticated, setUser } = useAuthStore();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authAPI.getCurrentUser()
        .then(response => setUser(response.data))
        .catch(() => localStorage.removeItem('access_token'));
    }
  }, [setUser]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/*"
          element={
            isAuthenticated ? (
              <MainLayout />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

function MainLayout() {
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-[#faf6ef] text-black">
      <nav className="bg-purple shadow-sm">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex space-x-8">
              <Link
                to="/dashboard"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
              >
                Dashboard
              </Link>
              <Link
                to="/products"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                Products
              </Link>
              <Link
                to="/orders"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                Orders
              </Link>
              {/* <Link
                to="/suppliers"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                Suppliers
              </Link> */}
              <Link
                to="/links"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                Links
              </Link>
              <Link
                to="/complaints"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                Complaints
              </Link>
              {/* <Link
                to="/messages"
                className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                Messages
              </Link> */}
              {user?.role === 'owner' && (
                <Link
                  to="/staff"
                  className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
                >
                  Staff Management
                </Link>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">{user?.full_name}</span>
              <button
                onClick={logout}
                className="text-sm text-gray-700 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto">
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/products" element={<Products />} />
          <Route path="/orders" element={<Orders />} />
          {/* <Route path="/suppliers" element={<Suppliers />} /> */}
          <Route path="/links" element={<Links />} />
          <Route path="/complaints" element={<Complaints />} />
          {/* <Route path="/messages" element={<Messages />} /> */}
          <Route path="/staff" element={<Staff />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
