import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../../core/constants/app_icons.dart';
import '../icons/custom_icon.dart';

/// Select Box 옵션 모델
class SelectOption<T> {
  final T value;
  final String label;
  final bool disabled;

  const SelectOption({
    required this.value,
    required this.label,
    this.disabled = false,
  });
}

/// 커스텀 Select Box 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class CustomSelectField<T> extends StatefulWidget {
  final String? labelText;
  final bool isRequired;
  final String? hintText;
  final String? helperText;
  final String? errorText;
  final T? value;
  final List<SelectOption<T>> options;
  final ValueChanged<T?>? onChanged;
  final bool enabled;
  final FormFieldValidator<T>? validator;
  final FocusNode? focusNode;
  final double borderRadius;
  final EdgeInsetsGeometry? contentPadding;
  final bool isCompact;

  const CustomSelectField({
    super.key,
    this.labelText,
    this.isRequired = false,
    this.hintText,
    this.helperText,
    this.errorText,
    this.value,
    required this.options,
    this.onChanged,
    this.enabled = true,
    this.validator,
    this.focusNode,
    this.borderRadius = 8.0,
    this.contentPadding,
    this.isCompact = false,
  });

  @override
  State<CustomSelectField<T>> createState() => _CustomSelectFieldState<T>();
}

class _CustomSelectFieldState<T> extends State<CustomSelectField<T>> {
  bool _isMenuOpen = false;

  @override
  Widget build(BuildContext context) {
    final hasError = widget.errorText != null && widget.errorText!.isNotEmpty;

    if (widget.isCompact) {
      return _buildCompactSelect(context, hasError);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.labelText != null) ...[
          Container(
            constraints: const BoxConstraints(
              maxWidth: double.infinity,
            ),
            child: Row(
              children: [
                Flexible(
                  child: Text(
                    widget.labelText!,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      height: 1.5,
                      color: hasError
                          ? Colors.red
                          : AppColors.grayScaleText,
                    ),
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                ),
                if (widget.isRequired) ...[
                  const SizedBox(width: 4),
                  Text(
                    '*',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      height: 1.5,
                      color: hasError
                          ? Colors.red
                          : AppColors.grayScaleText,
                    ),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: 6),
        ],
        DropdownButtonFormField<T>(
          value: widget.value,
          items: widget.options.map((option) {
            return DropdownMenuItem<T>(
              value: option.value,
              enabled: !option.disabled && widget.enabled,
              child: _SelectOptionItem(
                label: option.label,
                isSelected: widget.value == option.value,
                isDisabled: option.disabled || !widget.enabled,
                isCompact: false,
              ),
            );
          }).toList(),
          onChanged: widget.enabled ? (T? newValue) {
            widget.onChanged?.call(newValue);
            setState(() => _isMenuOpen = false);
          } : null,
          onTap: () {
            setState(() => _isMenuOpen = !_isMenuOpen);
          },
          validator: widget.validator,
          focusNode: widget.focusNode,
          menuMaxHeight: 300,
          itemHeight: 48,
          selectedItemBuilder: (BuildContext context) {
            // 선택된 값 표시용 빌더
            return widget.options.map((option) {
              return Text(
                option.label,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  height: 1.35, // line-height: 135% (21.6px / 16px)
                  color: widget.enabled
                      ? AppColors.grayScaleGuideText
                      : AppColors.medicalLightBlueGray,
                ),
                overflow: TextOverflow.ellipsis,
                maxLines: 1,
              );
            }).toList();
          },
          dropdownColor: Colors.white,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            height: 1.35, // line-height: 135% (21.6px / 16px)
            color: widget.enabled
                ? AppColors.grayScaleGuideText
                : AppColors.medicalLightBlueGray,
          ),
          icon: CustomIcon(
            icon: _isMenuOpen ? AppIcons.arrowDownSmall : AppIcons.arrowUpSmall,
            width: 17,
            height: 10,
            color: widget.enabled
                ? AppColors.grayScaleGuideText
                : AppColors.medicalPaleBlue,
          ),
          decoration: InputDecoration(
            hintText: widget.hintText,
            helperText: widget.helperText,
            errorText: widget.errorText,
            contentPadding: widget.contentPadding ??
                const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 16,
                ),
            filled: true,
            fillColor: widget.enabled
                ? AppColors.grayScaleBox3
                : AppColors.medicalOffWhite,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(
                color: hasError
                    ? Colors.red
                    : Colors.transparent,
                width: 0,
              ),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(
                color: hasError
                    ? Colors.red
                    : Colors.transparent,
                width: 0,
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(
                color: hasError
                    ? Colors.red
                    : AppColors.medicalDarkBlue,
                width: 2,
              ),
            ),
            disabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: const BorderSide(
                color: Colors.transparent,
                width: 0,
              ),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: const BorderSide(
                color: Colors.red,
                width: 1,
              ),
            ),
            focusedErrorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: const BorderSide(
                color: Colors.red,
                width: 2,
              ),
            ),
            hintStyle: const TextStyle(
              color: AppColors.grayScaleBlack,
              fontSize: 16,
              fontWeight: FontWeight.w400,
              height: 1.35,
            ),
            helperStyle: TextStyle(
              color: AppColors.medicalLightBlueGray,
              fontSize: 12,
            ),
            errorStyle: const TextStyle(
              color: Colors.red,
              fontSize: 12,
            ),
          ),
          // Compact 모드가 아닐 때만 기본 스타일 사용
        ),
      ],
    );
  }

  Widget _buildCompactSelect(BuildContext context, bool hasError) {
    return _CompactSelectField<T>(
      value: widget.value,
      options: widget.options,
      onChanged: widget.enabled ? widget.onChanged : null,
      enabled: widget.enabled,
      borderRadius: widget.borderRadius,
      hasError: hasError,
    );
  }
}

