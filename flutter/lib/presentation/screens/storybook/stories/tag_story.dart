import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/tags/custom_tag.dart';
import 'base_story.dart';

/// 태그 컴포넌트 스토리
class TagStory extends StatefulWidget {
  const TagStory({super.key});

  @override
  State<TagStory> createState() => _TagStoryState();
}

class _TagStoryState extends State<TagStory> {
  bool _enabled = true;
  TagType _selectedType = TagType.default_;
  TagSize _selectedSize = TagSize.medium;
  TagShape _selectedShape = TagShape.square;
  bool _closable = false;

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Tag',
      description: '태그 컴포넌트의 다양한 타입, 크기, 상태를 테스트할 수 있습니다.',
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
                title: const Text('Closable'),
                value: _closable,
                onChanged: (value) {
                  setState(() => _closable = value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Type',
            children: [
              RadioListTile<TagType>(
                title: const Text('Default'),
                value: TagType.default_,
                groupValue: _selectedType,
                onChanged: (value) {
                  setState(() => _selectedType = value ?? TagType.default_);
                },
              ),
              RadioListTile<TagType>(
                title: const Text('Primary'),
                value: TagType.primary,
                groupValue: _selectedType,
                onChanged: (value) {
                  setState(() => _selectedType = value ?? TagType.primary);
                },
              ),
              RadioListTile<TagType>(
                title: const Text('Success'),
                value: TagType.success,
                groupValue: _selectedType,
                onChanged: (value) {
                  setState(() => _selectedType = value ?? TagType.success);
                },
              ),
              RadioListTile<TagType>(
                title: const Text('Warning'),
                value: TagType.warning,
                groupValue: _selectedType,
                onChanged: (value) {
                  setState(() => _selectedType = value ?? TagType.warning);
                },
              ),
              RadioListTile<TagType>(
                title: const Text('Error'),
                value: TagType.error,
                groupValue: _selectedType,
                onChanged: (value) {
                  setState(() => _selectedType = value ?? TagType.error);
                },
              ),
              RadioListTile<TagType>(
                title: const Text('Info'),
                value: TagType.info,
                groupValue: _selectedType,
                onChanged: (value) {
                  setState(() => _selectedType = value ?? TagType.info);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Size',
            children: [
              RadioListTile<TagSize>(
                title: const Text('Small'),
                value: TagSize.small,
                groupValue: _selectedSize,
                onChanged: (value) {
                  setState(() => _selectedSize = value ?? TagSize.small);
                },
              ),
              RadioListTile<TagSize>(
                title: const Text('Medium'),
                value: TagSize.medium,
                groupValue: _selectedSize,
                onChanged: (value) {
                  setState(() => _selectedSize = value ?? TagSize.medium);
                },
              ),
              RadioListTile<TagSize>(
                title: const Text('Large'),
                value: TagSize.large,
                groupValue: _selectedSize,
                onChanged: (value) {
                  setState(() => _selectedSize = value ?? TagSize.large);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Shape',
            children: [
              RadioListTile<TagShape>(
                title: const Text('Square'),
                value: TagShape.square,
                groupValue: _selectedShape,
                onChanged: (value) {
                  setState(() => _selectedShape = value ?? TagShape.square);
                },
              ),
              RadioListTile<TagShape>(
                title: const Text('Round'),
                value: TagShape.round,
                groupValue: _selectedShape,
                onChanged: (value) {
                  setState(() => _selectedShape = value ?? TagShape.round);
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CustomTag(
            label: 'Tag Label',
            type: _selectedType,
            size: _selectedSize,
            shape: _selectedShape,
            closable: _closable,
            enabled: _enabled,
            onClose: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Tag closed')),
              );
            },
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Tag tapped')),
              );
            },
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'All Types',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              const CustomTag(label: 'Default', type: TagType.default_),
              const CustomTag(label: 'Primary', type: TagType.primary),
              const CustomTag(label: 'Success', type: TagType.success),
              const CustomTag(label: 'Warning', type: TagType.warning),
              const CustomTag(label: 'Error', type: TagType.error),
              const CustomTag(label: 'Info', type: TagType.info),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'All Sizes',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: const [
              CustomTag(label: 'Small', size: TagSize.small),
              CustomTag(label: 'Medium', size: TagSize.medium),
              CustomTag(label: 'Large', size: TagSize.large),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Closable Tags',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              CustomTag(
                label: 'Closable',
                closable: true,
                onClose: () {},
              ),
              CustomTag(
                label: 'Primary Closable',
                type: TagType.primary,
                closable: true,
                onClose: () {},
              ),
              CustomTag(
                label: 'Success Closable',
                type: TagType.success,
                closable: true,
                onClose: () {},
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'With Icons',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              CustomTag(
                label: 'With Icon',
                prefixIcon: Icon(
                  Icons.label,
                  size: 14,
                  color: AppColors.medicalDarkBlue,
                ),
              ),
              CustomTag(
                label: 'With Suffix',
                suffixIcon: Icon(
                  Icons.check_circle,
                  size: 14,
                  color: Colors.green,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Clickable Tags',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              CustomTag(
                label: 'Clickable',
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Tag clicked')),
                  );
                },
              ),
              CustomTag(
                label: 'Clickable Primary',
                type: TagType.primary,
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Tag clicked')),
                  );
                },
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Round Shape',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: const [
              CustomTag(label: 'Round Default', shape: TagShape.round),
              CustomTag(
                label: 'Round Primary',
                type: TagType.primary,
                shape: TagShape.round,
              ),
              CustomTag(
                label: 'Round Success',
                type: TagType.success,
                shape: TagShape.round,
              ),
              CustomTag(
                label: 'Round Closable',
                shape: TagShape.round,
                closable: true,
                onClose: null,
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Square vs Round',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: const [
              CustomTag(label: 'Square', shape: TagShape.square),
              CustomTag(label: 'Round', shape: TagShape.round),
              CustomTag(
                label: 'Square Primary',
                type: TagType.primary,
                shape: TagShape.square,
              ),
              CustomTag(
                label: 'Round Primary',
                type: TagType.primary,
                shape: TagShape.round,
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Disabled Tags',
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: const [
              CustomTag(label: 'Disabled', enabled: false),
              CustomTag(
                label: 'Disabled Closable',
                closable: true,
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

