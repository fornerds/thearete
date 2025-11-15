import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

// Flutter Web에서만 dart:html 사용
import 'dart:html' as html;
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:webview_flutter_web/webview_flutter_web.dart';

import '../../../core/constants/app_colors.dart';
import '../../widgets/common/inputs/custom_text_field.dart';
import '../../widgets/common/buttons/primary_button.dart';

/// 마이페이지 수정 화면
class MyShopEditScreen extends ConsumerStatefulWidget {
  const MyShopEditScreen({super.key});

  @override
  ConsumerState<MyShopEditScreen> createState() => _MyShopEditScreenState();
}

class _MyShopEditScreenState extends ConsumerState<MyShopEditScreen> {
  final _formKey = GlobalKey<FormState>();
  final _shopNameController = TextEditingController();
  final _addressController = TextEditingController();
  final _ownerNameController = TextEditingController();
  final _phoneController = TextEditingController();

  bool _isLoading = false;

  @override
  void dispose() {
    _shopNameController.dispose();
    _addressController.dispose();
    _ownerNameController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  void _handleSave() {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });

      // TODO: API 호출로 데이터 저장
      Future.delayed(const Duration(seconds: 1), () {
        if (mounted) {
          setState(() {
            _isLoading = false;
          });
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('저장되었습니다'),
              backgroundColor: Colors.green,
              behavior: SnackBarBehavior.floating,
            ),
          );
          context.pop();
        }
      });
    }
  }

  void _showAddressSearchModal(BuildContext context) {
    if (kIsWeb) {
      // Flutter Web에서는 팝업으로 Daum Postcode 열기
      _openDaumPostcodePopup(context);
    } else {
      // 모바일에서는 WebView 모달 사용
      showDialog(
        context: context,
        builder: (context) => Dialog(
          insetPadding: const EdgeInsets.all(16),
          child: Container(
            width: double.infinity,
            height: MediaQuery.of(context).size.height * 0.8,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              color: Colors.white,
            ),
            child: Column(
              children: [
                // 헤더
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: const BoxDecoration(
                    border: Border(
                      bottom: BorderSide(color: Colors.grey, width: 1),
                    ),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        '주소 검색',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.close),
                        onPressed: () => Navigator.of(context).pop(),
                      ),
                    ],
                  ),
                ),
                // WebView
                Expanded(
                  child: _AddressSearchWebView(
                    onAddressSelected: (address) {
                      _addressController.text = address;
                      Navigator.of(context).pop();
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }
  }

  void _openDaumPostcodePopup(BuildContext context) {
    if (!kIsWeb) return;
    
    // Flutter Web에서는 팝업으로 Daum Postcode 열기
    final script = r'''
      (function() {
        if (typeof daum === 'undefined') {
          var script = document.createElement('script');
          script.src = 'https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js';
          script.onload = function() {
            new daum.Postcode({
              oncomplete: function(data) {
                var address = '';
                if (data.userSelectedType === 'R') {
                  address = data.roadAddress;
                } else {
                  address = data.jibunAddress;
                }
                if (data.userSelectedType === 'R') {
                  if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                    address += ' (' + data.bname + ')';
                  }
                }
                window.postMessage({type: 'daumPostcode', address: address}, '*');
              },
              width: '100%',
              height: '100%'
            }).open();
          };
          document.head.appendChild(script);
        } else {
          new daum.Postcode({
            oncomplete: function(data) {
              var address = '';
              if (data.userSelectedType === 'R') {
                address = data.roadAddress;
              } else {
                address = data.jibunAddress;
              }
              if (data.userSelectedType === 'R') {
                if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                  address += ' (' + data.bname + ')';
                }
              }
              window.postMessage({type: 'daumPostcode', address: address}, '*');
            },
            width: '100%',
            height: '100%'
          }).open();
        }
      })();
    ''';

    // 메시지 리스너 등록 (한 번만)
    html.window.addEventListener('message', (html.Event event) {
      if (event is html.MessageEvent) {
        final data = event.data;
        if (data is Map && data['type'] == 'daumPostcode') {
          final address = data['address'] as String;
          setState(() {
            _addressController.text = address;
          });
          // FormField 상태 업데이트
          if (_formKey.currentState != null) {
            _formKey.currentState!.validate();
          }
        }
      }
    });

    // Daum Postcode 스크립트가 이미 로드되어 있는지 확인
    final existingScript = html.window.document.querySelector('script[src*="postcode.v2.js"]');
    if (existingScript == null) {
      final scriptElement = html.ScriptElement()
        ..src = 'https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js'
        ..type = 'text/javascript';
      
      scriptElement.onLoad.listen((_) {
        // 스크립트 로드 후 Postcode 실행
        _executePostcodeScript(script);
      });
      
      // head 요소 찾기
      final head = html.window.document.querySelector('head');
      if (head != null) {
        head.append(scriptElement);
      } else {
        html.window.document.documentElement!.append(scriptElement);
      }
    } else {
      // 이미 로드되어 있으면 바로 실행
      _executePostcodeScript(script);
    }
  }

  void _executePostcodeScript(String script) {
    // JavaScript 실행을 위해 ScriptElement 생성 및 추가
    if (kIsWeb) {
      final scriptElement = html.ScriptElement()
        ..text = script
        ..type = 'text/javascript';
      
      // head 요소 찾기
      final head = html.window.document.querySelector('head');
      if (head != null) {
        head.append(scriptElement);
      } else {
        html.window.document.documentElement!.append(scriptElement);
      }
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.grayScaleBackground,
      body: SafeArea(
        child: Column(
          children: [
            // 상단 헤더 (뒤로 가기 버튼 + 제목)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
              child: Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back, color: AppColors.grayScaleText),
                    onPressed: () => context.pop(),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
                  const SizedBox(width: 10),
                  const Text(
                    '마이페이지 수정',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: AppColors.grayScaleText,
                    ),
                  ),
                ],
              ),
            ),
            // 스크롤 가능한 컨텐츠 영역
            Expanded(
              child: SingleChildScrollView(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 16),

                        // 샵 상호명
                        CustomTextField(
                          labelText: '샵 상호명',
                          hintText: '샵 상호명을 입력하세요',
                          controller: _shopNameController,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return '샵 상호명을 입력해주세요';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 32),

                        // 샵 주소
                        FormField<String>(
                          initialValue: _addressController.text,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return '샵 주소를 입력해주세요';
                            }
                            return null;
                          },
                          builder: (formFieldState) {
                            final hasError = formFieldState.hasError;
                            final errorText = formFieldState.errorText;

                            return Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                // Label
                                Container(
                                  constraints: const BoxConstraints(
                                    maxWidth: double.infinity,
                                  ),
                                  child: Row(
                                    children: [
                                      Flexible(
                                        child: Text(
                                          '샵 주소',
                                          style: const TextStyle(
                                            fontSize: 20,
                                            fontWeight: FontWeight.w700,
                                            height: 1.5,
                                            color: AppColors.grayScaleText,
                                          ),
                                          overflow: TextOverflow.ellipsis,
                                          maxLines: 1,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(height: 6),
                                // Input Row
                                Row(
                                  children: [
                                    Expanded(
                                      child: SizedBox(
                                        height: 48,
                                        child: TextFormField(
                                          controller: _addressController,
                                          readOnly: true,
                                          enabled: true,
                                          onChanged: (value) {
                                            formFieldState.didChange(value);
                                          },
                                          style: const TextStyle(
                                            fontSize: 16,
                                            color: AppColors.grayScaleText,
                                          ),
                                          decoration: InputDecoration(
                                            hintText: '샵 주소를 입력하세요',
                                            contentPadding: const EdgeInsets.symmetric(
                                              horizontal: 16,
                                              vertical: 16,
                                            ),
                                            filled: true,
                                            fillColor: AppColors.grayScaleBox3,
                                            border: OutlineInputBorder(
                                              borderRadius: BorderRadius.circular(6),
                                              borderSide: BorderSide(
                                                color: hasError
                                                    ? Colors.red
                                                    : Colors.transparent,
                                                width: 0,
                                              ),
                                            ),
                                            enabledBorder: OutlineInputBorder(
                                              borderRadius: BorderRadius.circular(6),
                                              borderSide: BorderSide(
                                                color: hasError
                                                    ? Colors.red
                                                    : Colors.transparent,
                                                width: 0,
                                              ),
                                            ),
                                            focusedBorder: OutlineInputBorder(
                                              borderRadius: BorderRadius.circular(6),
                                              borderSide: BorderSide(
                                                color: hasError
                                                    ? Colors.red
                                                    : AppColors.medicalDarkBlue,
                                                width: 2,
                                              ),
                                            ),
                                            errorText: null,
                                            errorStyle: const TextStyle(height: 0, fontSize: 0),
                                            errorMaxLines: 0,
                                            hintStyle: const TextStyle(
                                              color: AppColors.grayScaleGuideText,
                                              fontSize: 16,
                                              fontWeight: FontWeight.w600,
                                              height: 1.35,
                                            ),
                                          ),
                                        ),
                                      ),
                                    ),
                                    const SizedBox(width: 10),
                                    SizedBox(
                                      height: 48,
                                      child: OutlinedButton(
                                        onPressed: () => _showAddressSearchModal(context),
                                        style: OutlinedButton.styleFrom(
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 16,
                                            vertical: 10,
                                          ),
                                          side: const BorderSide(
                                            color: AppColors.keyColor3,
                                            width: 1,
                                          ),
                                          backgroundColor: AppColors.grayScaleBackground,
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(4),
                                          ),
                                          minimumSize: const Size(0, 48),
                                        ),
                                        child: const Text(
                                          '주소검색',
                                          style: TextStyle(
                                            fontSize: 14,
                                            fontWeight: FontWeight.w700,
                                            height: 1.35, // line-height: 135% (18.9px / 14px)
                                            color: AppColors.keyColor3,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                // 에러 메시지 표시
                                if (hasError && errorText != null) ...[
                                  const SizedBox(height: 4),
                                  Text(
                                    errorText,
                                    style: const TextStyle(
                                      color: Colors.red,
                                      fontSize: 12,
                                      height: 1.2,
                                    ),
                                  ),
                                ],
                              ],
                            );
                          },
                        ),
                        const SizedBox(height: 32),

                        // 대표자명
                        CustomTextField(
                          labelText: '대표자명',
                          hintText: '대표자명을 입력하세요',
                          controller: _ownerNameController,
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return '대표자명을 입력해주세요';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 32),

                        // 전화번호
                        CustomTextField(
                          labelText: '전화번호',
                          hintText: '전화번호를 입력하세요',
                          controller: _phoneController,
                          keyboardType: TextInputType.phone,
                          inputFormatters: [
                            FilteringTextInputFormatter.digitsOnly,
                            LengthLimitingTextInputFormatter(11),
                          ],
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return '전화번호를 입력해주세요';
                            }
                            if (value.length < 10) {
                              return '올바른 전화번호 형식이 아닙니다';
                            }
                            return null;
                          },
                        ),
                        // 하단 고정 버튼을 위한 여백
                        const SizedBox(height: 100),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            // 하단 고정 저장 버튼
            Container(
              padding: const EdgeInsets.all(24.0),
              decoration: BoxDecoration(
                color: AppColors.grayScaleBackground,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 10,
                    offset: const Offset(0, -2),
                  ),
                ],
              ),
              child: SafeArea(
                top: false,
                child: SizedBox(
                  width: double.infinity,
                  child: PrimaryButton(
                    text: '저장하기',
                    onPressed: _isLoading ? null : _handleSave,
                    isLoading: _isLoading,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Daum Postcode를 표시하는 WebView 위젯
class _AddressSearchWebView extends StatefulWidget {
  final Function(String) onAddressSelected;

  const _AddressSearchWebView({
    required this.onAddressSelected,
  });

  @override
  State<_AddressSearchWebView> createState() => _AddressSearchWebViewState();
}

class _AddressSearchWebViewState extends State<_AddressSearchWebView> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    
    // Flutter Web에서 WebView 플랫폼 초기화
    if (kIsWeb) {
      WebViewPlatform.instance = WebWebViewPlatform();
    }
    
    _controller = WebViewController();
    
    // Flutter Web에서 지원되지 않는 메서드들은 조건부 처리
    if (!kIsWeb) {
      _controller
        ..setBackgroundColor(Colors.white)
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..addJavaScriptChannel(
          'AddressChannel',
          onMessageReceived: (JavaScriptMessage message) {
            final address = message.message;
            widget.onAddressSelected(address);
          },
        );
    }
    
    _controller
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (String url) {
            // 페이지 로드 완료 후 추가 설정이 필요하면 여기서 처리
          },
        ),
      )
      ..loadRequest(
        Uri.dataFromString(
          _getPostcodeHtml(),
          mimeType: 'text/html',
          encoding: Encoding.getByName('utf-8'),
        ),
      );
  }

  String _getPostcodeHtml() {
    return r'''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
  <style>
    body {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100vh;
      overflow: hidden;
    }
    #daum_postcode {
      width: 100%;
      height: 100%;
    }
  </style>
</head>
<body>
  <div id="daum_postcode"></div>
  <script>
    new daum.Postcode({
      oncomplete: function(data) {
        var address = '';
        if (data.userSelectedType === 'R') {
          address = data.roadAddress;
        } else {
          address = data.jibunAddress;
        }
        if (data.userSelectedType === 'R') {
          if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
            address += ' (' + data.bname + ')';
          }
        }
        if (window.AddressChannel) {
          AddressChannel.postMessage(address);
        }
      },
      width: '100%',
      height: '100%'
    }).embed(document.getElementById('daum_postcode'));
  </script>
</body>
</html>
    ''';
  }

  @override
  Widget build(BuildContext context) {
    return WebViewWidget(controller: _controller);
  }
}

