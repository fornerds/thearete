import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';
import '../../../widgets/common/pagination/custom_pagination.dart';
import 'base_story.dart';

/// 페이지네이션 컴포넌트 스토리
class PaginationStory extends StatefulWidget {
  const PaginationStory({super.key});

  @override
  State<PaginationStory> createState() => _PaginationStoryState();
}

class _PaginationStoryState extends State<PaginationStory> {
  int _currentPage1 = 1;
  int _currentPage2 = 5;
  int _currentPage3 = 1;
  int _currentPage4 = 10;
  int _currentPage5 = 1;
  
  bool _enabled = true;
  bool _showFirstLast = true;
  bool _showPrevNext = true;
  int _totalPages = 20;
  int _maxVisiblePages = 5;

  @override
  Widget build(BuildContext context) {
    return BaseStory(
      title: 'Pagination',
      description: '페이지네이션 컴포넌트의 다양한 옵션과 상태를 테스트할 수 있습니다.',
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
                title: const Text('Show First/Last'),
                value: _showFirstLast,
                onChanged: (value) {
                  setState(() => _showFirstLast = value);
                },
              ),
              SwitchListTile(
                title: const Text('Show Prev/Next'),
                value: _showPrevNext,
                onChanged: (value) {
                  setState(() => _showPrevNext = value);
                },
              ),
            ],
          ),
          ControlSection(
            title: 'Settings',
            children: [
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Total Pages',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  final pages = int.tryParse(value);
                  if (pages != null && pages > 0) {
                    setState(() {
                      _totalPages = pages;
                      if (_currentPage1 > pages) {
                        _currentPage1 = pages;
                      }
                      if (_currentPage2 > pages) {
                        _currentPage2 = pages;
                      }
                      if (_currentPage3 > pages) {
                        _currentPage3 = pages;
                      }
                      if (_currentPage4 > pages) {
                        _currentPage4 = pages;
                      }
                      if (_currentPage5 > pages) {
                        _currentPage5 = pages;
                      }
                    });
                  }
                },
              ),
              const SizedBox(height: 8),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Max Visible Pages',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                onChanged: (value) {
                  final max = int.tryParse(value);
                  if (max != null && max > 0) {
                    setState(() => _maxVisiblePages = max);
                  }
                },
              ),
            ],
          ),
        ],
      ),
      preview: Column(
        children: [
          CustomPagination(
            currentPage: _currentPage1,
            totalPages: _totalPages,
            enabled: _enabled,
            showFirstLast: _showFirstLast,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {
              setState(() => _currentPage1 = page);
            },
          ),
        ],
      ),
      variants: [
        _buildVariantCard(
          'First Page',
          CustomPagination(
            currentPage: 1,
            totalPages: _totalPages,
            enabled: _enabled,
            showFirstLast: _showFirstLast,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {
              setState(() => _currentPage2 = page);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Middle Page',
          CustomPagination(
            currentPage: _currentPage3,
            totalPages: _totalPages,
            enabled: _enabled,
            showFirstLast: _showFirstLast,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {
              setState(() => _currentPage3 = page);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Last Page',
          CustomPagination(
            currentPage: _totalPages,
            totalPages: _totalPages,
            enabled: _enabled,
            showFirstLast: _showFirstLast,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {
              setState(() => _currentPage4 = page);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Few Pages (5 pages)',
          CustomPagination(
            currentPage: _currentPage5,
            totalPages: 5,
            enabled: _enabled,
            showFirstLast: _showFirstLast,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {
              setState(() => _currentPage5 = page);
            },
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Without First/Last Buttons',
          CustomPagination(
            currentPage: 10,
            totalPages: _totalPages,
            enabled: _enabled,
            showFirstLast: false,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Without Prev/Next Buttons',
          CustomPagination(
            currentPage: 10,
            totalPages: _totalPages,
            enabled: _enabled,
            showFirstLast: _showFirstLast,
            showPrevNext: false,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {},
          ),
        ),
        const SizedBox(height: 16),
        _buildVariantCard(
          'Disabled',
          CustomPagination(
            currentPage: 10,
            totalPages: _totalPages,
            enabled: false,
            showFirstLast: _showFirstLast,
            showPrevNext: _showPrevNext,
            maxVisiblePages: _maxVisiblePages,
            onPageChanged: (page) {},
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

