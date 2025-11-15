import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/checkbox/custom_checkbox.dart';
import 'base_story.dart';

/// 체크박스 컴포넌트 스토리
class CheckboxStory extends StatefulWidget {
  const CheckboxStory({super.key});

  @override
  State<CheckboxStory> createState() => _CheckboxStoryState();
}

class _CheckboxStoryState extends State<CheckboxStory> {
  bool _value1 = false;
  bool _value2 = false;
  bool _value3 = false;
  List<bool> _groupValues = [false, false, false];
  List<bool> _groupValues2 = [false, false, false];
  List<bool> _groupValues3 = [false, false, false];
  
  bool _enabled = true;

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Checkbox',
      description: '체크박스 컴포넌트의 다양한 상태(default, hover, checked)를 테스트할 수 있습니다.',
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
            ],
          ),
        ],
      ),
      preview: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CustomCheckbox(
            value: _value1,
            onChanged: _enabled
                ? (value) {
                    setState(() => _value1 = value ?? false);
                  }
                : null,
            label: '옵션 1',
          ),
          const SizedBox(height: 8),
          CustomCheckbox(
            value: _value2,
            onChanged: _enabled
                ? (value) {
                    setState(() => _value2 = value ?? false);
                  }
                : null,
            label: '옵션 2',
          ),
          const SizedBox(height: 8),
          CustomCheckbox(
            value: _value3,
            onChanged: _enabled
                ? (value) {
                    setState(() => _value3 = value ?? false);
                  }
                : null,
            label: '옵션 3',
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'Checkbox Group',
          CustomCheckboxGroup(
            values: _groupValues,
            onChanged: (index) {
              setState(() {
                _groupValues[index] = !_groupValues[index];
              });
            },
            enabled: _enabled,
            options: const [
              CustomCheckboxOption(label: '옵션 1'),
              CustomCheckboxOption(label: '옵션 2'),
              CustomCheckboxOption(label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Horizontal Layout',
          CustomCheckboxGroup(
            values: _groupValues2,
            onChanged: (index) {
              setState(() {
                _groupValues2[index] = !_groupValues2[index];
              });
            },
            direction: Axis.horizontal,
            spacing: 24,
            options: const [
              CustomCheckboxOption(label: '옵션 1'),
              CustomCheckboxOption(label: '옵션 2'),
              CustomCheckboxOption(label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Disabled Option',
          CustomCheckboxGroup(
            values: _groupValues3,
            onChanged: (index) {
              setState(() {
                _groupValues3[index] = !_groupValues3[index];
              });
            },
            options: const [
              CustomCheckboxOption(label: '옵션 1'),
              CustomCheckboxOption(label: '옵션 2 (비활성화)', disabled: true),
              CustomCheckboxOption(label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Disabled Group',
          CustomCheckboxGroup(
            values: [true, false, true],
            onChanged: null,
            enabled: false,
            options: const [
              CustomCheckboxOption(label: '옵션 1'),
              CustomCheckboxOption(label: '옵션 2'),
              CustomCheckboxOption(label: '옵션 3'),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Different Sizes',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CustomCheckbox(
                value: true,
                onChanged: null,
                label: 'Small (16px)',
                size: 16,
              ),
              const SizedBox(height: 8),
              CustomCheckbox(
                value: true,
                onChanged: null,
                label: 'Medium (20px)',
                size: 20,
              ),
              const SizedBox(height: 8),
              CustomCheckbox(
                value: true,
                onChanged: null,
                label: 'Large (24px)',
                size: 24,
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'All States',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CustomCheckbox(
                value: false,
                onChanged: (value) {},
                label: 'Unchecked',
              ),
              const SizedBox(height: 8),
              CustomCheckbox(
                value: true,
                onChanged: (value) {},
                label: 'Checked',
              ),
              const SizedBox(height: 8),
              CustomCheckbox(
                value: false,
                onChanged: null,
                label: 'Disabled Unchecked',
                enabled: false,
              ),
              const SizedBox(height: 8),
              CustomCheckbox(
                value: true,
                onChanged: null,
                label: 'Disabled Checked',
                enabled: false,
              ),
            ],
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