/// Compact 모드 Select Field
class _CompactSelectField<T> extends StatefulWidget {
  final T? value;
  final List<SelectOption<T>> options;
  final ValueChanged<T?>? onChanged;
  final bool enabled;
  final double borderRadius;
  final bool hasError;

  const _CompactSelectField({
    required this.value,
    required this.options,
    this.onChanged,
    this.enabled = true,
    this.borderRadius = 99.0,
    this.hasError = false,
  });

  @override
  State<_CompactSelectField<T>> createState() => _CompactSelectFieldState<T>();
}

class _CompactSelectFieldState<T> extends State<_CompactSelectField<T>> {
  bool _isMenuOpen = false;

  @override
  Widget build(BuildContext context) {
    final selectedOption = widget.options.firstWhere(
      (option) => option.value == widget.value,
      orElse: () => widget.options.first,
    );

    return Container(
      padding: const EdgeInsets.only(left: 16, right: 10, top: 6, bottom: 6),
      decoration: BoxDecoration(
        color: AppColors.grayScaleBackground,
        borderRadius: BorderRadius.circular(widget.borderRadius),
        border: Border.all(
          color: widget.hasError
              ? Colors.red
              : AppColors.grayScaleLine,
          width: 1,
        ),
      ),
      child: DropdownButtonHideUnderline(
        child: Theme(
          data: Theme.of(context).copyWith(
            // Material의 기본 hover/selected 배경색 제거
            hoverColor: Colors.transparent,
            focusColor: Colors.transparent,
            splashColor: Colors.transparent,
            highlightColor: Colors.transparent,
            // 드롭다운 메뉴의 그림자 제거
            menuTheme: MenuThemeData(
              style: MenuStyle(
                elevation: WidgetStateProperty.all(0),
                shadowColor: WidgetStateProperty.all(Colors.transparent),
                backgroundColor: WidgetStateProperty.all(Colors.transparent),
                surfaceTintColor: WidgetStateProperty.all(Colors.transparent),
                shape: WidgetStateProperty.all(
                  RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(0),
                  ),
                ),
              ),
            ),
            // PopupMenuTheme도 설정하여 드롭다운 메뉴 스타일 제어
            popupMenuTheme: PopupMenuThemeData(
              elevation: 0,
              shadowColor: Colors.transparent,
              color: Colors.transparent,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(0),
              ),
            ),
          ),
          child: DropdownButton<T>(
            value: widget.value,
            items: widget.options.map((option) {
              return DropdownMenuItem<T>(
                value: option.value,
                enabled: !option.disabled && widget.enabled,
                child: _CompactSelectOptionItem(
                  label: option.label,
                  isSelected: widget.value == option.value,
                  isDisabled: option.disabled || !widget.enabled,
                ),
              );
            }).toList(),
          onChanged: widget.enabled
              ? (T? newValue) {
                  widget.onChanged?.call(newValue);
                  setState(() => _isMenuOpen = false);
                }
              : null,
          onTap: () {
            setState(() => _isMenuOpen = !_isMenuOpen);
          },
          isExpanded: false,
          icon: CustomIcon(
            icon: _isMenuOpen ? AppIcons.arrowUpSmall : AppIcons.arrowDownSmall,
            width: 10,
            height: 6,
            color: AppColors.grayScaleSubText1,
          ),
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: widget.enabled
                ? AppColors.grayScaleGuideText
                : AppColors.grayScaleGuideText,
            height: 1.35,
          ),
          dropdownColor: Colors.transparent, // 드롭다운 메뉴 배경을 투명하게
          menuMaxHeight: 300,
          itemHeight: null,
          // 옵션 아이템들 사이 간격을 위한 패딩
          padding: EdgeInsets.zero,
          selectedItemBuilder: (BuildContext context) {
            return widget.options.map((option) {
              return Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    option.label,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: widget.enabled
                          ? AppColors.grayScaleGuideText
                          : AppColors.grayScaleGuideText,
                      height: 1.35,
                    ),
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                  const SizedBox(width: 6), // gap: 6px
                ],
              );
            }).toList();
          },
          ),
        ),
      ),
    );
  }
}

