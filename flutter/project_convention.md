📋 프로젝트 개요
앱 종류: 클리닉 고객/시술 관리 앱
규모: 중대형 (15-16개 화면)
개발자 배경: React 웹 개발 경험
작업 위치: 프로젝트루트/flutter/ 폴더

🏗️ 아키텍처
패턴: Clean Architecture + MVVM
레이어 구조:
Presentation (UI + ViewModel)
↕ Riverpod
Domain (UseCase + Entity)
↕ get_it
Data (Repository + DataSource)
↕ http, Hive

🔧 기술 스택
용도라이브러리버전상태 관리flutter_riverpod^2.5.1의존성 주입get_it^7.6.7라우팅go_router^13.2.0로컬 저장소hive, hive_flutter^2.2.3네트워크http^1.2.0권한 관리permission_handler^11.3.0유틸리티equatable, dartz-

📁 폴더 구조
flutter/lib/
├── main.dart
├── core/
│   ├── di/injection.dart           # get_it 설정
│   ├── router/app_router.dart      # go_router 라우트
│   ├── constants/
│   └── utils/
├── data/                           # Data Layer
│   ├── datasources/
│   │   ├── remote/                 # API (http)
│   │   └── local/                  # Hive
│   ├── models/                     # DTO
│   └── repositories/               # Repository 구현
├── domain/                         # Domain Layer
│   ├── entities/                   # 비즈니스 모델
│   ├── repositories/               # Repository 인터페이스
│   └── usecases/                   # 비즈니스 로직
└── presentation/                   # Presentation Layer
├── providers/                  # Riverpod Providers
├── viewmodels/                 # StateNotifier
├── screens/                    # 화면
│   ├── auth/
│   │   ├── login_screen.dart
│   │   └── widgets/            # 화면 전용 위젯
│   ├── clients/
│   │   ├── client_list_screen.dart
│   │   ├── client_detail_screen.dart
│   │   └── widgets/
│   └── procedures/
└── widgets/                    # 공통 재사용 위젯
    ├── common/                 # 범용 컴포넌트
    │   ├── buttons/
    │   ├── inputs/
    │   ├── cards/
    │   └── indicators/
    └── layout/                 # 레이아웃 컴포넌트

🎯 코딩 규칙
1. 레이어 의존성 방향
   Presentation → Domain ← Data
   (Domain은 다른 레이어에 의존하지 않음)
2. 파일 명명 규칙
   dart// Entity
   class Client { }  // client.dart

// Model (DTO)
class ClientModel { }  // client_model.dart

// Repository Interface
abstract class ClientRepository { }  // client_repository.dart

// Repository Implementation
class ClientRepositoryImpl implements ClientRepository { }  // client_repository_impl.dart

// UseCase
class GetClientsUseCase { }  // get_clients_usecase.dart

// ViewModel
class ClientViewModel extends StateNotifier<ClientState> { }  // client_viewmodel.dart

// Screen
class ClientDetailScreen extends ConsumerWidget { }  // client_detail_screen.dart
3. Provider 정의 위치

ViewModel Provider: presentation/providers/ 폴더
UseCase Provider: UseCase 파일 내부에 함께 정의
Repository Provider: Repository 구현 파일 내부에 함께 정의

4. 상태 관리 패턴
   dart// 1. State 정의 (freezed 스타일 또는 일반 클래스)
   class ClientState {
   final bool isLoading;
   final List<Client>? clients;
   final String? errorMessage;
   }

// 2. ViewModel (StateNotifier)
class ClientViewModel extends StateNotifier<ClientState> {
final GetClientsUseCase getClientsUseCase;

ClientViewModel(this.getClientsUseCase) : super(ClientState());

Future<void> loadClients() async {
state = state.copyWith(isLoading: true);
final result = await getClientsUseCase.execute();
// ... 상태 업데이트
}
}

// 3. Provider 정의
final clientViewModelProvider = StateNotifierProvider<ClientViewModel, ClientState>(
(ref) => ClientViewModel(ref.read(getClientsUseCaseProvider)),
);

