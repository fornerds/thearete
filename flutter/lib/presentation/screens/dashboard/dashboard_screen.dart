import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_assets.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/constants/app_icons.dart';
import '../../widgets/common/buttons/primary_button.dart';
import '../../widgets/common/cards/customer_card.dart';
import '../../widgets/common/icons/custom_icon.dart';
import '../../widgets/common/inputs/custom_select_field.dart';

/// 대시보드 화면 (메인)
class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  // 정렬 옵션
  String? _sortOption = 'recent';
  final List<SelectOption<String>> _sortOptions = [
    const SelectOption(value: 'recent', label: '최근 업데이트 순'),
    const SelectOption(value: 'date', label: '날짜 순'),
    const SelectOption(value: 'name', label: '가나다 순'),
  ];

  // 임시 데이터 (나중에 API로 대체)
  final String _shopName = '더아레테 클리닉';
  final int _ongoingTreatments = 5;
  final int _pendingRetreatments = 3;
  final int _totalCustomers = 12;
  final int _pendingResults = 3; // 시술 결과 미입력 건수

  // 임시 고객 데이터
  final List<Map<String, dynamic>> _customers = [
    {
      'id': 1,
      'name': '홍길동',
      'gender': 'M',
      'age': 30,
      'treatmentName': '리프팅',
      'additionalTreatments': 2,
      'isPinned': true,
    },
    {
      'id': 2,
      'name': '김영희',
      'gender': 'F',
      'age': 28,
      'treatmentName': '보톡스',
      'additionalTreatments': 0,
      'isPinned': true,
    },
    {
      'id': 3,
      'name': '이철수',
      'gender': 'M',
      'age': 35,
      'treatmentName': '필러',
      'additionalTreatments': 1,
      'isPinned': false,
    },
    {
      'id': 4,
      'name': '박민수',
      'gender': 'M',
      'age': 42,
      'treatmentName': '히알루론산',
      'additionalTreatments': 3,
      'isPinned': false,
    },
    {
      'id': 5,
      'name': '최지은',
      'gender': 'F',
      'age': 25,
      'treatmentName': '레이저',
      'additionalTreatments': 0,
      'isPinned': false,
    },
    {
      'id': 6,
      'name': '정수진',
      'gender': 'F',
      'age': 33,
      'treatmentName': '보톡스',
      'additionalTreatments': 1,
      'isPinned': true,
    },
    {
      'id': 7,
      'name': '강동원',
      'gender': 'M',
      'age': 38,
      'treatmentName': '리프팅',
      'additionalTreatments': 0,
      'isPinned': false,
    },
    {
      'id': 8,
      'name': '윤서아',
      'gender': 'F',
      'age': 29,
      'treatmentName': '필러',
      'additionalTreatments': 2,
      'isPinned': false,
    },
    {
      'id': 9,
      'name': '조성민',
      'gender': 'M',
      'age': 45,
      'treatmentName': '히알루론산',
      'additionalTreatments': 1,
      'isPinned': false,
    },
    {
      'id': 10,
      'name': '한소희',
      'gender': 'F',
      'age': 27,
      'treatmentName': '보톡스',
      'additionalTreatments': 0,
      'isPinned': false,
    },
    {
      'id': 11,
      'name': '송태현',
      'gender': 'M',
      'age': 31,
      'treatmentName': '레이저',
      'additionalTreatments': 2,
      'isPinned': false,
    },
    {
      'id': 12,
      'name': '임지연',
      'gender': 'F',
      'age': 36,
      'treatmentName': '리프팅',
      'additionalTreatments': 1,
      'isPinned': false,
    },
  ];

  void _handlePinToggle(int customerId, bool isPinned) {
    setState(() {
      final index = _customers.indexWhere((c) => c['id'] == customerId);
      if (index != -1) {
        _customers[index]['isPinned'] = isPinned;
        // 고정된 항목을 맨 위로 이동
        if (isPinned) {
          final customer = _customers.removeAt(index);
          _customers.insert(0, customer);
        } else {
          // 고정 해제된 항목을 정렬에 따라 재배치
          _sortCustomers();
        }
      }
    });
  }

  void _sortCustomers() {
    switch (_sortOption) {
      case 'recent':
        // 최근 업데이트 순 (임시로 ID 순)
        _customers.sort((a, b) => (b['id'] as int).compareTo(a['id'] as int));
        break;
      case 'date':
        // 날짜 순 (임시로 ID 순)
        _customers.sort((a, b) => (a['id'] as int).compareTo(b['id'] as int));
        break;
      case 'name':
        // 가나다 순
        _customers.sort((a, b) => (a['name'] as String).compareTo(b['name'] as String));
        break;
    }
    // 고정된 항목을 맨 위로
    _customers.sort((a, b) {
      if (a['isPinned'] == true && b['isPinned'] != true) return -1;
      if (a['isPinned'] != true && b['isPinned'] == true) return 1;
      return 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.grayScaleBackground,
      body: SafeArea(
        child: Column(
          children: [
            // 상단 헤더 (로고 + 검색 버튼)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // 로고
                  Image.asset(
                    AppAssets.logo,
                    height: 32,
                    fit: BoxFit.contain,
                    errorBuilder: (context, error, stackTrace) {
                      return const Text(
                        '로고',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w700,
                          color: AppColors.grayScaleText,
                        ),
                      );
                    },
                  ),
                  // 검색 버튼
                  IconButton(
                    icon: CustomIcon(
                      icon: AppIcons.search,
                      size: 21,
                      color: AppColors.grayScaleText,
                    ),
                    onPressed: () {
                      // TODO: 검색 기능 구현
                    },
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                    tooltip: '검색',
                  ),
                ],
              ),
            ),
            // 스크롤 가능한 컨텐츠
            Expanded(
              child: SingleChildScrollView(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 8),
                      // 인사말 + 샵 이름 + 이동 버튼
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // "반갑습니다!" 텍스트
                          Text(
                            '반갑습니다!',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                              color: AppColors.grayScaleSubText1,
                              height: 1.35,
                            ),
                          ),
                          const SizedBox(height: 2),
                          // 상점 이름 + 화살표 (링크)
                          InkWell(
                            onTap: () {
                              context.push('/my-shop');
                            },
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                // 상점 이름 + "님"
                                Text.rich(
                                  TextSpan(
                                    children: [
                                      TextSpan(
                                        text: _shopName,
                                        style: TextStyle(
                                          fontSize: 24,
                                          fontWeight: FontWeight.w700,
                                          color: AppColors.grayScaleBlack,
                                          height: 1.5,
                                        ),
                                      ),
                                      TextSpan(
                                        text: '님',
                                        style: TextStyle(
                                          fontSize: 24,
                                          fontWeight: FontWeight.w500,
                                          color: AppColors.grayScaleSubText2,
                                          height: 1.5,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(width: 12), // 간격 증가 (4 -> 12)
                                // 화살표 아이콘
                                CustomIcon(
                                  icon: AppIcons.arrowRightSmall,
                                  size: 14,
                                  color: AppColors.grayScaleSubText2,
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),
                      // 통계 카드 (진행중인 시술, 재시술 대기 고객)
                      Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4),
                        child: IntrinsicHeight(
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              _StatCard(
                                title: '진행중인 시술',
                                count: _ongoingTreatments,
                                onTap: () {
                                  // TODO: 진행중인 시술 페이지로 이동
                                  context.push('/sessions');
                                },
                              ),
                              const SizedBox(width: 12), // 간격 증가 (6 -> 12)
                              // 구분선
                              Container(
                                width: 1,
                                height: double.infinity,
                                color: AppColors.grayScaleLine,
                              ),
                              const SizedBox(width: 12), // 간격 증가 (6 -> 12)
                              _StatCard(
                                title: '재시술 대기 고객',
                                count: _pendingRetreatments,
                                onTap: () {
                                  // TODO: 재시술 대기 페이지로 이동
                                  context.push('/sessions/pending');
                                },
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 24),
                      // 가로선
                      Container(
                        height: 1,
                        color: AppColors.grayScaleLineWeak,
                      ),
                      const SizedBox(height: 24),
                      // 신규 고객 등록하기 버튼
                      SizedBox(
                        width: double.infinity,
                        child: InkWell(
                          onTap: () {
                            context.push('/customers/new');
                          },
                          child: Padding(
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                // 플러스 아이콘
                                CustomIcon(
                                  icon: AppIcons.plusMedium,
                                  size: 20,
                                  color: AppColors.grayScaleSubText1,
                                ),
                                const SizedBox(width: 11),
                                // 텍스트
                                Text(
                                  '신규 고객 등록하기',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                    color: AppColors.grayScaleSubText1,
                                    height: 1.35, // 135%
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      // 진행중인 시술 버튼
                      SizedBox(
                        width: double.infinity,
                        child: InkWell(
                          onTap: () {
                            context.push('/sessions');
                          },
                          borderRadius: BorderRadius.circular(8),
                          child: Container(
                            height: 54,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 14,
                              vertical: 16,
                            ),
                            decoration: BoxDecoration(
                              color: AppColors.keyColor1,
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: AppColors.keyColor3,
                                width: 1,
                              ),
                            ),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                // 점 애니메이션과 텍스트
                                Expanded(
                                  flex: 1,
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    crossAxisAlignment: CrossAxisAlignment.center,
                                    children: [
                                      // 점 애니메이션
                                      SizedBox(
                                        width: 30,
                                        child: Center(
                                          child: _LoadingDots(),
                                        ),
                                      ),
                                      const SizedBox(width: 12),
                                      // 텍스트
                                      Align(
                                        alignment: Alignment.center,
                                        child: Text(
                                          '진행중인 시술',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.w700,
                                            height: 1.0, // line-height를 1.0으로 조정하여 정확한 정렬
                                            color: AppColors.keyColor3,
                                          ),
                                          textAlign: TextAlign.center,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                // 오른쪽 화살표 아이콘
                                CustomIcon(
                                  icon: AppIcons.arrowRightSmallDark,
                                  width: 6,
                                  height: 10,
                                  color: AppColors.medicalDarkBlue,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      // 시술 결과 미입력 버튼
                      SizedBox(
                        width: double.infinity,
                        child: InkWell(
                          onTap: () {
                            // TODO: 시술 결과 미입력 페이지로 이동
                            context.push('/sessions');
                          },
                          borderRadius: BorderRadius.circular(8),
                          child: Container(
                            height: 68,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 14,
                              vertical: 15.5, // vertical padding을 0.5px 줄여서 공간 확보
                            ),
                            decoration: BoxDecoration(
                              color: AppColors.grayScaleBackground,
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: AppColors.grayScaleLine,
                                width: 1,
                              ),
                            ),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                // 왼쪽: 아이콘과 텍스트
                                Row(
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    // announce 아이콘
                                    CustomIcon(
                                      icon: AppIcons.announce,
                                      size: 30,
                                    ),
                                    const SizedBox(width: 12),
                                    // 텍스트 (두 줄)
                                    Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Text(
                                          '시술 결과 미입력',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.w700,
                                            height: 1.15, // line-height 조정
                                            color: AppColors.grayScaleText,
                                          ),
                                        ),
                                        Text(
                                          '시술 결과 미입력 $_pendingResults건있어요!',
                                          style: TextStyle(
                                            fontSize: 12,
                                            fontWeight: FontWeight.w600,
                                            height: 1.15, // line-height 조정
                                            color: AppColors.grayScaleSubText3,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                                // 오른쪽: 화살표 아이콘
                                CustomIcon(
                                  icon: AppIcons.arrowRightSmallLight,
                                  size: 10,
                                  color: AppColors.grayScaleGuideText,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 32),
                      // 누적고객 헤더
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.baseline,
                            textBaseline: TextBaseline.alphabetic,
                            children: [
                              Text(
                                '누적고객',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w700,
                                  color: AppColors.grayScaleText,
                                  height: 1.35,
                                ),
                              ),
                              const SizedBox(width: 4),
                              Text(
                                '$_totalCustomers',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w700,
                                  color: AppColors.keyColor3,
                                  height: 1.35,
                                ),
                              ),
                            ],
                          ),
                          // 정렬 필터
                          CustomSelectField<String>(
                            value: _sortOption,
                            options: _sortOptions,
                            onChanged: (value) {
                              setState(() {
                                _sortOption = value;
                                _sortCustomers();
                              });
                            },
                            borderRadius: 99,
                            isCompact: true,
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      // 고객 카드 리스트
                      ..._customers.asMap().entries.expand((entry) {
                        final index = entry.key;
                        final customer = entry.value;
                        final isLast = index == _customers.length - 1;
                        
                        return [
                          CustomerCard(
                            name: customer['name'] as String,
                            gender: customer['gender'] as String?,
                            age: customer['age'] as int?,
                            treatmentName: customer['treatmentName'] as String?,
                            additionalTreatments: customer['additionalTreatments'] as int,
                            isPinned: customer['isPinned'] as bool,
                            onPinToggle: (pinned) {
                              _handlePinToggle(customer['id'] as int, pinned);
                            },
                            onTap: () {
                              context.push('/customers/${customer['id']}');
                            },
                          ),
                          if (!isLast)
                            Container(
                              height: 1,
                              color: AppColors.grayScaleLineWeak,
                            ),
                        ];
                      }),
                      const SizedBox(height: 24),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// 점 애니메이션 위젯
class _LoadingDots extends StatefulWidget {
  const _LoadingDots();

  @override
  State<_LoadingDots> createState() => _LoadingDotsState();
}

class _LoadingDotsState extends State<_LoadingDots>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1200),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: List.generate(3, (index) {
        return Padding(
          padding: EdgeInsets.only(right: index < 2 ? 4 : 0),
          child: AnimatedBuilder(
            animation: _controller,
            builder: (context, child) {
              // 각 점의 opacity를 순환시키기 (0.3 -> 0.6 -> 1.0 -> 0.3)
              final delay = index * 0.33; // 각 점마다 1/3씩 지연
              final cycle = (_controller.value + delay) % 1.0;
              
              // 부드러운 opacity 전환
              double opacity;
              if (cycle < 0.5) {
                // 0.3 -> 1.0
                opacity = 0.3 + (cycle / 0.5) * 0.7;
              } else {
                // 1.0 -> 0.3
                opacity = 1.0 - ((cycle - 0.5) / 0.5) * 0.7;
              }

              return Opacity(
                opacity: opacity.clamp(0.3, 1.0),
                child: CustomIcon(
                  icon: AppIcons.dotLoading,
                  size: 6,
                  color: AppColors.keyColor3,
                ),
              );
            },
          ),
        );
      }),
    );
  }
}

/// 통계 카드 위젯
class _StatCard extends StatelessWidget {
  final String title;
  final int count;
  final VoidCallback? onTap;

  const _StatCard({
    required this.title,
    required this.count,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(8),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.baseline,
        textBaseline: TextBaseline.alphabetic,
        children: [
          // 제목 텍스트
          Text(
            title,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w500,
              color: AppColors.grayScaleSubText1,
              height: 1.6, // 160%
            ),
          ),
          const SizedBox(width: 6),
          // 숫자 (텍스트와 baseline에 맞춰 정렬)
          Text(
            '$count',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: AppColors.keyColor3,
              height: 1.35, // 135%
            ),
          ),
        ],
      ),
    );
  }
}
