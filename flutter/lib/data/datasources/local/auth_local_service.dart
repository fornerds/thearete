import 'package:hive/hive.dart';

class AuthLocalService {
  static const String _authBox = 'auth';
  static const String _tokenKey = 'token';
  static const String _refreshTokenKey = 'refreshToken';
  
  Future<void> saveToken(String token, {String? refreshToken}) async {
    final box = await Hive.openBox(_authBox);
    await box.put(_tokenKey, token);
    if (refreshToken != null) {
      await box.put(_refreshTokenKey, refreshToken);
    }
  }
  
  String? getToken() {
    try {
      final box = Hive.box(_authBox);
      return box.get(_tokenKey);
    } catch (e) {
      // Box가 열리지 않은 경우 null 반환
      return null;
    }
  }
  
  String? getRefreshToken() {
    try {
      final box = Hive.box(_authBox);
      return box.get(_refreshTokenKey);
    } catch (e) {
      return null;
    }
  }
  
  Future<void> deleteToken() async {
    final box = await Hive.openBox(_authBox);
    await box.delete(_tokenKey);
    await box.delete(_refreshTokenKey);
  }
  
  bool isLoggedIn() {
    return getToken() != null;
  }
}