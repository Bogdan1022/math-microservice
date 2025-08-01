from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database path (local file)
DATABASE_URL = "sqlite+aiosqlite:///./math_requests.db"

# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory for async DB sessions
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for defining models
Base = declarative_base()

# This function initializes the database (runs on startup)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
