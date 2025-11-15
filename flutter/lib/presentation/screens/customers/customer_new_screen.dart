import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/constants/app_colors.dart';
import '../../widgets/common/buttons/primary_button.dart';
import '../../widgets/common/inputs/custom_number_field.dart';
import '../../widgets/common/inputs/custom_select_field.dart';
import '../../widgets/common/inputs/custom_text_area.dart';
import '../../widgets/common/inputs/custom_text_field.dart';
import '../../widgets/common/radio/custom_radio_button.dart';

/// 신규 고객 등록 화면
class CustomerNewScreen extends ConsumerStatefulWidget {
  const CustomerNewScreen({super.key});

  @override
  ConsumerState<CustomerNewScreen> createState() => _CustomerNewScreenState();
}

class _CustomerNewScreenState extends ConsumerState<CustomerNewScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _noteController = TextEditingController();

  String? _selectedBirthYear;
  String? _selectedGender;
  String? _selectedSkinType;
  bool _isLoading = false;

  // 년생 옵션 생성 (현재 연도 기준으로 100년 전부터 현재 연도까지)
  List<SelectOption<String>> get _birthYearOptions {
    final currentYear = DateTime.now().year;
    final startYear = currentYear - 100; // 100년 전부터
    final endYear = currentYear; // 현재 연도 출생연도 포함
    
    return List.generate(
      endYear - startYear + 1,
      (index) {
        final year = startYear + index;
        return SelectOption(
          value: year.toString(),
          label: '$year년생',
        );
      },
    ).reversed.toList(); // 최신순으로 정렬
  }

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _noteController.dispose();
    super.dispose();
  }

  Future<void> _handleSubmit() async {
    // 성별 필수 검증
    if (_selectedGender == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('성별을 선택해주세요'),
          backgroundColor: Colors.red,
          behavior: SnackBarBehavior.floating,
        ),
      );
      return;
    }

    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // TODO: API 호출로 고객 등록 처리
      // 년생에서 나이 계산
      // int? age;
      // if (_selectedBirthYear != null) {
      //   final birthYear = int.tryParse(_selectedBirthYear!);
      //   if (birthYear != null) {
      //     age = DateTime.now().year - birthYear;
      //   }
      // }
      // final customerData = {
      //   'name': _nameController.text.trim(),
      //   'age': age,
      //   'gender': _selectedGender,
      //   'phone': _phoneController.text.trim(),
      //   'skin_type': _selectedSkinType,
      //   'note': _noteController.text.trim().isNotEmpty ? _noteController.text.trim() : null,
      // };
      // await customerService.createCustomer(customerData);

      // 임시로 성공 처리
      await Future.delayed(const Duration(seconds: 1));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('고객이 등록되었습니다'),
            backgroundColor: Colors.green,
            behavior: SnackBarBehavior.floating,
          ),
        );
        context.pop();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('고객 등록에 실패했습니다: ${e.toString()}'),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.grayScaleBackground,
      body: SafeArea(
        child: Column(
          children: [
            // 상단 헤더 (뒤로 가기 버튼 + 제목)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
              child: Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back, color: AppColors.grayScaleText),
                    onPressed: () => context.pop(),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
                  const SizedBox(width: 10),
                  const Text(
                    '신규 고객 등록',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: AppColors.grayScaleText,
                    ),
                  ),
                ],
              ),
            ),
            // 스크롤 가능한 컨텐츠 영역
            Expanded(
              child: SingleChildScrollView(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 16),

                        // 고객명 (필수)
                        CustomTextField(
                          labelText: '고객명',
                          isRequired: true,
                          hintText: '고객명을 입력하세요',
                          controller: _nameController,
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return '고객명을 입력해주세요';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 32),
                        // 연락처 (필수)
                        CustomTextField(
                          labelText: '연락처',
                          isRequired: true,
                          hintText: '\'-\'표시를 생략하고 입력해 주세요.',
                          controller: _phoneController,
                          keyboardType: TextInputType.phone,
                          inputFormatters: [
                            FilteringTextInputFormatter.digitsOnly,
                            LengthLimitingTextInputFormatter(11),
                          ],
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return '연락처를 입력해주세요';
                            }
                            // 숫자만 검증 (10-11자리)
                            final phoneRegex = RegExp(r'^[0-9]{10,11}$');
                            if (!phoneRegex.hasMatch(value.trim())) {
                              return '올바른 연락처 형식이 아닙니다 (10-11자리 숫자)';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 32),

                        // 나이 (필수) - 년생 선택
                        CustomSelectField<String>(
                          labelText: '나이',
                          isRequired: true,
                          hintText: '나이를 선택해 주세요',
                          value: _selectedBirthYear,
                          options: _birthYearOptions,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return '나이를 선택해주세요';
                            }
                            return null;
                          },
                          onChanged: (value) {
                            setState(() {
                              _selectedBirthYear = value;
                            });
                          },
                        ),
                        const SizedBox(height: 32),

                        // 성별 (필수)
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  '성별',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.w700,
                                    height: 1.5,
                                    color: AppColors.grayScaleText,
                                  ),
                                ),
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
                            ),
                            const SizedBox(height: 6),
                            CustomRadioGroup<String>(
                              value: _selectedGender,
                              onChanged: (value) {
                                setState(() {
                                  _selectedGender = value;
                                });
                              },
                              direction: Axis.horizontal,
                              spacing: 24,
                              options: [
                                const CustomRadioOption(value: 'M', label: '남성'),
                                const CustomRadioOption(value: 'F', label: '여성'),
                                const CustomRadioOption(value: 'null', label: '모름'),
                              ],
                            ),
                          ],
                        ),
                        const SizedBox(height: 32),

                        // 피부타입 (필수)
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  '피부타입',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.w700,
                                    height: 1.5,
                                    color: AppColors.grayScaleText,
                                  ),
                                ),
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
                            ),
                            const SizedBox(height: 6),
                            CustomRadioGroup<String>(
                              value: _selectedSkinType,
                              onChanged: (value) {
                                setState(() {
                                  _selectedSkinType = value;
                                });
                              },
                              direction: Axis.horizontal,
                              spacing: 24,
                              options: const [
                                CustomRadioOption(value: '건성', label: '건성'),
                                CustomRadioOption(value: '지성', label: '지성'),
                                CustomRadioOption(value: '복합성', label: '복합성'),
                                CustomRadioOption(value: '민감성', label: '민감성'),
                                CustomRadioOption(value: '정상', label: '정상'),
                                CustomRadioOption(value: 'null', label: '모름'),
                              ],
                            ),
                          ],
                        ),
                        const SizedBox(height: 32),

                        // 특이사항 (옵션)
                        CustomTextArea(
                          labelText: '특이사항',
                          hintText: '특이사항을 입력하세요 (선택사항)',
                          controller: _noteController,
                          minLines: 3,
                          maxLines: 6,
                          maxLength: 100,
                          showCharacterCount: true,
                        ),
                        // 하단 고정 버튼을 위한 여백
                        const SizedBox(height: 100),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            // 하단 고정 버튼 (취소, 저장)
            Container(
              padding: const EdgeInsets.all(24.0),
              decoration: BoxDecoration(
                color: AppColors.grayScaleBackground,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 10,
                    offset: const Offset(0, -2),
                  ),
                ],
              ),
              child: SafeArea(
                top: false,
                child: Row(
                  children: [
                    // 취소 버튼
                    Expanded(
                      child: SizedBox(
                        height: 48,
                        child: OutlinedButton(
                          onPressed: _isLoading ? null : () => context.pop(),
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 10,
                            ),
                            backgroundColor: AppColors.keyColor1,
                            foregroundColor: AppColors.keyColor4,
                            side: BorderSide.none,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(6),
                            ),
                            elevation: 0,
                          ),
                          child: const Text(
                            '취소',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                              height: 1.35, // line-height: 135% (21.6px / 16px)
                            ),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    // 저장 버튼
                    Expanded(
                      child: PrimaryButton(
                        text: '저장',
                        onPressed: _isLoading ? null : _handleSubmit,
                        isLoading: _isLoading,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
