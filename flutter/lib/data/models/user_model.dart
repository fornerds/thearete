import 'package:json_annotation/json_annotation.dart';

import '../../domain/entities/user.dart';

part 'user_model.g.dart';

@JsonSerializable()
class UserModel {
  final String id;
  final String email;
  final String name;
  final String? profileImage;
  final DateTime createdAt;

  const UserModel({
    required this.id,
    required this.email,
    required this.name,
    this.profileImage,
    required this.createdAt,
  });
  
  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  
  Map<String, dynamic> toJson() => _$UserModelToJson(this);
  
  User toEntity() {
    return User(
      id: id,
      email: email,
      name: name,
      profileImage: profileImage,
      createdAt: createdAt,
    );
  }
  
  factory UserModel.fromEntity(User user) {
    return UserModel(
      id: user.id,
      email: user.email,
      name: user.name,
      profileImage: user.profileImage,
      createdAt: user.createdAt,
    );
  }
}