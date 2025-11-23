import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor для добавления токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  login: (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  getCurrentUser: () => api.get('/api/auth/me'),
  registerSupplier: (data: any) => api.post('/api/auth/register/supplier', data),
  createStaff: (data: any) => api.post('/api/auth/create-staff', data),
  getStaff: () => api.get('/api/auth/staff'),
  deleteStaff: (id: number) => api.delete(`/api/auth/staff/${id}`),
  deactivateAccount: () => api.delete('/api/auth/account'),
};

// Products API
export const productsAPI = {
  getMyProducts: () => api.get('/api/products/my-products'),
  createProduct: (data: any) => api.post('/api/products/', data),
  updateProduct: (id: number, data: any) => api.put(`/api/products/${id}`, data),
  deleteProduct: (id: number) => api.delete(`/api/products/${id}`),
  uploadImage: (id: number, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/api/products/${id}/image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Orders API
export const ordersAPI = {
  getMyOrders: () => api.get('/api/orders/my-orders'),
  getPendingOrders: () => api.get('/api/orders/pending/list'),
  getOrder: (id: number) => api.get(`/api/orders/${id}`),
  updateOrderStatus: (id: number, status: string, notes?: string) =>
    api.put(`/api/orders/${id}`, { status, notes }),
};

// Suppliers API
export const suppliersAPI = {
  getAllSuppliers: () => api.get('/api/suppliers/'),
  getSupplier: (id: number) => api.get(`/api/suppliers/${id}`),
};

// Links API
export const linksAPI = {
  requestLink: (supplier_id: number, notes?: string) =>
    api.post('/api/links/request', { supplier_id, notes }),
  getMyLinks: () => api.get('/api/links/my-links'),
  getPendingLinks: () => api.get('/api/links/pending'),
  getAcceptedLinks: () => api.get('/api/links/accepted'),
  updateLinkStatus: (id: number, status: string, notes?: string) =>
    api.put(`/api/links/${id}`, { status, notes }),
  blockLink: (id: number) => api.delete(`/api/links/${id}`),
};

// Complaints API
export const complaintsAPI = {
  getMyComplaints: () => api.get('/api/complaints/my-complaints'),
  getOpenComplaints: () => api.get('/api/complaints/open/list'),
  getComplaint: (id: number) => api.get(`/api/complaints/${id}`),
  updateComplaint: (id: number, data: any) => api.put(`/api/complaints/${id}`, data),
  escalateComplaint: (id: number) => api.post(`/api/complaints/${id}/escalate`, {}),
};

