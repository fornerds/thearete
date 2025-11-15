import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/app_colors.dart';

/// 커스텀 텍스트 영역 컴포넌트 (Textarea)
/// Figma 디자인 시스템 기반으로 제작
/// 여러 줄 텍스트 입력에 사용됩니다
class CustomTextArea extends StatefulWidget {
  final String? labelText;
  final bool isRequired;
  final String? hintText;
  final String? helperText;
  final String? errorText;
  final TextEditingController? controller;
  final bool enabled;
  final bool readOnly;
  final int? minLines;
  final int? maxLines;
  final int? maxLength;
  final ValueChanged<String>? onChanged;
  final VoidCallback? onTap;
  final FormFieldValidator<String>? validator;
  final List<TextInputFormatter>? inputFormatters;
  final FocusNode? focusNode;
  final double borderRadius;
  final EdgeInsetsGeometry? contentPadding;
  final bool showCharacterCount;

  const CustomTextArea({
    super.key,
    this.labelText,
    this.isRequired = false,
    this.hintText,
    this.helperText,
    this.errorText,
    this.controller,
    this.enabled = true,
    this.readOnly = false,
    this.minLines = 3,
    this.maxLines = 5,
    this.maxLength,
    this.onChanged,
    this.onTap,
    this.validator,
    this.inputFormatters,
    this.focusNode,
    this.borderRadius = 8.0,
    this.contentPadding,
    this.showCharacterCount = false,
  });

  @override
  State<CustomTextArea> createState() => _CustomTextAreaState();
}

class _CustomTextAreaState extends State<CustomTextArea> {
  bool _isFocused = false;
  int _currentLength = 0;

  @override
  void initState() {
    super.initState();
    _currentLength = widget.controller?.text.length ?? 0;
    widget.controller?.addListener(_updateLength);
    widget.focusNode?.addListener(_onFocusChange);
  }

  @override
  void didUpdateWidget(CustomTextArea oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.controller != oldWidget.controller) {
      oldWidget.controller?.removeListener(_updateLength);
      widget.controller?.addListener(_updateLength);
      _currentLength = widget.controller?.text.length ?? 0;
    }
    if (widget.focusNode != oldWidget.focusNode) {
      oldWidget.focusNode?.removeListener(_onFocusChange);
      widget.focusNode?.addListener(_onFocusChange);
    }
  }

  @override
  void dispose() {
    widget.controller?.removeListener(_updateLength);
    widget.focusNode?.removeListener(_onFocusChange);
    super.dispose();
  }

  void _updateLength() {
    setState(() {
      _currentLength = widget.controller?.text.length ?? 0;
    });
  }

  void _onFocusChange() {
    setState(() {
      _isFocused = widget.focusNode?.hasFocus ?? false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final hasError = widget.errorText != null && widget.errorText!.isNotEmpty;
    final remainingChars = widget.maxLength != null
        ? widget.maxLength! - _currentLength
        : null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.labelText != null) ...[
          Row(
            children: [
              Expanded(
                child: Text(
                  widget.labelText!,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                    height: 1.5, // line-height: 150% (27px / 18px)
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
                    fontSize: 18,
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
          const SizedBox(height: 6),
        ],
        SizedBox(
          height: 100,
          child: TextFormField(
            controller: widget.controller,
            enabled: widget.enabled,
            readOnly: widget.readOnly,
            minLines: widget.minLines,
            maxLines: widget.maxLines,
            maxLength: widget.maxLength,
            onChanged: (value) {
              _updateLength();
              widget.onChanged?.call(value);
            },
            onTap: widget.onTap,
            validator: widget.validator,
            inputFormatters: widget.inputFormatters,
            focusNode: widget.focusNode,
            style: TextStyle(
              fontSize: 16,
              color: widget.enabled
                  ? AppColors.medicalDarkBlue
                  : AppColors.medicalLightBlueGray,
            ),
            decoration: InputDecoration(
              hintText: widget.hintText,
              helperText: widget.helperText,
              errorText: widget.errorText,
              contentPadding: widget.contentPadding ??
                  const EdgeInsets.all(16),
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
                color: AppColors.grayScaleGuideText,
                fontSize: 16,
                fontWeight: FontWeight.w500,
                height: 1.35, // line-height: 135% (21.6px / 16px)
              ),
              helperStyle: TextStyle(
                color: AppColors.medicalLightBlueGray,
                fontSize: 12,
              ),
              errorStyle: const TextStyle(
                color: Colors.red,
                fontSize: 12,
              ),
              counterText: '',
            ),
          ),
        ),
        // 글자수 표시 (하단 오른쪽)
        if (widget.maxLength != null) ...[
          const SizedBox(height: 4),
          Align(
            alignment: Alignment.centerRight,
            child: Text(
              '$_currentLength / ${widget.maxLength}',
              style: const TextStyle(
                color: AppColors.grayScaleGuideText,
                fontSize: 14,
                fontWeight: FontWeight.w500,
                height: 1.35, // line-height: 135% (18.9px / 14px)
              ),
              textAlign: TextAlign.right,
            ),
          ),
        ],
      ],
    );
  }
}

