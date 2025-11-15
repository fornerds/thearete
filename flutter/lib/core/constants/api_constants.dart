class ApiConstants {
  static const String baseUrl = 'http://localhost:3000/api';
  
  // Auth endpoints
  static const String login = '/auth/login';
  static const String register = '/auth/register';
  static const String refreshToken = '/auth/refresh';
  
  // Client endpoints
  static const String clients = '/clients';
  static String clientDetail(String id) => '/clients/$id';
  
  // Procedure endpoints
  static const String procedures = '/procedures';
  static String procedureDetail(String id) => '/procedures/$id';
  static String procedureResult(String id) => '/procedures/$id/result';
  
  // Clinic endpoints
  static const String clinicDashboard = '/clinic/dashboard';
  static const String clinicInfo = '/clinic/info';
}