// 4. 화면에서 사용
class ClientListScreen extends ConsumerWidget {
@override
Widget build(BuildContext context, WidgetRef ref) {
final state = ref.watch(clientViewModelProvider);

    if (state.isLoading) return LoadingWidget();
    if (state.errorMessage != null) return ErrorWidget(state.errorMessage);
    return ListView(...);
}
}
5. API 호출 패턴
   dart// DataSource (http 사용)
   class ClientRemoteDataSource {
   final http.Client client;
   static const baseUrl = 'http://localhost:3000/api';

Future<List<ClientModel>> getClients() async {
final token = getIt<HiveService>().getToken();
final response = await client.get(
Uri.parse('$baseUrl/clients'),
headers: {
'Content-Type': 'application/json',
'Authorization': 'Bearer $token',
},
);

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => ClientModel.fromJson(json)).toList();
    } else {
      throw ServerException();
    }
}
}
6. 라우팅 패턴
   dart// app_router.dart
   final goRouter = GoRouter(
   initialLocation: '/login',
   routes: [
   GoRoute(
   path: '/login',
   builder: (context, state) => const LoginScreen(),
   ),
   GoRoute(
   path: '/clients/:id',
   builder: (context, state) {
   final clientId = state.pathParameters['id']!;
   return ClientDetailScreen(clientId: clientId);
   },
   ),
   ],
   redirect: (context, state) {
   // 로그인 체크 로직
   final isLoggedIn = /* Hive에서 토큰 확인 */;
   if (!isLoggedIn && state.matchedLocation != '/login') {
   return '/login';
   }
   return null;
   },
   );

// 화면 이동
context.go('/clients/$clientId');
context.push('/procedures/new');

🎨 위젯 구조 및 컴포넌트 패턴
컴포넌트 구조 전략
Feature-based + Component-based 하이브리드 방식 사용
- 공통 컴포넌트: widgets/common/ (2개 이상 화면에서 사용)
- 화면 전용 컴포넌트: screens/{feature}/widgets/ (특정 화면에서만 사용)
- 레이아웃 컴포넌트: widgets/layout/ (앱 전체 레이아웃)

왜 완전한 아토믹 디자인을 사용하지 않는가?
- 혼자 개발 시 과도한 추상화는 오히려 생산성을 떨어뜨림
- Flutter의 위젯 트리 특성상 atoms/molecules 구분이 모호함
- 필요할 때만 컴포넌트를 분리하는 실용적 접근이 더 효율적

위젯 분리 기준
1. 공통 컴포넌트로 분리하는 경우
   - 2개 이상의 화면에서 사용
   - 재사용 가능한 UI 패턴 (버튼, 입력 필드, 카드 등)
   - 앱 전체에서 일관된 스타일이 필요한 경우

2. 화면 전용 위젯으로 분리하는 경우
   - 특정 화면에서만 사용하지만 복잡한 로직을 가진 경우
   - Screen 파일이 200줄 이상이 될 때
   - 테스트를 위해 분리하고 싶은 경우

3. 인라인으로 작성하는 경우
   - 한 번만 사용되는 간단한 위젯
   - Screen 파일이 150줄 이하인 경우

위젯 작성 패턴
dart// 1. 공통 버튼 컴포넌트 (widgets/common/buttons/primary_button.dart)
class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final double? width;

  const PrimaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.width,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: isLoading
            ? const SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : Text(text),
      ),
    );
  }
}

// 2. 화면 전용 위젯 (screens/auth/widgets/login_form.dart)
class LoginForm extends StatelessWidget {
  final GlobalKey<FormState> formKey;
  final TextEditingController emailController;
  final TextEditingController passwordController;
  final bool obscurePassword;
  final VoidCallback onTogglePasswordVisibility;
  final VoidCallback onLogin;

  const LoginForm({
    super.key,
    required this.formKey,
    required this.emailController,
    required this.passwordController,
    required this.obscurePassword,
    required this.onTogglePasswordVisibility,
    required this.onLogin,
  });

