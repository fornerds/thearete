import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 커스텀 페이지네이션 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
/// 
/// 사용 예시:
/// ```dart
/// CustomPagination(
///   currentPage: 1,
///   totalPages: 10,
///   onPageChanged: (page) => print('Page changed to $page'),
/// )
/// ```
class CustomPagination extends StatelessWidget {
  /// 현재 페이지 번호 (1부터 시작)
  final int currentPage;
  
  /// 전체 페이지 수
  final int totalPages;
  
  /// 페이지 변경 시 호출되는 콜백
  final ValueChanged<int>? onPageChanged;
  
  /// 첫 페이지/마지막 페이지 버튼 표시 여부
  final bool showFirstLast;
  
  /// 이전/다음 페이지 버튼 표시 여부
  final bool showPrevNext;
  
  /// 최대 표시할 페이지 번호 개수
  final int maxVisiblePages;
  
  /// 컴포넌트 활성화 여부
  final bool enabled;

  const CustomPagination({
    super.key,
    required this.currentPage,
    required this.totalPages,
    this.onPageChanged,
    this.showFirstLast = true,
    this.showPrevNext = true,
    this.maxVisiblePages = 5,
    this.enabled = true,
  }) : assert(currentPage > 0 && currentPage <= totalPages,
           'currentPage must be between 1 and totalPages'),
       assert(totalPages > 0, 'totalPages must be greater than 0'),
       assert(maxVisiblePages > 0, 'maxVisiblePages must be greater than 0');

  @override
  Widget build(BuildContext context) {
    // 페이지가 1개 이하면 표시하지 않음
    if (totalPages <= 1) {
      return const SizedBox.shrink();
    }

    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      mainAxisSize: MainAxisSize.min,
      children: [
        // 첫 페이지 버튼
        if (showFirstLast) ...[
          _PaginationButton(
            icon: Icons.first_page,
            onPressed: enabled && currentPage > 1
                ? () => onPageChanged?.call(1)
                : null,
            tooltip: '첫 페이지',
          ),
          const SizedBox(width: 8),
        ],
        // 이전 페이지 버튼
        if (showPrevNext) ...[
          _PaginationButton(
            icon: Icons.chevron_left,
            onPressed: enabled && currentPage > 1
                ? () => onPageChanged?.call(currentPage - 1)
                : null,
            tooltip: '이전 페이지',
          ),
          const SizedBox(width: 8),
        ],
        // 페이지 번호들
        ..._buildPageNumbers(),
        // 다음 페이지 버튼
        if (showPrevNext) ...[
          const SizedBox(width: 8),
          _PaginationButton(
            icon: Icons.chevron_right,
            onPressed: enabled && currentPage < totalPages
                ? () => onPageChanged?.call(currentPage + 1)
                : null,
            tooltip: '다음 페이지',
          ),
        ],
        // 마지막 페이지 버튼
        if (showFirstLast) ...[
          const SizedBox(width: 8),
          _PaginationButton(
            icon: Icons.last_page,
            onPressed: enabled && currentPage < totalPages
                ? () => onPageChanged?.call(totalPages)
                : null,
            tooltip: '마지막 페이지',
          ),
        ],
      ],
    );
  }

  List<Widget> _buildPageNumbers() {
    final List<Widget> pages = [];
    final List<int> pageNumbers = _getPageNumbers();

    for (int i = 0; i < pageNumbers.length; i++) {
      final pageNum = pageNumbers[i];
      final isCurrentPage = pageNum == currentPage;

      pages.add(
        _PaginationPageButton(
          page: pageNum,
          isSelected: isCurrentPage,
          onPressed: enabled && !isCurrentPage
              ? () => onPageChanged?.call(pageNum)
              : null,
        ),
      );

      // 페이지 번호 사이에 ... 표시
      if (i < pageNumbers.length - 1 && pageNumbers[i + 1] - pageNum > 1) {
        pages.add(
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: Text(
              '...',
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: AppColors.medicalLightBlueGray,
              ),
            ),
          ),
        );
      }
      
      // 페이지 번호 사이 간격 추가
      if (i < pageNumbers.length - 1 && pageNumbers[i + 1] - pageNum == 1) {
        pages.add(const SizedBox(width: 4));
      }
    }

    return pages;
  }

  List<int> _getPageNumbers() {
    if (totalPages <= maxVisiblePages) {
      return List.generate(totalPages, (index) => index + 1);
    }

    final List<int> pages = [];
    final int halfVisible = maxVisiblePages ~/ 2;

    if (currentPage <= halfVisible + 1) {
      // 시작 부분
      for (int i = 1; i <= maxVisiblePages - 1; i++) {
        pages.add(i);
      }
      pages.add(totalPages);
    } else if (currentPage >= totalPages - halfVisible) {
      // 끝 부분
      pages.add(1);
      for (int i = totalPages - maxVisiblePages + 2; i <= totalPages; i++) {
        pages.add(i);
      }
    } else {
      // 중간 부분
      pages.add(1);
      for (int i = currentPage - halfVisible + 1; i <= currentPage + halfVisible - 1; i++) {
        pages.add(i);
      }
      pages.add(totalPages);
    }

    return pages;
  }
}

