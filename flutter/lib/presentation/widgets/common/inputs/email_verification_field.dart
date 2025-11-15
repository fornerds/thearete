import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/app_colors.dart';
import '../buttons/primary_button.dart';
import '../buttons/secondary_button.dart';
import 'custom_text_field.dart';

/// 이메일 인증 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
class EmailVerificationField extends StatefulWidget {
  final TextEditingController emailController;
  final TextEditingController verificationCodeController;
  final VoidCallback? onSendVerificationCode;
  final VoidCallback? onVerifyCode;
  final bool isCodeSent;
  final bool isCodeVerified;
  final bool isLoading;
  final String? emailError;
  final String? codeError;
  final int resendCooldownSeconds;
  final String? Function(String?)? emailValidator;

  const EmailVerificationField({
    super.key,
    required this.emailController,
    required this.verificationCodeController,
    this.onSendVerificationCode,
    this.onVerifyCode,
    this.isCodeSent = false,
    this.isCodeVerified = false,
    this.isLoading = false,
    this.emailError,
    this.codeError,
    this.resendCooldownSeconds = 180, // 기본 3분
    this.emailValidator,
  });

  @override
  State<EmailVerificationField> createState() => _EmailVerificationFieldState();
}

class _EmailVerificationFieldState extends State<EmailVerificationField> {
  Timer? _timer;
  int _remainingSeconds = 0;
  bool _canResend = false;

  @override
  void initState() {
    super.initState();
    if (widget.isCodeSent) {
      _startTimer();
    }
  }

  @override
  void didUpdateWidget(EmailVerificationField oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isCodeSent && !oldWidget.isCodeSent) {
      _startTimer();
    } else if (!widget.isCodeSent && oldWidget.isCodeSent) {
      _stopTimer();
    }
  }

  @override
  void dispose() {
    _stopTimer();
    super.dispose();
  }

  void _startTimer() {
    _remainingSeconds = widget.resendCooldownSeconds;
    _canResend = false;
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_remainingSeconds > 0) {
        setState(() {
          _remainingSeconds--;
        });
      } else {
        setState(() {
          _canResend = true;
        });
        _stopTimer();
      }
    });
  }

  void _stopTimer() {
    _timer?.cancel();
    _timer = null;
  }

  String _formatTime(int seconds) {
    final minutes = seconds ~/ 60;
    final secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // 이메일 입력 필드
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: CustomTextField(
                labelText: '이메일',
                hintText: '이메일을 입력하세요',
                prefixIconType: TextFieldIconType.email,
                controller: widget.emailController,
                keyboardType: TextInputType.emailAddress,
                enabled: !widget.isCodeVerified,
                errorText: widget.emailError,
                validator: widget.emailValidator ??
                    (value) {
                      if (value == null || value.isEmpty) {
                        return '이메일을 입력해주세요';
                      }
                      if (!value.contains('@')) {
                        return '올바른 이메일 형식이 아닙니다';
                      }
                      return null;
                    },
              ),
            ),
            const SizedBox(width: 8),
            // 인증번호 전송 버튼
            Padding(
              padding: const EdgeInsets.only(top: 28),
              child: SizedBox(
                width: 100,
                child: widget.isCodeVerified
                    ? Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 16,
                        ),
                        decoration: BoxDecoration(
                          color: AppColors.medicalPaleBlue,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Center(
                          child: Icon(
                            Icons.check_circle,
                            color: AppColors.medicalDarkBlue,
                            size: 20,
                          ),
                        ),
                      )
                    : PrimaryButton(
                        text: widget.isCodeSent
                            ? (_canResend ? '재전송' : _formatTime(_remainingSeconds))
                            : '인증번호\n전송',
                        onPressed: (_canResend || !widget.isCodeSent) &&
                                widget.onSendVerificationCode != null
                            ? () {
                                widget.onSendVerificationCode?.call();
                                if (!widget.isCodeSent) {
                                  _startTimer();
                                } else {
                                  _startTimer();
                                }
                              }
                            : null,
                        isLoading: widget.isLoading,
                        height: 56,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 12,
                        ),
                      ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        // 인증번호 입력 필드
        if (widget.isCodeSent && !widget.isCodeVerified) ...[
          CustomTextField(
            labelText: '인증번호',
            hintText: '인증번호 6자리를 입력하세요',
            controller: widget.verificationCodeController,
            keyboardType: TextInputType.number,
            maxLength: 6,
            inputFormatters: [
              FilteringTextInputFormatter.digitsOnly,
            ],
            errorText: widget.codeError,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '인증번호를 입력해주세요';
              }
              if (value.length != 6) {
                return '인증번호는 6자리입니다';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          // 인증 확인 버튼
          SizedBox(
            width: double.infinity,
            child: PrimaryButton(
              text: '인증 확인',
              onPressed: widget.onVerifyCode,
              isLoading: widget.isLoading,
            ),
          ),
        ],
        // 인증 완료 메시지
        if (widget.isCodeVerified) ...[
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.medicalPaleBlue.withOpacity(0.3),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: AppColors.medicalDarkBlue,
                width: 1,
              ),
            ),
            child: Row(
              children: [
                const Icon(
                  Icons.check_circle,
                  color: AppColors.medicalDarkBlue,
                  size: 20,
                ),
                const SizedBox(width: 8),
                Text(
                  '이메일 인증이 완료되었습니다',
                  style: TextStyle(
                    color: AppColors.medicalDarkBlue,
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }
}

