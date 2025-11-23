class Product {
  final int id;
  final int supplierId;
  final String name;
  final String? description;
  final String? category;
  final String unit;
  final double price;
  final int stockQuantity;
  final bool isAvailable;
  final bool hasImage;

  Product({
    required this.id,
    required this.supplierId,
    required this.name,
    this.description,
    this.category,
    required this.unit,
    required this.price,
    required this.stockQuantity,
    required this.isAvailable,
    required this.hasImage,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      supplierId: json['supplier_id'],
      name: json['name'],
      description: json['description'],
      category: json['category'],
      unit: json['unit'],
      price: (json['price'] as num).toDouble(),
      stockQuantity: json['stock_quantity'],
      isAvailable: json['is_available'],
      hasImage: json['has_image'] ?? false,
    );
  }
}
