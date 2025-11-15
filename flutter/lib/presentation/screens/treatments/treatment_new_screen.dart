import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';

import '../../../../core/constants/app_colors.dart';
import '../../../../core/constants/app_icons.dart';
import '../../widgets/common/buttons/primary_button.dart';
import '../../widgets/common/inputs/custom_text_field.dart';
import '../../widgets/common/radio/custom_radio_button.dart';
import '../../widgets/common/icons/custom_icon.dart';

/// 신규 시술정보 입력 화면
class TreatmentNewScreen extends ConsumerStatefulWidget {
  const TreatmentNewScreen({super.key});

  @override
  ConsumerState<TreatmentNewScreen> createState() => _TreatmentNewScreenState();
}

class _TreatmentNewScreenState extends ConsumerState<TreatmentNewScreen> {
  final _formKey = GlobalKey<FormState>();
  final _treatmentNameController = TextEditingController();
  final _otherBodyPartController = TextEditingController();

  String? _selectedTreatmentType;
  String? _selectedBodyPart;
  List<XFile> _selectedImageFiles = [];
  List<Uint8List> _selectedImageBytes = []; // 웹용
  final ImagePicker _imagePicker = ImagePicker();
  bool _isLoading = false;

  @override
  void dispose() {
    _treatmentNameController.dispose();
    _otherBodyPartController.dispose();
    super.dispose();
  }

  /// 이미지 선택
  Future<void> _pickImage() async {
    // 최대 10개 제한
    if (_selectedImageFiles.length >= 10) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('이미지는 최대 10개까지 선택할 수 있습니다'),
            backgroundColor: Colors.orange,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
      return;
    }

    try {
      final XFile? image = await _imagePicker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85,
      );

      if (image != null) {
        if (kIsWeb) {
          // 웹에서는 바이트 데이터로 읽기
          final bytes = await image.readAsBytes();
          setState(() {
            _selectedImageFiles.add(image);
            _selectedImageBytes.add(bytes);
          });
        } else {
          // 모바일에서는 파일 경로 사용
          setState(() {
            _selectedImageFiles.add(image);
          });
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('이미지 선택에 실패했습니다: ${e.toString()}'),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }

  /// 이미지 제거
  void _removeImage(int index) {
    setState(() {
      _selectedImageFiles.removeAt(index);
      if (kIsWeb && _selectedImageBytes.length > index) {
        _selectedImageBytes.removeAt(index);
      }
    });
  }

  Future<void> _handleSubmit() async {
    // 시술 종류 필수 검증
    if (_selectedTreatmentType == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('시술 종류를 선택해주세요'),
          backgroundColor: Colors.red,
          behavior: SnackBarBehavior.floating,
        ),
      );
      return;
    }