/// Compact 모드 옵션 아이템 위젯
class _CompactSelectOptionItem extends StatefulWidget {
  final String label;
  final bool isSelected;
  final bool isDisabled;

  const _CompactSelectOptionItem({
    required this.label,
    required this.isSelected,
    required this.isDisabled,
  });

  @override
  State<_CompactSelectOptionItem> createState() => _CompactSelectOptionItemState();
}

class _CompactSelectOptionItemState extends State<_CompactSelectOptionItem> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    // hover 또는 selected 상태에 따른 배경색
    final backgroundColor = _isHovered || widget.isSelected
        ? AppColors.grayScaleBox3 // hover/selected 배경색
        : AppColors.grayScaleBackground;

    return MouseRegion(
      onEnter: (_) {
        if (!widget.isDisabled) {
          setState(() => _isHovered = true);
        }
      },
      onExit: (_) {
        if (!widget.isDisabled) {
          setState(() => _isHovered = false);
        }
      },
      child: Container(
        width: double.infinity, // 전체 영역 차지
        margin: const EdgeInsets.symmetric(horizontal: 4, vertical: 2), // 옵션 아이템들 사이 간격 (gap: 4px를 위해 상하 2px씩, 좌우 4px)
        padding: const EdgeInsets.all(4), // padding: 4px
        decoration: BoxDecoration(
          color: backgroundColor, // 배경색 명확하게 설정
          borderRadius: BorderRadius.circular(6), // border-radius: 6px
          border: Border.all(
            color: AppColors.grayScaleLineWeak, // border: 1px solid var(--GraySacle-Line-Weak, #EEEFF1)
            width: 1,
          ),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center, // justify-content: center
          crossAxisAlignment: CrossAxisAlignment.center, // align-items: center
          children: [
            Text(
              widget.label,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: widget.isDisabled
                    ? AppColors.medicalLightBlueGray
                    : AppColors.grayScaleGuideText,
                height: 1.35,
              ),
              textAlign: TextAlign.center,
              overflow: TextOverflow.ellipsis,
              maxLines: 1,
            ),
          ],
        ),
      ),
    );
  }
}

/// Select Box 옵션 아이템 위젯
/// 드롭다운 메뉴에서 표시되는 각 옵션의 스타일을 정의
class _SelectOptionItem extends StatefulWidget {
  final String label;
  final bool isSelected;
  final bool isDisabled;
  final bool isCompact;

  const _SelectOptionItem({
    required this.label,
    required this.isSelected,
    required this.isDisabled,
    this.isCompact = false,
  });

  @override
  State<_SelectOptionItem> createState() => _SelectOptionItemState();
}

class _SelectOptionItemState extends State<_SelectOptionItem> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) {
        if (!widget.isDisabled) {
          setState(() => _isHovered = true);
        }
      },
      onExit: (_) {
        if (!widget.isDisabled) {
          setState(() => _isHovered = false);
        }
      },
      child: Container(
        height: 48,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: _getBackgroundColor(),
          borderRadius: BorderRadius.circular(0),
        ),
        child: Row(
          children: [
            Expanded(
              child: Text(
                widget.label,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  height: 1.35, // line-height: 135% (21.6px / 16px)
                  color: _getTextColor(),
                ),
              ),
            ),
            if (widget.isSelected) ...[
              const SizedBox(width: 8),
              Icon(
                Icons.check,
                size: 20,
                color: AppColors.medicalDarkBlue,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Color _getBackgroundColor() {
    if (widget.isDisabled) {
      return AppColors.medicalOffWhite;
    }
    if (widget.isSelected) {
      return AppColors.medicalPaleBlue.withOpacity(0.2);
    }
    if (_isHovered) {
      return AppColors.medicalPaleBlue.withOpacity(0.1);
    }
    return Colors.transparent;
  }

  Color _getTextColor() {
    if (widget.isDisabled) {
      return AppColors.medicalLightBlueGray;
    }
    return AppColors.grayScaleBlack; // 검정색
  }
}

