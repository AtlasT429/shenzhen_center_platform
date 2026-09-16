import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. 优先读取环境变量（用于云端 Streamlit Cloud 或自定义配置）
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. 如果没有配置环境变量，则回退到本地 MySQL 配置
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")  # 你的本地密码
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "sz_center_db")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 3. 根据数据库类型动态创建 engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite 适配 Streamlit 多线程
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # MySQL 配置
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_pre_ping=True,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """获取数据库 Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()