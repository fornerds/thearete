"""Service and repository generator for Excel API specifications."""

import os
from typing import Dict, List, Optional
from pathlib import Path

from .xlsx_api_parser import DomainInfo, EndpointInfo


class ServiceRepositoryGenerator:
    """Generator for service and repository files."""
    
    def __init__(self, services_dir: str = "app/services", repos_dir: str = "app/db/repositories"):
        self.services_dir = Path(services_dir)
        self.repos_dir = Path(repos_dir)
        self.services_dir.mkdir(parents=True, exist_ok=True)
        self.repos_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_services_and_repos(self, domains: Dict[str, DomainInfo], overwrite: bool = False) -> Dict[str, str]:
        """Generate service and repository files for all domains."""
        generated_files = {}
        
        for domain_name, domain_info in domains.items():
            # Generate service file
            service_code = self._generate_service_code(domain_info)
            service_file_path = self.services_dir / f"{self._to_snake_case(domain_name)}_service.py"
            
            if service_file_path.exists() and not overwrite:
                print(f"파일이 이미 존재합니다 (건너뜀): {service_file_path}")
            else:
                with open(service_file_path, 'w', encoding='utf-8') as f:
                    f.write(service_code)
                generated_files[f"{domain_name}_service"] = service_code
                print(f"✅ 서비스 생성 완료: {service_file_path}")
            
            # Generate repository file
            repo_code = self._generate_repository_code(domain_info)
            repo_file_path = self.repos_dir / f"{self._to_snake_case(domain_name)}_repo.py"
            
            if repo_file_path.exists() and not overwrite:
                print(f"파일이 이미 존재합니다 (건너뜀): {repo_file_path}")
            else:
                with open(repo_file_path, 'w', encoding='utf-8') as f:
                    f.write(repo_code)
                generated_files[f"{domain_name}_repo"] = repo_code
                print(f"✅ 리포지토리 생성 완료: {repo_file_path}")
        
        return generated_files
    
    def _generate_service_code(self, domain_info: DomainInfo) -> str:
        """Generate service code for a domain."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Collect imports
        imports = self._collect_service_imports(domain_info)
        
        # Generate service class
        service_class = self._generate_service_class(domain_info)
        
        # Combine all parts
        code = f'''"""Service layer for {domain_name} domain."""

{imports}

{service_class}
'''
        return code
    
    def _generate_repository_code(self, domain_info: DomainInfo) -> str:
        """Generate repository code for a domain."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Collect imports
        imports = self._collect_repository_imports(domain_info)
        
        # Generate repository class
        repo_class = self._generate_repository_class(domain_info)
        
        # Combine all parts
        code = f'''"""Repository layer for {domain_name} domain."""

{imports}

{repo_class}
'''
        return code
    
    def _collect_service_imports(self, domain_info: DomainInfo) -> str:
        """Collect necessary imports for service."""
        imports = set()
        
        # Base imports
        imports.add("from typing import List, Optional, Any")
        imports.add("from sqlalchemy.ext.asyncio import AsyncSession")
        
        # Repository import
        snake_domain = self._to_snake_case(domain_info.name)
        imports.add(f"from app.db.repositories.{snake_domain}_repo import {self._to_pascal_case(domain_info.name)}Repository")
        
        # Schema imports
        has_request_schemas = any(ep.request_schema for ep in domain_info.endpoints)
        has_response_schemas = any(ep.response_schema for ep in domain_info.endpoints)
        
        if has_request_schemas or has_response_schemas:
            imports.add("from app.schemas import *")
        
        # Model import
        imports.add(f"from app.db.models.{snake_domain} import {self._to_pascal_case(domain_info.name)}")
        
        # Convert to sorted list and format
        import_list = sorted(list(imports))
        return '\n'.join(import_list)
    
    def _collect_repository_imports(self, domain_info: DomainInfo) -> str:
        """Collect necessary imports for repository."""
        imports = set()
        
        # Base imports
        imports.add("from typing import List, Optional, Any")
        imports.add("from sqlalchemy.ext.asyncio import AsyncSession")
        imports.add("from sqlalchemy import select, update, delete")
        imports.add("from sqlalchemy.orm import selectinload")
        
        # Model import
        snake_domain = self._to_snake_case(domain_info.name)
        imports.add(f"from app.db.models.{snake_domain} import {self._to_pascal_case(domain_info.name)}")
        
        # Convert to sorted list and format
        import_list = sorted(list(imports))
        return '\n'.join(import_list)
    
    def _generate_service_class(self, domain_info: DomainInfo) -> str:
        """Generate service class."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        # Generate methods
        methods = []
        
        # Generate CRUD methods based on endpoints
        for endpoint in domain_info.endpoints:
            if endpoint.method.value == "GET":
                if endpoint.path_params:
                    # Get by ID
                    method = self._generate_get_by_id_method(domain_info)
                else:
                    # List all
                    method = self._generate_list_method(domain_info)
            elif endpoint.method.value == "POST":
                method = self._generate_create_method(domain_info)
            elif endpoint.method.value == "PUT":
                method = self._generate_update_method(domain_info)
            elif endpoint.method.value == "DELETE":
                method = self._generate_delete_method(domain_info)
            else:
                continue
            
            methods.append(method)
        
        # Remove duplicates
        unique_methods = []
        method_names = set()
        for method in methods:
            method_name = method.split('async def ')[1].split('(')[0]
            if method_name not in method_names:
                unique_methods.append(method)
                method_names.add(method_name)
        
        # Generate class
        class_code = f'''class {pascal_domain}Service:
    """Service for {domain_name} domain operations."""
    
    def __init__(self):
        self.repository = {pascal_domain}Repository()

{chr(10).join(unique_methods)}
'''
        return class_code
    
    def _generate_repository_class(self, domain_info: DomainInfo) -> str:
        """Generate repository class."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_info.name)
        
        # Generate methods
        methods = []
        
        # Generate CRUD methods based on endpoints
        for endpoint in domain_info.endpoints:
            if endpoint.method.value == "GET":
                if endpoint.path_params:
                    # Get by ID
                    method = self._generate_repo_get_by_id_method(domain_info)
                else:
                    # List all
                    method = self._generate_repo_list_method(domain_info)
            elif endpoint.method.value == "POST":
                method = self._generate_repo_create_method(domain_info)
            elif endpoint.method.value == "PUT":
                method = self._generate_repo_update_method(domain_info)
            elif endpoint.method.value == "DELETE":
                method = self._generate_repo_delete_method(domain_info)
            else:
                continue
            
            methods.append(method)
        
        # Remove duplicates and empty methods
        unique_methods = []
        method_names = set()
        for method in methods:
            if method and 'async def ' in method:
                method_name = method.split('async def ')[1].split('(')[0]
                if method_name not in method_names:
                    unique_methods.append(method)
                    method_names.add(method_name)
        
        # Generate class
        model_class = pascal_domain
        model_var = snake_domain
        
        class_code = f'''class {model_class}Repository:
    """Repository for {domain_name} domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, {model_var}_id: int) -> Optional[{model_class}]:
        """Get {model_var} by ID."""
        result = await db.execute(
            select({model_class}).where({model_class}.id == {model_var}_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[{model_class}]:
        """Get all {model_var}s with pagination."""
        result = await db.execute(
            select({model_class}).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, {model_var}_data: dict) -> {model_class}:
        """Create new {model_var}."""
        {model_var} = {model_class}(**{model_var}_data)
        db.add({model_var})
        await db.commit()
        await db.refresh({model_var})
        return {model_var}
    
    async def update(self, db: AsyncSession, {model_var}_id: int, {model_var}_data: dict) -> Optional[{model_class}]:
        """Update {model_var} by ID."""
        result = await db.execute(
            update({model_class})
            .where({model_class}.id == {model_var}_id)
            .values(**{model_var}_data)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, {model_var}_id)
        return None
    
    async def delete(self, db: AsyncSession, {model_var}_id: int) -> bool:
        """Delete {model_var} by ID."""
        result = await db.execute(
            delete({model_class}).where({model_class}.id == {model_var}_id)
        )
        await db.commit()
        return result.rowcount > 0

{chr(10).join(unique_methods)}
'''
        return class_code
    
    def _generate_get_by_id_method(self, domain_info: DomainInfo) -> str:
        """Generate get by ID method for service."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        return f'''    async def get_{snake_domain}_by_id(self, {snake_domain}_id: int) -> Optional[{pascal_domain}]:
        """Get {snake_domain} by ID."""
        return await self.repository.get_by_id({snake_domain}_id)'''
    
    def _generate_list_method(self, domain_info: DomainInfo) -> str:
        """Generate list method for service."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        return f'''    async def list_{snake_domain}s(self, skip: int = 0, limit: int = 100) -> List[{pascal_domain}]:
        """List all {snake_domain}s."""
        return await self.repository.get_all(skip=skip, limit=limit)'''
    
    def _generate_create_method(self, domain_info: DomainInfo) -> str:
        """Generate create method for service."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        return f'''    async def create_{snake_domain}(self, request_data: dict) -> {pascal_domain}:
        """Create new {snake_domain}."""
        return await self.repository.create(request_data)'''
    
    def _generate_update_method(self, domain_info: DomainInfo) -> str:
        """Generate update method for service."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        return f'''    async def update_{snake_domain}(self, {snake_domain}_id: int, request_data: dict) -> Optional[{pascal_domain}]:
        """Update {snake_domain} by ID."""
        return await self.repository.update({snake_domain}_id, request_data)'''
    
    def _generate_delete_method(self, domain_info: DomainInfo) -> str:
        """Generate delete method for service."""
        domain_name = domain_info.name
        snake_domain = self._to_snake_case(domain_name)
        pascal_domain = self._to_pascal_case(domain_name)
        
        return f'''    async def delete_{snake_domain}(self, {snake_domain}_id: int) -> bool:
        """Delete {snake_domain} by ID."""
        return await self.repository.delete({snake_domain}_id)'''
    
    def _generate_repo_get_by_id_method(self, domain_info: DomainInfo) -> str:
        """Generate get by ID method for repository."""
        # This is already included in the base repository class
        return ""
    
    def _generate_repo_list_method(self, domain_info: DomainInfo) -> str:
        """Generate list method for repository."""
        # This is already included in the base repository class
        return ""
    
    def _generate_repo_create_method(self, domain_info: DomainInfo) -> str:
        """Generate create method for repository."""
        # This is already included in the base repository class
        return ""
    
    def _generate_repo_update_method(self, domain_info: DomainInfo) -> str:
        """Generate update method for repository."""
        # This is already included in the base repository class
        return ""
    
    def _generate_repo_delete_method(self, domain_info: DomainInfo) -> str:
        """Generate delete method for repository."""
        # This is already included in the base repository class
        return ""
    
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
