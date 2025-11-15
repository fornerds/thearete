import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../providers/auth_provider.dart';
import '../../viewmodels/auth_viewmodel.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_assets.dart';
import '../../widgets/common/inputs/custom_text_field.dart';
import '../../widgets/common/buttons/primary_button.dart';

/// 로그인 화면
/// Figma 디자인 시스템 기반으로 제작
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() {
    if (_formKey.currentState!.validate()) {
      ref.read(authStateProvider.notifier).login(
            _emailController.text.trim(),
            _passwordController.text,
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authStateProvider);
    final size = MediaQuery.of(context).size;

    // 에러 메시지 표시
    ref.listen<AuthState>(authStateProvider, (previous, next) {
      if (next.errorMessage != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(next.errorMessage!),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
          ),
        );
        // 에러 메시지 표시 후 클리어
        Future.microtask(() {
          ref.read(authStateProvider.notifier).clearError();
        });
      }
    });

    return Scaffold(
      backgroundColor: AppColors.grayScaleBackground,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // 로고 위 여백
                  const SizedBox(height: 81),
                  
                  // 로고 (화면 너비에 따라 반응형 크기 조정)
                  Center(
                    child: LayoutBuilder(
                      builder: (context, constraints) {
                        // 화면 너비의 40%를 최대 너비로 사용 (최소 200px, 최대 300px)
                        final maxWidth = constraints.maxWidth * 0.4;
                        final logoWidth = maxWidth.clamp(200.0, 300.0);
                        
                        return Image.asset(
                          AppAssets.logo,
                          width: logoWidth,
                          fit: BoxFit.contain,
                          errorBuilder: (context, error, stackTrace) {
                            // 이미지 로드 실패 시 대체 위젯
                            return SizedBox(
                              width: logoWidth,
                              child: Center(
                                child: Text(
                                  'SkinTone',
                                  style: TextStyle(
                                    fontSize: logoWidth * 0.2,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.medicalDarkBlue,
                                  ),
                                ),
                              ),
                            );
                          },
                        );
                      },
                    ),
                  ),
                  
                  // 로고 아래 여백
                  const SizedBox(height: 81),

                  // 최상위 컨테이너: 이메일/비밀번호/로그인 버튼 + 비밀번호 찾기/회원가입 링크
                  // flex-direction: column, align-items: flex-start, gap: 14px
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // 이메일/비밀번호/로그인 버튼을 묶는 컨테이너
                      // flex-direction: column, align-items: center, gap: 40px
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          // 이메일과 비밀번호 inputbox를 묶는 컨테이너
                          // flex-direction: column, align-items: flex-start, gap: 32px
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // 이메일 입력 필드
                              CustomTextField(
                                labelText: '이메일',
                                hintText: '이메일을 입력하세요',
                                controller: _emailController,
                                keyboardType: TextInputType.emailAddress,
                                textInputAction: TextInputAction.next,
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return '이메일을 입력해주세요';
                                  }
                                  if (!RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(value)) {
                                    return '올바른 이메일 형식이 아닙니다';
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 32),

                              // 비밀번호 입력 필드
                              CustomTextField(
                                labelText: '비밀번호',
                                hintText: '비밀번호를 입력하세요',
                                controller: _passwordController,
                                obscureText: true,
                                textInputAction: TextInputAction.done,
                                onSubmitted: (_) => _handleLogin(),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return '비밀번호를 입력해주세요';
                                  }
                                  if (value.length < 6) {
                                    return '비밀번호는 6자 이상이어야 합니다';
                                  }
                                  return null;
                                },
                              ),
                            ],
                          ),
                          const SizedBox(height: 40),

                          // 로그인 버튼 (너비 100%)
                          SizedBox(
                            width: double.infinity,
                            child: PrimaryButton(
                              text: '로그인',
                              onPressed: authState.isLoading ? null : _handleLogin,
                              isLoading: authState.isLoading,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 14),

                      // 비밀번호 찾기 & 회원가입 링크
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          // 비밀번호 찾기 링크
                          TextButton(
                            onPressed: () {
                              // TODO: 비밀번호 찾기 화면으로 이동
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('비밀번호 찾기 기능은 추후 구현 예정입니다'),
                                ),
                              );
                            },
                            style: TextButton.styleFrom(
                              padding: EdgeInsets.zero,
                              minimumSize: Size.zero,
                              tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                            ),
                            child: const Text(
                              '비밀번호 찾기',
                              style: TextStyle(
                                color: AppColors.grayScaleSubText2,
                                fontSize: 14,
                                fontWeight: FontWeight.w700,
                                height: 1.35, // line-height: 135% (18.9px / 14px)
                                decoration: TextDecoration.underline,
                                decorationStyle: TextDecorationStyle.solid,
                              ),
                            ),
                          ),
                          // 회원가입 링크
                          TextButton(
                            onPressed: () {
                              context.push('/signup');
                            },
                            style: TextButton.styleFrom(
                              padding: EdgeInsets.zero,
                              minimumSize: Size.zero,
                              tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                            ),
                            child: const Text(
                              '회원가입',
                              style: TextStyle(
                                color: AppColors.keyColor4,
                                fontSize: 14,
                                fontWeight: FontWeight.w700,
                                height: 1.35, // line-height: 135% (18.9px / 14px)
                                decoration: TextDecoration.underline,
                                decorationStyle: TextDecorationStyle.solid,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),

                  // 하단 여백
                  SizedBox(height: size.height * 0.1),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}