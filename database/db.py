from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

ASYNC_DB_URL = "mysql+aiomysql://root:root@localhost:3306/demo"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = async_sessionmaker(bind=async_engine, autoflush=False)

Base = declarative_base()
