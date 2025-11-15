import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 커스텀 체크박스 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
/// default, hover, checked 상태를 지원합니다
class CustomCheckbox extends StatefulWidget {
  final bool value;
  final ValueChanged<bool?>? onChanged;
  final String label;
  final bool enabled;
  final double? size;
  final EdgeInsetsGeometry? padding;
  final TextStyle? labelStyle;
  final bool tristate;

  const CustomCheckbox({
    super.key,
    required this.value,
    required this.onChanged,
    required this.label,
    this.enabled = true,
    this.size,
    this.padding,
    this.labelStyle,
    this.tristate = false,
  });

  @override
  State<CustomCheckbox> createState() => _CustomCheckboxState();
}

class _CustomCheckboxState extends State<CustomCheckbox> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    final size = widget.size ?? 20.0;
    final isActive = widget.enabled && widget.onChanged != null;
    final isChecked = widget.value;

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
                if (widget.tristate) {
                  // tristate: null -> true -> false -> null
                  if (widget.value == true) {
                    widget.onChanged?.call(false);
                  } else if (widget.value == false) {
                    widget.onChanged?.call(null);
                  } else {
                    widget.onChanged?.call(true);
                  }
                } else {
                  widget.onChanged?.call(!widget.value);
                }
              }
            : null,
        borderRadius: BorderRadius.circular(4),
        child: Padding(
          padding: widget.padding ?? const EdgeInsets.symmetric(vertical: 8),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              // 체크박스 사각형
              AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                width: size,
                height: size,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(4),
                  border: Border.all(
                    color: _getBorderColor(),
                    width: 2,
                  ),
                  color: _getBackgroundColor(),
                ),
                child: _getCheckIcon(size),
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
                        fontWeight: isChecked
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

  Widget? _getCheckIcon(double size) {
    if (!widget.value) return null;

    return Center(
      child: AnimatedScale(
        scale: widget.value ? 1.0 : 0.0,
        duration: const Duration(milliseconds: 200),
        child: Icon(
          Icons.check,
          size: size * 0.7,
          color: _getCheckColor(),
        ),
      ),
    );
  }

  Color _getBorderColor() {
    if (!widget.enabled || widget.onChanged == null) {
      return AppColors.medicalPaleBlue;
    }

    if (widget.value) {
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

    if (widget.value) {
      return AppColors.medicalDarkBlue;
    }

    if (_isHovered) {
      return AppColors.medicalPaleBlue.withOpacity(0.3);
    }

    return Colors.white;
  }

  Color _getCheckColor() {
    if (!widget.enabled || widget.onChanged == null) {
      return AppColors.medicalLightBlueGray;
    }

    return Colors.white;
  }
}

/// 체크박스 그룹 컴포넌트
/// 여러 체크박스를 그룹으로 관리합니다
class CustomCheckboxGroup extends StatelessWidget {
  final List<bool> values;
  final ValueChanged<int>? onChanged;
  final List<CustomCheckboxOption> options;
  final bool enabled;
  final Axis direction;
  final double spacing;
  final EdgeInsetsGeometry? padding;

  const CustomCheckboxGroup({
    super.key,
    required this.values,
    required this.onChanged,
    required this.options,
    this.enabled = true,
    this.direction = Axis.vertical,
    this.spacing = 8.0,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    final children = options.asMap().entries.map((entry) {
      final index = entry.key;
      final option = entry.value;
      final isChecked = index < values.length ? values[index] : false;

      return CustomCheckbox(
        value: isChecked,
        onChanged: enabled && !option.disabled
            ? (value) {
                onChanged?.call(index);
              }
            : null,
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

/// 체크박스 옵션 모델
class CustomCheckboxOption {
  final String label;
  final bool disabled;
  final double? size;
  final TextStyle? labelStyle;

  const CustomCheckboxOption({
    required this.label,
    this.disabled = false,
    this.size,
    this.labelStyle,
  });
}

