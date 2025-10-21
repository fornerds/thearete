"""Pydantic schema generator for Excel API specifications."""

import os
from typing import Dict, List, Optional, Set
from pathlib import Path

from .xlsx_api_parser import DomainInfo, EndpointInfo, SchemaInfo, FieldInfo


class PydanticSchemaGenerator:
    """Generator for Pydantic schema files."""
    
    def __init__(self, output_dir: str = "app/schemas"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_schemas(self, domains: Dict[str, DomainInfo], overwrite: bool = False) -> Dict[str, str]:
        """Generate schema files for all domains."""
        generated_files = {}
        
        # Group schemas by domain
        domain_schemas = self._group_schemas_by_domain(domains)
        
        for domain_name, schemas in domain_schemas.items():
            # Generate request schemas
            request_schemas = [s for s in schemas if 'request' in s.name.lower()]
            if request_schemas:
                request_code = self._generate_request_schema_code(domain_name, request_schemas)
                file_path = self.output_dir / f"{self._to_snake_case(domain_name)}_request.py"
                
                if file_path.exists() and not overwrite:
                    print(f"파일이 이미 존재합니다 (건너뜀): {file_path}")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(request_code)
                    generated_files[f"{domain_name}_request"] = request_code
                    print(f"✅ 요청 스키마 생성 완료: {file_path}")
            
            # Generate response schemas
            response_schemas = [s for s in schemas if 'response' in s.name.lower()]
            if response_schemas:
                response_code = self._generate_response_schema_code(domain_name, response_schemas)
                file_path = self.output_dir / f"{self._to_snake_case(domain_name)}_response.py"
                
                if file_path.exists() and not overwrite:
                    print(f"파일이 이미 존재합니다 (건너뜀): {file_path}")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(response_code)
                    generated_files[f"{domain_name}_response"] = response_code
                    print(f"✅ 응답 스키마 생성 완료: {file_path}")
        
        return generated_files
    
    def _group_schemas_by_domain(self, domains: Dict[str, DomainInfo]) -> Dict[str, List[SchemaInfo]]:
        """Group schemas by domain."""
        domain_schemas = {}
        
        for domain_name, domain_info in domains.items():
            schemas = []
            
            for endpoint in domain_info.endpoints:
                if endpoint.request_schema:
                    schemas.append(endpoint.request_schema)
                if endpoint.response_schema:
                    schemas.append(endpoint.response_schema)
            
            if schemas:
                domain_schemas[domain_name] = schemas
        
        return domain_schemas
    
    def _generate_request_schema_code(self, domain_name: str, schemas: List[SchemaInfo]) -> str:
        """Generate request schema code."""
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Collect imports
        imports = self._collect_schema_imports(schemas)
        
        # Generate schema classes
        schema_classes = []
        for schema in schemas:
            class_code = self._generate_schema_class(schema, "request")
            schema_classes.append(class_code)
        
        # Combine all parts
        code = f'''"""Pydantic request schemas for {domain_name} domain."""

{imports}

{chr(10).join(schema_classes)}
'''
        return code
    
    def _generate_response_schema_code(self, domain_name: str, schemas: List[SchemaInfo]) -> str:
        """Generate response schema code."""
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Collect imports
        imports = self._collect_schema_imports(schemas)
        
        # Generate schema classes
        schema_classes = []
        for schema in schemas:
            class_code = self._generate_schema_class(schema, "response")
            schema_classes.append(class_code)
        
        # Combine all parts
        code = f'''"""Pydantic response schemas for {domain_name} domain."""

{imports}

{chr(10).join(schema_classes)}
'''
        return code
    
    def _collect_schema_imports(self, schemas: List[SchemaInfo]) -> str:
        """Collect necessary imports for schemas."""
        imports = set()
        
        # Base imports
        imports.add("from pydantic import BaseModel, Field")
        imports.add("from typing import List, Optional, Any")
        
        # Check for specific types
        has_datetime = False
        has_date = False
        has_time = False
        has_uuid = False
        
        for schema in schemas:
            for field in schema.fields:
                field_type = field.type.lower()
                if 'datetime' in field_type:
                    has_datetime = True
                elif 'date' in field_type and 'datetime' not in field_type:
                    has_date = True
                elif 'time' in field_type and 'datetime' not in field_type:
                    has_time = True
                elif 'uuid' in field_type:
                    has_uuid = True
        
        if has_datetime:
            imports.add("from datetime import datetime")
        if has_date:
            imports.add("from datetime import date")
        if has_time:
            imports.add("from datetime import time")
        if has_uuid:
            imports.add("from uuid import UUID")
        
        # Convert to sorted list and format
        import_list = sorted(list(imports))
        return '\n'.join(import_list)
    
    def _generate_schema_class(self, schema: SchemaInfo, schema_type: str) -> str:
        """Generate a single schema class."""
        class_name = self._clean_schema_name(schema.name)
        
        # Generate field definitions
        field_definitions = []
        for field in schema.fields:
            field_def = self._generate_field_definition(field)
            field_definitions.append(field_def)
        
        # Generate docstring
        docstring = schema.description or f"{schema_type.title()} schema for {class_name}"
        
        # Generate class
        class_code = f'''class {class_name}(BaseModel):
    """{docstring}"""
    
{chr(10).join(field_definitions)}
'''
        return class_code
    
    def _generate_field_definition(self, field: FieldInfo) -> str:
        """Generate field definition."""
        field_name = field.name
        field_type = self._convert_python_type(field.type)
        
        # Handle optional fields
        if not field.is_required:
            if not field_type.startswith('Optional[') and field_type != 'Any':
                field_type = f"Optional[{field_type}]"
        
        # Generate field definition
        field_parts = [f"    {field_name}: {field_type}"]
        
        # Add Field() with constraints if needed
        field_constraints = []
        
        if field.is_required:
            field_constraints.append("...")
        elif field.default_value is not None:
            field_constraints.append(f"default={field.default_value}")
        else:
            field_constraints.append("None")
        
        if field.description:
            field_constraints.append(f'description="{field.description}"')
        
        if field_constraints:
            field_parts.append(f" = Field({', '.join(field_constraints)})")
        
        return ''.join(field_parts)
    
    def _convert_python_type(self, type_str: str) -> str:
        """Convert type string to Python type."""
        type_str = type_str.strip()
        
        # Handle generic types
        if '<' in type_str and '>' in type_str:
            return type_str
        
        # Handle basic types
        type_mapping = {
            'int': 'int',
            'float': 'float',
            'str': 'str',
            'string': 'str',
            'bool': 'bool',
            'boolean': 'bool',
            'datetime': 'datetime',
            'date': 'date',
            'time': 'time',
            'dict': 'dict',
            'object': 'dict',
            'list': 'List[Any]',
            'array': 'List[Any]',
            'any': 'Any',
        }
        
        return type_mapping.get(type_str.lower(), 'str')
    
    def _clean_schema_name(self, name: str) -> str:
        """Clean schema name for class name."""
        # Remove domain prefix and type suffix
        parts = name.split('_')
        
        # Remove common prefixes/suffixes
        if len(parts) >= 3:
            # Format: domain_type_number -> TypeNumber
            type_part = parts[-2]  # request or response
            number_part = parts[-1]  # number
            
            return f"{self._to_pascal_case(type_part)}{number_part}"
        elif len(parts) >= 2:
            # Format: domain_type -> Type
            type_part = parts[-1]
            return self._to_pascal_case(type_part)
        else:
            return self._to_pascal_case(name)
    
    def _to_snake_case(self, name: str) -> str:
        """Convert to snake_case."""
        import re
        # Convert to lowercase and replace spaces/underscores with underscores
        name = re.sub(r'[^a-zA-Z0-9]', '_', name.lower())
        # Remove multiple consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        return name.strip('_')
    
    def _to_pascal_case(self, name: str) -> str:
        """Convert to PascalCase."""
        import re
        # Split by non-alphanumeric characters
        parts = re.split(r'[^a-zA-Z0-9]', name)
        # Capitalize each part
        return ''.join(part.capitalize() for part in parts if part)
