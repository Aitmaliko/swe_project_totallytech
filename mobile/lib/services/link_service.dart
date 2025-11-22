import '../models/link.dart';
import 'api_service.dart';

class LinkService {
  final ApiService _api = ApiService();

  Future<Link> requestLink(int supplierId, String? notes) async {
    final request = LinkRequest(supplierId: supplierId, notes: notes);
    final response = await _api.post('/api/links/request', request.toJson());
    return Link.fromJson(response);
  }

  Future<List<Link>> getPendingLinks() async {
    final response = await _api.get('/api/links/pending');
    return (response as List).map((json) => Link.fromJson(json)).toList();
  }

  Future<List<Link>> getMyLinks() async {
    final response = await _api.get('/api/links/my-links');
    return (response as List).map((json) => Link.fromJson(json)).toList();
  }

  Future<List<Link>> getAcceptedLinks() async {
    final response = await _api.get('/api/links/accepted');
    return (response as List).map((json) => Link.fromJson(json)).toList();
  }

  Future<Link> updateLinkStatus(
    int linkId,
    String status,
    String? notes,
  ) async {
    final data = {'status': status, if (notes != null) 'notes': notes};
    final response = await _api.put('/api/links/$linkId', data);
    return Link.fromJson(response);
  }

  Future<void> blockLink(int linkId) async {
    await _api.delete('/api/links/$linkId');
  }
}
