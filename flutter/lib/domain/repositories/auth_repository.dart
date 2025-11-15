import 'package:dartz/dartz.dart';

import '../../core/utils/failures.dart';
import '../entities/auth_data.dart';

abstract class AuthRepository {
  Future<Either<Failure, AuthData>> login(String email, String password);
  Future<Either<Failure, AuthData>> register(String email, String password, String name);
  Future<Either<Failure, Unit>> logout();
}