/// 페이지네이션 버튼 (이전/다음/첫/마지막)
class _PaginationButton extends StatefulWidget {
  final IconData icon;
  final VoidCallback? onPressed;
  final String? tooltip;

  const _PaginationButton({
    required this.icon,
    this.onPressed,
    this.tooltip,
  });

  @override
  State<_PaginationButton> createState() => _PaginationButtonState();
}

class _PaginationButtonState extends State<_PaginationButton> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    final isEnabled = widget.onPressed != null;
    
    return Tooltip(
      message: widget.tooltip ?? '',
      child: MouseRegion(
        onEnter: (_) {
          if (isEnabled) {
            setState(() => _isHovered = true);
          }
        },
        onExit: (_) {
          if (isEnabled) {
            setState(() => _isHovered = false);
          }
        },
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: widget.onPressed,
            borderRadius: BorderRadius.circular(8),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              width: 36,
              height: 36,
              decoration: BoxDecoration(
                color: _getBackgroundColor(),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _getBorderColor(),
                  width: 1,
                ),
              ),
              child: Icon(
                widget.icon,
                size: 20,
                color: _getIconColor(),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Color _getBackgroundColor() {
    if (widget.onPressed == null) {
      return AppColors.medicalOffWhite;
    }
    if (_isHovered) {
      return AppColors.medicalPaleBlue.withOpacity(0.2);
    }
    return Colors.white;
  }

  Color _getBorderColor() {
    if (widget.onPressed == null) {
      return AppColors.medicalPaleBlue;
    }
    if (_isHovered) {
      return AppColors.medicalBlueGray;
    }
    return AppColors.medicalPaleBlue;
  }

  Color _getIconColor() {
    if (widget.onPressed == null) {
      return AppColors.medicalLightBlueGray;
    }
    return AppColors.medicalDarkBlue;
  }
}

/// 페이지 번호 버튼
class _PaginationPageButton extends StatefulWidget {
  final int page;
  final bool isSelected;
  final VoidCallback? onPressed;

  const _PaginationPageButton({
    required this.page,
    required this.isSelected,
    this.onPressed,
  });

  @override
  State<_PaginationPageButton> createState() => _PaginationPageButtonState();
}

class _PaginationPageButtonState extends State<_PaginationPageButton> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) {
        if (widget.onPressed != null) {
          setState(() => _isHovered = true);
        }
      },
      onExit: (_) {
        if (widget.onPressed != null) {
          setState(() => _isHovered = false);
        }
      },
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: widget.onPressed,
          borderRadius: BorderRadius.circular(6),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            width: 36,
            height: 36,
            decoration: BoxDecoration(
              color: _getBackgroundColor(),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: _getBorderColor(),
                width: widget.isSelected ? 2 : 1,
              ),
            ),
            child: Center(
              child: Text(
                widget.page.toString(),
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: widget.isSelected
                      ? FontWeight.w600
                      : FontWeight.w500,
                  color: _getTextColor(),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Color _getBackgroundColor() {
    if (widget.isSelected) {
      return AppColors.medicalDarkBlue;
    }

    if (_isHovered && widget.onPressed != null) {
      return AppColors.medicalPaleBlue.withOpacity(0.3);
    }

    return Colors.white;
  }

  Color _getBorderColor() {
    if (widget.isSelected) {
      return AppColors.medicalDarkBlue;
    }

    if (_isHovered && widget.onPressed != null) {
      return AppColors.medicalBlueGray;
    }

    return AppColors.medicalPaleBlue;
  }

  Color _getTextColor() {
    if (widget.isSelected) {
      return Colors.white;
    }

    if (widget.onPressed == null) {
      return AppColors.medicalLightBlueGray;
    }

    return AppColors.medicalDarkBlue;
  }
}

