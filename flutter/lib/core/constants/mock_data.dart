import '../../domain/entities/user.dart';
import '../../domain/entities/auth_data.dart';

class MockData {
  // 테스트용 로그인 계정
  static const String mockEmail = 'test@test.com';
  static const String mockPassword = '123456';
  
  // Mock 사용자 데이터
  static final User mockUser = User(
    id: '1',
    email: mockEmail,
    name: '테스트 사용자',
    profileImage: null,
    createdAt: DateTime.now(),
  );
  
  // Mock 인증 데이터
  static final AuthData mockAuthData = AuthData(
    token: 'mock_access_token_12345',
    refreshToken: 'mock_refresh_token_67890',
    user: mockUser,
  );
  
  // 유효한 로그인인지 확인
  static bool isValidLogin(String email, String password) {
    return email == mockEmail && password == mockPassword;
  }
}