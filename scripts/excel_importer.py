import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from app.core.db import SessionLocal

def init_mock_data():
    """初始化深圳区域 20 个项目的样板数据"""
    db = SessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        db.execute(text("TRUNCATE TABLE t_safety_data;"))
        db.execute(text("TRUNCATE TABLE t_project;"))
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        # 20 个项目明细（涵盖写字楼、商业综合体、公共物业）
        projects = [
            ("PRJ001", "深圳中心大厦", "写字楼", "深圳", "张经理"),
            ("PRJ002", "海纳商业广场", "商业综合体", "深圳", "李经理"),
            ("PRJ003", "科技园区公建项目", "公共物业", "深圳", "王经理"),
            ("PRJ004", "南山智谷大厦", "写字楼", "深圳", "赵经理"),
            ("PRJ005", "前海金融中心", "写字楼", "深圳", "陈经理"),
            ("PRJ006", "宝安万科广场", "商业综合体", "深圳", "刘经理"),
            ("PRJ007", "福田市民中心服务区", "公共物业", "深圳", "杨经理"),
            ("PRJ008", "龙岗创新产业园", "公共物业", "深圳", "黄经理"),
            ("PRJ009", "罗湖万象天地", "商业综合体", "深圳", "周经理"),
            ("PRJ010", "龙华科技大厦", "写字楼", "深圳", "吴经理"),
            ("PRJ011", "光明科学城园区", "公共物业", "深圳", "徐经理"),
            ("PRJ012", "盐田港运营中心", "公共物业", "深圳", "孙经理"),
            ("PRJ013", "坪山高新产业园", "公共物业", "深圳", "胡经理"),
            ("PRJ014", "大鹏生态旅游区物业", "公共物业", "深圳", "朱经理"),
            ("PRJ015", "后海总部基地A座", "写字楼", "深圳", "高经理"),
            ("PRJ016", "深圳湾1号服务区", "商业综合体", "深圳", "林经理"),
            ("PRJ017", "河套科创中心", "写字楼", "深圳", "何经理"),
            ("PRJ018", "西丽湖科教城", "公共物业", "深圳", "郭经理"),
            ("PRJ019", "深圳北站商务中心", "写字楼", "深圳", "罗经理"),
            ("PRJ020", "会展中心展馆大厦", "公共物业", "深圳", "梁经理"),
        ]
        
        for pid, pname, btype, reg, mgr in projects:
            db.execute(
                text("INSERT INTO t_project (project_id, project_name, business_type, region, manager) VALUES (:pid, :pname, :btype, :reg, :mgr)"),
                {"pid": pid, "pname": pname, "btype": btype, "reg": reg, "mgr": mgr}
            )
            
            # 生成配套安全数据
            hazard = (hash(pid) % 30) + 10
            rectified = hazard - (hash(pid) % 3)
            rate = round((rectified / hazard) * 100, 2)
            score = round(90 + (hash(pid) % 10) - (hazard - rectified) * 2, 1)
            risk = "高风险" if rate < 85 else ("中风险" if rate < 95 else "低风险")
            
            db.execute(
                text("""INSERT INTO t_safety_data 
                     (project_id, record_date, hazard_count, rectified_count, rectification_rate, risk_level, safety_score, inspection_detail)
                     VALUES (:pid, '2026-08-01', :hz, :rc, :rt, :rk, :sc, :dt)"""),
                {"pid": pid, "hz": hazard, "rc": rectified, "rt": rate, "rk": risk, "sc": score, "dt": f"{pname}月度安全日常抽检完成，整体运行稳定。"}
            )
            
        db.commit()
        print("✅ 20个项目数据批量初始化成功！")
    except Exception as e:
        db.rollback()
        print(f"❌ 批量初始化失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_mock_data()