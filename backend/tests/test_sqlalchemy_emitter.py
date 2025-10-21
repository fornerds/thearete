"""Tests for SQLAlchemy emitter."""

import pytest
from tools.utils.mermaid_erd_parser import MermaidERDParser, ERDSchema, Table, Column, Relationship, RelationshipType
from tools.utils.sqlalchemy_emitter import SQLAlchemyEmitter


class TestSQLAlchemyEmitter:
    """Test cases for SQLAlchemyEmitter."""
    
    def test_generate_simple_model(self):
        """Test generating a simple model."""
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
        
        emitter = SQLAlchemyEmitter(schema)
        user_table = schema.tables["USER"]
        code = emitter._generate_model_code(user_table)
        
        # Check basic structure
        assert "class User(Base):" in code
        assert "__tablename__ = \"user\"" in code
        assert "from app.db.base import Base" in code
        
        # Check column definitions
        assert "id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)" in code
        assert "name: Mapped[str] = mapped_column(String(255), comment=\"사용자명\")" in code
        assert "email: Mapped[str] = mapped_column(String(255), comment=\"이메일\")" in code
        assert "is_active: Mapped[bool] = mapped_column(Boolean)" in code
    
    def test_generate_model_with_foreign_key(self):
        """Test generating a model with foreign key."""
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
        
        emitter = SQLAlchemyEmitter(schema)
        order_table = schema.tables["ORDER"]
        code = emitter._generate_model_code(order_table)
        
        # Check foreign key
        assert "user_id: Mapped[int] = mapped_column(Integer, ForeignKey(\"user.id\"), nullable=False)" in code
        assert "from sqlalchemy import ForeignKey" in code
    
    def test_generate_model_with_relationships(self):
        """Test generating a model with relationships."""
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
        
        emitter = SQLAlchemyEmitter(schema)
        emitter._prepare_relationships()
        
        # Generate USER model
        user_table = schema.tables["USER"]
        user_code = emitter._generate_model_code(user_table)
        
        # Check relationship
        assert "orders: Mapped[List[\"Order\"]] = relationship(\"Order\", back_populates=\"user\", cascade=\"all, delete-orphan\")" in user_code
        assert "from sqlalchemy.orm import relationship" in user_code
        
        # Generate ORDER model
        order_table = schema.tables["ORDER"]
        order_code = emitter._generate_model_code(order_table)
        
        # Check back reference
        assert "user: Mapped[\"User\"] = relationship(\"User\", back_populates=\"orders\")" in order_code
    
    def test_generate_model_with_enum(self):
        """Test generating a model with enum."""
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
        
        emitter = SQLAlchemyEmitter(schema)
        user_table = schema.tables["USER"]
        code = emitter._generate_model_code(user_table)
        
        # Check enum column
        assert "gender: Mapped[str] = mapped_column(Enum(\"M\", \"F\"), comment=\"성별 (M/F)\")" in code
        assert "from sqlalchemy import Enum" in code
    
    def test_generate_model_with_datetime(self):
        """Test generating a model with datetime columns."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name
        datetime created_at
        datetime updated_at
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        emitter = SQLAlchemyEmitter(schema)
        user_table = schema.tables["USER"]
        code = emitter._generate_model_code(user_table)
        
        # Check datetime columns with auto-update
        assert "created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)" in code
        assert "updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)" in code
        assert "from datetime import datetime" in code
    
    def test_generate_model_with_constraints(self):
        """Test generating a model with various constraints."""
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
        
        emitter = SQLAlchemyEmitter(schema)
        user_table = schema.tables["USER"]
        code = emitter._generate_model_code(user_table)
        
        # Check constraints
        assert "email: Mapped[str] = mapped_column(String(255), unique=True)" in code
        assert "name: Mapped[str] = mapped_column(String(255), nullable=False)" in code
        assert "is_active: Mapped[bool] = mapped_column(Boolean, default=true)" in code
    
    def test_generate_model_with_text_type(self):
        """Test generating a model with text type."""
        erd_content = """
