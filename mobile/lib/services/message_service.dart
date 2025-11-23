import '../models/message.dart';
import 'api_service.dart';

class MessageService {
  final ApiService _api = ApiService();

  Future<Message> sendTextMessage(int linkId, String content) async {
    final data = {
      'link_id': linkId,
      'message_type': 'text',
      'content': content,
    };
    final response = await _api.post('/api/messages/', data);
    return Message.fromJson(response);
  }

  Future<List<Message>> getMessages(
    int linkId, {
    int skip = 0,
    int limit = 100,
  }) async {
    final response = await _api.get(
      '/api/messages/link/$linkId?skip=$skip&limit=$limit',
    );
    return (response as List).map((json) => Message.fromJson(json)).toList();
  }

  Future<void> markAsRead(int messageId) async {
    await _api.put('/api/messages/$messageId/read', {});
  }

  Future<Map<String, dynamic>> getUnreadCount() async {
    return await _api.get('/api/messages/unread/count');
  }

  String getMessageFileUrl(int messageId) {
    return '${ApiService.baseUrl}/api/messages/$messageId/file';
  }
}