  @override
  Widget build(BuildContext context) {
    return Form(
      key: formKey,
      child: Column(
        children: [
          TextFormField(
            controller: emailController,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
              labelText: '이메일',
              prefixIcon: Icon(Icons.email),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '이메일을 입력해주세요';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: passwordController,
            obscureText: obscurePassword,
            decoration: InputDecoration(
              labelText: '비밀번호',
              prefixIcon: const Icon(Icons.lock),
              suffixIcon: IconButton(
                icon: Icon(
                  obscurePassword ? Icons.visibility : Icons.visibility_off,
                ),
                onPressed: onTogglePasswordVisibility,
              ),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '비밀번호를 입력해주세요';
              }
              return null;
            },
          ),
          const SizedBox(height: 24),
          PrimaryButton(
            text: '로그인',
            onPressed: onLogin,
          ),
        ],
      ),
    );
  }
}

// 3. Screen에서 사용 (screens/auth/login_screen.dart)
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() {
    if (_formKey.currentState!.validate()) {
      ref.read(authStateProvider.notifier).login(
            _emailController.text.trim(),
            _passwordController.text,
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authStateProvider);

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: LoginForm(
            formKey: _formKey,
            emailController: _emailController,
            passwordController: _passwordController,
            obscurePassword: _obscurePassword,
            onTogglePasswordVisibility: () {
              setState(() {
                _obscurePassword = !_obscurePassword;
              });
            },
            onLogin: _handleLogin,
          ),
        ),
      ),
    );
  }
}

위젯 파일 명명 규칙
- 공통 컴포넌트: snake_case (예: primary_button.dart, custom_text_field.dart)
- 화면 전용 위젯: snake_case (예: login_form.dart, client_card.dart)
- 위젯 클래스명: PascalCase (예: PrimaryButton, LoginForm)

권장 공통 컴포넌트 목록
widgets/common/
├── buttons/
│   ├── primary_button.dart      # 주요 액션 버튼
│   ├── secondary_button.dart    # 보조 액션 버튼
│   └── text_button.dart         # 텍스트 버튼
├── inputs/
│   ├── custom_text_field.dart    # 커스텀 텍스트 필드
│   ├── custom_dropdown.dart     # 드롭다운
│   └── search_field.dart        # 검색 필드
├── cards/
│   ├── info_card.dart           # 정보 카드
│   └── action_card.dart         # 액션 가능한 카드
└── indicators/
    ├── loading_widget.dart       # 로딩 인디케이터
    └── error_widget.dart        # 에러 표시 위젯

🔐 세션 관리
구현 방식
Hive (토큰 저장) + Riverpod (상태 관리) + go_router (자동 리다이렉션)
1. 토큰 저장/로드 (Hive)
   dart// core/services/auth_local_service.dart
   class AuthLocalService {
   static const String _authBox = 'auth';
   static const String _tokenKey = 'token';
   static const String _refreshTokenKey = 'refreshToken';

Future<void> saveToken(String token, {String? refreshToken}) async {
final box = await Hive.openBox(_authBox);
await box.put(_tokenKey, token);
if (refreshToken != null) {
await box.put(_refreshTokenKey, refreshToken);
}
}

String? getToken() {
final box = Hive.box(_authBox);
return box.get(_tokenKey);
}

Future<void> deleteToken() async {
final box = await Hive.openBox(_authBox);
await box.delete(_tokenKey);
await box.delete(_refreshTokenKey);
}

bool isLoggedIn() {
return getToken() != null;
}
}
2. 인증 상태 관리 (Riverpod)
   dart// presentation/providers/auth_provider.dart
   final authStateProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
   return AuthNotifier(ref.read(loginUseCaseProvider));
   });

