import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/app_colors.dart';

/// 텍스트 필드 아이콘 타입
enum TextFieldIconType {
  search,
  select,
  calendar,
  email,
  lock,
  person,
  phone,
  location,
}

/// 커스텀 텍스트 필드 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class CustomTextField extends StatefulWidget {
  final String? labelText;
  final bool isRequired;
  final String? hintText;
  final String? helperText;
  final String? errorText;
  final TextEditingController? controller;
  final bool obscureText;
  final bool enabled;
  final bool readOnly;
  final TextInputType? keyboardType;
  final TextInputAction? textInputAction;
  final int? maxLines;
  final int? maxLength;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final VoidCallback? onTap;
  final VoidCallback? onIconTap;
  final FormFieldValidator<String>? validator;
  final List<TextInputFormatter>? inputFormatters;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final TextFieldIconType? prefixIconType;
  final TextFieldIconType? suffixIconType;
  final FocusNode? focusNode;
  final double borderRadius;
  final EdgeInsetsGeometry? contentPadding;

  const CustomTextField({
    super.key,
    this.labelText,
    this.isRequired = false,
    this.hintText,
    this.helperText,
    this.errorText,
    this.controller,
    this.obscureText = false,
    this.enabled = true,
    this.readOnly = false,
    this.keyboardType,
    this.textInputAction,
    this.maxLines = 1,
    this.maxLength,
    this.onChanged,
    this.onSubmitted,
    this.onTap,
    this.onIconTap,
    this.validator,
    this.inputFormatters,
    this.prefixIcon,
    this.suffixIcon,
    this.prefixIconType,
    this.suffixIconType,
    this.focusNode,
    this.borderRadius = 6.0,
    this.contentPadding,
  });

  @override
  State<CustomTextField> createState() => _CustomTextFieldState();
}

class _CustomTextFieldState extends State<CustomTextField> {
  bool _obscureText = false;

  @override
  void initState() {
    super.initState();
    _obscureText = widget.obscureText;
  }

  void _toggleObscureText() {
    setState(() {
      _obscureText = !_obscureText;
    });
  }

  /// 아이콘 타입에 따라 아이콘 위젯 생성
  Widget? _buildIcon(TextFieldIconType? iconType, {bool isPrefix = true}) {
    if (iconType == null) return null;

    IconData iconData;
    switch (iconType) {
      case TextFieldIconType.search:
        iconData = Icons.search;
        break;
      case TextFieldIconType.select:
        iconData = Icons.arrow_drop_down;
        break;
      case TextFieldIconType.calendar:
        iconData = Icons.calendar_today;
        break;
      case TextFieldIconType.email:
        iconData = Icons.email_outlined;
        break;
      case TextFieldIconType.lock:
        iconData = Icons.lock_outline;
        break;
      case TextFieldIconType.person:
        iconData = Icons.person_outline;
        break;
      case TextFieldIconType.phone:
        iconData = Icons.phone_outlined;
        break;
      case TextFieldIconType.location:
        iconData = Icons.location_on_outlined;
        break;
    }

    final icon = Icon(
      iconData,
      color: widget.enabled
          ? AppColors.grayScaleText
          : AppColors.medicalPaleBlue,
      size: 24,
    );

    // 아이콘에 탭 이벤트가 있으면 GestureDetector로 감싸기
    if (widget.onIconTap != null && widget.enabled) {
      return GestureDetector(
        onTap: widget.onIconTap,
        child: Padding(
          padding: EdgeInsets.only(
            left: isPrefix ? 0 : 12,
            right: isPrefix ? 12 : 0,
          ),
          child: icon,
        ),
      );
    }

    return icon;
  }

