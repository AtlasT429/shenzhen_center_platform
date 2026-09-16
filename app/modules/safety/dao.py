import pandas as pd
from sqlalchemy import text
from app.core.db import engine

class SafetyDAO:
    @staticmethod
    def get_safety_summary():
        """获取安全驾驶舱核心 KPI 统计数据"""
        query = text("""
            SELECT 
                COUNT(DISTINCT s.project_id) as total_projects,
                SUM(s.hazard_count) as total_hazards,
                SUM(s.rectified_count) as total_rectified,
                ROUND(AVG(s.safety_score), 1) as avg_score
            FROM t_safety_data s
        """)
        with engine.connect() as conn:
            result = conn.execute(query).fetchone()
            return result

    @staticmethod
    def get_project_safety_list():
        """获取项目安全明细列表（含项目名称联表查询）"""
        query = text("""
            SELECT 
                p.project_id,
                p.project_name,
                p.business_type,
                p.manager,
                s.record_date,
                s.hazard_count,
                s.rectified_count,
                s.rectification_rate,
                s.risk_level,
                s.safety_score,
                s.inspection_detail
            FROM t_project p
            LEFT JOIN t_safety_data s ON p.project_id = s.project_id
            ORDER BY s.safety_score ASC
        """)
        return pd.read_sql(query, con=engine)