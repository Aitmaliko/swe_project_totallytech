class Order {
  final int id;
  final int consumerId;
  final int supplierId;
  final String status;
  final double totalAmount;
  final String? notes;
  final DateTime createdAt;
  final List<OrderItem> items;

  Order({
    required this.id,
    required this.consumerId,
    required this.supplierId,
    required this.status,
    required this.totalAmount,
    this.notes,
    required this.createdAt,
    required this.items,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      consumerId: json['consumer_id'],
      supplierId: json['supplier_id'],
      status: json['status'],
      totalAmount: (json['total_amount'] as num).toDouble(),
      notes: json['notes'],
      createdAt: DateTime.parse(json['created_at']),
      items: (json['items'] as List)
          .map((item) => OrderItem.fromJson(item))
          .toList(),
    );
  }
}

class OrderItem {
  final int id;
  final int productId;
  final int quantity;
  final double unitPrice;
  final double totalPrice;

  OrderItem({
    required this.id,
    required this.productId,
    required this.quantity,
    required this.unitPrice,
    required this.totalPrice,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'],
      productId: json['product_id'],
      quantity: json['quantity'],
      unitPrice: (json['unit_price'] as num).toDouble(),
      totalPrice: (json['total_price'] as num).toDouble(),
    );
  }
}

class CreateOrderRequest {
  final int supplierId;
  final List<OrderItemRequest> items;
  final String? notes;

  CreateOrderRequest({
    required this.supplierId,
    required this.items,
    this.notes,
  });

  Map<String, dynamic> toJson() => {
    'supplier_id': supplierId,
    'items': items.map((item) => item.toJson()).toList(),
    'notes': notes,
  };
}

class OrderItemRequest {
  final int productId;
  final int quantity;

  OrderItemRequest({required this.productId, required this.quantity});

  Map<String, dynamic> toJson() => {
    'product_id': productId,
    'quantity': quantity,
  };
}
