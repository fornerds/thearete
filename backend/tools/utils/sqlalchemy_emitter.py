"""SQLAlchemy code emitter for generating models from ERD schema."""

import os
from typing import Dict, List, Optional, Set
from datetime import datetime

from .mermaid_erd_parser import ERDSchema, Table, Column, Relationship, RelationshipType


class SQLAlchemyEmitter:
    """Generates SQLAlchemy model code from ERD schema."""
    
    def __init__(self, schema: ERDSchema):
        self.schema = schema
        self.imports = set()
        self.relationships = {}  # Table name -> List of relationships
        
    def generate_models(self, output_dir: str, overwrite: bool = False) -> Dict[str, str]:
        """Generate SQLAlchemy model files."""
        # Prepare relationships mapping
        self._prepare_relationships()
        
        generated_files = {}
        
        for table_name, table in self.schema.tables.items():
            model_code = self._generate_model_code(table)
            generated_files[table_name] = model_code
            
            # Write to file
            file_path = os.path.join(output_dir, f"{self._to_snake_case(table_name)}.py")
            
            if os.path.exists(file_path) and not overwrite:
                print(f"파일이 이미 존재합니다 (건너뜀): {file_path}")
                continue
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(model_code)
                
        # Generate __init__.py
        init_code = self._generate_init_code()
        init_path = os.path.join(output_dir, "__init__.py")
        
        if os.path.exists(init_path) and not overwrite:
            print(f"__init__.py가 이미 존재합니다 (건너뜀): {init_path}")
        else:
            with open(init_path, 'w', encoding='utf-8') as f:
                f.write(init_code)
                
        generated_files['__init__'] = init_code
        
        return generated_files
    
    def _prepare_relationships(self) -> None:
        """Prepare relationships mapping for each table."""
        for table_name in self.schema.tables.keys():
            self.relationships[table_name] = []
            
        for relationship in self.schema.relationships:
            self.relationships[relationship.from_table].append(relationship)
            self.relationships[relationship.to_table].append(relationship)
    
    def _generate_model_code(self, table: Table) -> str:
        """Generate SQLAlchemy model code for a table."""
        class_name = self._to_pascal_case(table.name)
        
        # Collect imports
        imports = self._collect_imports(table)
        
        # Generate columns
        columns_code = self._generate_columns_code(table)
        
        # Generate relationships
        relationships_code = self._generate_relationships_code(table)
        
        # Generate __repr__ method
        repr_code = self._generate_repr_code(table)
        
        # Generate docstring
        docstring = self._generate_docstring(table)
        
        # Combine all parts
        code = f'''"""Database model for {table.name} table."""

{imports}

from app.db.base import Base


class {class_name}(Base):
    """{docstring}"""
    
    __tablename__ = "{self._to_snake_case(table.name)}"
    
{columns_code}
{relationships_code}
{repr_code}
'''
        return code
    
    def _collect_imports(self, table: Table) -> str:
        """Collect necessary imports for the table."""
        imports = set()
        
        # Base imports
        imports.add("from typing import List, Optional")
        imports.add("from datetime import datetime")
        
        # Column type imports
        for column in table.columns:
            sqlalchemy_type = self._get_sqlalchemy_type(column.data_type)
            
            if sqlalchemy_type in ['String', 'Text']:
                imports.add("from sqlalchemy import String, Text")
            elif sqlalchemy_type in ['Integer', 'BigInteger', 'SmallInteger']:
                imports.add("from sqlalchemy import Integer, BigInteger, SmallInteger")
            elif sqlalchemy_type == 'Boolean':
                imports.add("from sqlalchemy import Boolean")
            elif sqlalchemy_type == 'DateTime':
                imports.add("from sqlalchemy import DateTime")
            elif sqlalchemy_type == 'Date':
                imports.add("from sqlalchemy import Date")
            elif sqlalchemy_type == 'Time':
                imports.add("from sqlalchemy import Time")
            elif sqlalchemy_type == 'Float':
                imports.add("from sqlalchemy import Float")
            elif sqlalchemy_type == 'Numeric':
                imports.add("from sqlalchemy import Numeric")
            elif sqlalchemy_type == 'Enum':
                imports.add("from sqlalchemy import Enum")
            elif sqlalchemy_type == 'JSON':
                imports.add("from sqlalchemy import JSON")
        
        # Foreign key imports
        has_fk = any(col.is_foreign_key for col in table.columns)
        if has_fk:
            imports.add("from sqlalchemy import ForeignKey")
        
        # Relationship imports
        has_relationships = table.name in self.relationships and self.relationships[table.name]
        if has_relationships:
            imports.add("from sqlalchemy.orm import relationship")
        
        # Mapped imports
        imports.add("from sqlalchemy.orm import Mapped, mapped_column")
        
        # Convert to sorted list and format
        import_list = sorted(list(imports))
        return '\n'.join(import_list)
    
    def _generate_columns_code(self, table: Table) -> str:
        """Generate column definitions code."""
        lines = []
        
        for column in table.columns:
            line = self._generate_column_line(column)
            lines.append(line)
        
        return '\n'.join(lines)
    
    def _generate_column_line(self, column: Column) -> str:
        """Generate a single column definition line."""
        sqlalchemy_type = self._get_sqlalchemy_type(column.data_type)
        python_type = self._get_python_type(column.data_type, column.is_nullable)
        
        # Start with type annotation
        line = f"    {column.name}: Mapped[{python_type}] = mapped_column("
        
        # Add SQLAlchemy type
        if sqlalchemy_type == 'String':
            # Determine string length
            length = self._get_string_length(column.data_type)
            line += f"{sqlalchemy_type}({length})"
        elif sqlalchemy_type == 'Enum':
            # Handle enum type
            enum_values = self._get_enum_values(column.comment)
            if enum_values:
                line += f"{sqlalchemy_type}({enum_values})"
            else:
                line += "String"
        else:
            line += sqlalchemy_type
        
        # Add constraints
        constraints = []
        
        if column.is_primary_key:
            constraints.append("primary_key=True")
            constraints.append("index=True")
        
        if column.is_foreign_key and column.foreign_table:
            fk_table = self._to_snake_case(column.foreign_table)
            fk_column = column.foreign_column or 'id'
            constraints.append(f'ForeignKey("{fk_table}.{fk_column}")')
        
        if not column.is_nullable:
            constraints.append("nullable=False")
        
        if column.is_unique:
            constraints.append("unique=True")
        
        if column.default_value:
            default_val = self._format_default_value(column.default_value, column.data_type)
            constraints.append(f"default={default_val}")
        
        # Add comment
        if column.comment:
            constraints.append(f'comment="{column.comment}"')
        
        # Add special handling for created_at/updated_at
        if column.name in ['created_at', 'updated_at']:
            if column.name == 'created_at':
                constraints.append("default=datetime.utcnow")
            elif column.name == 'updated_at':
                constraints.append("default=datetime.utcnow")
                constraints.append("onupdate=datetime.utcnow")
        
        # Add constraints to line
        if constraints:
            line += ", " + ", ".join(constraints)
        
        line += ")"
        
        return line
    
    def _generate_relationships_code(self, table: Table) -> str:
        """Generate relationship definitions code."""
        if table.name not in self.relationships or not self.relationships[table.name]:
            return ""
        
        lines = []
        lines.append("")
        lines.append("    # Relationships")
        
        for relationship in self.relationships[table.name]:
            if relationship.from_table == table.name:
                # This table is the "from" side
                rel_code = self._generate_relationship_code(relationship, is_from_side=True)
            else:
                # This table is the "to" side
                rel_code = self._generate_relationship_code(relationship, is_from_side=False)
            
            if rel_code:
                lines.append(rel_code)
        
        return '\n'.join(lines)
    
    def _generate_relationship_code(self, relationship: Relationship, is_from_side: bool) -> str:
        """Generate relationship code for a specific relationship."""
        if relationship.relationship_type == RelationshipType.MANY_TO_MANY:
            # Many-to-many relationships are handled separately
            return ""
        
        if is_from_side:
            # From side of relationship
            if relationship.relationship_type == RelationshipType.ONE_TO_MANY:
                # One-to-many: this table has many of the other table
                target_table = self._to_pascal_case(relationship.to_table)
                target_attr = self._to_snake_case(relationship.to_table)
                
                return f'    {target_attr}: Mapped[List["{target_table}"]] = relationship("{target_table}", back_populates="{self._to_snake_case(relationship.from_table)}", cascade="all, delete-orphan")'
            
            elif relationship.relationship_type == RelationshipType.MANY_TO_ONE:
                # Many-to-one: this table belongs to the other table
                target_table = self._to_pascal_case(relationship.to_table)
                target_attr = self._to_snake_case(relationship.to_table)
                
                return f'    {target_attr}: Mapped["{target_table}"] = relationship("{target_table}", back_populates="{self._to_snake_case(relationship.from_table)}")'
            
            elif relationship.relationship_type == RelationshipType.ONE_TO_ONE:
                # One-to-one: this table has one of the other table
                target_table = self._to_pascal_case(relationship.to_table)
                target_attr = self._to_snake_case(relationship.to_table)
                
                return f'    {target_attr}: Mapped[Optional["{target_table}"]] = relationship("{target_table}", back_populates="{self._to_snake_case(relationship.from_table)}", uselist=False)'
        
        else:
            # To side of relationship
            if relationship.relationship_type == RelationshipType.ONE_TO_MANY:
                # One-to-many: this table belongs to the other table
                target_table = self._to_pascal_case(relationship.from_table)
                target_attr = self._to_snake_case(relationship.from_table)
                
                return f'    {target_attr}: Mapped["{target_table}"] = relationship("{target_table}", back_populates="{self._to_snake_case(relationship.to_table)}")'
            
            elif relationship.relationship_type == RelationshipType.MANY_TO_ONE:
                # Many-to-one: this table has many of the other table
                target_table = self._to_pascal_case(relationship.from_table)
                target_attr = self._to_snake_case(relationship.from_table)
                
                return f'    {target_attr}: Mapped[List["{target_table}"]] = relationship("{target_table}", back_populates="{self._to_snake_case(relationship.to_table)}", cascade="all, delete-orphan")'
            
            elif relationship.relationship_type == RelationshipType.ONE_TO_ONE:
                # One-to-one: this table has one of the other table
                target_table = self._to_pascal_case(relationship.from_table)
                target_attr = self._to_snake_case(relationship.from_table)
                
                return f'    {target_attr}: Mapped[Optional["{target_table}"]] = relationship("{target_table}", back_populates="{self._to_snake_case(relationship.to_table)}", uselist=False)'
        
        return ""
    
    def _generate_repr_code(self, table: Table) -> str:
        """Generate __repr__ method code."""
        # Find primary key column
        pk_column = next((col for col in table.columns if col.is_primary_key), None)
        if not pk_column:
            return ""
        
        # Find a few key columns for representation
        key_columns = []
        for col in table.columns[:3]:  # Take first 3 columns
            if col.name != pk_column.name:
                key_columns.append(col)
        
        if not key_columns:
            return f'    def __repr__(self) -> str:\n        return f"<{self._to_pascal_case(table.name)}({pk_column.name}={{self.{pk_column.name}}})>"'
        
        # Generate repr with key columns
        repr_parts = [f"{pk_column.name}={{self.{pk_column.name}}}"]
        for col in key_columns:
            repr_parts.append(f"{col.name}='{{self.{col.name}}}'")
        
        repr_str = ", ".join(repr_parts)
        
        return f'    def __repr__(self) -> str:\n        return f"<{self._to_pascal_case(table.name)}({repr_str})>"'
    
    def _generate_docstring(self, table: Table) -> str:
        """Generate docstring for the table."""
        if table.comment:
            return table.comment
        return f"{self._to_pascal_case(table.name)} model."
    
    def _generate_init_code(self) -> str:
        """Generate __init__.py code."""
        imports = []
        
        for table_name in self.schema.tables.keys():
            class_name = self._to_pascal_case(table_name)
            module_name = self._to_snake_case(table_name)
            imports.append(f"from app.db.models.{module_name} import {class_name}  # noqa: F401")
        
        imports.sort()
        
        # Generate __all__ list
        all_classes = [self._to_pascal_case(name) for name in self.schema.tables.keys()]
        all_classes.sort()
        
        code = f'''"""Database models package."""

# Import all models here to ensure they are registered with SQLAlchemy
{chr(10).join(imports)}

__all__ = {all_classes}
'''
        return code
    
    def _get_sqlalchemy_type(self, mermaid_type: str) -> str:
        """Get SQLAlchemy type from Mermaid type."""
        type_mapping = {
            'bigint': 'BigInteger',
            'int': 'Integer',
            'tinyint': 'SmallInteger',
            'smallint': 'SmallInteger',
            'serial': 'Integer',
            'string': 'String',
            'varchar': 'String',
            'text': 'Text',
            'boolean': 'Boolean',
            'bool': 'Boolean',
            'datetime': 'DateTime',
            'date': 'Date',
            'time': 'Time',
            'float': 'Float',
            'double': 'Float',
            'decimal': 'Numeric',
            'numeric': 'Numeric',
            'enum': 'Enum',
            'json': 'JSON',
            'uuid': 'String',
            'timestamptz': 'DateTime',
            'timestamp': 'DateTime',
        }
        
        return type_mapping.get(mermaid_type.lower(), 'String')
    
    def _get_python_type(self, mermaid_type: str, is_nullable: bool) -> str:
        """Get Python type annotation from Mermaid type."""
        type_mapping = {
            'bigint': 'int',
            'int': 'int',
            'tinyint': 'int',
            'smallint': 'int',
            'serial': 'int',
            'string': 'str',
            'varchar': 'str',
            'text': 'str',
            'boolean': 'bool',
            'bool': 'bool',
            'datetime': 'datetime',
            'date': 'datetime',
            'time': 'datetime',
            'float': 'float',
            'double': 'float',
            'decimal': 'float',
            'numeric': 'float',
            'enum': 'str',
            'json': 'dict',
            'uuid': 'str',
            'timestamptz': 'datetime',
            'timestamp': 'datetime',
        }
        
        python_type = type_mapping.get(mermaid_type.lower(), 'str')
        
        if is_nullable and python_type not in ['dict', 'list']:
            return f"Optional[{python_type}]"
        
        return python_type
    
    def _get_string_length(self, mermaid_type: str) -> int:
        """Get string length from Mermaid type."""
        if mermaid_type.lower() == 'text':
            return 0  # No length for Text
        
        # Extract length from varchar(n) format
        import re
        match = re.search(r'varchar\((\d+)\)', mermaid_type.lower())
        if match:
            return int(match.group(1))
        
        # Default lengths
        if mermaid_type.lower() in ['string', 'varchar']:
            return 255
        
        return 255
    
    def _get_enum_values(self, comment: Optional[str]) -> Optional[str]:
        """Extract enum values from comment."""
        if not comment:
            return None
        
        # Look for enum values in comment (e.g., "M/F", "A/B/C")
        import re
        match = re.search(r'\(([^)]+)\)', comment)
        if match:
            values = match.group(1).split('/')
            quoted_values = [f'"{v.strip()}"' for v in values]
            return f"({', '.join(quoted_values)})"
        
        return None
    
    def _format_default_value(self, default_value: str, data_type: str) -> str:
        """Format default value for SQLAlchemy."""
        if data_type.lower() in ['boolean', 'bool']:
            return default_value.lower()
        elif data_type.lower() in ['string', 'varchar', 'text']:
            return f'"{default_value}"'
        elif data_type.lower() in ['datetime', 'timestamptz', 'timestamp']:
            if default_value.lower() == 'now()':
                return 'datetime.utcnow'
            return f'"{default_value}"'
        else:
            return default_value
    
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
