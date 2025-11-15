import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/buttons/primary_button.dart';
import '../../../widgets/common/buttons/secondary_button.dart';
import '../../../widgets/common/buttons/text_button.dart';
import 'base_story.dart';

/// 버튼 컴포넌트 스토리
class ButtonStory extends StatefulWidget {
  const ButtonStory({super.key});

  @override
  State<ButtonStory> createState() => _ButtonStoryState();
}

class _ButtonStoryState extends State<ButtonStory> {
  bool _primaryLoading = false;
  bool _secondaryLoading = false;
  bool _textLoading = false;
  bool _primaryEnabled = true;
  bool _secondaryEnabled = true;
  bool _textEnabled = true;
  String _primaryText = 'Primary Button';
  String _secondaryText = 'Secondary Button';
  String _textButtonText = 'Text Button';

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Buttons',
      description: 'Primary, Secondary, Text 버튼 컴포넌트의 다양한 상태를 테스트할 수 있습니다.',
      controls: Column(
        children: [
          ControlSection(
            title: 'Primary Button',
            children: [
              SwitchListTile(
                title: const Text('Enabled'),
                value: _primaryEnabled,
                onChanged: (value) {
                  setState(() => _primaryEnabled = value);
                },
              ),
              SwitchListTile(
                title: const Text('Loading'),
                value: _primaryLoading,
                onChanged: (value) {
                  setState(() => _primaryLoading = value);
                },
              ),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Button Text',
                  border: OutlineInputBorder(),
                ),
                onChanged: (value) {
                  setState(() => _primaryText = value.isEmpty ? 'Primary Button' : value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Secondary Button',
            children: [
              SwitchListTile(
                title: const Text('Enabled'),
                value: _secondaryEnabled,
                onChanged: (value) {
                  setState(() => _secondaryEnabled = value);
                },
              ),
              SwitchListTile(
                title: const Text('Loading'),
                value: _secondaryLoading,
                onChanged: (value) {
                  setState(() => _secondaryLoading = value);
                },
              ),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Button Text',
                  border: OutlineInputBorder(),
                ),
                onChanged: (value) {
                  setState(() => _secondaryText = value.isEmpty ? 'Secondary Button' : value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Text Button',
            children: [
              SwitchListTile(
                title: const Text('Enabled'),
                value: _textEnabled,
                onChanged: (value) {
                  setState(() => _textEnabled = value);
                },
              ),
              SwitchListTile(
                title: const Text('Loading'),
                value: _textLoading,
                onChanged: (value) {
                  setState(() => _textLoading = value);
                },
              ),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Button Text',
                  border: OutlineInputBorder(),
                ),
                onChanged: (value) {
                  setState(() => _textButtonText = value.isEmpty ? 'Text Button' : value);
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          PrimaryButton(
            text: _primaryText,
            onPressed: _primaryEnabled ? () {} : null,
            isLoading: _primaryLoading,
          ),
          const SizedBox(height: 16),
          SecondaryButton(
            text: _secondaryText,
            onPressed: _secondaryEnabled ? () {} : null,
            isLoading: _secondaryLoading,
          ),
          const SizedBox(height: 16),
          AppTextButton(
            text: _textButtonText,
            onPressed: _textEnabled ? () {} : null,
            isLoading: _textLoading,
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'Full Width',
          Column(
            children: [
              SizedBox(
                width: double.infinity,
                child: PrimaryButton(
                  text: 'Full Width Primary',
                  onPressed: () {},
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: SecondaryButton(
                  text: 'Full Width Secondary',
                  onPressed: () {},
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Different Sizes',
          Column(
            children: [
              PrimaryButton(
                text: 'Default',
                onPressed: () {},
              ),
              const SizedBox(height: 12),
              PrimaryButton(
                text: 'Small',
                onPressed: () {},
                height: 40,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              ),
              const SizedBox(height: 12),
              PrimaryButton(
                text: 'Large',
                onPressed: () {},
                height: 64,
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 20),
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

