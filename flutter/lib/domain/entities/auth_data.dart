import 'package:equatable/equatable.dart';
import 'user.dart';

class AuthData extends Equatable {
  final String token;
  final String? refreshToken;
  final User user;
  
  const AuthData({
    required this.token,
    this.refreshToken,
    required this.user,
  });
  
  @override
  List<Object?> get props => [token, refreshToken, user];
}