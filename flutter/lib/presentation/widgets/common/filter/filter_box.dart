import 'package:flutter/material.dart';
import '../../../../core/constants/app_colors.dart';

/// 필터 옵션 모델
class FilterOption {
  final String id;
  final String label;
  final bool disabled;

  const FilterOption({
    required this.id,
    required this.label,
    this.disabled = false,
  });
}

/// 필터 타입
enum FilterType {
  single,   // 하나만 선택 가능
  multiple, // 여러 개 선택 가능
}

/// 필터링 박스 컴포넌트
/// Figma 디자인 시스템 기반으로 제작
/// 칩/태그 형태의 필터링 UI
class FilterBox extends StatefulWidget {
  final String? title;
  final FilterType type;
  final List<FilterOption> options;
  final List<String> selectedIds;
  final String? selectedId; // single 타입일 때 사용
  final ValueChanged<List<String>>? onChanged; // multiple 타입일 때 사용
  final ValueChanged<String?>? onSingleChanged; // single 타입일 때 사용
  final bool enabled;
  final Axis direction;
  final double spacing;
  final EdgeInsetsGeometry? padding;
  final double borderRadius;

  FilterBox({
    super.key,
    this.title,
    required this.type,
    required this.options,
    this.selectedIds = const [],
    this.selectedId,
    this.onChanged,
    this.onSingleChanged,
    this.enabled = true,
    this.direction = Axis.horizontal,
    this.spacing = 8.0,
    this.padding,
    this.borderRadius = 8.0,
  });

  @override
  State<FilterBox> createState() => _FilterBoxState();
}

class _FilterBoxState extends State<FilterBox> {
  late List<String> _selectedIds;
  String? _selectedId;
  final Map<String, bool> _hoverStates = {};

  @override
  void initState() {
    super.initState();
    _selectedIds = List.from(widget.selectedIds);
    _selectedId = widget.selectedId;
  }

  @override
  void didUpdateWidget(FilterBox oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.selectedIds != oldWidget.selectedIds) {
      _selectedIds = List.from(widget.selectedIds);
    }
    if (widget.selectedId != oldWidget.selectedId) {
      _selectedId = widget.selectedId;
    }
  }

  void _handleOptionTap(String optionId) {
    if (!widget.enabled) return;

    setState(() {
      if (widget.type == FilterType.single) {
        // 하나만 선택 가능
        _selectedId = _selectedId == optionId ? null : optionId;
        widget.onSingleChanged?.call(_selectedId);
      } else {
        // 여러 개 선택 가능
        if (_selectedIds.contains(optionId)) {
          _selectedIds.remove(optionId);
        } else {
          _selectedIds.add(optionId);
        }
        widget.onChanged?.call(_selectedIds);
      }
    });
  }

  bool _isSelected(String optionId) {
    if (widget.type == FilterType.single) {
      return _selectedId == optionId;
    } else {
      return _selectedIds.contains(optionId);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (widget.title != null) ...[
          Text(
            widget.title!,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: AppColors.medicalDarkBlue,
            ),
          ),
          const SizedBox(height: 12),
        ],
        Padding(
          padding: widget.padding ?? EdgeInsets.zero,
          child: _buildFilterChips(),
        ),
      ],
    );
  }

  Widget _buildFilterChips() {
    final chips = widget.options.map((option) {
      final isSelected = _isSelected(option.id);
      final isHovered = _hoverStates[option.id] ?? false;
      final isDisabled = !widget.enabled || option.disabled;

      return _FilterChip(
        label: option.label,
        isSelected: isSelected,
        isHovered: isHovered,
        isDisabled: isDisabled,
        borderRadius: widget.borderRadius,
        onTap: () => _handleOptionTap(option.id),
        onHover: (hovered) {
          if (!isDisabled) {
            setState(() {
              _hoverStates[option.id] = hovered;
            });
          }
        },
      );
    }).toList();

    if (widget.direction == Axis.horizontal) {
      return Wrap(
        spacing: widget.spacing,
        runSpacing: widget.spacing,
        children: chips,
      );
    } else {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: chips
            .map((chip) => Padding(
                  padding: EdgeInsets.only(bottom: widget.spacing),
                  child: chip,
                ))
            .toList(),
      );
    }
  }
}

/// 필터 칩 위젯
class _FilterChip extends StatelessWidget {
  final String label;
  final bool isSelected;
  final bool isHovered;
  final bool isDisabled;
  final VoidCallback onTap;
  final ValueChanged<bool> onHover;
  final double borderRadius;

  const _FilterChip({
    required this.label,
    required this.isSelected,
    required this.isHovered,
    required this.isDisabled,
    required this.onTap,
    required this.onHover,
    required this.borderRadius,
  });

  /// X 아이콘 위젯
  Widget _buildCloseIcon() {
    return CustomPaint(
      size: const Size(16, 16),
      painter: _CloseIconPainter(
        color: isSelected ? Colors.white : AppColors.medicalLightBlueGray,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => onHover(true),
      onExit: (_) => onHover(false),
      child: InkWell(
        onTap: isDisabled ? null : onTap,
        borderRadius: BorderRadius.circular(borderRadius),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: EdgeInsets.symmetric(
            horizontal: isSelected ? 12 : 16,
            vertical: 10,
          ),
          decoration: BoxDecoration(
            color: _getBackgroundColor(),
            borderRadius: BorderRadius.circular(borderRadius),
            border: Border.all(
              color: _getBorderColor(),
              width: 1.5,
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                label,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                  color: _getTextColor(),
                ),
              ),
              if (isSelected && !isDisabled) ...[
                const SizedBox(width: 8),
                _buildCloseIcon(),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Color _getBackgroundColor() {
    if (isDisabled) {
      return AppColors.medicalOffWhite;
    }

    if (isSelected) {
      return AppColors.medicalDarkBlue;
    }

    if (isHovered) {
      return AppColors.medicalPaleBlue.withOpacity(0.3);
    }

    return Colors.white;
  }

  Color _getBorderColor() {
    if (isDisabled) {
      return AppColors.medicalPaleBlue;
    }

    if (isSelected) {
      return AppColors.medicalDarkBlue;
    }

    if (isHovered) {
      return AppColors.medicalBlueGray;
    }

    return AppColors.medicalLightBlueGray;
  }

  Color _getTextColor() {
    if (isDisabled) {
      return AppColors.medicalLightBlueGray;
    }

    if (isSelected) {
      return Colors.white;
    }

    return AppColors.medicalDarkBlue;
  }
}

/// X 아이콘 페인터
class _CloseIconPainter extends CustomPainter {
  final Color color;

  _CloseIconPainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 1.4
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..style = PaintingStyle.stroke;

    // X 아이콘 그리기
    // 왼쪽 위에서 오른쪽 아래로
    canvas.drawLine(
      Offset(3.5, 3.5),
      Offset(size.width - 3.5, size.height - 3.5),
      paint,
    );
    // 왼쪽 아래에서 오른쪽 위로
    canvas.drawLine(
      Offset(3.5, size.height - 3.5),
      Offset(size.width - 3.5, 3.5),
      paint,
    );
  }

  @override
  bool shouldRepaint(_CloseIconPainter oldDelegate) {
    return oldDelegate.color != color;
  }
}
