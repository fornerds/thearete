import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 시술 세션 등록 화면
class TreatmentSessionNewScreen extends ConsumerStatefulWidget {
  final String treatmentId;

  const TreatmentSessionNewScreen({
    super.key,
    required this.treatmentId,
  });

  @override
  ConsumerState<TreatmentSessionNewScreen> createState() =>
      _TreatmentSessionNewScreenState();
}

class _TreatmentSessionNewScreenState
    extends ConsumerState<TreatmentSessionNewScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('세션 등록'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              '세션 등록 화면',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 16),
            Text(
              '시술 ID: ${widget.treatmentId}',
              style: const TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}

