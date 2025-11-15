import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_web_plugins/flutter_web_plugins.dart';

import 'core/di/injection.dart';
import 'core/router/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Web에서 해시 라우팅 제거 (/#/login -> /login)
  if (kIsWeb) {
    usePathUrlStrategy();
  }
  
  // Hive 초기화
  await Hive.initFlutter();
  
  // 의존성 주입 설정
  await setupDependencies();
  
  runApp(
    const ProviderScope(
      child: TheAreteApp(),
    ),
  );
}

class TheAreteApp extends ConsumerWidget {
  const TheAreteApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(goRouterProvider);
    
    return MaterialApp.router(
      title: 'TheArete Clinic',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      routerConfig: router,
    );
  }
}