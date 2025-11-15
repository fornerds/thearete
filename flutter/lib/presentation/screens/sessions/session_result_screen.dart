import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 세션 결과 화면
class SessionResultScreen extends ConsumerStatefulWidget {
  final String sessionId;

  const SessionResultScreen({
    super.key,
    required this.sessionId,
  });

  @override
  ConsumerState<SessionResultScreen> createState() =>
      _SessionResultScreenState();
}

class _SessionResultScreenState extends ConsumerState<SessionResultScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('세션 결과'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              '세션 결과 화면',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 16),
            Text(
              '세션 ID: ${widget.sessionId}',
              style: const TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}

