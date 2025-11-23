// import { useEffect, useState } from 'react';
// import { suppliersAPI, linksAPI } from '../api';

// interface Supplier {
//   id: number;
//   company_name: string;
//   company_address: string | null;
//   tax_id: string | null;
//   description: string | null;
// }

// export default function Suppliers() {
//   const [suppliers, setSuppliers] = useState<Supplier[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [selectedSupplier, setSelectedSupplier] = useState<number | null>(null);
//   const [notes, setNotes] = useState('');
//   const [showModal, setShowModal] = useState(false);

//   useEffect(() => {
//     loadSuppliers();
//   }, []);

//   const loadSuppliers = async () => {
//     try {
//       const response = await suppliersAPI.getAllSuppliers();
//       setSuppliers(response.data);
//     } catch (error) {
//       console.error('Failed to load suppliers:', error);
//       alert('Failed to load suppliers:');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleRequestLink = (supplierId: number) => {
//     setSelectedSupplier(supplierId);
//     setNotes('');
//     setShowModal(true);
//   };

//   const handleSubmitRequest = async () => {
//     if (!selectedSupplier) return;

//     try {
//       await linksAPI.requestLink(selectedSupplier, notes);
//       alert('Contact request sent successfully!');
//       setShowModal(false);
//       setSelectedSupplier(null);
//       setNotes('');
//     } catch (error: any) {
//       console.error('Failed to request link:', error);
//       const errorMessage = error.response?.data?.detail || 'Failed to request contact link:';
//       alert(errorMessage);
//     }
//   };

//   if (loading) {
//     return <div className="p-6">Loading...</div>;
//   }

//   return (
//     <div className="p-6">
//       <h1 className="text-3xl font-bold mb-6">Search For Suppliers</h1>

//       <div className="bg-white rounded-lg shadow overflow-hidden">
//         <table className="min-w-full divide-y divide-gray-200">
//           <thead className="bg-gray-50">
//             <tr>
//               <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
//                 ID
//               </th>
//               <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
//                 Company Name
//               </th>
//               <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
//                 Adress
//               </th>
//               <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
//                 Tax ID
//               </th>
//               <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
//                 Action
//               </th>
//             </tr>
//           </thead>
//           <tbody className="bg-white divide-y divide-gray-200">
//             {suppliers.length === 0 ? (
//               <tr>
//                 <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
//                   Suppliers Not Found
//                 </td>
//               </tr>
//             ) : (
//               suppliers.map((supplier) => (
//                 <tr key={supplier.id}>
//                   <td className="px-6 py-4 whitespace-nowrap">{supplier.id}</td>
//                   <td className="px-6 py-4 whitespace-nowrap">
//                     <div className="text-sm font-medium text-gray-900">
//                       {supplier.company_name}
//                     </div>
//                   </td>
//                   <td className="px-6 py-4">{supplier.company_address || '-'}</td>
//                   <td className="px-6 py-4 whitespace-nowrap">
//                     {supplier.tax_id || '-'}
//                   </td>
//                   <td className="px-6 py-4 whitespace-nowrap text-right">
//                     <button
//                       onClick={() => handleRequestLink(supplier.id)}
//                       className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//                     >
//                       Send request
//                     </button>
//                   </td>
//                 </tr>
//               ))
//             )}
//           </tbody>
//         </table>
//       </div>

//       {/* Модальное окно для отправки запроса */}
//       {showModal && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
//           <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
//             <h2 className="text-xl font-bold mb-4">Sent contact link request</h2>
            
//             <div className="mb-4">
//               <label className="block text-sm font-medium text-gray-700 mb-2">
//                 Notes (optional)
//               </label>
//               <textarea
//                 value={notes}
//                 onChange={(e) => setNotes(e.target.value)}
//                 className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
//                 rows={4}
//                 placeholder="Add notes to your request..."
//               />
//             </div>

//             <div className="flex space-x-3">
//               <button
//                 onClick={handleSubmitRequest}
//                 className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//               >
//                 Send
//               </button>
//               <button
//                 onClick={() => {
//                   setShowModal(false);
//                   setSelectedSupplier(null);
//                   setNotes('');
//                 }}
//                 className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
//               >
//                 Cancel
//               </button>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }
