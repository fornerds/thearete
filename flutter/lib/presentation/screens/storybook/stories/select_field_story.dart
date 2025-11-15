import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/inputs/custom_select_field.dart';
import 'base_story.dart';

/// Select Box 컴포넌트 스토리
class SelectFieldStory extends StatefulWidget {
  const SelectFieldStory({super.key});

  @override
  State<SelectFieldStory> createState() => _SelectFieldStoryState();
}

class _SelectFieldStoryState extends State<SelectFieldStory> {
  String? _selectedValue1;
  String? _selectedValue2;
  String? _selectedValue3;
  int? _selectedValue4;
  
  bool _enabled = true;
  bool _hasError = false;
  bool _isRequired = false;

  final List<SelectOption<String>> _stringOptions = [
    const SelectOption(value: 'option1', label: '옵션 1'),
    const SelectOption(value: 'option2', label: '옵션 2'),
    const SelectOption(value: 'option3', label: '옵션 3'),
    const SelectOption(value: 'option4', label: '옵션 4 (비활성화)', disabled: true),
    const SelectOption(value: 'option5', label: '옵션 5'),
  ];

  final List<SelectOption<int>> _intOptions = [
    const SelectOption(value: 1, label: '1번'),
    const SelectOption(value: 2, label: '2번'),
    const SelectOption(value: 3, label: '3번'),
    const SelectOption(value: 4, label: '4번'),
  ];

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Select Field',
      description: '드롭다운 선택 컴포넌트의 다양한 옵션과 상태를 테스트할 수 있습니다.',
      controls: Column(
        children: [
          ControlSection(
            title: 'General',
            children: [
              SwitchListTile(
                title: const Text('Enabled'),
                value: _enabled,
                onChanged: (value) {
                  setState(() => _enabled = value);
                },
              ),
              SwitchListTile(
                title: const Text('Has Error'),
                value: _hasError,
                onChanged: (value) {
                  setState(() => _hasError = value);
                },
              ),
              SwitchListTile(
                title: const Text('Required'),
                value: _isRequired,
                onChanged: (value) {
                  setState(() => _isRequired = value);
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        children: [
          CustomSelectField<String>(
            labelText: 'Basic Select',
            hintText: '옵션을 선택하세요',
            value: _selectedValue1,
            options: _stringOptions,
            isRequired: _isRequired,
            enabled: _enabled,
            errorText: _hasError ? '에러 메시지가 표시됩니다' : null,
            onChanged: (value) {
              setState(() => _selectedValue1 = value);
            },
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'With Required Label',
          CustomSelectField<String>(
            labelText: '필수 선택',
            hintText: '옵션을 선택하세요',
            value: _selectedValue2,
            options: _stringOptions,
            isRequired: true,
            onChanged: (value) {
              setState(() => _selectedValue2 = value);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Helper Text',
          CustomSelectField<String>(
            labelText: '카테고리',
            hintText: '카테고리를 선택하세요',
            helperText: '원하는 카테고리를 선택해주세요',
            value: _selectedValue3,
            options: _stringOptions,
            onChanged: (value) {
              setState(() => _selectedValue3 = value);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Error',
          CustomSelectField<String>(
            labelText: '에러 상태',
            hintText: '옵션을 선택하세요',
            value: null,
            options: _stringOptions,
            errorText: '필수 입력 항목입니다',
            onChanged: (value) {
              setState(() {});
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Disabled',
          CustomSelectField<String>(
            labelText: '비활성화',
            hintText: '옵션을 선택하세요',
            value: 'option1',
            options: _stringOptions,
            enabled: false,
            onChanged: (value) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Integer Type',
          CustomSelectField<int>(
            labelText: '숫자 선택',
            hintText: '숫자를 선택하세요',
            value: _selectedValue4,
            options: _intOptions,
            isRequired: true,
            onChanged: (value) {
              setState(() => _selectedValue4 = value);
            },
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

