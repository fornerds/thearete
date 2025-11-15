import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/app_colors.dart';

/// 커스텀 숫자 입력 필드 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
/// 숫자 전용 입력에 사용되며, 증가/감소 버튼을 포함합니다
class CustomNumberField extends StatefulWidget {
  final String? labelText;
  final bool isRequired;
  final String? hintText;
  final String? helperText;
  final String? errorText;
  final TextEditingController? controller;
  final bool enabled;
  final int? min;
  final int? max;
  final int? step;
  final ValueChanged<int?>? onChanged;
  final FormFieldValidator<int>? validator;
  final FocusNode? focusNode;
  final double borderRadius;
  final EdgeInsetsGeometry? contentPadding;
  final bool showIncrementButtons;
  final String? suffixText;

  const CustomNumberField({
    super.key,
    this.labelText,
    this.isRequired = false,
    this.hintText,
    this.helperText,
    this.errorText,
    this.controller,
    this.enabled = true,
    this.min,
    this.max,
    this.step = 1,
    this.onChanged,
    this.validator,
    this.focusNode,
    this.borderRadius = 8.0,
    this.contentPadding,
    this.showIncrementButtons = true,
    this.suffixText,
  });

  @override
  State<CustomNumberField> createState() => _CustomNumberFieldState();
}

class _CustomNumberFieldState extends State<CustomNumberField> {
  bool _isFocused = false;
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller ?? TextEditingController();
    widget.focusNode?.addListener(_onFocusChange);
  }

  @override
  void didUpdateWidget(CustomNumberField oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.controller != oldWidget.controller) {
      _controller = widget.controller ?? TextEditingController();
    }
    if (widget.focusNode != oldWidget.focusNode) {
      oldWidget.focusNode?.removeListener(_onFocusChange);
      widget.focusNode?.addListener(_onFocusChange);
    }
  }

  @override
  void dispose() {
    if (widget.controller == null) {
      _controller.dispose();
    }
    widget.focusNode?.removeListener(_onFocusChange);
    super.dispose();
  }

  void _onFocusChange() {
    setState(() {
      _isFocused = widget.focusNode?.hasFocus ?? false;
    });
  }

  int? _getCurrentValue() {
    final text = _controller.text.replaceAll(RegExp(r'[^\d-]'), '');
    if (text.isEmpty) return null;
    return int.tryParse(text);
  }

  void _increment() {
    if (!widget.enabled) return;
    
    final currentValue = _getCurrentValue() ?? 0;
    final newValue = currentValue + (widget.step ?? 1);
    final finalValue = widget.max != null && newValue > widget.max!
        ? widget.max!
        : newValue;
    
    _controller.text = finalValue.toString();
    widget.onChanged?.call(finalValue);
  }

  void _decrement() {
    if (!widget.enabled) return;
    
    final currentValue = _getCurrentValue() ?? 0;
    final newValue = currentValue - (widget.step ?? 1);
    final finalValue = widget.min != null && newValue < widget.min!
        ? widget.min!
        : newValue;
    
    _controller.text = finalValue.toString();
    widget.onChanged?.call(finalValue);
  }

  @override
  Widget build(BuildContext context) {
    final hasError = widget.errorText != null && widget.errorText!.isNotEmpty;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.labelText != null) ...[
          Row(
            children: [
              Text(
                widget.labelText!,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: hasError
                      ? Colors.red
                      : _isFocused
                          ? AppColors.medicalDarkBlue
                          : AppColors.medicalDarkBlue,
                ),
              ),
              if (widget.isRequired) ...[
                const SizedBox(width: 4),
                Text(
                  '*',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: hasError
                        ? Colors.red
                        : _isFocused
                            ? AppColors.medicalDarkBlue
                            : AppColors.medicalDarkBlue,
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: 8),
        ],
        Row(
          children: [
            Expanded(
              child: TextFormField(
                controller: _controller,
                enabled: widget.enabled,
                keyboardType: const TextInputType.numberWithOptions(signed: true),
                focusNode: widget.focusNode,
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'^-?\d*')),
                  if (widget.min != null || widget.max != null)
                    _NumberRangeFormatter(
                      min: widget.min,
                      max: widget.max,
                    ),
                ],
                onChanged: (value) {
                  final intValue = int.tryParse(value);
                  widget.onChanged?.call(intValue);
                },
                validator: widget.validator != null
                    ? (value) {
                        if (value == null || value.isEmpty) {
                          return widget.validator!(null);
                        }
                        final intValue = int.tryParse(value);
                        return widget.validator!(intValue);
                      }
                    : null,
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
                  suffixText: widget.suffixText,
                  contentPadding: widget.contentPadding ??
                      const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 16,
                      ),
                  filled: true,
                  fillColor: widget.enabled
                      ? Colors.white
                      : AppColors.medicalOffWhite,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(widget.borderRadius),
                    borderSide: BorderSide(
                      color: hasError
                          ? Colors.red
                          : AppColors.medicalPaleBlue,
                      width: 1,
                    ),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(widget.borderRadius),
                    borderSide: BorderSide(
                      color: hasError
                          ? Colors.red
                          : AppColors.medicalPaleBlue,
                      width: 1,
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(widget.borderRadius),
                    borderSide: BorderSide(
                      color: hasError
                          ? Colors.red
                          : AppColors.medicalDarkBlue,
                      width: 2,
                    ),
                  ),
                  disabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(widget.borderRadius),
                    borderSide: BorderSide(
                      color: AppColors.medicalPaleBlue,
                      width: 1,
                    ),
                  ),
                  errorBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(widget.borderRadius),
                    borderSide: const BorderSide(
                      color: Colors.red,
                      width: 1,
                    ),
                  ),
                  focusedErrorBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(widget.borderRadius),
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
                  helperStyle: TextStyle(
                    color: AppColors.medicalLightBlueGray,
                    fontSize: 12,
                  ),
                  errorStyle: const TextStyle(
                    color: Colors.red,
                    fontSize: 12,
                  ),
                ),
              ),
            ),
            if (widget.showIncrementButtons && widget.enabled) ...[
              const SizedBox(width: 8),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  _IncrementButton(
                    icon: Icons.add,
                    onPressed: _increment,
                    enabled: widget.max == null ||
                        (_getCurrentValue() ?? 0) < widget.max!,
                  ),
                  const SizedBox(height: 2),
                  _IncrementButton(
                    icon: Icons.remove,
                    onPressed: _decrement,
                    enabled: widget.min == null ||
                        (_getCurrentValue() ?? 0) > widget.min!,
                  ),
                ],
              ),
            ],
          ],
        ),
      ],
    );
  }
}

