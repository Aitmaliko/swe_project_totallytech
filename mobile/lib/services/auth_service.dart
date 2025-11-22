import '../models/user.dart';
import 'api_service.dart';

class AuthService {
  final ApiService _api = ApiService();

  Future<User> login(String email, String password) async {
    final loginData = {'username': email, 'password': password};

    final response = await _api.postFormData(
      '/api/auth/login',
      loginData,
      requiresAuth: false,
    );

    final tokens = AuthTokens.fromJson(response);
    await _api.saveTokens(tokens.accessToken, tokens.refreshToken);

    return await getCurrentUser();
  }

  Future<User> registerConsumer(RegisterConsumerRequest request) async {
    await _api.post(
      '/api/auth/register/consumer',
      request.toJson(),
      requiresAuth: false,
    );

    return await login(request.email, request.password);
  }

  Future<User> getCurrentUser() async {
    final response = await _api.get('/api/auth/me');
    return User.fromJson(response);
  }

  Future<void> logout() async {
    await _api.clearTokens();
  }

  Future<bool> isLoggedIn() async {
    await _api.loadTokens();
    return _api.accessToken != null;
  }
}
