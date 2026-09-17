import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_url() -> str:
    """获取数据库连接字符串（优先级：环境变量 -> Streamlit Secrets -> 本地默认）"""
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    try:
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
        if "mysql" in st.secrets:
            sec = st.secrets["mysql"]
            return f"mysql+pymysql://{sec['user']}:{sec['password']}@{sec['host']}:{sec['port']}/{sec['database']}?charset=utf8mb4"
    except Exception:
        pass

    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "123456")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    dbname = os.getenv("DB_NAME", "sz_center_db")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"


DATABASE_URL = get_database_url()

# 过滤 URL 中传入的 ssl_mode 参数，避免 PyMySQL 解析报错
if "ssl_mode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("?ssl_mode=REQUIRED", "").replace("&ssl_mode=REQUIRED", "")

# 打印日志辅助排查（只显示 Host）
print(f"[DB Config Check] Connecting to host: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

# PyMySQL 专属 SSL 参数配置
connect_args = {}
if "aivencloud.com" in DATABASE_URL:
    connect_args["ssl"] = {"ssl_mode": "REQUIRED"}

# 创建 Engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800,
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