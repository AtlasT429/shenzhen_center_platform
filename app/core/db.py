import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_url() -> str:
    """按优先级获取数据库连接字符串：
    1. 环境变量 DATABASE_URL
    2. Streamlit Secrets (st.secrets["DATABASE_URL"] 或 st.secrets["mysql"])
    3. 本地环境变量 / 默认值 (localhost)
    """
    # 1. 优先读取系统环境变量 DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    # 2. 尝试从 Streamlit Secrets 中读取
    try:
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
        
        if "mysql" in st.secrets:
            sec = st.secrets["mysql"]
            user = sec.get("user", "root")
            password = sec.get("password", "")
            host = sec.get("host", "localhost")
            port = sec.get("port", 3306)
            dbname = sec.get("database", "sz_center_db")
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"
    except Exception:
        # 非 Streamlit 环境运行或未配置 secrets 时跳过
        pass

    # 3. 回退到本地环境变量 / 默认连接
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "123456")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    dbname = os.getenv("DB_NAME", "sz_center_db")
    
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4"


DATABASE_URL = get_database_url()

# 根据数据库类型动态创建 engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_pre_ping=True,  # 配合 Streamlit 长时间连空闲，自动检查重连
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