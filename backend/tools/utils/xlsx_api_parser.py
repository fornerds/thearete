"""Excel API specification parser for generating FastAPI routes."""

import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum

import pandas as pd


class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class FieldInfo:
    """Information about a field in request/response."""
    name: str
    type: str
    is_required: bool = False
    description: Optional[str] = None
    default_value: Optional[Any] = None


@dataclass
class SchemaInfo:
    """Information about a Pydantic schema."""
    name: str
    fields: List[FieldInfo] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class EndpointInfo:
    """Information about an API endpoint."""
    api_number: int
    screen_mapping: Optional[str]
    domain: str
    method: HTTPMethod
    endpoint: str
    auth_required: bool
    request_schema: Optional[SchemaInfo] = None
    response_schema: Optional[SchemaInfo] = None
    description: Optional[str] = None
    detailed_requirements: Optional[str] = None
    path_params: List[str] = field(default_factory=list)
    
    @property
    def route_name(self) -> str:
        """Generate route name from endpoint."""
        # Remove leading slash and replace slashes with underscores
        route_name = self.endpoint.lstrip('/').replace('/', '_')
        # Replace path parameters with descriptive names
        route_name = re.sub(r'\{[^}]+\}', 'by_id', route_name)
        return route_name
    
    @property
    def function_name(self) -> str:
        """Generate function name from method and endpoint."""
        method_lower = self.method.value.lower()
        
        # Extract action from endpoint
        if '{' in self.endpoint:
            # Has path parameters
            if method_lower == 'get':
                return f"get_{self.route_name}"
            elif method_lower == 'put':
                return f"update_{self.route_name}"
            elif method_lower == 'delete':
                return f"delete_{self.route_name}"
        
        # No path parameters
        if method_lower == 'get':
            return f"list_{self.route_name}"
        elif method_lower == 'post':
            return f"create_{self.route_name}"
        elif method_lower == 'put':
            return f"update_{self.route_name}"
        elif method_lower == 'delete':
            return f"delete_{self.route_name}"
        
        return f"{method_lower}_{self.route_name}"


@dataclass
class DomainInfo:
    """Information about a domain group."""
    name: str
    endpoints: List[EndpointInfo] = field(default_factory=list)


