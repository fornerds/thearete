import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 고객 목록 화면
class CustomersScreen extends ConsumerWidget {
  const CustomersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('고객 목록'),
      ),
      body: const Center(
        child: Text(
          '고객 목록 화면',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}

