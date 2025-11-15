import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/inputs/email_verification_field.dart';
import 'base_story.dart';

/// 이메일 인증 컴포넌트 스토리
class EmailVerificationStory extends StatefulWidget {
  const EmailVerificationStory({super.key});

  @override
  State<EmailVerificationStory> createState() => _EmailVerificationStoryState();
}

class _EmailVerificationStoryState extends State<EmailVerificationStory> {
  final _emailController = TextEditingController();
  final _codeController = TextEditingController();
  
  bool _isCodeSent = false;
  bool _isCodeVerified = false;
  bool _isLoading = false;
  String? _emailError;
  String? _codeError;
  int _cooldownSeconds = 180;

  @override
  void dispose() {
    _emailController.dispose();
    _codeController.dispose();
    super.dispose();
  }

  void _handleSendCode() {
    setState(() {
      _isLoading = true;
      _emailError = null;
    });

    // 시뮬레이션: 2초 후 코드 전송 완료
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _isCodeSent = true;
          _isLoading = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('인증번호가 전송되었습니다')),
        );
      }
    });
  }

  void _handleVerifyCode() {
    setState(() {
      _isLoading = true;
      _codeError = null;
    });

    // 시뮬레이션: 2초 후 인증 완료
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _isCodeVerified = true;
          _isLoading = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('이메일 인증이 완료되었습니다')),
        );
      }
    });
  }

  void _reset() {
    setState(() {
      _isCodeSent = false;
      _isCodeVerified = false;
      _isLoading = false;
      _emailError = null;
      _codeError = null;
      _emailController.clear();
      _codeController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Email Verification',
      description: '이메일 인증 컴포넌트의 다양한 상태와 옵션을 테스트할 수 있습니다.',
      controls: Column(
        children: [
          ControlSection(
            title: 'State',
            children: [
              SwitchListTile(
                title: const Text('Code Sent'),
                value: _isCodeSent,
                onChanged: (value) {
                  setState(() => _isCodeSent = value);
                },
              ),
              SwitchListTile(
                title: const Text('Code Verified'),
                value: _isCodeVerified,
                onChanged: (value) {
                  setState(() => _isCodeVerified = value);
                },
              ),
              SwitchListTile(
                title: const Text('Loading'),
                value: _isLoading,
                onChanged: (value) {
                  setState(() => _isLoading = value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Errors',
            children: [
              SwitchListTile(
                title: const Text('Email Error'),
                value: _emailError != null,
                onChanged: (value) {
                  setState(() {
                    _emailError = value ? '이메일 형식이 올바르지 않습니다' : null;
                  });
                },
              ),
              SwitchListTile(
                title: const Text('Code Error'),
                value: _codeError != null,
                onChanged: (value) {
                  setState(() {
                    _codeError = value ? '인증번호가 일치하지 않습니다' : null;
                  });
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Settings',
            children: [
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Cooldown (seconds)',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _cooldownSeconds = int.tryParse(value) ?? 180;
                  });
                },
              ),
            ],
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _reset,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.medicalBlueGray,
              foregroundColor: Colors.white,
            ),
            child: const Text('Reset'),
          ),
        ],
      ),
      preview: EmailVerificationField(
        emailController: _emailController,
        verificationCodeController: _codeController,
        onSendVerificationCode: _handleSendCode,
        onVerifyCode: _handleVerifyCode,
        isCodeSent: _isCodeSent,
        isCodeVerified: _isCodeVerified,
        isLoading: _isLoading,
        emailError: _emailError,
        codeError: _codeError,
        resendCooldownSeconds: _cooldownSeconds,
      ),
      variants: [
        _buildVariantCard(
          'Initial State',
          EmailVerificationField(
            emailController: TextEditingController(),
            verificationCodeController: TextEditingController(),
            onSendVerificationCode: () {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Code Sent State',
          EmailVerificationField(
            emailController: TextEditingController(text: 'test@example.com'),
            verificationCodeController: TextEditingController(),
            onSendVerificationCode: () {},
            onVerifyCode: () {},
            isCodeSent: true,
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Verified State',
          EmailVerificationField(
            emailController: TextEditingController(text: 'test@example.com'),
            verificationCodeController: TextEditingController(text: '123456'),
            onSendVerificationCode: () {},
            onVerifyCode: () {},
            isCodeSent: true,
            isCodeVerified: true,
          ),
        ),
      ],
    );
  }

  Widget _buildVariantCard(String title, Widget content) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: AppColors.medicalDarkBlue,
              ),
            ),
            const SizedBox(height: 12),
            content,
          ],
        ),
      ),
    );
  }
}

