import 'package:flutter/material.dart';

/// 앱에서 사용하는 색상 상수
/// Figma 디자인에서 추출한 키컬러를 관리합니다.
class AppColors {
  AppColors._();
  // Medical Theme Colors (Figma에서 추출한 색상 팔레트)
  // AdobeColor-Blurred interior of hospital - abstract medical background
  /// 짙은 남색 - 주요 텍스트, 강조 요소에 사용
  static const Color medicalDarkBlue = Color(0xFF1B4159);

  /// 중간 톤의 청회색 - 보조 요소, 배경에 사용
  static const Color medicalBlueGray = Color(0xFF45718C);

  /// 밝은 청회색 - 경계선, 구분선에 사용
  static const Color medicalLightBlueGray = Color(0xFF6894A6);

  /// 옅은 하늘색 - 배경, 여백에 사용
  static const Color medicalPaleBlue = Color(0xFFBFD1D9);

  /// 거의 흰색에 가까운 옅은 회색 - 메인 배경색에 사용
  static const Color medicalOffWhite = Color(0xFFF2F2F2);

  // GrayScale Colors (Figma 디자인 시스템)
  /// 배경색 - 흰색
  static const Color grayScaleBackground = Color(0xFFFFFFFF);

  /// 텍스트 색상
  static const Color grayScaleText = Color(0xFF374151);

  /// 박스 색상 1 - 프로필 아이콘 배경색
  static const Color grayScaleBox1 = Color(0xFFEAEBEF);

  /// 입력 필드 배경색
  static const Color grayScaleBox3 = Color(0xFFF9FAFB);

  /// 가이드 텍스트 색상 (Placeholder 등)
  static const Color grayScaleGuideText = Color(0xFFBAC2D0);

  // Key Colors (Figma 디자인 시스템)
  /// 키컬러 4 - 버튼 배경색
  static const Color keyColor4 = Color(0xFF45718C); // medicalBlueGray와 동일

  /// 박스 색상 - 버튼 텍스트 색상
  static const Color box = Color(0xFFF6F6F6);

  /// 서브 텍스트 1 색상
  static const Color grayScaleSubText1 = Color(0xFF4B5563);

  /// 서브 텍스트 2 색상
  static const Color grayScaleSubText2 = Color(0xFF6B7280);

  /// 서브 텍스트 3 색상
  static const Color grayScaleSubText3 = Color(0xFF959BA9);

  /// 블랙 색상
  static const Color grayScaleBlack = Color(0xFF1F2937);

  /// 라인 색상 (구분선)
  static const Color grayScaleLine = Color(0xFFE5E7EB);

  /// 약한 라인 색상 (가로선)
  static const Color grayScaleLineWeak = Color(0xFFEEEFF1);

  /// 키컬러 2 - 핀 아이콘 활성화 fill 색상
  static const Color keyColor2 = Color(0xFFBFD2D9);

  /// 키컬러 3 - 주소 검색 버튼 테두리 색상, 핀 아이콘 활성화 stroke 색상
  static const Color keyColor3 = Color(0xFF6994A5);

  /// 키컬러 1 - 진행중인 시술 버튼 배경색
  static const Color keyColor1 = Color(0xFFF2F6F6);
}


