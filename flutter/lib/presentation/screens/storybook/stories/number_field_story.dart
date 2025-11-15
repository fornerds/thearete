import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/inputs/custom_number_field.dart';
import 'base_story.dart';

/// 숫자 입력 필드 컴포넌트 스토리
class NumberFieldStory extends StatefulWidget {
  const NumberFieldStory({super.key});

  @override
  State<NumberFieldStory> createState() => _NumberFieldStoryState();
}

class _NumberFieldStoryState extends State<NumberFieldStory> {
  final _controller1 = TextEditingController();
  final _controller2 = TextEditingController();
  final _controller3 = TextEditingController();
  final _controller4 = TextEditingController();
  final _controller5 = TextEditingController();
  
  bool _enabled = true;
  bool _hasError = false;
  bool _isRequired = false;
  bool _showButtons = true;
  int? _min;
  int? _max;
  int _step = 1;

  @override
  void dispose() {
    _controller1.dispose();
    _controller2.dispose();
    _controller3.dispose();
    _controller4.dispose();
    _controller5.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Number Field',
      description: '숫자 전용 입력 필드 컴포넌트의 다양한 옵션과 상태를 테스트할 수 있습니다.',
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
              SwitchListTile(
                title: const Text('Show Increment Buttons'),
                value: _showButtons,
                onChanged: (value) {
                  setState(() => _showButtons = value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Range',
            children: [
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Min Value (empty to disable)',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _min = value.isEmpty ? null : int.tryParse(value);
                  });
                },
              ),
              const SizedBox(height: 8),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Max Value (empty to disable)',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _max = value.isEmpty ? null : int.tryParse(value);
                  });
                },
              ),
              const SizedBox(height: 8),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Step',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _step = int.tryParse(value) ?? 1;
                  });
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        children: [
          CustomNumberField(
            labelText: 'Basic Number Field',
            hintText: '숫자를 입력하세요',
            controller: _controller1,
            enabled: _enabled,
            isRequired: _isRequired,
            min: _min,
            max: _max,
            step: _step,
            showIncrementButtons: _showButtons,
            errorText: _hasError ? '에러 메시지가 표시됩니다' : null,
            onChanged: (value) {
              print('Value changed: $value');
            },
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'With Range (0-100)',
          CustomNumberField(
            labelText: '숫자 입력',
            hintText: '0부터 100까지',
            controller: _controller2,
            min: 0,
            max: 100,
            step: 5,
            showIncrementButtons: true,
            onChanged: (value) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Suffix Text',
          CustomNumberField(
            labelText: '수량',
            hintText: '수량을 입력하세요',
            controller: _controller3,
            suffixText: '개',
            showIncrementButtons: true,
            onChanged: (value) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Without Buttons',
          CustomNumberField(
            labelText: '숫자 입력',
            hintText: '버튼 없이 입력',
            controller: _controller4,
            showIncrementButtons: false,
            onChanged: (value) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Error',
          CustomNumberField(
            labelText: '에러 상태',
            hintText: '숫자를 입력하세요',
            controller: _controller5,
            errorText: '필수 입력 항목입니다',
            showIncrementButtons: true,
            onChanged: (value) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Required Field',
          CustomNumberField(
            labelText: '필수 숫자 입력',
            hintText: '숫자를 입력하세요',
            controller: TextEditingController(),
            isRequired: true,
            min: 1,
            max: 999,
            showIncrementButtons: true,
            onChanged: (value) {},
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

