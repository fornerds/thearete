import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/inputs/custom_text_field.dart';
import 'base_story.dart';

/// 텍스트 필드 컴포넌트 스토리
class TextFieldStory extends StatefulWidget {
  const TextFieldStory({super.key});

  @override
  State<TextFieldStory> createState() => _TextFieldStoryState();
}

class _TextFieldStoryState extends State<TextFieldStory> {
  final _controller1 = TextEditingController();
  final _controller2 = TextEditingController();
  final _controller3 = TextEditingController();
  final _controller4 = TextEditingController();
  final _controller5 = TextEditingController();
  
  bool _enabled = true;
  bool _hasError = false;
  bool _obscureText = false;
  bool _isRequired = false;
  TextFieldIconType? _prefixIconType;
  TextFieldIconType? _suffixIconType;

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
      title: 'Text Field',
      description: '커스텀 텍스트 필드 컴포넌트의 다양한 옵션과 상태를 테스트할 수 있습니다.',
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
                title: const Text('Obscure Text'),
                value: _obscureText,
                onChanged: (value) {
                  setState(() => _obscureText = value);
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
            title: 'Prefix Icon',
            children: [
              DropdownButtonFormField<TextFieldIconType?>(
                decoration: const InputDecoration(
                  labelText: 'Prefix Icon Type',
                  border: OutlineInputBorder(),
                ),
                value: _prefixIconType,
                items: [
                  const DropdownMenuItem(
                    value: null,
                    child: Text('None'),
                  ),
                  ...TextFieldIconType.values.map((type) {
                    return DropdownMenuItem(
                      value: type,
                      child: Text(type.name),
                    );
                  }),
                ],
                onChanged: (value) {
                  setState(() => _prefixIconType = value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Suffix Icon',
            children: [
              DropdownButtonFormField<TextFieldIconType?>(
                decoration: const InputDecoration(
                  labelText: 'Suffix Icon Type',
                  border: OutlineInputBorder(),
                ),
                value: _suffixIconType,
                items: [
                  const DropdownMenuItem(
                    value: null,
                    child: Text('None'),
                  ),
                  ...TextFieldIconType.values.map((type) {
                    return DropdownMenuItem(
                      value: type,
                      child: Text(type.name),
                    );
                  }),
                ],
                onChanged: (value) {
                  setState(() => _suffixIconType = value);
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        children: [
          CustomTextField(
            labelText: 'Basic Text Field',
            hintText: '텍스트를 입력하세요',
            controller: _controller1,
            enabled: _enabled,
            isRequired: _isRequired,
            errorText: _hasError ? '에러 메시지가 표시됩니다' : null,
          ),
          const SizedBox(height: 16),
          CustomTextField(
            labelText: 'With Icons',
            hintText: '아이콘이 있는 필드',
            controller: _controller2,
            prefixIconType: _prefixIconType,
            suffixIconType: _suffixIconType,
            enabled: _enabled,
          ),
          const SizedBox(height: 16),
          CustomTextField(
            labelText: 'Password Field',
            hintText: '비밀번호를 입력하세요',
            controller: _controller3,
            obscureText: _obscureText,
            enabled: _enabled,
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'With Different Icon Types',
          Column(
            children: [
              CustomTextField(
                labelText: 'Search',
                hintText: '검색어를 입력하세요',
                controller: _controller4,
                prefixIconType: TextFieldIconType.search,
              ),
              const SizedBox(height: 16),
              CustomTextField(
                labelText: 'Select',
                hintText: '선택하세요',
                controller: _controller5,
                suffixIconType: TextFieldIconType.select,
                readOnly: true,
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Select dialog would open here')),
                  );
                },
              ),
              const SizedBox(height: 16),
              CustomTextField(
                labelText: 'Calendar',
                hintText: '날짜를 선택하세요',
                controller: TextEditingController(),
                suffixIconType: TextFieldIconType.calendar,
                readOnly: true,
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Date picker would open here')),
                  );
                },
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

