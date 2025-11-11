import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:thearete_clinic/presentation/widgets/common/inputs/custom_select_field.dart';

void main() {
  group('CustomSelectField 위젯 테스트', () {
    testWidgets('기본 Select Field가 올바르게 표시되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
        SelectOption(value: 'option2', label: '옵션 2'),
        SelectOption(value: 'option3', label: '옵션 3'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              labelText: '선택',
              options: options,
            ),
          ),
        ),
      );

      // 라벨이 표시되어야 함
      expect(find.text('선택'), findsOneWidget);
      
      // 드롭다운 버튼이 표시되어야 함
      expect(find.byType(DropdownButtonFormField<String>), findsOneWidget);
    });

    testWidgets('필수 필드일 때 별표가 표시되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              labelText: '선택',
              isRequired: true,
              options: options,
            ),
          ),
        ),
      );

      // 별표가 표시되어야 함
      expect(find.text('*'), findsOneWidget);
    });

    testWidgets('값이 선택되면 해당 값이 표시되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
        SelectOption(value: 'option2', label: '옵션 2'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              value: 'option1',
              options: options,
            ),
          ),
        ),
      );

      // 선택된 값의 라벨이 표시되어야 함
      expect(find.text('옵션 1'), findsWidgets);
    });

    testWidgets('onChanged 콜백이 올바르게 호출되어야 함', (WidgetTester tester) async {
      String? selectedValue;
      
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
        SelectOption(value: 'option2', label: '옵션 2'),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
              onChanged: (value) => selectedValue = value,
            ),
          ),
        ),
      );

      // 드롭다운을 탭하여 열기
      await tester.tap(find.byType(DropdownButtonFormField<String>));
      await tester.pumpAndSettle();

      // 옵션을 선택
      await tester.tap(find.text('옵션 2').last);
      await tester.pumpAndSettle();

      expect(selectedValue, equals('option2'));
    });

    testWidgets('비활성화된 옵션이 올바르게 생성되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
        SelectOption(value: 'option2', label: '옵션 2', disabled: true),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
            ),
          ),
        ),
      );

      // 드롭다운이 표시되어야 함
      expect(find.byType(DropdownButtonFormField<String>), findsOneWidget);
      
      // 비활성화된 옵션이 포함된 컴포넌트가 생성되어야 함
      expect(find.byType(CustomSelectField<String>), findsOneWidget);
    });

    testWidgets('enabled가 false이면 드롭다운이 비활성화되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
              enabled: false,
            ),
          ),
        ),
      );

      // 드롭다운이 비활성화되어 있어야 함
      final dropdown = tester.widget<DropdownButtonFormField<String>>(
        find.byType(DropdownButtonFormField<String>),
      );
      expect(dropdown.onChanged, isNull);
    });

    testWidgets('에러 텍스트가 표시되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
              errorText: '필수 항목입니다',
            ),
          ),
        ),
      );

      // 에러 텍스트가 표시되어야 함
      expect(find.text('필수 항목입니다'), findsOneWidget);
    });

    testWidgets('힌트 텍스트가 표시되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
              hintText: '옵션을 선택하세요',
            ),
          ),
        ),
      );

      // 힌트 텍스트가 표시되어야 함
      expect(find.text('옵션을 선택하세요'), findsOneWidget);
    });

    testWidgets('헬퍼 텍스트가 표시되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
              helperText: '도움말 텍스트',
            ),
          ),
        ),
      );

      // 헬퍼 텍스트가 표시되어야 함
      expect(find.text('도움말 텍스트'), findsOneWidget);
    });

    testWidgets('FormFieldValidator가 올바르게 작동해야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: 'option1', label: '옵션 1'),
      ];

      final formKey = GlobalKey<FormState>();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Form(
              key: formKey,
              child: CustomSelectField<String>(
                options: options,
                validator: (value) {
                  if (value == null) {
                    return '값을 선택해주세요';
                  }
                  return null;
                },
              ),
            ),
          ),
        ),
      );

      // 폼 검증 실행
      formKey.currentState!.validate();
      await tester.pump();

      // 에러 메시지가 표시되어야 함
      expect(find.text('값을 선택해주세요'), findsOneWidget);
    });

    testWidgets('여러 옵션이 있을 때 모두 생성되어야 함', (WidgetTester tester) async {
      const options = [
        SelectOption(value: '1', label: '옵션 1'),
        SelectOption(value: '2', label: '옵션 2'),
        SelectOption(value: '3', label: '옵션 3'),
        SelectOption(value: '4', label: '옵션 4'),
        SelectOption(value: '5', label: '옵션 5'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CustomSelectField<String>(
              options: options,
            ),
          ),
        ),
      );

      // 드롭다운이 표시되어야 함
      expect(find.byType(DropdownButtonFormField<String>), findsOneWidget);
      
      // 컴포넌트가 올바르게 생성되어야 함
      expect(find.byType(CustomSelectField<String>), findsOneWidget);
    });
  });

  group('SelectOption 모델 테스트', () {
    test('SelectOption이 올바르게 생성되어야 함', () {
      const option = SelectOption(
        value: 'test',
        label: '테스트',
        disabled: false,
      );

      expect(option.value, equals('test'));
      expect(option.label, equals('테스트'));
      expect(option.disabled, isFalse);
    });

    test('SelectOption의 기본값이 올바르게 설정되어야 함', () {
      const option = SelectOption(
        value: 'test',
        label: '테스트',
      );

      expect(option.disabled, isFalse);
    });
  });
}

