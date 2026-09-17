import os
import ssl
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_url() -> str:
    """获取数据库连接字符串（优先读取 Secrets/环境变量）"""
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

# 1. 彻底清理 URL 中的 ssl 参数，避免 PyMySQL 重复解析传参报错
for query_param in ["?ssl_mode=REQUIRED", "&ssl_mode=REQUIRED", "?ssl_mode=REQUIRED&", "ssl_mode=REQUIRED"]:
    DATABASE_URL = DATABASE_URL.replace(query_param, "")

# 2. 构造连接参数：对 Aiven 强制使用 Python 标准库的 SSL Context 握手
connect_args = {}
if "aivencloud.com" in DATABASE_URL:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE  # 跳过本地证书文件校验，直接完成加密握手
    connect_args["ssl"] = ssl_context

# 3. 创建引擎
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