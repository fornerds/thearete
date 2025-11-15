// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'auth_data_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

AuthDataModel _$AuthDataModelFromJson(Map<String, dynamic> json) =>
    AuthDataModel(
      token: json['token'] as String,
      refreshToken: json['refreshToken'] as String?,
      user: UserModel.fromJson(json['user'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$AuthDataModelToJson(AuthDataModel instance) =>
    <String, dynamic>{
      'token': instance.token,
      'refreshToken': instance.refreshToken,
      'user': instance.user,
    };
