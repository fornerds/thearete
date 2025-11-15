import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final String? profileImage;
  final DateTime createdAt;
  
  const User({
    required this.id,
    required this.email,
    required this.name,
    this.profileImage,
    required this.createdAt,
  });
  
  @override
  List<Object?> get props => [id, email, name, profileImage, createdAt];
}