import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/di/injection.dart';
import '../../data/datasources/local/auth_local_service.dart';
import '../../domain/entities/user.dart';
import '../../domain/usecases/login_usecase.dart';

class AuthState {
  final bool isLoading;
  final bool isLoggedIn;
  final String? token;
  final User? user;
  final String? errorMessage;
  
  AuthState({
    this.isLoading = false,
    this.isLoggedIn = false,
    this.token,
    this.user,
    this.errorMessage,
  });
  
  AuthState copyWith({
    bool? isLoading,
    bool? isLoggedIn,
    String? token,
    User? user,
    String? errorMessage,
  }) {
    return AuthState(
      isLoading: isLoading ?? this.isLoading,
      isLoggedIn: isLoggedIn ?? this.isLoggedIn,
      token: token ?? this.token,
      user: user ?? this.user,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}

class AuthViewModel extends StateNotifier<AuthState> {
  final LoginUseCase loginUseCase;
  final AuthLocalService _localService = getIt<AuthLocalService>();
  
  AuthViewModel(this.loginUseCase) : super(AuthState()) {
    _checkLoginStatus();
  }
  
  // 앱 시작 시 로그인 상태 확인
  void _checkLoginStatus() {
    final token = _localService.getToken();
    if (token != null) {
      state = state.copyWith(isLoggedIn: true, token: token);
    }
  }
  
  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    
    final result = await loginUseCase.execute(email, password);
    
    result.fold(
      (failure) => state = state.copyWith(
        isLoading: false,
        errorMessage: failure.message,
      ),
      (authData) => state = state.copyWith(
        isLoading: false,
        isLoggedIn: true,
        token: authData.token,
        user: authData.user,
        errorMessage: null,
      ),
    );
  }
  
  Future<void> logout() async {
    await _localService.deleteToken();
    state = AuthState(); // 초기 상태로 리셋
  }
  
  void clearError() {
    state = state.copyWith(errorMessage: null);
  }
}