    // 시술 부위 필수 검증
    if (_selectedBodyPart == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('시술 부위를 선택해주세요'),
          backgroundColor: Colors.red,
          behavior: SnackBarBehavior.floating,
        ),
      );
      return;
    }

    // 기타 선택 시 추가 입력 검증
    if (_selectedBodyPart == '기타') {
      if (_otherBodyPartController.text.trim().isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('기타 시술 부위를 입력해주세요'),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
          ),
        );
        return;
      }
    }

    // 시술 전 사진 필수 검증
    if (_selectedImageFiles.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('시술 전 사진을 선택해주세요'),
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
      // TODO: API 호출로 시술정보 등록 처리
      // final treatmentData = {
      //   'name': _treatmentNameController.text.trim(),
      //   'type': _selectedTreatmentType,
      //   'body_part': _selectedBodyPart == '기타' 
      //       ? _otherBodyPartController.text.trim()
      //       : _selectedBodyPart,
      //   'before_image': _selectedImage,
      // };
      // await treatmentService.createTreatment(treatmentData);

      // 임시로 성공 처리
      await Future.delayed(const Duration(seconds: 1));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('시술정보가 등록되었습니다'),
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
            content: Text('시술정보 등록에 실패했습니다: ${e.toString()}'),
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
                    '시술정보 입력',
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

                        // 시술명 (필수)
                        CustomTextField(
                          labelText: '시술명',
                          isRequired: true,
                          hintText: '시술명을 입력하세요',
                          controller: _treatmentNameController,
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return '시술명을 입력해주세요';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 32),

                        // 시술 종류 (필수)
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  '시술 종류',
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
                              value: _selectedTreatmentType,
                              onChanged: (value) {
                                setState(() {
                                  _selectedTreatmentType = value;
                                });
                              },
                              direction: Axis.horizontal,
                              spacing: 24,
                              options: const [
                                CustomRadioOption(value: '튼살-경', label: '튼살-경'),
                                CustomRadioOption(value: '튼살-중', label: '튼살-중'),
                                CustomRadioOption(value: '백반증', label: '백반증'),
                                CustomRadioOption(value: '흉터', label: '흉터'),
                              ],
                            ),
                          ],
                        ),
                        const SizedBox(height: 32),

                        // 시술 부위 (필수)
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  '시술 부위',
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
                              value: _selectedBodyPart,
                              onChanged: (value) {
                                setState(() {
                                  _selectedBodyPart = value;
                                  // 기타가 아닌 경우 기타 입력 필드 초기화
                                  if (value != '기타') {
                                    _otherBodyPartController.clear();
                                  }
                                });
                              },
                              direction: Axis.horizontal,
                              spacing: 24,
                              options: const [
                                CustomRadioOption(value: '얼굴', label: '얼굴'),
                                CustomRadioOption(value: '목', label: '목'),
                                CustomRadioOption(value: '팔', label: '팔'),
                                CustomRadioOption(value: '다리', label: '다리'),
                                CustomRadioOption(value: '입술', label: '입술'),
                                CustomRadioOption(value: '손', label: '손'),
                                CustomRadioOption(value: '발', label: '발'),
                                CustomRadioOption(value: '유륜', label: '유륜'),
                                CustomRadioOption(value: '기타', label: '기타'),
                              ],
                            ),
                            // 기타 선택 시 추가 입력 필드
                            if (_selectedBodyPart == '기타') ...[
                              const SizedBox(height: 16),
                              CustomTextField(
                                labelText: null,
                                hintText: '자세한 부위를 입력해주세요',
                                controller: _otherBodyPartController,
                                validator: (value) {
                                  if (value == null || value.trim().isEmpty) {
                                    return '자세한 부위를 입력해주세요';
                                  }
                                  return null;
                                },
                              ),
                            ],
                          ],
                        ),
                        const SizedBox(height: 32),

                        // 시술 전 사진 (필수)
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Text(
                                  '시술 전 사진',
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
                            // 이미지 리스트 (가로 스크롤)
                            SingleChildScrollView(
                              scrollDirection: Axis.horizontal,
                              child: Row(
                                children: [
                                  // 이미지 추가 버튼 (가장 왼쪽, 최대 10개까지)
                                  if (_selectedImageFiles.length < 10)
                                    Padding(
                                      padding: const EdgeInsets.only(right: 8),
                                      child: GestureDetector(
                                        onTap: _pickImage,
                                        child: Container(
                                          width: 60,
                                          height: 60,
                                          decoration: BoxDecoration(
                                            color: AppColors.grayScaleBox3, // #F9FAFB
                                            borderRadius: BorderRadius.circular(4), // border-radius: 4px
                                            border: Border.all(
                                              color: Colors.transparent,
                                              width: 0,
                                            ),
                                          ),
                                          child: Column(
                                            mainAxisAlignment: MainAxisAlignment.center, // justify-content: center
                                            crossAxisAlignment: CrossAxisAlignment.center, // align-items: center
                                            mainAxisSize: MainAxisSize.min,
                                            children: [
                                              CustomIcon(
                                                icon: AppIcons.camera,
                                                width: 29,
                                                height: 24,
                                                color: AppColors.grayScaleGuideText,
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    ),
                                  // 선택된 이미지들 (오른쪽에 붙어서 표시)
                                  ...List.generate(
                                    _selectedImageFiles.length,
                                    (index) => Padding(
                                      padding: EdgeInsets.only(
                                        right: index < _selectedImageFiles.length - 1 ? 8 : 0,
                                      ),
                                      child: Stack(
                                        children: [
                                          Container(
                                            width: 60,
                                            height: 60,
                                            decoration: BoxDecoration(
                                              color: AppColors.grayScaleBox3,
                                              borderRadius: BorderRadius.circular(4),
                                              border: Border.all(
                                                color: Colors.transparent,
                                                width: 0,
                                              ),
                                            ),
                                            child: ClipRRect(
                                              borderRadius: BorderRadius.circular(4),
                                              child: kIsWeb && index < _selectedImageBytes.length
                                                  ? Image.memory(
                                                      _selectedImageBytes[index],
                                                      width: 60,
                                                      height: 60,
                                                      fit: BoxFit.cover,
                                                    )
                                                  : Image.file(
                                                      File(_selectedImageFiles[index].path),
                                                      width: 60,
                                                      height: 60,
                                                      fit: BoxFit.cover,
                                                    ),
                                            ),
                                          ),
                                          // 삭제 버튼 (오른쪽 상단, 위에서 4px, 오른쪽에서 4px)
                                          Positioned(
                                            top: 4,
                                            right: 4,
                                            child: GestureDetector(
                                              onTap: () {
                                                _removeImage(index);
                                              },
                                              behavior: HitTestBehavior.opaque,
                                              child: Container(
                                                width: 20,
                                                height: 20,
                                                decoration: BoxDecoration(
                                                  color: Colors.black.withOpacity(0.5),
                                                  shape: BoxShape.circle,
                                                ),
                                                child: const Center(
                                                  child: CustomIcon(
                                                    icon: AppIcons.closeWhite,
                                                    size: 12,
                                                  ),
                                                ),
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
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
                    // 다음 버튼
                    Expanded(
                      child: PrimaryButton(
                        text: '다음',
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