erDiagram
    USER {
        int id PK
        text bio "자기소개"
        string name
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        emitter = SQLAlchemyEmitter(schema)
        user_table = schema.tables["USER"]
        code = emitter._generate_model_code(user_table)
        
        # Check text column
        assert "bio: Mapped[str] = mapped_column(Text, comment=\"자기소개\")" in code
        assert "from sqlalchemy import Text" in code
    
    def test_generate_model_with_numeric_types(self):
        """Test generating a model with numeric types."""
        erd_content = """
erDiagram
    PRODUCT {
        int id PK
        float price "가격"
        decimal weight "무게"
        bigint stock "재고수량"
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        emitter = SQLAlchemyEmitter(schema)
        product_table = schema.tables["PRODUCT"]
        code = emitter._generate_model_code(product_table)
        
        # Check numeric columns
        assert "price: Mapped[float] = mapped_column(Float, comment=\"가격\")" in code
        assert "weight: Mapped[float] = mapped_column(Numeric, comment=\"무게\")" in code
        assert "stock: Mapped[int] = mapped_column(BigInteger, comment=\"재고수량\")" in code
    
    def test_generate_repr_method(self):
        """Test generating __repr__ method."""
        erd_content = """
erDiagram
    USER {
        int id PK
        string name "사용자명"
        string email "이메일"
    }
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        emitter = SQLAlchemyEmitter(schema)
        user_table = schema.tables["USER"]
        code = emitter._generate_model_code(user_table)
        
        # Check __repr__ method
        assert "def __repr__(self) -> str:" in code
        assert "return f\"<User(id={self.id}, name='{self.name}', email='{self.email}')>\"" in code
    
    def test_generate_init_file(self):
        """Test generating __init__.py file."""
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
"""
        parser = MermaidERDParser()
        schema = parser.parse(erd_content)
        
        emitter = SQLAlchemyEmitter(schema)
        init_code = emitter._generate_init_code()
        
        # Check imports
        assert "from app.db.models.order import Order  # noqa: F401" in init_code
        assert "from app.db.models.user import User  # noqa: F401" in init_code
        
        # Check __all__
        assert "__all__ = ['Order', 'User']" in init_code
    
    def test_type_mapping(self):
        """Test type mapping methods."""
        parser = MermaidERDParser()
        schema = parser.parse("erDiagram\nUSER { int id PK }")
        emitter = SQLAlchemyEmitter(schema)
        
        # Test SQLAlchemy type mapping
        assert emitter._get_sqlalchemy_type("bigint") == "BigInteger"
        assert emitter._get_sqlalchemy_type("int") == "Integer"
        assert emitter._get_sqlalchemy_type("string") == "String"
        assert emitter._get_sqlalchemy_type("text") == "Text"
        assert emitter._get_sqlalchemy_type("boolean") == "Boolean"
        assert emitter._get_sqlalchemy_type("datetime") == "DateTime"
        assert emitter._get_sqlalchemy_type("float") == "Float"
        assert emitter._get_sqlalchemy_type("enum") == "Enum"
        
        # Test Python type mapping
        assert emitter._get_python_type("int", False) == "int"
        assert emitter._get_python_type("int", True) == "Optional[int]"
        assert emitter._get_python_type("string", False) == "str"
        assert emitter._get_python_type("string", True) == "Optional[str]"
        assert emitter._get_python_type("boolean", False) == "bool"
        assert emitter._get_python_type("datetime", False) == "datetime"
    
    def test_string_length_extraction(self):
        """Test string length extraction."""
        parser = MermaidERDParser()
        schema = parser.parse("erDiagram\nUSER { int id PK }")
        emitter = SQLAlchemyEmitter(schema)
        
        # Test various string types
        assert emitter._get_string_length("text") == 0
        assert emitter._get_string_length("string") == 255
        assert emitter._get_string_length("varchar") == 255
        assert emitter._get_string_length("varchar(100)") == 100
        assert emitter._get_string_length("varchar(500)") == 500
    
    def test_enum_values_extraction(self):
        """Test enum values extraction."""
        parser = MermaidERDParser()
        schema = parser.parse("erDiagram\nUSER { int id PK }")
        emitter = SQLAlchemyEmitter(schema)
        
        # Test enum values extraction
        assert emitter._get_enum_values("성별 (M/F)") == '("M", "F")'
        assert emitter._get_enum_values("상태 (A/B/C)") == '("A", "B", "C")'
        assert emitter._get_enum_values("일반 텍스트") is None
        assert emitter._get_enum_values(None) is None
    
    def test_default_value_formatting(self):
        """Test default value formatting."""
        parser = MermaidERDParser()
        schema = parser.parse("erDiagram\nUSER { int id PK }")
        emitter = SQLAlchemyEmitter(schema)
        
        # Test default value formatting
        assert emitter._format_default_value("true", "boolean") == "true"
        assert emitter._format_default_value("false", "boolean") == "false"
        assert emitter._format_default_value("test", "string") == '"test"'
        assert emitter._format_default_value("now()", "datetime") == "datetime.utcnow"
        assert emitter._format_default_value("123", "int") == "123"
    
    def test_case_conversion(self):
        """Test case conversion methods."""
        parser = MermaidERDParser()
        schema = parser.parse("erDiagram\nUSER { int id PK }")
        emitter = SQLAlchemyEmitter(schema)
        
        # Test snake_case conversion
        assert emitter._to_snake_case("USER") == "user"
        assert emitter._to_snake_case("USER_PROFILE") == "user_profile"
        assert emitter._to_snake_case("UserProfile") == "user_profile"
        
        # Test PascalCase conversion
        assert emitter._to_pascal_case("user") == "User"
        assert emitter._to_pascal_case("user_profile") == "UserProfile"
        assert emitter._to_pascal_case("USER_PROFILE") == "UserProfile"
