"""Database initialization script with safe reset functionality."""

import asyncio
import logging
import os
import sys
from typing import Optional

import click
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_async_session, engine
from app.scripts.seed import seed_database

logger = logging.getLogger(__name__)


async def check_database_connection() -> bool:
    """Check if database connection is available."""
    try:
        async with get_async_session() as db:
            await db.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


async def drop_all_tables() -> None:
    """Drop all tables from the database."""
    logger.warning("Dropping all tables...")
    
    # Import all models to ensure they are registered
    from app.db.models import *  # noqa: F401, F403
    
    from app.db.base import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    logger.info("All tables dropped successfully")


async def create_all_tables() -> None:
    """Create all tables in the database."""
    logger.info("Creating all tables...")
    
    # Import all models to ensure they are registered
    from app.db.models import *  # noqa: F401, F403
    
    from app.db.base import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("All tables created successfully")


async def run_migrations() -> None:
    """Run database migrations using Alembic."""
    import subprocess
    
    logger.info("Running database migrations...")
    
    try:
        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("Migrations completed successfully")
        logger.debug(f"Migration output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        raise


async def reset_database(use_migrations: bool = True) -> None:
    """Reset the database by dropping and recreating all tables."""
    logger.info("Starting database reset...")
    
    # Check database connection
    if not await check_database_connection():
        logger.error("Cannot connect to database. Please check your configuration.")
        sys.exit(1)
    
    try:
        if use_migrations:
            # Use Alembic for migrations
            logger.info("Using Alembic migrations for database reset")
            
            # Drop all tables
            await drop_all_tables()
            
            # Run migrations
            await run_migrations()
        else:
            # Use SQLAlchemy metadata
            logger.info("Using SQLAlchemy metadata for database reset")
            
            # Drop all tables
            await drop_all_tables()
            
            # Create all tables
            await create_all_tables()
        
        logger.info("Database reset completed successfully")
        
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise


async def init_database(use_migrations: bool = True, seed: bool = False) -> None:
    """Initialize the database with tables and optionally seed data."""
    logger.info("Starting database initialization...")
    
    # Check database connection
    if not await check_database_connection():
        logger.error("Cannot connect to database. Please check your configuration.")
        sys.exit(1)
    
    try:
        if use_migrations:
            # Use Alembic for migrations
            logger.info("Using Alembic migrations for database initialization")
            await run_migrations()
        else:
            # Use SQLAlchemy metadata
            logger.info("Using SQLAlchemy metadata for database initialization")
            await create_all_tables()
        
        logger.info("Database initialization completed successfully")
        
        # Seed database if requested
        if seed:
            logger.info("Seeding database with sample data...")
            await seed_database()
            logger.info("Database seeding completed")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def confirm_action(message: str) -> bool:
    """Ask for user confirmation."""
    response = input(f"{message} (y/N): ").strip().lower()
    return response in ['y', 'yes']


@click.command()
@click.option(
    '--reset', 
    is_flag=True, 
    help='Reset the database (drop all tables and recreate)'
)
@click.option(
    '--init', 
    is_flag=True, 
    help='Initialize the database (create tables)'
)
@click.option(
    '--seed', 
    is_flag=True, 
    help='Seed the database with sample data'
)
@click.option(
    '--no-migrations', 
    is_flag=True, 
    help='Use SQLAlchemy metadata instead of Alembic migrations'
)
@click.option(
    '--force', 
    is_flag=True, 
    help='Skip confirmation prompts'
)
@click.option(
    '--env', 
    default='.env',
    help='Environment file to load (default: .env)'
)
def main(
    reset: bool,
    init: bool,
    seed: bool,
    no_migrations: bool,
    force: bool,
    env: str
):
    """Database initialization and management script."""
    
    # Load environment variables
    if os.path.exists(env):
        from dotenv import load_dotenv
        load_dotenv(env)
        logger.info(f"Loaded environment variables from {env}")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    use_migrations = not no_migrations
    
    async def run_operations():
        if reset:
            # Database reset
            if not force:
                if not confirm_action(
                    "⚠️  WARNING: This will DROP ALL TABLES and DELETE ALL DATA. "
                    "Are you sure you want to continue?"
                ):
                    logger.info("Database reset cancelled by user")
                    return
            
            await reset_database(use_migrations)
            
            if seed:
                logger.info("Seeding database after reset...")
                await seed_database()
        
        elif init:
            # Database initialization
            await init_database(use_migrations, seed)
        
        elif seed:
            # Seed only
            logger.info("Seeding database with sample data...")
            await seed_database()
        
        else:
            # Show help
            click.echo("No operation specified. Use --help for options.")
            click.echo("\nAvailable operations:")
            click.echo("  --init     Initialize database (create tables)")
            click.echo("  --reset    Reset database (drop and recreate tables)")
            click.echo("  --seed     Seed database with sample data")
            click.echo("\nOptions:")
            click.echo("  --no-migrations  Use SQLAlchemy metadata instead of Alembic")
            click.echo("  --force          Skip confirmation prompts")
            click.echo("  --env FILE       Load environment variables from FILE")
    
    # Run the operations
    try:
        asyncio.run(run_operations())
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