  @override
  Widget build(BuildContext context) {
    final hasError = widget.errorText != null && widget.errorText!.isNotEmpty;

    // prefixIcon 우선순위: prefixIcon > prefixIconType
    final effectivePrefixIcon = widget.prefixIcon ??
        _buildIcon(widget.prefixIconType, isPrefix: true);

    // suffixIcon 우선순위: obscureText > suffixIcon > suffixIconType
    Widget? effectiveSuffixIcon;
    if (widget.obscureText) {
      effectiveSuffixIcon = IconButton(
        icon: Icon(
          _obscureText ? Icons.visibility : Icons.visibility_off,
          color: AppColors.grayScaleText,
        ),
        onPressed: _toggleObscureText,
      );
    } else {
      effectiveSuffixIcon = widget.suffixIcon ??
          _buildIcon(widget.suffixIconType, isPrefix: false);
    }

    // Label과 Input을 묶는 Container (flex-direction: column, gap: 6px, border-radius: 6px)
    // 배경색은 전체 페이지 기본 색상이므로 Container에는 적용하지 않음
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
          if (widget.labelText != null) ...[
            // Label 스타일 (font-size: 20px, font-weight: 700, line-height: 150%, color: #374151)
            Container(
              constraints: const BoxConstraints(
                maxWidth: double.infinity,
              ),
              child: Row(
                children: [
                  Flexible(
                    child: Text(
                      widget.labelText!,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        height: 1.5, // line-height: 150%
                        color: AppColors.grayScaleText,
                      ),
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                    ),
                  ),
                  if (widget.isRequired) ...[
                    const SizedBox(width: 4),
                    const Text(
                      '*',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        height: 1.5,
                        color: AppColors.grayScaleText,
                      ),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 6), // gap: 6px
          ],
          // Input 스타일 (height: 48px, padding: 16px, background: #F9FAFB)
          FormField<String>(
            initialValue: widget.controller?.text ?? '',
            validator: widget.validator,
            builder: (formFieldState) {
              final validatorError = formFieldState.hasError
                  ? formFieldState.errorText
                  : null;
              final effectiveErrorText = widget.errorText ?? validatorError;
              final effectiveHasError = effectiveErrorText != null && effectiveErrorText.isNotEmpty;

              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    height: 48,
                    child: TextFormField(
                      controller: widget.controller,
                      obscureText: widget.obscureText ? _obscureText : false,
                      enabled: widget.enabled,
                      readOnly: widget.readOnly,
                      keyboardType: widget.keyboardType,
                      textInputAction: widget.textInputAction,
                      maxLines: widget.maxLines,
                      maxLength: widget.maxLength,
                      onChanged: (value) {
                        formFieldState.didChange(value);
                        widget.onChanged?.call(value);
                      },
                      onFieldSubmitted: widget.onSubmitted,
                      onTap: widget.onTap,
                      inputFormatters: widget.inputFormatters,
                      focusNode: widget.focusNode,
                      style: TextStyle(
                        fontSize: 16,
                        color: widget.enabled
                            ? AppColors.grayScaleText
                            : AppColors.medicalLightBlueGray,
                      ),
                      decoration: InputDecoration(
                        hintText: widget.hintText,
                        helperText: widget.helperText,
                        // errorText를 null로 설정하여 TextFormField 내부에서 에러 메시지가 표시되지 않도록 함
                        // 대신 아래에서 별도로 에러 메시지를 표시
                        errorText: null,
                        errorStyle: const TextStyle(height: 0, fontSize: 0),
                        errorMaxLines: 0,
                        prefixIcon: effectivePrefixIcon != null
                            ? Padding(
                                padding: const EdgeInsets.only(left: 16, right: 10), // gap: 10px
                                child: effectivePrefixIcon,
                              )
                            : null,
                        suffixIcon: effectiveSuffixIcon != null
                            ? Padding(
                                padding: const EdgeInsets.only(left: 10, right: 16), // gap: 10px
                                child: effectiveSuffixIcon,
                              )
                            : null,
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
                            color: effectiveHasError
                                ? Colors.red
                                : Colors.transparent,
                            width: 0,
                          ),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(6),
                          borderSide: BorderSide(
                            color: effectiveHasError
                                ? Colors.red
                                : Colors.transparent,
                            width: 0,
                          ),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(6),
                          borderSide: BorderSide(
                            color: effectiveHasError
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
                          color: AppColors.grayScaleGuideText,
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          height: 1.35, // line-height: 135% (21.6px / 16px)
                        ),
                        helperStyle: const TextStyle(
                          color: AppColors.medicalLightBlueGray,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ),
                  // 에러 메시지 또는 헬퍼 텍스트를 별도로 표시 (레이아웃 유지)
                  if (effectiveHasError) ...[
                    const SizedBox(height: 4),
                    Text(
                      effectiveErrorText!,
                      style: const TextStyle(
                        color: Colors.red,
                        fontSize: 12,
                        height: 1.2,
                      ),
                    ),
                  ] else if (widget.helperText != null && widget.helperText!.isNotEmpty) ...[
                    const SizedBox(height: 4),
                    Text(
                      widget.helperText!,
                      style: const TextStyle(
                        color: AppColors.medicalLightBlueGray,
                        fontSize: 12,
                        height: 1.2,
                      ),
                    ),
                  ],
                ],
              );
            },
          ),
        ],
    );
  }
}