class ExcelAPIParser:
    """Parser for Excel API specifications."""
    
    # Type mapping from Excel to Python/Pydantic
    TYPE_MAPPING = {
        'int': 'int',
        'integer': 'int',
        'number': 'float',
        'float': 'float',
        'string': 'str',
        'str': 'str',
        'text': 'str',
        'boolean': 'bool',
        'bool': 'bool',
        'datetime': 'datetime',
        'date': 'date',
        'time': 'time',
        'array': 'List',
        'list': 'List',
        'object': 'dict',
        'dict': 'dict',
    }
    
    def __init__(self):
        self.domains: Dict[str, DomainInfo] = {}
        self.schemas: Dict[str, SchemaInfo] = {}
        
    def parse_excel(self, file_path: str) -> Dict[str, DomainInfo]:
        """Parse Excel API specification file."""
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Excel 파일을 읽을 수 없습니다: {str(e)}")
        
        # Validate required columns
        required_columns = [
            'API 번호', '화면 매핑', '구분', 'HTTP Method', 'Endpoint', 
            '인증', '요청 데이터 예시 (✅ = 필수)', '응답 예시', '설명'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"필수 컬럼이 누락되었습니다: {missing_columns}")
        
        # Process each row
        for index, row in df.iterrows():
            try:
                endpoint_info = self._parse_row(row, index + 2)  # +2 for header and 0-based index
                if endpoint_info:
                    self._add_to_domain(endpoint_info)
            except Exception as e:
                raise ValueError(f"행 {index + 2} 파싱 오류: {str(e)}")
        
        return self.domains
    
    def _parse_row(self, row: pd.Series, row_number: int) -> Optional[EndpointInfo]:
        """Parse a single row from Excel."""
        # Skip empty rows
        if pd.isna(row['API 번호']):
            return None
        
        # Parse basic information
        api_number = int(row['API 번호'])
        screen_mapping = row['화면 매핑'] if not pd.isna(row['화면 매핑']) else None
        method_str = str(row['HTTP Method']).strip().upper()
        endpoint = str(row['Endpoint']).strip()
        auth_str = str(row['인증']).strip() if not pd.isna(row['인증']) else "불필요"
        description = str(row['설명']).strip() if not pd.isna(row['설명']) else None
        
        # Extract domain from endpoint
        domain = self._extract_domain_from_endpoint(endpoint)
        
        # Parse detailed requirements (비고 column)
        detailed_requirements = None
        if '비고' in row and not pd.isna(row['비고']):
            detailed_requirements = str(row['비고']).strip()
        
        # Validate HTTP method
        try:
            method = HTTPMethod(method_str)
        except ValueError:
            raise ValueError(f"잘못된 HTTP Method: {method_str}")
        
        # Parse authentication
        auth_required = auth_str.lower() in ['필요', 'required', 'true', '1']
        
        # Extract path parameters
        path_params = self._extract_path_params(endpoint)
        
        # Parse request schema
        request_schema = None
        if not pd.isna(row['요청 데이터 예시 (✅ = 필수)']):
            request_schema = self._parse_json_schema(
                str(row['요청 데이터 예시 (✅ = 필수)']),
                f"{domain}_request_{api_number}"
            )
        
        # Parse response schema
        response_schema = None
        if not pd.isna(row['응답 예시']):
            response_schema = self._parse_json_schema(
                str(row['응답 예시']),
                f"{domain}_response_{api_number}"
            )
        
        return EndpointInfo(
            api_number=api_number,
            screen_mapping=screen_mapping,
            domain=domain,
            method=method,
            endpoint=endpoint,
            auth_required=auth_required,
            request_schema=request_schema,
            response_schema=response_schema,
            description=description,
            detailed_requirements=detailed_requirements,
            path_params=path_params
        )
    
    def _extract_path_params(self, endpoint: str) -> List[str]:
        """Extract path parameters from endpoint."""
        pattern = r'\{([^}]+)\}'
        matches = re.findall(pattern, endpoint)
        return matches
    
    def _extract_domain_from_endpoint(self, endpoint: str) -> str:
        """Extract domain from endpoint path."""
        # Remove leading slash and split by slash
        path_parts = endpoint.lstrip('/').split('/')
        
        # Skip 'api' and version parts
        if len(path_parts) >= 3 and path_parts[0] == 'api' and path_parts[1].startswith('v'):
            # Extract domain from the third part
            domain_part = path_parts[2]
        elif len(path_parts) >= 1:
            # Use first part as domain
            domain_part = path_parts[0]
        else:
            domain_part = 'unknown'
        
        # Clean up domain name
        domain_part = domain_part.replace('-', '_').replace('_', ' ')
        
        # Map common domain names
        domain_mapping = {
            'shops': 'shop',
            'customers': 'customer', 
            'treatments': 'treatment',
            'treatment_sessions': 'treatment_session',
            'skin_measurements': 'skin_measurement',
            'color_recipes': 'color_recipe',
            'treatment_photos': 'treatment_photo',
            'auth': 'auth',
            'shop_summary': 'shop_summary'
        }
        
        return domain_mapping.get(domain_part, domain_part)
    
    def _parse_json_schema(self, json_str: str, schema_name: str) -> SchemaInfo:
        """Parse JSON string to SchemaInfo."""
        try:
            # Clean up the JSON string
            json_str = json_str.strip()
            
            # Handle cases where it might not be valid JSON
            if not json_str.startswith('{') and not json_str.startswith('['):
                # Try to wrap in braces
                json_str = f'{{{json_str}}}'
            
            # Parse JSON
            data = json.loads(json_str)
            
            # Convert to SchemaInfo
            fields = []
            
            if isinstance(data, dict):
                for key, value in data.items():
                    field_info = self._parse_field(key, value)
                    fields.append(field_info)
            elif isinstance(data, list) and data:
                # Handle array response
                if isinstance(data[0], dict):
                    for key, value in data[0].items():
                        field_info = self._parse_field(key, value)
                        fields.append(field_info)
            
            return SchemaInfo(
                name=schema_name,
                fields=fields,
                description=f"Schema for {schema_name}"
            )
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract fields manually
            fields = self._parse_fields_from_text(json_str)
            return SchemaInfo(
                name=schema_name,
                fields=fields,
                description=f"Schema for {schema_name}"
            )
    
    def _parse_field(self, key: str, value: Any) -> FieldInfo:
        """Parse a field from JSON data."""
        # Check if field is required (has ✅ prefix)
        is_required = key.startswith('✅')
        field_name = key.lstrip('✅')
        
        # Determine field type
        field_type = self._infer_type(value)
        
        return FieldInfo(
            name=field_name,
            type=field_type,
            is_required=is_required,
            description=None
        )
    
    def _parse_fields_from_text(self, text: str) -> List[FieldInfo]:
        """Parse fields from text when JSON parsing fails."""
        fields = []
        
        # Try to extract field patterns like "field_name": "type"
        pattern = r'["\']?([^"\':\s]+)["\']?\s*:\s*["\']?([^"\',\s}]+)["\']?'
        matches = re.findall(pattern, text)
        
        for field_name, field_type in matches:
            # Skip if it looks like a value rather than a field
            if field_name in ['true', 'false', 'null', 'undefined']:
                continue
                
            is_required = field_name.startswith('✅')
            clean_name = field_name.lstrip('✅')
            
            fields.append(FieldInfo(
                name=clean_name,
                type=self._infer_type_from_string(field_type),
                is_required=is_required
            ))
        
        return fields
    
    def _infer_type(self, value: Any) -> str:
        """Infer Python type from JSON value."""
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            # Try to infer more specific types from string values
            if value.lower() in ['true', 'false']:
                return 'bool'
            elif value.isdigit():
                return 'int'
            elif value.replace('.', '').isdigit():
                return 'float'
            else:
                return 'str'
        elif isinstance(value, list):
            if value:
                item_type = self._infer_type(value[0])
                return f'List[{item_type}]'
            else:
                return 'List[Any]'
        elif isinstance(value, dict):
            return 'dict'
        else:
            return 'Any'
    
    def _infer_type_from_string(self, type_str: str) -> str:
        """Infer Python type from string representation."""
        type_str = type_str.lower().strip()
        
        # Handle array types
        if type_str.startswith('array<') and type_str.endswith('>'):
            inner_type = type_str[6:-1]
            return f'List[{self.TYPE_MAPPING.get(inner_type, "Any")}]'
        
        # Handle generic types
        if '<' in type_str and '>' in type_str:
            base_type = type_str.split('<')[0]
            inner_type = type_str.split('<')[1].rstrip('>')
            return f'{self.TYPE_MAPPING.get(base_type, "Any")}[{self.TYPE_MAPPING.get(inner_type, "Any")}]'
        
        return self.TYPE_MAPPING.get(type_str, 'str')
    
    def _add_to_domain(self, endpoint_info: EndpointInfo) -> None:
        """Add endpoint to appropriate domain."""
        domain_name = endpoint_info.domain
        
        if domain_name not in self.domains:
            self.domains[domain_name] = DomainInfo(name=domain_name)
        
        self.domains[domain_name].endpoints.append(endpoint_info)
        
        # Store schemas
        if endpoint_info.request_schema:
            self.schemas[endpoint_info.request_schema.name] = endpoint_info.request_schema
        if endpoint_info.response_schema:
            self.schemas[endpoint_info.response_schema.name] = endpoint_info.response_schema
    
    def get_schema_by_name(self, name: str) -> Optional[SchemaInfo]:
        """Get schema by name."""
        return self.schemas.get(name)
    
    def get_all_schemas(self) -> Dict[str, SchemaInfo]:
        """Get all schemas."""
        return self.schemas
    
    def validate_parsed_data(self) -> List[str]:
        """Validate parsed data and return any issues."""
        issues = []
        
        for domain_name, domain_info in self.domains.items():
            # Check for duplicate endpoints within domain
            endpoints = [ep.endpoint for ep in domain_info.endpoints]
            duplicates = [ep for ep in set(endpoints) if endpoints.count(ep) > 1]
            if duplicates:
                issues.append(f"도메인 '{domain_name}'에 중복 엔드포인트가 있습니다: {duplicates}")
            
            # Check for duplicate function names
            function_names = [ep.function_name for ep in domain_info.endpoints]
            duplicate_functions = [name for name in set(function_names) if function_names.count(name) > 1]
            if duplicate_functions:
                issues.append(f"도메인 '{domain_name}'에 중복 함수명이 있습니다: {duplicate_functions}")
        
        return issues
