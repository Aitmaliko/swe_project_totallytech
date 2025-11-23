class Message {
  final int id;
  final int linkId;
  final int senderId;
  final String messageType;
  final String? content;
  final String? fileName;
  final String? fileMimeType;
  final bool isRead;
  final DateTime createdAt;
  final bool hasFile;

  Message({
    required this.id,
    required this.linkId,
    required this.senderId,
    required this.messageType,
    this.content,
    this.fileName,
    this.fileMimeType,
    required this.isRead,
    required this.createdAt,
    required this.hasFile,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      linkId: json['link_id'],
      senderId: json['sender_id'],
      messageType: json['message_type'],
      content: json['content'],
      fileName: json['file_name'],
      fileMimeType: json['file_mime_type'],
      isRead: json['is_read'],
      createdAt: DateTime.parse(json['created_at']),
      hasFile: json['has_file'] ?? false,
    );
  }
}
