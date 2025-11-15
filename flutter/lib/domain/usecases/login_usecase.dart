import 'package:dartz/dartz.dart';

import '../../core/utils/failures.dart';
import '../entities/auth_data.dart';
import '../repositories/auth_repository.dart';

class LoginUseCase {
  final AuthRepository repository;
  
  LoginUseCase(this.repository);
  
  Future<Either<Failure, AuthData>> execute(String email, String password) async {
    if (email.isEmpty || password.isEmpty) {
      return const Left(ValidationFailure('이메일과 비밀번호를 입력해주세요.'));
    }
    
    if (!_isValidEmail(email)) {
      return const Left(ValidationFailure('올바른 이메일 형식이 아닙니다.'));
    }
    
    return await repository.login(email, password);
  }
  
  bool _isValidEmail(String email) {
    return RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(email);
  }
}