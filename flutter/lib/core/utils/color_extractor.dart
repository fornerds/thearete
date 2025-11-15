import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

/// Figma 이미지에서 키컬러를 추출하는 유틸리티
class ColorExtractor {
  /// 이미지에서 주요 색상을 추출합니다.
  /// 
  /// [imageBytes] 이미지 바이트 데이터
  /// [sampleCount] 샘플링할 픽셀 수 (기본값: 100)
  /// 
  /// Returns 가장 많이 나타나는 색상
  static Future<Color> extractDominantColor(
    Uint8List imageBytes, {
    int sampleCount = 100,
  }) async {
    final codec = await ui.instantiateImageCodec(imageBytes);
    final frame = await codec.getNextFrame();
    final image = frame.image;

    final pixelData = await image.toByteData(format: ui.ImageByteFormat.rawRgba);
    if (pixelData == null) {
      return Colors.grey;
    }

    final width = image.width;
    final height = image.height;
    final pixels = pixelData.buffer.asUint8List();

    // 샘플링할 픽셀 위치 계산
    final step = (width * height / sampleCount).ceil();
    final colorCounts = <Color, int>{};

    for (int i = 0; i < pixels.length; i += step * 4) {
      if (i + 3 >= pixels.length) break;

      final r = pixels[i];
      final g = pixels[i + 1];
      final b = pixels[i + 2];
      final a = pixels[i + 3];

      // 투명도가 낮은 픽셀은 제외
      if (a < 128) continue;

      final color = Color.fromARGB(255, r, g, b);
      colorCounts[color] = (colorCounts[color] ?? 0) + 1;
    }

    // 가장 많이 나타나는 색상 반환
    if (colorCounts.isEmpty) {
      return Colors.grey;
    }

    return colorCounts.entries
        .reduce((a, b) => a.value > b.value ? a : b)
        .key;
  }

  /// 이미지에서 여러 주요 색상을 추출합니다.
  /// 
  /// [imageBytes] 이미지 바이트 데이터
  /// [colorCount] 추출할 색상 개수 (기본값: 5)
  /// 
  /// Returns 색상 리스트 (가장 많이 나타나는 순서)
  static Future<List<Color>> extractPalette(
    Uint8List imageBytes, {
    int colorCount = 5,
  }) async {
    final codec = await ui.instantiateImageCodec(imageBytes);
    final frame = await codec.getNextFrame();
    final image = frame.image;

    final pixelData = await image.toByteData(format: ui.ImageByteFormat.rawRgba);
    if (pixelData == null) {
      return [Colors.grey];
    }

    final width = image.width;
    final height = image.height;
    final pixels = pixelData.buffer.asUint8List();

    final step = (width * height / 500).ceil();
    final colorCounts = <Color, int>{};

    for (int i = 0; i < pixels.length; i += step * 4) {
      if (i + 3 >= pixels.length) break;

      final r = pixels[i];
      final g = pixels[i + 1];
      final b = pixels[i + 2];
      final a = pixels[i + 3];

      if (a < 128) continue;

      final color = Color.fromARGB(255, r, g, b);
      colorCounts[color] = (colorCounts[color] ?? 0) + 1;
    }

    if (colorCounts.isEmpty) {
      return [Colors.grey];
    }

    final sortedColors = colorCounts.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));

    return sortedColors
        .take(colorCount)
        .map((e) => e.key)
        .toList();
  }

  /// Figma 색상 값(RGBA)을 Flutter Color로 변환합니다.
  /// 
  /// [r] Red 값 (0-1)
  /// [g] Green 값 (0-1)
  /// [b] Blue 값 (0-1)
  /// [a] Alpha 값 (0-1, 기본값: 1.0)
  /// 
  /// Returns Flutter Color 객체
  static Color fromFigmaRgba(double r, double g, double b, [double a = 1.0]) {
    return Color.fromRGBO(
      (r * 255).round(),
      (g * 255).round(),
      (b * 255).round(),
      a,
    );
  }

  /// 16진수 색상 코드를 Flutter Color로 변환합니다.
  /// 
  /// [hex] 16진수 색상 코드 (예: "#FF5733" 또는 "FF5733")
  /// 
  /// Returns Flutter Color 객체
  static Color fromHex(String hex) {
    final hexColor = hex.replaceAll('#', '');
    return Color(int.parse(hexColor, radix: 16) + 0xFF000000);
  }
}


