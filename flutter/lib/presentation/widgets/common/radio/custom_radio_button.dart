import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 커스텀 라디오 버튼 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
/// default, hover, checked 상태를 지원합니다
class CustomRadioButton<T> extends StatefulWidget {
  final T value;
  final T? groupValue;
  final ValueChanged<T?>? onChanged;
  final String label;
  final bool enabled;
  final double? size;
  final EdgeInsetsGeometry? padding;
  final TextStyle? labelStyle;

  const CustomRadioButton({
    super.key,
    required this.value,
    required this.groupValue,
    required this.onChanged,
    required this.label,
    this.enabled = true,
    this.size,
    this.padding,
    this.labelStyle,
  });

  @override
  State<CustomRadioButton<T>> createState() => _CustomRadioButtonState<T>();
}

class _CustomRadioButtonState<T> extends State<CustomRadioButton<T>> {
  bool _isHovered = false;

  bool get _isChecked => widget.value == widget.groupValue;

  @override
  Widget build(BuildContext context) {
    final size = widget.size ?? 20.0;
    final isActive = widget.enabled && widget.onChanged != null;

    return MouseRegion(
      onEnter: (_) {
        if (isActive) {
          setState(() => _isHovered = true);
        }
      },
      onExit: (_) {
        if (isActive) {
          setState(() => _isHovered = false);
        }
      },
      child: InkWell(
        onTap: isActive
            ? () {
                widget.onChanged?.call(widget.value);
              }
            : null,
        borderRadius: BorderRadius.circular(4),
        child: Padding(
          padding: widget.padding ?? const EdgeInsets.symmetric(vertical: 8),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              // 라디오 버튼 원형
              AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                width: size,
                height: size,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: _getBorderColor(),
                    width: 2,
                  ),
                  color: _getBackgroundColor(),
                ),
                child: _isChecked
                    ? Center(
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          width: size * 0.5,
                          height: size * 0.5,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: _getDotColor(),
                          ),
                        ),
                      )
                    : null,
              ),
              const SizedBox(width: 12),
              // 라벨
              Flexible(
                child: Text(
                  widget.label,
                  style: widget.labelStyle ??
                      TextStyle(
                        fontSize: 16,
                        color: isActive
                            ? AppColors.medicalDarkBlue
                            : AppColors.medicalLightBlueGray,
                        fontWeight: _isChecked
                            ? FontWeight.w600
                            : FontWeight.normal,
                      ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getBorderColor() {
    if (!widget.enabled || widget.onChanged == null) {
      return AppColors.medicalPaleBlue;
    }

    if (_isChecked) {
      return AppColors.medicalDarkBlue;
    }

    if (_isHovered) {
      return AppColors.medicalBlueGray;
    }

    return AppColors.medicalLightBlueGray;
  }

  Color _getBackgroundColor() {
    if (!widget.enabled || widget.onChanged == null) {
      return AppColors.medicalOffWhite;
    }

    if (_isHovered && !_isChecked) {
      return AppColors.medicalPaleBlue.withOpacity(0.3);
    }

    return Colors.white;
  }

  Color _getDotColor() {
    if (!widget.enabled || widget.onChanged == null) {
      return AppColors.medicalLightBlueGray;
    }

    return AppColors.medicalDarkBlue;
  }
}

/// 라디오 버튼 그룹 컴포넌트
/// 여러 라디오 버튼을 그룹으로 관리합니다
class CustomRadioGroup<T> extends StatelessWidget {
  final T? value;
  final ValueChanged<T?>? onChanged;
  final List<CustomRadioOption<T>> options;
  final bool enabled;
  final Axis direction;
  final double spacing;
  final EdgeInsetsGeometry? padding;

  const CustomRadioGroup({
    super.key,
    required this.value,
    required this.onChanged,
    required this.options,
    this.enabled = true,
    this.direction = Axis.vertical,
    this.spacing = 8.0,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    final children = options.map((option) {
      return CustomRadioButton<T>(
        value: option.value,
        groupValue: value,
        onChanged: enabled ? onChanged : null,
        label: option.label,
        enabled: enabled && !option.disabled,
        size: option.size,
        labelStyle: option.labelStyle,
      );
    }).toList();

    Widget content;
    if (direction == Axis.vertical) {
      content = Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: children
            .map((child) => Padding(
                  padding: EdgeInsets.only(bottom: spacing),
                  child: child,
                ))
            .toList(),
      );
    } else {
      content = Wrap(
        spacing: spacing,
        runSpacing: spacing,
        children: children,
      );
    }

    return Padding(
      padding: padding ?? EdgeInsets.zero,
      child: content,
    );
  }
}

/// 라디오 버튼 옵션 모델
class CustomRadioOption<T> {
  final T value;
  final String label;
  final bool disabled;
  final double? size;
  final TextStyle? labelStyle;

  const CustomRadioOption({
    required this.value,
    required this.label,
    this.disabled = false,
    this.size,
    this.labelStyle,
  });
}

