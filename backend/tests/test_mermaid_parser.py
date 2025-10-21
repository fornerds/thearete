"""Tests for Mermaid ERD parser."""

import pytest
from tools.utils.mermaid_erd_parser import MermaidERDParser, Column, Table, Relationship, RelationshipType


class TestMermaidERDParser:
    """Test cases for MermaidERDParser."""
    
    def test_parse_simple_table(self):
        """Test parsing a simple table definition."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name "사용자명"
        string email "이메일"
        boolean is_active
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        assert len(schema.tables) == 1
        assert "USER" in schema.tables
        
        user_table = schema.tables["USER"]
        assert len(user_table.columns) == 4
        
        # Check ID column
        id_col = user_table.columns[0]
        assert id_col.name == "id"
        assert id_col.data_type == "int"
        assert id_col.is_primary_key is True
        assert id_col.is_nullable is False
        
        # Check name column
        name_col = user_table.columns[1]
        assert name_col.name == "name"
        assert name_col.data_type == "string"
        assert name_col.comment == "사용자명"
        assert name_col.is_primary_key is False
    
    def test_parse_relationship(self):
        """Test parsing relationships."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name
    }
    
    ORDER {
        int id PK
        int user_id FK
        string status
    }
    
    USER ||--o{ ORDER : "has many"
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        assert len(schema.relationships) == 1
        
        rel = schema.relationships[0]
        assert rel.from_table == "USER"
        assert rel.to_table == "ORDER"
        assert rel.relationship_type == RelationshipType.ONE_TO_MANY
        assert rel.label == "has many"
    
    def test_parse_foreign_key(self):
        """Test parsing foreign key columns."""
        erd_content = """
erDiagram
    ORDER {
        int id PK
        int user_id FK
        string status
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        order_table = schema.tables["ORDER"]
        user_id_col = order_table.columns[1]
        
        assert user_id_col.name == "user_id"
        assert user_id_col.is_foreign_key is True
        assert user_id_col.is_nullable is False
    
    def test_parse_enum_type(self):
        """Test parsing enum types."""
        erd_content = """
erDiagram
    USER {
        int id PK
        enum gender "성별 (M/F)"
        string name
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        user_table = schema.tables["USER"]
        gender_col = user_table.columns[1]
        
        assert gender_col.name == "gender"
        assert gender_col.data_type == "enum"
        assert gender_col.comment == "성별 (M/F)"
    
    def test_parse_multiple_tables(self):
        """Test parsing multiple tables."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name
    }
    
    ORDER {
        int id PK
        int user_id FK
        string status
    }
    
    PRODUCT {
        int id PK
        string name
        float price
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        assert len(schema.tables) == 3
        assert "USER" in schema.tables
        assert "ORDER" in schema.tables
        assert "PRODUCT" in schema.tables
    
    def test_parse_complex_relationships(self):
        """Test parsing complex relationships."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name
    }
    
    ORDER {
        int id PK
        int user_id FK
        string status
    }
    
    PRODUCT {
        int id PK
        string name
    }
    
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
    }
    
    USER ||--o{ ORDER : "has many"
    ORDER ||--o{ ORDER_ITEM : "has many"
    PRODUCT ||--o{ ORDER_ITEM : "has many"
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        assert len(schema.relationships) == 3
        
        # Check relationship types
        rel_types = [rel.relationship_type for rel in schema.relationships]
        assert RelationshipType.ONE_TO_MANY in rel_types
    
    def test_parse_table_with_comments(self):
        """Test parsing tables with comments."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name "사용자명"
        string email "이메일 주소"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        user_table = schema.tables["USER"]
        
        # Check comments
        name_col = next(col for col in user_table.columns if col.name == "name")
        assert name_col.comment == "사용자명"
        
        email_col = next(col for col in user_table.columns if col.name == "email")
        assert email_col.comment == "이메일 주소"
    
    def test_parse_constraints(self):
        """Test parsing various constraints."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string email UNIQUE
        string name NOT NULL
        boolean is_active DEFAULT true
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        user_table = schema.tables["USER"]
        
        # Check email column
        email_col = next(col for col in user_table.columns if col.name == "email")
        assert email_col.is_unique is True
        
        # Check name column
        name_col = next(col for col in user_table.columns if col.name == "name")
        assert name_col.is_nullable is False
        
        # Check is_active column
        active_col = next(col for col in user_table.columns if col.name == "is_active")
        assert active_col.default_value == "true"
    
    def test_validate_schema(self):
        """Test schema validation."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name
    }
    
    ORDER {
        int id PK
        int user_id FK
        string status
    }
    
    USER ||--o{ ORDER : "has many"
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        issues = parser.validate_schema()
        assert len(issues) == 0  # Should be no issues
    
    def test_validate_schema_with_issues(self):
        """Test schema validation with issues."""
        erd_content = """
erDiagram
    USER {
        string name
    }
    
    ORDER {
        int id PK
        int user_id FK
        string status
    }
    
    USER ||--o{ ORDER : "has many"
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        issues = parser.validate_schema()
        assert len(issues) > 0  # Should have issues (USER table has no PK)
        assert any("USER" in issue and "기본키" in issue for issue in issues)
    
    def test_type_mapping(self):
        """Test type mapping from Mermaid to SQLAlchemy."""
        parser = MermaidERDParser()
        
        # Test various type mappings
        assert parser.get_sqlalchemy_type("bigint") == "BigInteger"
        assert parser.get_sqlalchemy_type("int") == "Integer"
        assert parser.get_sqlalchemy_type("string") == "String"
        assert parser.get_sqlalchemy_type("text") == "Text"
        assert parser.get_sqlalchemy_type("boolean") == "Boolean"
        assert parser.get_sqlalchemy_type("datetime") == "DateTime"
        assert parser.get_sqlalchemy_type("float") == "Float"
        assert parser.get_sqlalchemy_type("enum") == "Enum"
        assert parser.get_sqlalchemy_type("unknown_type") == "String"  # Default
    
    def test_parse_real_world_example(self):
        """Test parsing a real-world ERD example."""
        erd_content = """
erDiagram
    SHOP {
        bigint id PK
        string name "상호명"
        string address "주소"
        string owner_name "대표자명"
        string phone "전화번호"
        string email "이메일 (로그인 ID)"
        string password "비밀번호 (암호화 저장)"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }
    
    CUSTOMER {
        bigint id PK
        bigint shop_id FK
        string name "고객명"
        int age "나이"
        enum gender "성별 (M/F)"
        string phone "연락처"
        string skin_type "피부타입"
        text note "특이사항"
        datetime created_at
        datetime updated_at
        boolean is_deleted
    }
    
    SHOP ||--o{ CUSTOMER : "has many"
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        assert len(schema.tables) == 2
        assert len(schema.relationships) == 1
        
        # Check SHOP table
        shop_table = schema.tables["SHOP"]
        assert len(shop_table.columns) == 10
        assert shop_table.columns[0].name == "id"
        assert shop_table.columns[0].is_primary_key is True
        
        # Check CUSTOMER table
        customer_table = schema.tables["CUSTOMER"]
        assert len(customer_table.columns) == 10
        shop_id_col = next(col for col in customer_table.columns if col.name == "shop_id")
        assert shop_id_col.is_foreign_key is True
        
        # Check relationship
        rel = schema.relationships[0]
        assert rel.from_table == "SHOP"
        assert rel.to_table == "CUSTOMER"
        assert rel.relationship_type == RelationshipType.ONE_TO_MANY
