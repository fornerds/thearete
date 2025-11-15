import 'package:dartz/dartz.dart';

import '../../core/constants/mock_data.dart';
import '../../core/utils/exceptions.dart';
import '../../core/utils/failures.dart';
import '../../domain/entities/auth_data.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/local/auth_local_service.dart';
import '../datasources/remote/auth_remote_datasource.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalService localService;
  
  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localService,
  });
  
  @override
  Future<Either<Failure, AuthData>> login(String email, String password) async {
    try {
      // Mock 데이터로 테스트 (실제 API 호출 대신)
      if (MockData.isValidLogin(email, password)) {
        // 로컬에 토큰 저장
        await localService.saveToken(
          MockData.mockAuthData.token,
          refreshToken: MockData.mockAuthData.refreshToken,
        );
        
        return Right(MockData.mockAuthData);
      } else {
        return const Left(AuthFailure('이메일 또는 비밀번호가 잘못되었습니다.'));
      }
      
      // 실제 API 호출 (주석 처리)
      // final authData = await remoteDataSource.login(email, password);
      // await localService.saveToken(
      //   authData.token,
      //   refreshToken: authData.refreshToken,
      // );
      // return Right(authData.toEntity());
    } catch (e) {
      return Left(NetworkFailure('로그인 중 오류가 발생했습니다.'));
    }
  }
  
  @override
  Future<Either<Failure, AuthData>> register(String email, String password, String name) async {
    try {
      final authData = await remoteDataSource.register(email, password, name);
      
      // 로컬에 토큰 저장
      await localService.saveToken(
        authData.token,
        refreshToken: authData.refreshToken,
      );
      
      return Right(authData.toEntity());
    } on NetworkException catch (e) {
      return Left(NetworkFailure(e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } catch (e) {
      return Left(NetworkFailure('알 수 없는 오류가 발생했습니다.'));
    }
  }
  
  @override
  Future<Either<Failure, Unit>> logout() async {
    try {
      await localService.deleteToken();
      return const Right(unit);
    } catch (e) {
      return Left(CacheFailure('로그아웃 중 오류가 발생했습니다.'));
    }
  }
}