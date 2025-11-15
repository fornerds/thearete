import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/di/injection.dart';
import '../../domain/usecases/login_usecase.dart';
import '../viewmodels/auth_viewmodel.dart';

final authStateProvider = StateNotifierProvider<AuthViewModel, AuthState>((ref) {
  return AuthViewModel(getIt<LoginUseCase>());
});