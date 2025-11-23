import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String _webBaseUrl = kReleaseMode
      ? String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000')
      : 'http://localhost:8000';
  static const String _androidBaseUrl = 'http://10.0.2.2:8000';
  static const String _defaultBaseUrl = 'http://localhost:8000';

  static String get baseUrl {
    if (kIsWeb) return _webBaseUrl;

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return _androidBaseUrl;
      default:
        return _defaultBaseUrl;
    }
  }

  String? _accessToken;
  String? _refreshToken;

  // Публичный геттер для проверки токена
  String? get accessToken => _accessToken;

  Future<void> loadTokens() async {
    final prefs = await SharedPreferences.getInstance();
    _accessToken = prefs.getString('access_token');
    _refreshToken = prefs.getString('refresh_token');
  }

  Future<void> saveTokens(String accessToken, String refreshToken) async {
    _accessToken = accessToken;
    _refreshToken = refreshToken;

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', accessToken);
    await prefs.setString('refresh_token', refreshToken);
  }

  Future<void> clearTokens() async {
    _accessToken = null;
    _refreshToken = null;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('refresh_token');
  }

  Map<String, String> _getHeaders({bool includeAuth = true}) {
    final headers = {'Content-Type': 'application/json'};

    if (includeAuth && _accessToken != null) {
      headers['Authorization'] = 'Bearer $_accessToken';
    }

    return headers;
  }

  Future<dynamic> get(String endpoint, {bool requiresAuth = true}) async {
    if (requiresAuth) await loadTokens();

    final response = await http.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: _getHeaders(includeAuth: requiresAuth),
    );

    return _handleResponse(response);
  }

  Future<dynamic> post(
    String endpoint,
    Map<String, dynamic> data, {
    bool requiresAuth = true,
  }) async {
    if (requiresAuth) await loadTokens();

    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: _getHeaders(includeAuth: requiresAuth),
      body: json.encode(data),
    );

    return _handleResponse(response);
  }

  Future<dynamic> postFormData(
    String endpoint,
    Map<String, String> data, {
    bool requiresAuth = true,
  }) async {
    if (requiresAuth) await loadTokens();

    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: {
        if (requiresAuth && _accessToken != null)
          'Authorization': 'Bearer $_accessToken',
      },
      body: data,
    );

    return _handleResponse(response);
  }

  Future<dynamic> put(
    String endpoint,
    Map<String, dynamic> data, {
    bool requiresAuth = true,
  }) async {
    if (requiresAuth) await loadTokens();

    final response = await http.put(
      Uri.parse('$baseUrl$endpoint'),
      headers: _getHeaders(includeAuth: requiresAuth),
      body: json.encode(data),
    );

    return _handleResponse(response);
  }

  Future<dynamic> delete(String endpoint, {bool requiresAuth = true}) async {
    if (requiresAuth) await loadTokens();

    final response = await http.delete(
      Uri.parse('$baseUrl$endpoint'),
      headers: _getHeaders(includeAuth: requiresAuth),
    );

    return _handleResponse(response);
  }

  dynamic _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return null;
      return json.decode(response.body);
    } else {
      final error = json.decode(response.body);
      throw Exception(error['detail'] ?? 'Unknown error');
    }
  }
}
