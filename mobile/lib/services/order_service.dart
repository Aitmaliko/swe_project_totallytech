import '../models/order.dart';
import 'api_service.dart';

class OrderService {
  final ApiService _api = ApiService();

  Future<Order> createOrder(CreateOrderRequest request) async {
    final response = await _api.post('/api/orders/', request.toJson());
    return Order.fromJson(response);
  }

  Future<List<Order>> getMyOrders() async {
    final response = await _api.get('/api/orders/my-orders');
    return (response as List).map((json) => Order.fromJson(json)).toList();
  }

  Future<Order> getOrder(int orderId) async {
    final response = await _api.get('/api/orders/$orderId');
    return Order.fromJson(response);
  }

  Future<List<Order>> getPendingOrders() async {
    final response = await _api.get('/api/orders/pending/list');
    return (response as List).map((json) => Order.fromJson(json)).toList();
  }

  Future<Order> updateOrderStatus(
    int orderId,
    String status,
    String? notes,
  ) async {
    final data = {'status': status, if (notes != null) 'notes': notes};
    final response = await _api.put('/api/orders/$orderId', data);
    return Order.fromJson(response);
  }

  Future<void> cancelOrder(int orderId) async {
    await _api.delete('/api/orders/$orderId');
  }
}
