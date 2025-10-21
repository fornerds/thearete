"""FastAPI router generator for Excel API specifications."""

import os
from typing import Dict, List, Optional
from pathlib import Path

from .xlsx_api_parser import DomainInfo, EndpointInfo, SchemaInfo, FieldInfo


class FastAPIRouterGenerator:
    """Generator for FastAPI router files."""
    
    def __init__(self, output_dir: str = "app/api/v1"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_routers(self, domains: Dict[str, DomainInfo], overwrite: bool = False) -> Dict[str, str]:
        """Generate router files for all domains."""
        generated_files = {}
        
        for domain_name, domain_info in domains.items():
            router_code = self._generate_router_code(domain_info)
            file_path = self.output_dir / f"routes_{self._to_snake_case(domain_name)}.py"
            
            if file_path.exists() and not overwrite:
                print(f"파일이 이미 존재합니다 (건너뜀): {file_path}")
                continue
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(router_code)
            
            generated_files[domain_name] = router_code
            print(f"✅ 라우터 생성 완료: {file_path}")
        
        return generated_files
    
    def _generate_router_code(self, domain_info: DomainInfo) -> str:
        """Generate router code for a domain."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        
        # Collect imports
        imports = self._collect_router_imports(domain_info)
        
        # Generate router definition
        router_def = f"router = APIRouter(prefix=\"/v1/{snake_domain}\", tags=[\"{domain_name}\"])"
        
        # Generate endpoint functions
        endpoint_functions = []
        for endpoint in domain_info.endpoints:
            function_code = self._generate_endpoint_function(endpoint)
            endpoint_functions.append(function_code)
        
        # Combine all parts
        code = f'''"""FastAPI router for {domain_name} domain."""

{imports}

{router_def}

{chr(10).join(endpoint_functions)}
'''
        return code
    
    def _collect_router_imports(self, domain_info: DomainInfo) -> str:
        """Collect necessary imports for router."""
        imports = set()
        
        # Base imports
        imports.add("from fastapi import APIRouter, Depends, HTTPException, status")
        imports.add("from typing import List, Optional")
        
        # Check if any endpoint requires authentication
        has_auth = any(ep.auth_required for ep in domain_info.endpoints)
        if has_auth:
            imports.add("from app.core.auth import get_current_user")
            imports.add("from app.db.models.user import User")
        
        # Check if any endpoint has path parameters
        has_path_params = any(ep.path_params for ep in domain_info.endpoints)
        if has_path_params:
            imports.add("from fastapi import Path")
        
        # Check if any endpoint has request/response schemas
        has_request_schemas = any(ep.request_schema for ep in domain_info.endpoints)
        has_response_schemas = any(ep.response_schema for ep in domain_info.endpoints)
        
        if has_request_schemas or has_response_schemas:
            imports.add("from app.schemas import *")
        
        # Service imports
        snake_domain = self._to_snake_case(domain_info.name)
        imports.add(f"from app.services.{snake_domain}_service import {self._to_pascal_case(domain_info.name)}Service")
        
        # Convert to sorted list and format
        import_list = sorted(list(imports))
        return '\n'.join(import_list)
    
    def _generate_endpoint_function(self, endpoint: EndpointInfo) -> str:
        """Generate function code for an endpoint."""
        function_name = endpoint.function_name
        method = endpoint.method.value.lower()
        endpoint_path = endpoint.endpoint
        
        # Generate function signature
        signature_parts = [f"@router.{method}(\"{endpoint_path}\")"]
        
        # Add summary and description
        if endpoint.description:
            signature_parts.append(f"@router.{method}(\"{endpoint_path}\", summary=\"{endpoint.description}\")")
        
        # Generate function parameters
        params = self._generate_function_parameters(endpoint)
        
        # Generate function body
        body = self._generate_function_body(endpoint)
        
        # Generate response model
        response_model = ""
        if endpoint.response_schema:
            response_model = f" -> {endpoint.response_schema.name}"
        
        # Combine all parts
        function_code = f'''{chr(10).join(signature_parts)}
async def {function_name}({params}){response_model}:
    """{endpoint.description or f"{endpoint.method.value} {endpoint.endpoint}"}"""
{body}
'''
        return function_code
    
    def _generate_function_parameters(self, endpoint: EndpointInfo) -> str:
        """Generate function parameters."""
        params = []
        
        # Add path parameters
        for param in endpoint.path_params:
            params.append(f"{param}: int = Path(..., description=f\"{param} ID\")")
        
        # Add request body
        if endpoint.request_schema:
            params.append(f"request: {endpoint.request_schema.name}")
        
        # Add authentication
        if endpoint.auth_required:
            params.append("current_user: User = Depends(get_current_user)")
        
        return ", ".join(params)
    
    def _generate_function_body(self, endpoint: EndpointInfo) -> str:
        """Generate function body."""
        domain_name = endpoint.domain
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Generate service call
        service_call = f"service = {pascal_domain}Service()"
        
        # Generate method call based on HTTP method
        if endpoint.method.value == "GET":
            if endpoint.path_params:
                # Get single item
                method_call = f"result = await service.get_{snake_domain}_by_id({endpoint.path_params[0]})"
            else:
                # List items
                method_call = f"result = await service.list_{snake_domain}s()"
        elif endpoint.method.value == "POST":
            method_call = f"result = await service.create_{snake_domain}(request)"
        elif endpoint.method.value == "PUT":
            method_call = f"result = await service.update_{snake_domain}({endpoint.path_params[0]}, request)"
        elif endpoint.method.value == "DELETE":
            method_call = f"result = await service.delete_{snake_domain}({endpoint.path_params[0]})"
        else:
            method_call = f"result = await service.{endpoint.function_name}()"
        
        # Generate error handling
        error_handling = f'''    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{pascal_domain} not found"
        )'''
        
        # Generate return statement
        return_statement = "    return result"
        
        # Combine body parts
        body_parts = [
            f"    {service_call}",
            f"    {method_call}",
            error_handling,
            return_statement
        ]
        
        return '\n'.join(body_parts)
    
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
