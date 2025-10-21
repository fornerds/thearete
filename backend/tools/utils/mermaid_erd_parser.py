"""Mermaid ERD parser for converting to SQLAlchemy models."""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum


class RelationshipType(Enum):
    """Relationship types in Mermaid ERD."""
    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"


@dataclass
class Column:
    """Represents a database column."""
    name: str
    data_type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_nullable: bool = True
    is_unique: bool = False
    default_value: Optional[str] = None
    comment: Optional[str] = None
    foreign_table: Optional[str] = None
    foreign_column: Optional[str] = None


@dataclass
class Table:
    """Represents a database table."""
    name: str
    columns: List[Column] = field(default_factory=list)
    comment: Optional[str] = None


@dataclass
class Relationship:
    """Represents a relationship between tables."""
    from_table: str
    to_table: str
    relationship_type: RelationshipType
    from_cardinality: str  # "||", "|o", "o|", "o{", "||", "o{"
    to_cardinality: str    # "||", "|o", "o|", "o{", "||", "o{"
    label: Optional[str] = None


@dataclass
class ERDSchema:
    """Complete ERD schema representation."""
    tables: Dict[str, Table] = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)


class MermaidERDParser:
    """Parser for Mermaid ERD syntax."""
    
    # Type mapping from Mermaid to SQLAlchemy
    TYPE_MAPPING = {
        'bigint': 'BigInteger',
        'int': 'Integer',
        'tinyint': 'SmallInteger',
        'smallint': 'SmallInteger',
        'serial': 'Integer',  # Will be handled as Identity
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
        'uuid': 'String',  # UUID as String(36)
        'timestamptz': 'DateTime',
        'timestamp': 'DateTime',
    }
    
    def __init__(self):
        self.schema = ERDSchema()
        self.current_table = None
        
    def parse(self, content: str) -> ERDSchema:
        """Parse Mermaid ERD content and return ERDSchema."""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('%%'):
                continue
                
            # Skip erDiagram declaration
            if line.startswith('erDiagram'):
                continue
                
            try:
                # Parse relationship definition first (more specific)
                if self._is_relationship_definition(line):
                    self._parse_relationship_definition(line, line_num)
                # Parse table definition
                elif self._is_table_definition(line):
                    self._parse_table_definition(line, line_num)
                # Parse table content (columns)
                elif self._is_table_content(line):
                    self._parse_table_content(line, line_num)
                    
            except Exception as e:
                raise ValueError(f"파싱 오류 (라인 {line_num}): {line}\n오류: {str(e)}")
                
        return self.schema
    
    def _is_table_definition(self, line: str) -> bool:
        """Check if line is a table definition."""
        return re.match(r'^\s*[A-Z_][A-Z0-9_]*\s*\{', line) is not None
    
    def _is_table_content(self, line: str) -> bool:
        """Check if line is table content (columns)."""
        return re.match(r'^\s*[a-z_][a-z0-9_]*\s+[a-z]+', line) is not None
    
    def _is_relationship_definition(self, line: str) -> bool:
        """Check if line is a relationship definition."""
        # More flexible pattern to match relationship definitions
        pattern = r'^\s*[A-Z_][A-Z0-9_]*\s+[|o]{2}[-]{1,2}[o|]\{\s*[A-Z_][A-Z0-9_]*'
        return re.match(pattern, line) is not None
    
    def _parse_table_definition(self, line: str, line_num: int) -> None:
        """Parse table definition line."""
        match = re.match(r'^\s*([A-Z_][A-Z0-9_]*)\s*\{', line)
        if not match:
            raise ValueError(f"테이블 정의 형식이 올바르지 않습니다: {line}")
            
        table_name = match.group(1)
        self.current_table = table_name
        
        # Extract comment if present
        comment_match = re.search(r'"([^"]*)"', line)
        comment = comment_match.group(1) if comment_match else None
        
        if table_name not in self.schema.tables:
            self.schema.tables[table_name] = Table(name=table_name, comment=comment)
        else:
            self.schema.tables[table_name].comment = comment
    
    def _parse_table_content(self, line: str, line_num: int) -> None:
        """Parse table content (columns) line."""
        if not self.current_table:
            raise ValueError("테이블 정의 없이 컬럼이 정의되었습니다")
            
        # Parse column definition
        # Format: type name "comment" [constraints]
        parts = line.strip().split()
        if len(parts) < 2:
            raise ValueError(f"컬럼 정의 형식이 올바르지 않습니다: {line}")
            
        data_type = parts[0]
        column_name = parts[1]
        
        # Extract comment
        comment = None
        comment_match = re.search(r'"([^"]*)"', line)
        if comment_match:
            comment = comment_match.group(1)
        
        # Parse constraints
        constraints = self._parse_constraints(line)
        
        # Create column
        column = Column(
            name=column_name,
            data_type=data_type,
            comment=comment,
            **constraints
        )
        
        self.schema.tables[self.current_table].columns.append(column)
    
    def _parse_constraints(self, line: str) -> Dict[str, any]:
        """Parse column constraints from line."""
        constraints = {
            'is_primary_key': False,
            'is_foreign_key': False,
            'is_nullable': True,
            'is_unique': False,
            'default_value': None,
            'foreign_table': None,
            'foreign_column': None,
        }
        
        # Check for PK
        if 'PK' in line:
            constraints['is_primary_key'] = True
            constraints['is_nullable'] = False
            
        # Check for FK
        if 'FK' in line:
            constraints['is_foreign_key'] = True
            constraints['is_nullable'] = False
            
        # Check for NOT NULL (explicit)
        if 'NOT NULL' in line.upper():
            constraints['is_nullable'] = False
            
        # Check for UNIQUE
        if 'UNIQUE' in line.upper():
            constraints['is_unique'] = True
            
        # Check for DEFAULT value
        default_match = re.search(r"DEFAULT\s+([^\s]+)", line, re.IGNORECASE)
        if default_match:
            constraints['default_value'] = default_match.group(1)
            
        return constraints
    
    def _parse_relationship_definition(self, line: str, line_num: int) -> None:
        """Parse relationship definition line."""
        # Format: TABLE1 ||--o{ TABLE2 : "label"
        pattern = r'^\s*([A-Z_][A-Z0-9_]*)\s+([|o]{2}[-]{1,2}[o|]\{)\s*([A-Z_][A-Z0-9_]*)(?:\s*:\s*"([^"]*)")?'
        match = re.match(pattern, line)
        
        if not match:
            raise ValueError(f"관계 정의 형식이 올바르지 않습니다: {line}")
            
        from_table = match.group(1)
        cardinality = match.group(2)
        to_table = match.group(3)
        label = match.group(4) if match.group(4) else None
        
        # Parse cardinality
        from_cardinality, to_cardinality = self._parse_cardinality(cardinality)
        
        # Determine relationship type
        relationship_type = self._determine_relationship_type(from_cardinality, to_cardinality)
        
        relationship = Relationship(
            from_table=from_table,
            to_table=to_table,
            relationship_type=relationship_type,
            from_cardinality=from_cardinality,
            to_cardinality=to_cardinality,
            label=label
        )
        
        self.schema.relationships.append(relationship)
    
    def _parse_cardinality(self, cardinality: str) -> Tuple[str, str]:
        """Parse cardinality string into from/to cardinalities."""
        # Split cardinality string (e.g., "||--o{" -> "||" and "o{")
        parts = cardinality.split('--')
        if len(parts) != 2:
            raise ValueError(f"카디널리티 형식이 올바르지 않습니다: {cardinality}")
            
        return parts[0], parts[1]
    
    def _determine_relationship_type(self, from_cardinality: str, to_cardinality: str) -> RelationshipType:
        """Determine relationship type from cardinalities."""
        # One-to-one: || -- ||
        if from_cardinality == "||" and to_cardinality == "||":
            return RelationshipType.ONE_TO_ONE
            
        # One-to-many: || -- o{
        if from_cardinality == "||" and to_cardinality == "o{":
            return RelationshipType.ONE_TO_MANY
            
        # Many-to-one: o{ -- ||
        if from_cardinality == "o{" and to_cardinality == "||":
            return RelationshipType.MANY_TO_ONE
            
        # Many-to-many: o{ -- o{
        if from_cardinality == "o{" and to_cardinality == "o{":
            return RelationshipType.MANY_TO_MANY
            
        # Handle other cases (|o, o|, etc.)
        if "o" in from_cardinality and "o" in to_cardinality:
            return RelationshipType.MANY_TO_MANY
        elif "||" in from_cardinality and "o" in to_cardinality:
            return RelationshipType.ONE_TO_MANY
        elif "o" in from_cardinality and "||" in to_cardinality:
            return RelationshipType.MANY_TO_ONE
        else:
            return RelationshipType.ONE_TO_ONE
    
    def get_sqlalchemy_type(self, mermaid_type: str) -> str:
        """Get SQLAlchemy type from Mermaid type."""
        return self.TYPE_MAPPING.get(mermaid_type.lower(), 'String')
    
    def validate_schema(self) -> List[str]:
        """Validate the parsed schema and return any issues."""
        issues = []
        
        # Check if all tables exist
        for relationship in self.schema.relationships:
            if relationship.from_table not in self.schema.tables:
                issues.append(f"관계에서 참조하는 테이블이 존재하지 않습니다: {relationship.from_table}")
            if relationship.to_table not in self.schema.tables:
                issues.append(f"관계에서 참조하는 테이블이 존재하지 않습니다: {relationship.to_table}")
        
        # Check for tables without primary keys
        for table_name, table in self.schema.tables.items():
            has_pk = any(col.is_primary_key for col in table.columns)
            if not has_pk:
                issues.append(f"테이블 '{table_name}'에 기본키가 없습니다")
        
        # Check for foreign key references
        for table_name, table in self.schema.tables.items():
            for column in table.columns:
                if column.is_foreign_key and not column.foreign_table:
                    # Try to infer foreign table from column name
                    if column.name.endswith('_id'):
                        potential_table = column.name[:-3].upper()
                        if potential_table in self.schema.tables:
                            column.foreign_table = potential_table
                            column.foreign_column = 'id'
                        else:
                            # Try alternative naming patterns
                            # e.g., session_id -> TREATMENT_SESSION
                            if potential_table == 'SESSION':
                                if 'TREATMENT_SESSION' in self.schema.tables:
                                    column.foreign_table = 'TREATMENT_SESSION'
                                    column.foreign_column = 'id'
                                else:
                                    issues.append(f"테이블 '{table_name}'의 컬럼 '{column.name}'에 대한 외래키 테이블을 찾을 수 없습니다")
                            else:
                                issues.append(f"테이블 '{table_name}'의 컬럼 '{column.name}'에 대한 외래키 테이블을 찾을 수 없습니다")
        
        return issues