class AuthNotifier extends StateNotifier<AuthState> {
final LoginUseCase loginUseCase;
final AuthLocalService _localService = getIt<AuthLocalService>();

AuthNotifier(this.loginUseCase) : super(AuthState()) {
_checkLoginStatus();
}

// 앱 시작 시 로그인 상태 확인
void _checkLoginStatus() {
final token = _localService.getToken();
if (token != null) {
state = state.copyWith(isLoggedIn: true, token: token);
}
}

Future<void> login(String email, String password) async {
state = state.copyWith(isLoading: true);

    final result = await loginUseCase.execute(email, password);
    result.fold(
      (failure) => state = state.copyWith(
        isLoading: false,
        errorMessage: failure.message,
      ),
      (authData) {
        _localService.saveToken(authData.token);
        state = state.copyWith(
          isLoading: false,
          isLoggedIn: true,
          token: authData.token,
          user: authData.user,
        );
      },
    );
}

Future<void> logout() async {
await _localService.deleteToken();
state = AuthState(); // 초기 상태로
}
}
3. 자동 로그인 리다이렉션 (go_router)
   dart// core/router/app_router.dart
   final goRouterProvider = Provider<GoRouter>((ref) {
   final authState = ref.watch(authStateProvider);

return GoRouter(
initialLocation: '/login',
redirect: (context, state) {
final isLoggedIn = authState.isLoggedIn;
final isGoingToLogin = state.matchedLocation == '/login';

      // 로그인 안 했는데 로그인 페이지가 아니면 → 로그인으로
      if (!isLoggedIn && !isGoingToLogin) {
        return '/login';
      }
      
      // 로그인 했는데 로그인 페이지 가려고 하면 → 메인으로
      if (isLoggedIn && isGoingToLogin) {
        return '/';
      }
      
      return null; // 그대로 진행
    },
    routes: [
      GoRoute(path: '/login', builder: (context, state) => LoginScreen()),
      GoRoute(path: '/', builder: (context, state) => MainScreen()),
      // ... 나머지 라우트
    ],
);
});

// main.dart에서 사용
MaterialApp.router(
routerConfig: ref.watch(goRouterProvider),
)
4. API 요청 시 자동 토큰 첨부
   dart// data/datasources/remote/base_api_service.dart
   class BaseApiService {
   final http.Client client;
   final AuthLocalService _authService = getIt<AuthLocalService>();
   static const baseUrl = 'http://localhost:3000/api';

Future<http.Response> get(String endpoint) async {
final token = _authService.getToken();

    final response = await client.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    );
    
    // 401 에러 시 자동 로그아웃
    if (response.statusCode == 401) {
      await _authService.deleteToken();
      throw UnauthorizedException();
    }
    
    return response;
}
}
5. 토큰 만료 처리 (선택사항)
   dart// Refresh Token이 있는 경우
   class TokenRefreshService {
   Future<void> refreshToken() async {
   final refreshToken = _authService.getRefreshToken();
   if (refreshToken == null) throw UnauthorizedException();

   final response = await http.post(
   Uri.parse('$baseUrl/auth/refresh'),
   body: json.encode({'refreshToken': refreshToken}),
   );

   if (response.statusCode == 200) {
   final newToken = json.decode(response.body)['token'];
   await _authService.saveToken(newToken);
   } else {
   await _authService.deleteToken();
   throw UnauthorizedException();
   }
   }
   }
   세션 관리 흐름
1. 앱 시작 → Hive에서 토큰 확인 → AuthState 업데이트
2. 로그인 성공 → 토큰 Hive 저장 → AuthState 업데이트 → 메인 화면
3. 모든 API 요청 → 자동으로 토큰 헤더 추가
4. 401 에러 → 자동 로그아웃 → 로그인 화면
5. 로그아웃 버튼 → Hive 토큰 삭제 → AuthState 초기화 → 로그인 화면

📄 주요 페이지 및 API
페이지라우트API로그인/loginPOST /api/auth/login회원가입/registerPOST /api/auth/register메인/GET /api/clinic/dashboard고객 목록/GET /api/clients고객 상세/clients/:idGET /api/clients/:id고객 등록/clients/newPOST /api/clients시술 등록/procedures/newPOST /api/procedures시술 결과 입력/procedures/:id/resultPUT /api/procedures/:id/result마이페이지/my-pageGET /api/clinic/info

⚠️ 주의사항
코드 작성 시

항상 Clean Architecture 레이어 구조를 따를 것
Entity와 Model 구분 (Entity는 순수 Dart, Model은 fromJson/toJson 포함)
에러 처리는 Either<Failure, Success> 패턴 사용 (dartz)
주석 많이 작성 (특히 Flutter 특유의 문법)
React와 다른 부분은 설명 추가

파일 생성 시

새 기능 추가 시 모든 레이어(Data, Domain, Presentation) 파일 함께 생성
폴더 구조 정확히 준수
Provider는 적절한 위치에 정의

API 연동 시

백엔드 로컬 서버: http://localhost:3000/api
토큰은 Hive에 저장
모든 API 호출에 Authorization 헤더 포함 (로그인 제외)