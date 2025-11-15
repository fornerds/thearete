import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// 마이페이지 화면
class MyShopScreen extends ConsumerWidget {
  const MyShopScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('마이페이지'),
      ),
      body: const Center(
        child: Text(
          '마이페이지 화면',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}

