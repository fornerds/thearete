import 'package:json_annotation/json_annotation.dart';

import '../../domain/entities/auth_data.dart';
import '../../domain/entities/user.dart';
import 'user_model.dart';

part 'auth_data_model.g.dart';

@JsonSerializable()
class AuthDataModel {
  final String token;
  final String? refreshToken;
  final UserModel user;

  const AuthDataModel({
    required this.token,
    this.refreshToken,
    required this.user,
  });
  
  factory AuthDataModel.fromJson(Map<String, dynamic> json) => _$AuthDataModelFromJson(json);
  
  Map<String, dynamic> toJson() => _$AuthDataModelToJson(this);
  
  AuthData toEntity() {
    return AuthData(
      token: token,
      refreshToken: refreshToken,
      user: user.toEntity(),
    );
  }
  
  factory AuthDataModel.fromEntity(AuthData authData) {
    return AuthDataModel(
      token: authData.token,
      refreshToken: authData.refreshToken,
      user: UserModel.fromEntity(authData.user),
    );
  }
}