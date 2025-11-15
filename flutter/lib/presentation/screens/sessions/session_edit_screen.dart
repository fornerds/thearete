import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 세션 수정 화면
class SessionEditScreen extends ConsumerStatefulWidget {
  final String sessionId;

  const SessionEditScreen({
    super.key,
    required this.sessionId,
  });

  @override
  ConsumerState<SessionEditScreen> createState() => _SessionEditScreenState();
}

class _SessionEditScreenState extends ConsumerState<SessionEditScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('세션 수정'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              '세션 수정 화면',
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

