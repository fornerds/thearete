import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../../core/di/injection.dart';
import '../../../core/utils/exceptions.dart';
import '../local/auth_local_service.dart';

class BaseApiService {
  final http.Client client;
  final AuthLocalService _authService = getIt<AuthLocalService>();
  static const String baseUrl = 'http://localhost:3000/api';
  
  BaseApiService(this.client);
  
  Future<http.Response> get(String endpoint) async {
    final token = _authService.getToken();
    
    try {
      final response = await client.get(
        Uri.parse('$baseUrl$endpoint'),
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );
      
      _handleErrorResponse(response);
      return response;
    } catch (e) {
      throw NetworkException('네트워크 오류가 발생했습니다.');
    }
  }
  
  Future<http.Response> post(String endpoint, {Map<String, dynamic>? body}) async {
    final token = _authService.getToken();
    
    try {
      final response = await client.post(
        Uri.parse('$baseUrl$endpoint'),
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
        body: body != null ? json.encode(body) : null,
      );
      
      _handleErrorResponse(response);
      return response;
    } catch (e) {
      throw NetworkException('네트워크 오류가 발생했습니다.');
    }
  }
  
  Future<http.Response> put(String endpoint, {Map<String, dynamic>? body}) async {
    final token = _authService.getToken();
    
    try {
      final response = await client.put(
        Uri.parse('$baseUrl$endpoint'),
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
        body: body != null ? json.encode(body) : null,
      );
      
      _handleErrorResponse(response);
      return response;
    } catch (e) {
      throw NetworkException('네트워크 오류가 발생했습니다.');
    }
  }
  
  Future<http.Response> delete(String endpoint) async {
    final token = _authService.getToken();
    
    try {
      final response = await client.delete(
        Uri.parse('$baseUrl$endpoint'),
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );
      
      _handleErrorResponse(response);
      return response;
    } catch (e) {
      throw NetworkException('네트워크 오류가 발생했습니다.');
    }
  }
  
  void _handleErrorResponse(http.Response response) {
    switch (response.statusCode) {
      case 401:
        // 토큰 만료 시 자동 로그아웃
        _authService.deleteToken();
        throw UnauthorizedException('인증이 만료되었습니다. 다시 로그인해주세요.');
      case 403:
        throw ForbiddenException('접근 권한이 없습니다.');
      case 404:
        throw NotFoundException('요청한 리소스를 찾을 수 없습니다.');
      case 500:
        throw ServerException('서버 오류가 발생했습니다.');
      default:
        if (response.statusCode >= 400) {
          throw ServerException('오류가 발생했습니다. (${response.statusCode})');
        }
    }
  }
}