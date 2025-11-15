import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/inputs/custom_text_area.dart';
import 'base_story.dart';

/// 텍스트 영역 컴포넌트 스토리
class TextAreaStory extends StatefulWidget {
  const TextAreaStory({super.key});

  @override
  State<TextAreaStory> createState() => _TextAreaStoryState();
}

class _TextAreaStoryState extends State<TextAreaStory> {
  final _controller1 = TextEditingController();
  final _controller2 = TextEditingController();
  final _controller3 = TextEditingController();
  final _controller4 = TextEditingController();
  final _controller5 = TextEditingController();
  
  bool _enabled = true;
  bool _hasError = false;
  bool _readOnly = false;
  bool _showCharacterCount = false;
  bool _isRequired = false;
  int _minLines = 3;
  int _maxLines = 5;
  int? _maxLength;

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
      title: 'Text Area',
      description: '여러 줄 텍스트 입력을 위한 Textarea 컴포넌트의 다양한 옵션과 상태를 테스트할 수 있습니다.',
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
                title: const Text('Read Only'),
                value: _readOnly,
                onChanged: (value) {
                  setState(() => _readOnly = value);
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
                title: const Text('Show Character Count'),
                value: _showCharacterCount,
                onChanged: (value) {
                  setState(() => _showCharacterCount = value);
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
          ControlSection(
            title: 'Lines',
            children: [
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Min Lines',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _minLines = int.tryParse(value) ?? 3;
                  });
                },
              ),
              const SizedBox(height: 8),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Max Lines',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _maxLines = int.tryParse(value) ?? 5;
                  });
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Max Length',
            children: [
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Max Length (0 to disable)',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  setState(() {
                    _maxLength = value.isEmpty
                        ? null
                        : (int.tryParse(value) ?? 0) > 0
                            ? int.tryParse(value)
                            : null;
                  });
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        children: [
          CustomTextArea(
            labelText: 'Basic Text Area',
            hintText: '여러 줄 텍스트를 입력하세요',
            controller: _controller1,
            enabled: _enabled,
            readOnly: _readOnly,
            isRequired: _isRequired,
            minLines: _minLines,
            maxLines: _maxLines,
            maxLength: _maxLength,
            showCharacterCount: _showCharacterCount,
            errorText: _hasError ? '에러 메시지가 표시됩니다' : null,
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'With Character Count',
          CustomTextArea(
            labelText: '메모',
            hintText: '메모를 입력하세요 (최대 200자)',
            controller: _controller2,
            minLines: 3,
            maxLines: 6,
            maxLength: 200,
            showCharacterCount: true,
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Large Text Area',
          CustomTextArea(
            labelText: '상세 설명',
            hintText: '상세한 설명을 입력하세요',
            controller: _controller3,
            minLines: 5,
            maxLines: 10,
            helperText: '최대 10줄까지 입력 가능합니다',
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Small Text Area',
          CustomTextArea(
            labelText: '짧은 메모',
            hintText: '짧은 메모를 입력하세요',
            controller: _controller4,
            minLines: 2,
            maxLines: 3,
            maxLength: 100,
            showCharacterCount: true,
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Read Only',
          CustomTextArea(
            labelText: '읽기 전용',
            controller: TextEditingController(
              text: '이 텍스트 영역은 읽기 전용입니다. 수정할 수 없습니다.',
            ),
            readOnly: true,
            minLines: 3,
            maxLines: 5,
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Error',
          CustomTextArea(
            labelText: '에러 상태',
            hintText: '에러가 있는 텍스트 영역',
            controller: _controller5,
            minLines: 3,
            maxLines: 5,
            errorText: '필수 입력 항목입니다',
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

