import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:thearete_clinic/presentation/widgets/common/pagination/custom_pagination.dart';

void main() {
  group('CustomPagination 위젯 테스트', () {
    testWidgets('페이지가 1개 이하면 표시되지 않아야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 1,
              totalPages: 1,
            ),
          ),
        ),
      );

      // 페이지네이션이 표시되지 않아야 함
      expect(find.byType(CustomPagination), findsOneWidget);
      expect(find.byIcon(Icons.first_page), findsNothing);
      expect(find.byIcon(Icons.chevron_left), findsNothing);
    });

    testWidgets('기본 페이지네이션 구조가 올바르게 표시되어야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 1,
              totalPages: 10,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      // 첫 페이지, 이전, 다음, 마지막 버튼이 표시되어야 함
      expect(find.byIcon(Icons.first_page), findsOneWidget);
      expect(find.byIcon(Icons.chevron_left), findsOneWidget);
      expect(find.byIcon(Icons.chevron_right), findsOneWidget);
      expect(find.byIcon(Icons.last_page), findsOneWidget);
      
      // 페이지 번호가 표시되어야 함
      expect(find.text('1'), findsWidgets);
    });

    testWidgets('현재 페이지가 첫 페이지일 때 이전 버튼이 비활성화되어야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 1,
              totalPages: 10,
            ),
          ),
        ),
      );

      // 이전 버튼과 첫 페이지 버튼이 비활성화되어야 함
      final prevButton = find.byIcon(Icons.chevron_left);
      final firstButton = find.byIcon(Icons.first_page);
      
      expect(prevButton, findsOneWidget);
      expect(firstButton, findsOneWidget);
      
      // 버튼을 탭해도 콜백이 호출되지 않아야 함 (비활성화 상태)
      await tester.tap(prevButton);
      await tester.pump();
    });

    testWidgets('현재 페이지가 마지막 페이지일 때 다음 버튼이 비활성화되어야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 10,
              totalPages: 10,
            ),
          ),
        ),
      );

      // 다음 버튼과 마지막 페이지 버튼이 비활성화되어야 함
      final nextButton = find.byIcon(Icons.chevron_right);
      final lastButton = find.byIcon(Icons.last_page);
      
      expect(nextButton, findsOneWidget);
      expect(lastButton, findsOneWidget);
    });

    testWidgets('페이지 번호를 탭하면 onPageChanged 콜백이 호출되어야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 1,
              totalPages: 10,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      // 페이지 번호 2를 찾아서 탭
      final page2Button = find.text('2');
      expect(page2Button, findsOneWidget);
      
      await tester.tap(page2Button);
      await tester.pump();
      
      expect(selectedPage, equals(2));
    });

    testWidgets('이전 버튼을 탭하면 이전 페이지로 이동해야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      final prevButton = find.byIcon(Icons.chevron_left);
      await tester.tap(prevButton);
      await tester.pump();
      
      expect(selectedPage, equals(4));
    });

    testWidgets('다음 버튼을 탭하면 다음 페이지로 이동해야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      final nextButton = find.byIcon(Icons.chevron_right);
      await tester.tap(nextButton);
      await tester.pump();
      
      expect(selectedPage, equals(6));
    });

    testWidgets('첫 페이지 버튼을 탭하면 첫 페이지로 이동해야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      final firstButton = find.byIcon(Icons.first_page);
      await tester.tap(firstButton);
      await tester.pump();
      
      expect(selectedPage, equals(1));
    });

    testWidgets('마지막 페이지 버튼을 탭하면 마지막 페이지로 이동해야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      final lastButton = find.byIcon(Icons.last_page);
      await tester.tap(lastButton);
      await tester.pump();
      
      expect(selectedPage, equals(10));
    });

    testWidgets('많은 페이지가 있을 때 생략 표시(...)가 나타나야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 20,
            ),
          ),
        ),
      );

      // 생략 표시가 나타나야 함
      expect(find.text('...'), findsWidgets);
    });

    testWidgets('showFirstLast가 false이면 첫/마지막 버튼이 표시되지 않아야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              showFirstLast: false,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.first_page), findsNothing);
      expect(find.byIcon(Icons.last_page), findsNothing);
      expect(find.byIcon(Icons.chevron_left), findsOneWidget);
      expect(find.byIcon(Icons.chevron_right), findsOneWidget);
    });

    testWidgets('showPrevNext가 false이면 이전/다음 버튼이 표시되지 않아야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              showPrevNext: false,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.chevron_left), findsNothing);
      expect(find.byIcon(Icons.chevron_right), findsNothing);
      expect(find.byIcon(Icons.first_page), findsOneWidget);
      expect(find.byIcon(Icons.last_page), findsOneWidget);
    });

    testWidgets('enabled가 false이면 모든 버튼이 비활성화되어야 함', (WidgetTester tester) async {
      int? selectedPage;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 10,
              enabled: false,
              onPageChanged: (page) => selectedPage = page,
            ),
          ),
        ),
      );

      // 버튼을 탭해도 콜백이 호출되지 않아야 함
      final nextButton = find.byIcon(Icons.chevron_right);
      await tester.tap(nextButton);
      await tester.pump();
      
      expect(selectedPage, isNull);
    });

    testWidgets('현재 페이지가 하이라이트되어야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 3,
              totalPages: 10,
            ),
          ),
        ),
      );

      // 현재 페이지 번호가 표시되어야 함
      final currentPageText = find.text('3');
      expect(currentPageText, findsOneWidget);
    });

    testWidgets('maxVisiblePages에 따라 표시되는 페이지 수가 제한되어야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 5,
              totalPages: 20,
              maxVisiblePages: 3,
            ),
          ),
        ),
      );

      // maxVisiblePages보다 많은 페이지 번호가 직접 표시되지 않아야 함
      // 생략 표시가 나타나야 함
      expect(find.text('...'), findsWidgets);
    });

    testWidgets('페이지가 적을 때는 모든 페이지 번호가 표시되어야 함', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomPagination(
              currentPage: 1,
              totalPages: 5,
            ),
          ),
        ),
      );

      // 모든 페이지 번호가 표시되어야 함
      for (int i = 1; i <= 5; i++) {
        expect(find.text(i.toString()), findsOneWidget);
      }
      
      // 생략 표시가 없어야 함
      expect(find.text('...'), findsNothing);
    });
  });

  group('CustomPagination 엣지 케이스 테스트', () {
    test('currentPage가 totalPages보다 크면 assertion 에러가 발생해야 함', () {
      expect(
        () {
          // const 생성자에서는 컴파일 타임에 assertion이 체크되므로
          // 동적으로 생성하여 테스트
          CustomPagination(
            currentPage: 11,
            totalPages: 10,
          );
        },
        throwsAssertionError,
      );
    });

    test('currentPage가 0 이하면 assertion 에러가 발생해야 함', () {
      expect(
        () {
          CustomPagination(
            currentPage: 0,
            totalPages: 10,
          );
        },
        throwsAssertionError,
      );
    });

    test('totalPages가 0 이하면 assertion 에러가 발생해야 함', () {
      expect(
        () {
          CustomPagination(
            currentPage: 1,
            totalPages: 0,
          );
        },
        throwsAssertionError,
      );
    });

    test('maxVisiblePages가 0 이하면 assertion 에러가 발생해야 함', () {
      expect(
        () {
          CustomPagination(
            currentPage: 1,
            totalPages: 10,
            maxVisiblePages: 0,
          );
        },
        throwsAssertionError,
      );
    });
  });
}

