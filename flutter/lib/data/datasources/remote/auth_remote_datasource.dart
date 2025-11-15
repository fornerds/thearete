import 'dart:convert';

import '../../../core/utils/exceptions.dart';
import '../../models/auth_data_model.dart';
import '../../models/user_model.dart';
import 'base_api_service.dart';

class AuthRemoteDataSource {
  final BaseApiService apiService;
  
  AuthRemoteDataSource(this.apiService);
  
  Future<AuthDataModel> login(String email, String password) async {
    try {
      final response = await apiService.post('/auth/login', body: {
        'email': email,
        'password': password,
      });
      
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        return AuthDataModel(
          token: data['token'],
          refreshToken: data['refreshToken'],
          user: UserModel.fromJson(data['user']),
        );
      } else {
        throw ServerException('로그인에 실패했습니다.');
      }
    } catch (e) {
      if (e is AppException) {
        rethrow;
      }
      throw NetworkException('네트워크 오류가 발생했습니다.');
    }
  }
  
  Future<AuthDataModel> register(String email, String password, String name) async {
    try {
      final response = await apiService.post('/auth/register', body: {
        'email': email,
        'password': password,
        'name': name,
      });
      
      if (response.statusCode == 201) {
        final Map<String, dynamic> data = json.decode(response.body);
        return AuthDataModel(
          token: data['token'],
          refreshToken: data['refreshToken'],
          user: UserModel.fromJson(data['user']),
        );
      } else {
        throw ServerException('회원가입에 실패했습니다.');
      }
    } catch (e) {
      if (e is AppException) {
        rethrow;
      }
      throw NetworkException('네트워크 오류가 발생했습니다.');
    }
  }
}