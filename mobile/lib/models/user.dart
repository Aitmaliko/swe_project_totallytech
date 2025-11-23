class User {
  final int id;
  final String email;
  final String? phone;
  final String fullName;
  final String role;
  final bool isActive;

  User({
    required this.id,
    required this.email,
    this.phone,
    required this.fullName,
    required this.role,
    required this.isActive,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      phone: json['phone'],
      fullName: json['full_name'],
      role: json['role'],
      isActive: json['is_active'],
    );
  }
}

class LoginRequest {
  final String email;
  final String password;

  LoginRequest({required this.email, required this.password});

  Map<String, dynamic> toJson() => {
    'username': email, // OAuth2PasswordRequestForm uses 'username'
    'password': password,
  };
}

class RegisterConsumerRequest {
  final String email;
  final String phone;
  final String fullName;
  final String password;
  final String businessName;
  final String? businessType;
  final String? address;

  RegisterConsumerRequest({
    required this.email,
    required this.phone,
    required this.fullName,
    required this.password,
    required this.businessName,
    this.businessType,
    this.address,
  });

  Map<String, dynamic> toJson() => {
    'user': {
      'email': email,
      'phone': phone,
      'full_name': fullName,
      'password': password,
      'role': 'consumer',
    },
    'consumer_info': {
      'business_name': businessName,
      'business_type': businessType,
      'address': address,
    },
  };
}

class AuthTokens {
  final String accessToken;
  final String refreshToken;

  AuthTokens({required this.accessToken, required this.refreshToken});

  factory AuthTokens.fromJson(Map<String, dynamic> json) {
    return AuthTokens(
      accessToken: json['access_token'],
      refreshToken: json['refresh_token'],
    );
  }
}
