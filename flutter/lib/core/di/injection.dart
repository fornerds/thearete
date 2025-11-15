import 'package:get_it/get_it.dart';
import 'package:http/http.dart' as http;

import '../../data/datasources/local/auth_local_service.dart';
import '../../data/datasources/remote/auth_remote_datasource.dart';
import '../../data/datasources/remote/base_api_service.dart';
import '../../data/repositories/auth_repository_impl.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/usecases/login_usecase.dart';

final getIt = GetIt.instance;

Future<void> setupDependencies() async {
  // HTTP Client
  getIt.registerLazySingleton<http.Client>(() => http.Client());
  
  // Local Services
  getIt.registerLazySingleton<AuthLocalService>(() => AuthLocalService());
  
  // API Services
  getIt.registerLazySingleton<BaseApiService>(
    () => BaseApiService(getIt<http.Client>()),
  );
  
  // Remote Data Sources
  getIt.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSource(getIt<BaseApiService>()),
  );
  
  // Repositories
  getIt.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: getIt<AuthRemoteDataSource>(),
      localService: getIt<AuthLocalService>(),
    ),
  );
  
  // Use Cases
  getIt.registerLazySingleton<LoginUseCase>(
    () => LoginUseCase(getIt<AuthRepository>()),
  );
}