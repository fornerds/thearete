import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 세션 목록 화면
class SessionsScreen extends ConsumerWidget {
  const SessionsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('세션 목록'),
      ),
      body: const Center(
        child: Text(
          '세션 목록 화면',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}

