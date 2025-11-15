import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 고객 시술 등록 화면
class CustomerTreatmentNewScreen extends ConsumerStatefulWidget {
  final String customerId;

  const CustomerTreatmentNewScreen({
    super.key,
    required this.customerId,
  });

  @override
  ConsumerState<CustomerTreatmentNewScreen> createState() =>
      _CustomerTreatmentNewScreenState();
}

class _CustomerTreatmentNewScreenState
    extends ConsumerState<CustomerTreatmentNewScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('시술 등록'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              '시술 등록 화면',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 16),
            Text(
              '고객 ID: ${widget.customerId}',
              style: const TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}

