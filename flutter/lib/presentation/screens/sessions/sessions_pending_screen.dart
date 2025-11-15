import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 대기 중인 세션 목록 화면
class SessionsPendingScreen extends ConsumerWidget {
  const SessionsPendingScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('대기 중인 세션'),
      ),
      body: const Center(
        child: Text(
          '대기 중인 세션 화면',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}

