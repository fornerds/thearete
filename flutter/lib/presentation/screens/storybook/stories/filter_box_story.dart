import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/filter/filter_box.dart';
import 'base_story.dart';

/// 필터링 박스 컴포넌트 스토리
class FilterBoxStory extends StatefulWidget {
  const FilterBoxStory({super.key});

  @override
  State<FilterBoxStory> createState() => _FilterBoxStoryState();
}

class _FilterBoxStoryState extends State<FilterBoxStory> {
  List<String> _multipleSelected = [];
  String? _singleSelected;
  List<String> _multipleSelected2 = [];
  String? _singleSelected2;
  
  bool _enabled = true;
  Axis _direction = Axis.horizontal;

  final List<FilterOption> _options = const [
    FilterOption(id: 'option1', label: '옵션 1'),
    FilterOption(id: 'option2', label: '옵션 2'),
    FilterOption(id: 'option3', label: '옵션 3'),
    FilterOption(id: 'option4', label: '옵션 4 (비활성화)', disabled: true),
    FilterOption(id: 'option5', label: '옵션 5'),
  ];

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Filter Box',
      description: '필터링 박스 컴포넌트의 다양한 옵션과 상태를 테스트할 수 있습니다. 칩 형태의 필터링 UI입니다.',
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
          ControlSection(
            title: 'Layout',
            children: [
              RadioListTile<Axis>(
                title: const Text('Horizontal'),
                value: Axis.horizontal,
                groupValue: _direction,
                onChanged: (value) {
                  setState(() => _direction = value ?? Axis.horizontal);
                },
              ),
              RadioListTile<Axis>(
                title: const Text('Vertical'),
                value: Axis.vertical,
                groupValue: _direction,
                onChanged: (value) {
                  setState(() => _direction = value ?? Axis.vertical);
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          FilterBox(
            title: 'Multiple Selection',
            type: FilterType.multiple,
            options: _options,
            selectedIds: _multipleSelected,
            enabled: _enabled,
            direction: _direction,
            onChanged: (selectedIds) {
              setState(() => _multipleSelected = selectedIds);
            },
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'Single Selection',
          FilterBox(
            title: 'Single Selection',
            type: FilterType.single,
            options: _options,
            selectedId: _singleSelected,
            enabled: _enabled,
            direction: _direction,
            onSingleChanged: (value) {
              setState(() => _singleSelected = value);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Multiple with Selection',
          FilterBox(
            title: '카테고리',
            type: FilterType.multiple,
            options: _options,
            selectedIds: _multipleSelected2,
            enabled: _enabled,
            direction: _direction,
            onChanged: (selectedIds) {
              setState(() => _multipleSelected2 = selectedIds);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Single with Selection',
          FilterBox(
            title: '정렬',
            type: FilterType.single,
            options: _options,
            selectedId: _singleSelected2,
            enabled: _enabled,
            direction: _direction,
            onSingleChanged: (value) {
              setState(() => _singleSelected2 = value);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Disabled Filter Box',
          FilterBox(
            title: '비활성화 필터',
            type: FilterType.multiple,
            options: _options,
            selectedIds: ['option1', 'option2'],
            enabled: false,
            direction: _direction,
            onChanged: (selectedIds) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Without Title',
          FilterBox(
            type: FilterType.multiple,
            options: _options,
            selectedIds: _multipleSelected,
            enabled: _enabled,
            direction: _direction,
            onChanged: (selectedIds) {
              setState(() => _multipleSelected = selectedIds);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Many Options',
          FilterBox(
            title: '많은 옵션',
            type: FilterType.multiple,
            options: List.generate(
              15,
              (index) => FilterOption(
                id: 'option${index + 1}',
                label: '옵션 ${index + 1}',
              ),
            ),
            selectedIds: ['option1', 'option3', 'option5', 'option7'],
            enabled: _enabled,
            direction: _direction,
            onChanged: (selectedIds) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Vertical Layout',
          FilterBox(
            title: '수직 레이아웃',
            type: FilterType.multiple,
            options: _options,
            selectedIds: ['option1', 'option3'],
            enabled: _enabled,
            direction: Axis.vertical,
            spacing: 12,
            onChanged: (selectedIds) {},
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
