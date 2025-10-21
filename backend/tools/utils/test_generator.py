"""Test generator for Excel API specifications."""

import os
from typing import Dict, List, Optional
from pathlib import Path

from .xlsx_api_parser import DomainInfo, EndpointInfo


class TestGenerator:
    """Generator for API test files."""
    
    def __init__(self, output_dir: str = "tests/api"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_tests(self, domains: Dict[str, DomainInfo], overwrite: bool = False) -> Dict[str, str]:
        """Generate test files for all domains."""
        generated_files = {}
        
        for domain_name, domain_info in domains.items():
            # Generate test file for each endpoint
            for endpoint in domain_info.endpoints:
                test_code = self._generate_endpoint_test_code(endpoint)
                test_file_name = f"test_{self._to_snake_case(domain_name)}_{endpoint.function_name}.py"
                test_file_path = self.output_dir / test_file_name
                
                if test_file_path.exists() and not overwrite:
                    print(f"파일이 이미 존재합니다 (건너뜀): {test_file_path}")
                    continue
                
                with open(test_file_path, 'w', encoding='utf-8') as f:
                    f.write(test_code)
                
                generated_files[f"{domain_name}_{endpoint.function_name}"] = test_code
                print(f"✅ 테스트 생성 완료: {test_file_path}")
        
        return generated_files
    
    def _generate_endpoint_test_code(self, endpoint: EndpointInfo) -> str:
        """Generate test code for an endpoint."""
        domain_name = endpoint.domain
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Collect imports
        imports = self._collect_test_imports(endpoint)
        
        # Generate test class
        test_class = self._generate_test_class(endpoint)
        
        # Combine all parts
        code = f'''"""Tests for {domain_name} {endpoint.function_name} endpoint."""

{imports}

{test_class}
'''
        return code
    
    def _collect_test_imports(self, endpoint: EndpointInfo) -> str:
        """Collect necessary imports for test."""
        imports = set()
        
        # Base imports
        imports.add("import pytest")
        imports.add("from httpx import AsyncClient")
        imports.add("from fastapi.testclient import TestClient")
        imports.add("from unittest.mock import AsyncMock, patch")
        
        # App imports
        imports.add("from app.main import app")
        
        # Schema imports if needed
        if endpoint.request_schema or endpoint.response_schema:
            imports.add("from app.schemas import *")
        
        # Auth imports if needed
        if endpoint.auth_required:
            imports.add("from app.core.auth import create_access_token")
            imports.add("from app.db.models.user import User")
        
        # Convert to sorted list and format
        import_list = sorted(list(imports))
        return '\n'.join(import_list)
    
    def _generate_test_class(self, endpoint: EndpointInfo) -> str:
        """Generate test class for endpoint."""
        domain_name = endpoint.domain
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Generate test methods
        test_methods = []
        
        # Generate happy path test
        happy_path_test = self._generate_happy_path_test(endpoint)
        test_methods.append(happy_path_test)
        
        # Generate error tests
        error_tests = self._generate_error_tests(endpoint)
        test_methods.extend(error_tests)
        
        # Generate auth test if needed
        if endpoint.auth_required:
            auth_test = self._generate_auth_test(endpoint)
            test_methods.append(auth_test)
        
        # Generate class
        class_code = f'''class Test{self._to_pascal_case(endpoint.function_name)}:
    """Test cases for {endpoint.function_name} endpoint."""
    
{chr(10).join(test_methods)}
'''
        return class_code
    
    def _generate_happy_path_test(self, endpoint: EndpointInfo) -> str:
        """Generate happy path test."""
        domain_name = endpoint.domain
        snake_domain = self._to_snake_case(domain_name)
        method = endpoint.method.value.lower()
        endpoint_path = endpoint.endpoint
        
        # Generate test data
        test_data = self._generate_test_data(endpoint)
        
        # Generate auth setup if needed
        auth_setup = ""
        auth_header = ""
        if endpoint.auth_required:
            auth_setup = '''        # Create test user and token
        test_user = User(id=1, email="test@example.com", username="testuser")
        token = create_access_token(data={"sub": test_user.email})
        auth_header = {"Authorization": f"Bearer {token}"}'''
            auth_header = ", headers=auth_header"
        
        # Generate response assertion
        response_assertion = self._generate_response_assertion(endpoint)
        
        # Generate test method
        test_method = f'''    @pytest.mark.asyncio
    async def test_{method}_{snake_domain}_success(self):
        """Test successful {method} request to {endpoint_path}."""
{auth_setup}
        
        # Test data
{test_data}
        
        # Mock service response
        with patch("app.api.v1.routes_{snake_domain}.{self._to_pascal_case(domain_name)}Service") as mock_service:
            mock_instance = AsyncMock()
            mock_service.return_value = mock_instance
            
            # Configure mock response
            mock_instance.{endpoint.function_name}.return_value = {self._generate_mock_response(endpoint)}
            
            # Make request
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.{method}("{endpoint_path}"{auth_header})
            
            # Assertions
            assert response.status_code == 200
{response_assertion}
'''
        return test_method
    
    def _generate_error_tests(self, endpoint: EndpointInfo) -> List[str]:
        """Generate error test cases."""
        tests = []
        domain_name = endpoint.domain
        snake_domain = self._to_snake_case(domain_name)
        method = endpoint.method.value.lower()
        endpoint_path = endpoint.endpoint
        
        # 404 test for GET/PUT/DELETE with path params
        if endpoint.path_params and method in ['get', 'put', 'delete']:
            test_404 = f'''    @pytest.mark.asyncio
    async def test_{method}_{snake_domain}_not_found(self):
        """Test 404 error when {snake_domain} not found."""
        # Mock service to return None
        with patch("app.api.v1.routes_{snake_domain}.{self._to_pascal_case(domain_name)}Service") as mock_service:
            mock_instance = AsyncMock()
            mock_service.return_value = mock_instance
            mock_instance.{endpoint.function_name}.return_value = None
            
            # Make request
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.{method}("{endpoint_path}")
            
            # Assertions
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()
'''
            tests.append(test_404)
        
        # 422 test for POST/PUT with invalid data
        if method in ['post', 'put'] and endpoint.request_schema:
            test_422 = f'''    @pytest.mark.asyncio
    async def test_{method}_{snake_domain}_invalid_data(self):
        """Test 422 error with invalid request data."""
        invalid_data = {{"invalid_field": "invalid_value"}}
        
        # Make request
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.{method}("{endpoint_path}", json=invalid_data)
        
        # Assertions
        assert response.status_code == 422
'''
            tests.append(test_422)
        
        return tests
    
    def _generate_auth_test(self, endpoint: EndpointInfo) -> str:
        """Generate authentication test."""
        domain_name = endpoint.domain
        snake_domain = self._to_snake_case(domain_name)
        method = endpoint.method.value.lower()
        endpoint_path = endpoint.endpoint
        
        return f'''    @pytest.mark.asyncio
    async def test_{method}_{snake_domain}_unauthorized(self):
        """Test 401 error when not authenticated."""
        # Make request without auth header
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.{method}("{endpoint_path}")
        
        # Assertions
        assert response.status_code == 401
'''
    
    def _generate_test_data(self, endpoint: EndpointInfo) -> str:
        """Generate test data for endpoint."""
        if endpoint.request_schema:
            # Generate sample data based on schema
            sample_data = {}
            for field in endpoint.request_schema.fields:
                sample_data[field.name] = self._generate_sample_value(field.type)
            
            return f'''        test_data = {sample_data}'''
        else:
            return '''        test_data = {}'''
    
    def _generate_sample_value(self, field_type: str) -> str:
        """Generate sample value for field type."""
        field_type = field_type.lower()
        
        if 'int' in field_type:
            return "1"
        elif 'float' in field_type or 'number' in field_type:
            return "1.0"
        elif 'bool' in field_type:
            return "True"
        elif 'list' in field_type or 'array' in field_type:
            return "[]"
        elif 'dict' in field_type or 'object' in field_type:
            return "{}"
        else:
            return '"test_string"'
    
    def _generate_mock_response(self, endpoint: EndpointInfo) -> str:
        """Generate mock response for endpoint."""
        if endpoint.response_schema:
            # Generate sample response based on schema
            sample_response = {}
            for field in endpoint.response_schema.fields:
                sample_response[field.name] = self._generate_sample_value(field.type)
            
            return f"{sample_response}"
        else:
            return '{"message": "success"}'
    
    def _generate_response_assertion(self, endpoint: EndpointInfo) -> str:
        """Generate response assertion."""
        if endpoint.response_schema:
            return '''            response_data = response.json()
            assert isinstance(response_data, dict)
            # Add specific field assertions based on response schema'''
        else:
            return '''            response_data = response.json()
            assert isinstance(response_data, dict)'''
    
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
