import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 태그 타입
enum TagType {
  default_, // 기본 태그
  primary,  // 주요 태그
  success,   // 성공 태그
  warning,   // 경고 태그
  error,     // 에러 태그
  info,      // 정보 태그
}

/// 태그 크기
enum TagSize {
  small,
  medium,
  large,
}

/// 태그 형태
enum TagShape {
  square,  // 사각형 (기본)
  round,   // 둥근 형태
}

/// 커스텀 태그 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class CustomTag extends StatefulWidget {
  final String label;
  final TagType type;
  final TagSize size;
  final TagShape shape;
  final bool closable;
  final VoidCallback? onClose;
  final VoidCallback? onTap;
  final bool enabled;
  final Color? backgroundColor;
  final Color? textColor;
  final Color? borderColor;
  final double? borderRadius;
  final EdgeInsetsGeometry? padding;
  final Widget? prefixIcon;
  final Widget? suffixIcon;

  const CustomTag({
    super.key,
    required this.label,
    this.type = TagType.default_,
    this.size = TagSize.medium,
    this.shape = TagShape.square,
    this.closable = false,
    this.onClose,
    this.onTap,
    this.enabled = true,
    this.backgroundColor,
    this.textColor,
    this.borderColor,
    this.borderRadius,
    this.padding,
    this.prefixIcon,
    this.suffixIcon,
  });

  @override
  State<CustomTag> createState() => _CustomTagState();
}

class _CustomTagState extends State<CustomTag> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    final isClickable = widget.onTap != null && widget.enabled;
    final isClosable = widget.closable && widget.onClose != null && widget.enabled;

    return MouseRegion(
      onEnter: (_) {
        if (isClickable || isClosable) {
          setState(() => _isHovered = true);
        }
      },
      onExit: (_) {
        if (isClickable || isClosable) {
          setState(() => _isHovered = false);
        }
      },
      child: InkWell(
        onTap: isClickable ? widget.onTap : null,
        borderRadius: BorderRadius.circular(widget.borderRadius ?? _getBorderRadius()),
        child: Container(
          padding: widget.padding ?? _getPadding(),
          decoration: BoxDecoration(
            color: _getBackgroundColor(),
            borderRadius: BorderRadius.circular(widget.borderRadius ?? _getBorderRadius()),
            border: Border.all(
              color: _getBorderColor(),
              width: 1,
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (widget.prefixIcon != null) ...[
                widget.prefixIcon!,
                const SizedBox(width: 6),
              ],
              Text(
                widget.label,
                style: TextStyle(
                  fontSize: _getFontSize(),
                  fontWeight: FontWeight.w500,
                  color: _getTextColor(),
                ),
              ),
              if (widget.suffixIcon != null) ...[
                const SizedBox(width: 6),
                widget.suffixIcon!,
              ],
              if (isClosable) ...[
                const SizedBox(width: 6),
                GestureDetector(
                  onTap: () {
                    widget.onClose?.call();
                  },
                  child: _CloseIcon(
                    size: _getCloseIconSize(),
                    color: _getTextColor(),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  double _getBorderRadius() {
    // borderRadius가 명시적으로 지정된 경우 사용
    if (widget.borderRadius != null) {
      return widget.borderRadius!;
    }

    // round 형태인 경우 매우 큰 값을 사용하여 완전히 둥글게
    if (widget.shape == TagShape.round) {
      return 999.0; // 충분히 큰 값으로 완전히 둥근 형태
    }

    // square 형태인 경우 크기에 따라
    switch (widget.size) {
      case TagSize.small:
        return 4.0;
      case TagSize.medium:
        return 6.0;
      case TagSize.large:
        return 8.0;
    }
  }

  EdgeInsetsGeometry _getPadding() {
    switch (widget.size) {
      case TagSize.small:
        return const EdgeInsets.symmetric(horizontal: 8, vertical: 4);
      case TagSize.medium:
        return const EdgeInsets.symmetric(horizontal: 12, vertical: 6);
      case TagSize.large:
        return const EdgeInsets.symmetric(horizontal: 16, vertical: 8);
    }
  }

  double _getFontSize() {
    switch (widget.size) {
      case TagSize.small:
        return 12.0;
      case TagSize.medium:
        return 14.0;
      case TagSize.large:
        return 16.0;
    }
  }

  double _getCloseIconSize() {
    switch (widget.size) {
      case TagSize.small:
        return 12.0;
      case TagSize.medium:
        return 14.0;
      case TagSize.large:
        return 16.0;
    }
  }

  Color _getBackgroundColor() {
    if (widget.backgroundColor != null) {
      return widget.backgroundColor!;
    }

    if (!widget.enabled) {
      return AppColors.medicalOffWhite;
    }

    if (_isHovered && widget.onTap != null) {
      return _getTypeColor().withOpacity(0.1);
    }

    switch (widget.type) {
      case TagType.default_:
        return AppColors.medicalPaleBlue.withOpacity(0.3);
      case TagType.primary:
        return AppColors.medicalDarkBlue.withOpacity(0.1);
      case TagType.success:
        return Colors.green.withOpacity(0.1);
      case TagType.warning:
        return Colors.orange.withOpacity(0.1);
      case TagType.error:
        return Colors.red.withOpacity(0.1);
      case TagType.info:
        return Colors.blue.withOpacity(0.1);
    }
  }

  Color _getBorderColor() {
    if (widget.borderColor != null) {
      return widget.borderColor!;
    }

    if (!widget.enabled) {
      return AppColors.medicalPaleBlue;
    }

    if (_isHovered && widget.onTap != null) {
      return _getTypeColor();
    }

    switch (widget.type) {
      case TagType.default_:
        return AppColors.medicalPaleBlue;
      case TagType.primary:
        return AppColors.medicalDarkBlue;
      case TagType.success:
        return Colors.green;
      case TagType.warning:
        return Colors.orange;
      case TagType.error:
        return Colors.red;
      case TagType.info:
        return Colors.blue;
    }
  }

  Color _getTextColor() {
    if (widget.textColor != null) {
      return widget.textColor!;
    }

    if (!widget.enabled) {
      return AppColors.medicalLightBlueGray;
    }

    return _getTypeColor();
  }

  Color _getTypeColor() {
    switch (widget.type) {
      case TagType.default_:
        return AppColors.medicalDarkBlue;
      case TagType.primary:
        return AppColors.medicalDarkBlue;
      case TagType.success:
        return Colors.green.shade700;
      case TagType.warning:
        return Colors.orange.shade700;
      case TagType.error:
        return Colors.red.shade700;
      case TagType.info:
        return Colors.blue.shade700;
    }
  }
}

/// X 아이콘 위젯
class _CloseIcon extends StatelessWidget {
  final double size;
  final Color color;

  const _CloseIcon({
    required this.size,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: _CloseIconPainter(
        color: color,
        size: size,
      ),
    );
  }
}

/// X 아이콘 페인터
class _CloseIconPainter extends CustomPainter {
  final Color color;
  final double size;

  _CloseIconPainter({
    required this.color,
    required this.size,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 1.4
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..style = PaintingStyle.stroke;

    final padding = this.size * 0.2;

    // X 아이콘 그리기
    canvas.drawLine(
      Offset(padding, padding),
      Offset(size.width - padding, size.height - padding),
      paint,
    );
    canvas.drawLine(
      Offset(padding, size.height - padding),
      Offset(size.width - padding, padding),
      paint,
    );
  }

  @override
  bool shouldRepaint(_CloseIconPainter oldDelegate) {
    return oldDelegate.color != color || oldDelegate.size != size;
  }
}

