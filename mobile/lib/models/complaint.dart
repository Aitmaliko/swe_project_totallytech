class Complaint {
  final int id;
  final int? orderId;
  final int linkId;
  final int createdById;
  final int? assignedToId;
  final String title;
  final String description;
  final String complaintType;
  final String status;
  final String priority;
  final String? resolutionNotes;
  final DateTime createdAt;

  Complaint({
    required this.id,
    this.orderId,
    required this.linkId,
    required this.createdById,
    this.assignedToId,
    required this.title,
    required this.description,
    required this.complaintType,
    required this.status,
    required this.priority,
    this.resolutionNotes,
    required this.createdAt,
  });

  factory Complaint.fromJson(Map<String, dynamic> json) {
    return Complaint(
      id: json['id'],
      orderId: json['order_id'],
      linkId: json['link_id'],
      createdById: json['created_by_id'],
      assignedToId: json['assigned_to_id'],
      title: json['title'],
      description: json['description'],
      complaintType: json['complaint_type'] ?? 'other',
      status: json['status'],
      priority: json['priority'],
      resolutionNotes: json['resolution_notes'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class CreateComplaintRequest {
  final int? orderId;
  final int? linkId;
  final String title;
  final String description;
  final String complaintType;
  final String priority;

  CreateComplaintRequest({
    this.orderId,
    this.linkId,
    required this.title,
    required this.description,
    required this.complaintType,
    this.priority = 'normal',
  });

  Map<String, dynamic> toJson() => {
    if (orderId != null) 'order_id': orderId,
    if (linkId != null) 'link_id': linkId,
    'title': title,
    'description': description,
    'complaint_type': complaintType,
    'priority': priority,
  };
}
