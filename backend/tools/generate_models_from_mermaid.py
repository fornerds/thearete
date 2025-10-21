#!/usr/bin/env python3
"""Generate SQLAlchemy models from Mermaid ERD."""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from tools.utils.mermaid_erd_parser import MermaidERDParser
from tools.utils.sqlalchemy_emitter import SQLAlchemyEmitter


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mermaid ERD에서 SQLAlchemy 모델을 생성합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python tools/generate_models_from_mermaid.py
  python tools/generate_models_from_mermaid.py --dry-run
  python tools/generate_models_from_mermaid.py --overwrite
  python tools/generate_models_from_mermaid.py --tables SHOP,CUSTOMER
  python tools/generate_models_from_mermaid.py --exclude-tables PHOTO
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        default='docs/ERD.mmd',
        help='입력 Mermaid ERD 파일 경로 (기본값: docs/ERD.mmd)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='app/db/models',
        help='출력 디렉토리 경로 (기본값: app/db/models)'
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
        '--tables',
        help='포함할 테이블 목록 (쉼표로 구분)'
    )
    
    parser.add_argument(
        '--exclude-tables',
        help='제외할 테이블 목록 (쉼표로 구분)'
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
        
        # 출력 디렉토리 생성
        output_path = Path(args.output)
        if not args.dry_run:
            output_path.mkdir(parents=True, exist_ok=True)
        
        # ERD 파일 읽기
        print(f"📖 ERD 파일 읽는 중: {input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            erd_content = f.read()
        
        # 파싱
        print("🔍 ERD 파싱 중...")
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        # 스키마 검증
        print("✅ 스키마 검증 중...")
        issues = parser.validate_schema()
        if issues:
            print("⚠️  스키마 검증 중 발견된 문제들:")
            for issue in issues:
                print(f"   - {issue}")
            print()
        
        # 테이블 필터링
        if args.tables or args.exclude_tables:
            schema = filter_tables(schema, args.tables, args.exclude_tables)
        
        # 코드 생성
        print("🏗️  SQLAlchemy 모델 코드 생성 중...")
        emitter = SQLAlchemyEmitter(schema)
        
        if args.dry_run:
            print("🔍 드라이런 모드 - 생성될 파일들:")
            generated_files = {}
            for table_name in schema.tables.keys():
                model_code = emitter._generate_model_code(schema.tables[table_name])
                generated_files[table_name] = model_code
                
                file_path = output_path / f"{emitter._to_snake_case(table_name)}.py"
                print(f"   📄 {file_path}")
                if args.verbose:
                    print("   " + "="*50)
                    print(model_code)
                    print("   " + "="*50)
                    print()
            
            # __init__.py
            init_code = emitter._generate_init_code()
            init_path = output_path / "__init__.py"
            print(f"   📄 {init_path}")
            if args.verbose:
                print("   " + "="*50)
                print(init_code)
                print("   " + "="*50)
        else:
            generated_files = emitter.generate_models(str(output_path), args.overwrite)
            
            print("✅ 모델 파일 생성 완료!")
            for table_name, code in generated_files.items():
                if table_name == '__init__':
                    file_path = output_path / "__init__.py"
                else:
                    file_path = output_path / f"{emitter._to_snake_case(table_name)}.py"
                print(f"   📄 {file_path}")
        
        # 통계 출력
        print(f"\n📊 생성 통계:")
        print(f"   - 테이블 수: {len(schema.tables)}")
        print(f"   - 관계 수: {len(schema.relationships)}")
        
        # 다음 단계 안내
        if not args.dry_run:
            print(f"\n🚀 다음 단계:")
            print(f"   1. Alembic 마이그레이션 생성:")
            print(f"      alembic revision --autogenerate -m \"autogen from erd\"")
            print(f"   2. 마이그레이션 실행:")
            print(f"      alembic upgrade head")
            print(f"   3. 또는 Makefile 사용:")
            print(f"      make revision-auto")
            print(f"      make migrate")
        
        return 0
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def filter_tables(schema, include_tables: Optional[str], exclude_tables: Optional[str]):
    """Filter tables based on include/exclude options."""
    if include_tables:
        include_list = [t.strip().upper() for t in include_tables.split(',')]
        filtered_tables = {k: v for k, v in schema.tables.items() if k in include_list}
        schema.tables = filtered_tables
        
        # Also filter relationships
        filtered_relationships = []
        for rel in schema.relationships:
            if rel.from_table in filtered_tables and rel.to_table in filtered_tables:
                filtered_relationships.append(rel)
        schema.relationships = filtered_relationships
    
    if exclude_tables:
        exclude_list = [t.strip().upper() for t in exclude_tables.split(',')]
        filtered_tables = {k: v for k, v in schema.tables.items() if k not in exclude_list}
        schema.tables = filtered_tables
        
        # Also filter relationships
        filtered_relationships = []
        for rel in schema.relationships:
            if rel.from_table in filtered_tables and rel.to_table in filtered_tables:
                filtered_relationships.append(rel)
        schema.relationships = filtered_relationships
    
    return schema


if __name__ == '__main__':
    sys.exit(main())