/// 증가/감소 버튼 위젯
class _IncrementButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onPressed;
  final bool enabled;

  const _IncrementButton({
    required this.icon,
    required this.onPressed,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 32,
      height: 32,
      decoration: BoxDecoration(
        color: enabled
            ? AppColors.medicalPaleBlue.withOpacity(0.3)
            : AppColors.medicalOffWhite,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(
          color: enabled
              ? AppColors.medicalPaleBlue
              : AppColors.medicalPaleBlue.withOpacity(0.5),
          width: 1,
        ),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: enabled ? onPressed : null,
          borderRadius: BorderRadius.circular(4),
          child: Icon(
            icon,
            size: 18,
            color: enabled
                ? AppColors.medicalDarkBlue
                : AppColors.medicalLightBlueGray,
          ),
        ),
      ),
    );
  }
}

/// 숫자 범위 포맷터
class _NumberRangeFormatter extends TextInputFormatter {
  final int? min;
  final int? max;

  _NumberRangeFormatter({this.min, this.max});

  @override
  TextEditingValue formatEditUpdate(
    TextEditingValue oldValue,
    TextEditingValue newValue,
  ) {
    if (newValue.text.isEmpty) {
      return newValue;
    }

    final intValue = int.tryParse(newValue.text);
    if (intValue == null) {
      return oldValue;
    }

    if (min != null && intValue < min!) {
      return TextEditingValue(
        text: min!.toString(),
        selection: TextSelection.collapsed(offset: min!.toString().length),
      );
    }

    if (max != null && intValue > max!) {
      return TextEditingValue(
        text: max!.toString(),
        selection: TextSelection.collapsed(offset: max!.toString().length),
      );
    }

    return newValue;
  }
}

