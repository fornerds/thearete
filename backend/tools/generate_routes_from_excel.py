#!/usr/bin/env python3
"""Generate FastAPI routes from Excel API specification."""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from tools.utils.xlsx_api_parser import ExcelAPIParser
from tools.utils.fastapi_router_generator import FastAPIRouterGenerator
from tools.utils.pydantic_schema_generator import PydanticSchemaGenerator
from tools.utils.service_repository_generator import ServiceRepositoryGenerator
from tools.utils.test_generator import TestGenerator


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Excel API 스펙에서 FastAPI 라우터, 스키마, 서비스, 테스트를 생성합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python tools/generate_routes_from_excel.py
  python tools/generate_routes_from_excel.py --dry-run
  python tools/generate_routes_from_excel.py --overwrite
  python tools/generate_routes_from_excel.py --domains 사용자,상품
  python tools/generate_routes_from_excel.py --exclude-domains 관리자
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        default='docs/API.xlsx',
        help='입력 Excel API 스펙 파일 경로 (기본값: docs/API.xlsx)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='app',
        help='출력 디렉토리 경로 (기본값: app)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 파일을 생성하지 않고 출력만 확인'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='기존 파일을 덮어쓰기'
    )
    
    parser.add_argument(
        '--domains',
        help='포함할 도메인 목록 (쉼표로 구분)'
    )
    
    parser.add_argument(
        '--exclude-domains',
        help='제외할 도메인 목록 (쉼표로 구분)'
    )
    
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='테스트 파일 생성 건너뜀'
    )
    
    parser.add_argument(
        '--skip-services',
        action='store_true',
        help='서비스 및 리포지토리 파일 생성 건너뜀'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='상세한 출력'
    )
    
    args = parser.parse_args()
    
    try:
        # 입력 파일 확인
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ 입력 파일을 찾을 수 없습니다: {input_path}")
            return 1
        
        # Excel 파일 파싱
        print(f"📖 Excel API 스펙 파일 읽는 중: {input_path}")
        parser = ExcelAPIParser()
        domains = parser.parse_excel(str(input_path))
        
        # 스키마 검증
        print("✅ 파싱된 데이터 검증 중...")
        issues = parser.validate_parsed_data()
        if issues:
            print("⚠️  검증 중 발견된 문제들:")
            for issue in issues:
                print(f"   - {issue}")
            print()
        
        # 도메인 필터링
        if args.domains or args.exclude_domains:
            domains = filter_domains(domains, args.domains, args.exclude_domains)
        
        # 통계 출력
        total_endpoints = sum(len(domain.endpoints) for domain in domains.values())
        print(f"\n📊 파싱 통계:")
        print(f"   - 도메인 수: {len(domains)}")
        print(f"   - 엔드포인트 수: {total_endpoints}")
        
        if args.dry_run:
            print("🔍 드라이런 모드 - 생성될 파일들:")
            _show_dry_run_output(domains, args)
        else:
            # 코드 생성
            print("🏗️  FastAPI 코드 생성 중...")
            generated_files = generate_all_code(domains, args)
            
            print("✅ 코드 생성 완료!")
            print(f"   - 생성된 파일 수: {len(generated_files)}")
        
        # 다음 단계 안내
        if not args.dry_run:
            print(f"\n🚀 다음 단계:")
            print(f"   1. 생성된 라우터를 main.py에 등록")
            print(f"   2. 데이터베이스 모델 생성 (필요시)")
            print(f"   3. 테스트 실행:")
            print(f"      pytest tests/api/")
            print(f"   4. 서버 실행:")
            print(f"      uvicorn app.main:app --reload")
        
        return 0
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def filter_domains(domains, include_domains: Optional[str], exclude_domains: Optional[str]):
    """Filter domains based on include/exclude options."""
    filtered_domains = domains.copy()
    
    if include_domains:
        include_list = [d.strip() for d in include_domains.split(',')]
        filtered_domains = {k: v for k, v in filtered_domains.items() if k in include_list}
    
    if exclude_domains:
        exclude_list = [d.strip() for d in exclude_domains.split(',')]
        filtered_domains = {k: v for k, v in filtered_domains.items() if k not in exclude_list}
    
    return filtered_domains


def _show_dry_run_output(domains, args):
    """Show what files would be generated in dry run mode."""
    for domain_name, domain_info in domains.items():
        snake_domain = _to_snake_case(domain_name)
        
        print(f"\n📁 도메인: {domain_name}")
        
        # Router files
        print(f"   📄 app/api/v1/routes_{snake_domain}.py")
        
        # Schema files
        has_request_schemas = any(ep.request_schema for ep in domain_info.endpoints)
        has_response_schemas = any(ep.response_schema for ep in domain_info.endpoints)
        
        if has_request_schemas:
            print(f"   📄 app/schemas/{snake_domain}_request.py")
        if has_response_schemas:
            print(f"   📄 app/schemas/{snake_domain}_response.py")
        
        # Service and repository files
        if not args.skip_services:
            print(f"   📄 app/services/{snake_domain}_service.py")
            print(f"   📄 app/db/repositories/{snake_domain}_repo.py")
        
        # Test files
        if not args.skip_tests:
            for endpoint in domain_info.endpoints:
                print(f"   📄 tests/api/test_{snake_domain}_{endpoint.function_name}.py")


def generate_all_code(domains, args):
    """Generate all code files."""
    generated_files = {}
    
    # Generate routers
    router_generator = FastAPIRouterGenerator()
    router_files = router_generator.generate_routers(domains, args.overwrite)
    generated_files.update(router_files)
    
    # Generate schemas
    schema_generator = PydanticSchemaGenerator()
    schema_files = schema_generator.generate_schemas(domains, args.overwrite)
    generated_files.update(schema_files)
    
    # Generate services and repositories
    if not args.skip_services:
        service_repo_generator = ServiceRepositoryGenerator()
        service_repo_files = service_repo_generator.generate_services_and_repos(domains, args.overwrite)
        generated_files.update(service_repo_files)
    
    # Generate tests
    if not args.skip_tests:
        test_generator = TestGenerator()
        test_files = test_generator.generate_tests(domains, args.overwrite)
        generated_files.update(test_files)
    
    return generated_files


def _to_snake_case(name: str) -> str:
    """Convert to snake_case."""
    import re
    # Convert to lowercase and replace spaces/underscores with underscores
    name = re.sub(r'[^a-zA-Z0-9]', '_', name.lower())
    # Remove multiple consecutive underscores
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    return name.strip('_')


if __name__ == '__main__':
    sys.exit(main())
