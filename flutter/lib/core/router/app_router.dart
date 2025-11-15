import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../presentation/providers/auth_provider.dart';
import '../../presentation/screens/auth/login_screen.dart';
import '../../presentation/screens/auth/signup_screen.dart';
import '../../presentation/screens/dashboard/dashboard_screen.dart';
import '../../presentation/screens/my_shop/my_shop_screen.dart';
import '../../presentation/screens/my_shop/my_shop_edit_screen.dart';
import '../../presentation/screens/customers/customers_screen.dart';
import '../../presentation/screens/customers/customer_new_screen.dart';
import '../../presentation/screens/customers/customer_detail_screen.dart';
import '../../presentation/screens/customers/customer_treatment_new_screen.dart';
import '../../presentation/screens/treatments/treatment_detail_screen.dart';
import '../../presentation/screens/treatments/treatment_session_new_screen.dart';
import '../../presentation/screens/sessions/sessions_screen.dart';
import '../../presentation/screens/sessions/sessions_pending_screen.dart';
import '../../presentation/screens/sessions/session_detail_screen.dart';
import '../../presentation/screens/sessions/session_edit_screen.dart';
import '../../presentation/screens/sessions/session_result_screen.dart';
import '../../presentation/screens/sessions/session_analysis_screen.dart';
import '../../presentation/screens/storybook/component_showcase_screen.dart';

final goRouterProvider = Provider<GoRouter>((ref) {
  // TODO: 개발 중 - 인증 상태 확인 비활성화
  // final authState = ref.watch(authStateProvider);
  
  return GoRouter(
    initialLocation: '/dashboard', // 개발 중 메인페이지로 시작
    // Web에서 해시 라우팅 제거 (/#/login -> /login)
    // go_router는 기본적으로 path-based URL을 사용하므로 추가 설정 불필요
    // TODO: 로그인 확인 로직 임시 주석처리 (개발 중)
    // redirect: (context, state) {
    //   final isLoggedIn = authState.isLoggedIn;
    //   final isGoingToLogin = state.matchedLocation == '/login';
    //   final isGoingToSignup = state.matchedLocation == '/signup';
    //   
    //   // 로그인 안 했는데 로그인/회원가입 페이지가 아니면 → 로그인으로
    //   if (!isLoggedIn && !isGoingToLogin && !isGoingToSignup) {
    //     return '/login';
    //   }
    //   
    //   // 로그인 했는데 로그인/회원가입 페이지 가려고 하면 → 대시보드로
    //   if (isLoggedIn && (isGoingToLogin || isGoingToSignup)) {
    //     return '/dashboard';
    //   }
    //   
    //   return null; // 그대로 진행
    // },
    routes: [
      // 인증 관련
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/signup',
        builder: (context, state) => const SignupScreen(),
      ),
      
      // 대시보드 (메인)
      GoRoute(
        path: '/dashboard',
        builder: (context, state) => const DashboardScreen(),
      ),
      
      // 마이페이지
      GoRoute(
        path: '/my-shop',
        builder: (context, state) => const MyShopScreen(),
        routes: [
          GoRoute(
            path: 'edit',
            builder: (context, state) => const MyShopEditScreen(),
          ),
        ],
      ),
      
      // 고객 관리
      GoRoute(
        path: '/customers',
        builder: (context, state) => const CustomersScreen(),
        routes: [
          GoRoute(
            path: 'new',
            builder: (context, state) => const CustomerNewScreen(),
          ),
          GoRoute(
            path: ':customerId',
            builder: (context, state) {
              final customerId = state.pathParameters['customerId']!;
              return CustomerDetailScreen(customerId: customerId);
            },
            routes: [
              GoRoute(
                path: 'treatments/new',
                builder: (context, state) {
                  final customerId = state.pathParameters['customerId']!;
                  return CustomerTreatmentNewScreen(customerId: customerId);
                },
              ),
            ],
          ),
        ],
      ),
      
      // 시술 관리
      GoRoute(
        path: '/treatments/:treatmentId',
        builder: (context, state) {
          final treatmentId = state.pathParameters['treatmentId']!;
          return TreatmentDetailScreen(treatmentId: treatmentId);
        },
        routes: [
          GoRoute(
            path: 'sessions/new',
            builder: (context, state) {
              final treatmentId = state.pathParameters['treatmentId']!;
              return TreatmentSessionNewScreen(treatmentId: treatmentId);
            },
          ),
        ],
      ),
      
      // 세션 관리
      GoRoute(
        path: '/sessions',
        builder: (context, state) => const SessionsScreen(),
        routes: [
          GoRoute(
            path: 'pending',
            builder: (context, state) => const SessionsPendingScreen(),
          ),
          GoRoute(
            path: ':sessionId',
            builder: (context, state) {
              final sessionId = state.pathParameters['sessionId']!;
              return SessionDetailScreen(sessionId: sessionId);
            },
            routes: [
              GoRoute(
                path: 'edit',
                builder: (context, state) {
                  final sessionId = state.pathParameters['sessionId']!;
                  return SessionEditScreen(sessionId: sessionId);
                },
              ),
              GoRoute(
                path: 'result',
                builder: (context, state) {
                  final sessionId = state.pathParameters['sessionId']!;
                  return SessionResultScreen(sessionId: sessionId);
                },
              ),
              GoRoute(
                path: 'analysis',
                builder: (context, state) {
                  final sessionId = state.pathParameters['sessionId']!;
                  return SessionAnalysisScreen(sessionId: sessionId);
                },
              ),
            ],
          ),
        ],
      ),
      
      // 기존 라우트 (하위 호환성) - 대시보드로 리다이렉트
      GoRoute(
        path: '/',
        redirect: (context, state) => '/dashboard',
      ),
      GoRoute(
        path: '/storybook',
        builder: (context, state) => const ComponentShowcaseScreen(),
      ),
    ],
  );
});