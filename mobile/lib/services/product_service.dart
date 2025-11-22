import '../models/product.dart';
import 'api_service.dart';

class ProductService {
  final ApiService _api = ApiService();

  Future<List<Product>> getSupplierProducts(int supplierId) async {
    final response = await _api.get('/api/products/supplier/$supplierId');
    return (response as List).map((json) => Product.fromJson(json)).toList();
  }

  Future<List<Product>> getMyProducts() async {
    final response = await _api.get('/api/products/my-products');
    return (response as List).map((json) => Product.fromJson(json)).toList();
  }

  Future<Product> createProduct({
    required String name,
    required String description,
    required String category,
    required String unit,
    required double price,
    required int stockQuantity,
  }) async {
    final data = {
      'name': name,
      'description': description,
      'category': category,
      'unit': unit,
      'price': price,
      'stock_quantity': stockQuantity,
      'is_available': true,
    };
    final response = await _api.post('/api/products/', data);
    return Product.fromJson(response);
  }

  Future<Product> updateProduct(
    int productId,
    Map<String, dynamic> data,
  ) async {
    final response = await _api.put('/api/products/$productId', data);
    return Product.fromJson(response);
  }

  String getProductImageUrl(int productId) {
    return '${ApiService.baseUrl}/api/products/$productId/image';
  }
}
