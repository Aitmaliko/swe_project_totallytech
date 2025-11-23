import '../models/complaint.dart';
import 'api_service.dart';

class ComplaintService {
  final ApiService _api = ApiService();

  Future<Complaint> createComplaint(CreateComplaintRequest request) async {
    final response = await _api.post('/api/complaints/', request.toJson());
    return Complaint.fromJson(response);
  }

  Future<List<Complaint>> getMyComplaints() async {
    final response = await _api.get('/api/complaints/my-complaints');
    return (response as List).map((json) => Complaint.fromJson(json)).toList();
  }

  Future<Complaint> getComplaint(int complaintId) async {
    final response = await _api.get('/api/complaints/$complaintId');
    return Complaint.fromJson(response);
  }

  Future<Complaint> updateComplaint(
    int complaintId, {
    String? status,
    int? assignedToId,
    String? resolutionNotes,
  }) async {
    final data = {
      if (status != null) 'status': status,
      if (assignedToId != null) 'assigned_to_id': assignedToId,
      if (resolutionNotes != null) 'resolution_notes': resolutionNotes,
    };
    final response = await _api.put('/api/complaints/$complaintId', data);
    return Complaint.fromJson(response);
  }

  Future<Complaint> escalateComplaint(int complaintId) async {
    final response = await _api.post(
      '/api/complaints/$complaintId/escalate',
      {},
    );
    return Complaint.fromJson(response);
  }

  Future<List<Complaint>> getOpenComplaints() async {
    final response = await _api.get('/api/complaints/open/list');
    return (response as List).map((json) => Complaint.fromJson(json)).toList();
  }
}
