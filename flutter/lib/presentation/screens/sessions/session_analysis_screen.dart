import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 세션 분석 화면
class SessionAnalysisScreen extends ConsumerWidget {
  final String sessionId;

  const SessionAnalysisScreen({
    super.key,
    required this.sessionId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('세션 분석'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              '세션 분석 화면',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 16),
            Text(
              '세션 ID: $sessionId',
              style: const TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}

