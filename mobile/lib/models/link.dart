class Link {
  final int id;
  final int consumerId;
  final int supplierId;
  final String? consumerName;
  final String? supplierName;
  final String status;
  final DateTime requestedAt;
  final DateTime? respondedAt;
  final String? notes;

  Link({
    required this.id,
    required this.consumerId,
    required this.supplierId,
    this.consumerName,
    this.supplierName,
    required this.status,
    required this.requestedAt,
    this.respondedAt,
    this.notes,
  });

  factory Link.fromJson(Map<String, dynamic> json) {
    return Link(
      id: json['id'],
      consumerId: json['consumer_id'],
      supplierId: json['supplier_id'],
      consumerName: json['consumer_name'],
      supplierName: json['supplier_name'],
      status: json['status'],
      requestedAt: DateTime.parse(json['requested_at']),
      respondedAt: json['responded_at'] != null
          ? DateTime.parse(json['responded_at'])
          : null,
      notes: json['notes'],
    );
  }
}

class LinkRequest {
  final int supplierId;
  final String? notes;

  LinkRequest({required this.supplierId, this.notes});

  Map<String, dynamic> toJson() => {'supplier_id': supplierId, 'notes': notes};
}
