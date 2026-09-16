import streamlit as st
import pandas as pd
from sqlalchemy import text
from app.core.db import engine
from app.modules.safety.dao import SafetyDAO
from app.core.theme import COLOR_TOP, COLOR_MID, COLOR_LOW, COLOR_LINE, TEXT_COLOR, PLOTLY_THEME

def render_p02():
    st.subheader("📋 安全板块项目列表与数据管理 (P02)")
    
    # --- 模块 1：前端 Excel 拖拽上传与一键入库 ---
    with st.expander("📥 批量数据导入 (支持上传 Excel 文件)", expanded=False):
        uploaded_file = st.file_uploader("选择要上传的安全运营数据 Excel 表格", type=["xlsx", "xls"])
        if uploaded_file is not None:
            try:
                # 读取上传的 Excel
                df_upload = pd.read_excel(uploaded_file)
                st.write("📌 **解析到的数据预览：**")
                st.dataframe(df_upload.head(3), use_container_width=True)
                
                if st.button("🚀 确认并一键写入数据库"):
                    with engine.begin() as conn:
                        # 遍历写入或追加数据
                        for _, row in df_upload.iterrows():
                            conn.execute(
                                text("""
                                    INSERT INTO t_safety_data 
                                    (project_id, record_date, hazard_count, rectified_count, rectification_rate, risk_level, safety_score, inspection_detail)
                                    VALUES (:project_id, :record_date, :hazard_count, :rectified_count, :rectification_rate, :risk_level, :safety_score, :inspection_detail)
                                    ON DUPLICATE KEY UPDATE
                                    hazard_count=VALUES(hazard_count),
                                    rectified_count=VALUES(rectified_count),
                                    rectification_rate=VALUES(rectification_rate),
                                    risk_level=VALUES(risk_level),
                                    safety_score=VALUES(safety_score),
                                    inspection_detail=VALUES(inspection_detail)
                                """),
                                row.to_dict()
                            )
                    st.success("✅ 数据成功导入并同步数据库！")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ 解析或入库失败: {e}")

    st.markdown("---")

    # --- 模块 2：多维筛选与数据展示 ---
    df = SafetyDAO.get_project_safety_list()
    if df.empty:
        st.info("暂无项目数据，请在上方上传 Excel 或初始化数据。")
        return
        
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        types = ["全部"] + list(df["business_type"].dropna().unique())
        selected_type = st.selectbox("业态筛选", types)
    with col_f2:
        risks = ["全部"] + list(df["risk_level"].dropna().unique())
        selected_risk = st.selectbox("风险等级筛选", risks)
    with col_f3:
        search_keyword = st.text_input("搜索项目名称/负责人", "")

    # 执行过滤逻辑
    filtered_df = df.copy()
    if selected_type != "全部":
        filtered_df = filtered_df[filtered_df["business_type"] == selected_type]
    if selected_risk != "全部":
        filtered_df = filtered_df[filtered_df["risk_level"] == selected_risk]
    if search_keyword:
        filtered_df = filtered_df[
            filtered_df["project_name"].str.contains(search_keyword, case=False, na=False) |
            filtered_df["manager"].str.contains(search_keyword, case=False, na=False)
        ]

    st.markdown(f"**当前筛选结果：共 {len(filtered_df)} 条项目记录**")
    
    rename_dict = {
        "project_id": "项目ID",
        "project_name": "项目名称",
        "business_type": "业态类型",
        "manager": "负责人",
        "record_date": "统计日期",
        "hazard_count": "隐患数",
        "rectified_count": "已整改",
        "rectification_rate": "整改率(%)",
        "risk_level": "风险等级",
        "safety_score": "安全得分",
        "inspection_detail": "巡查/抽检异常备注"
    }
    
    display_df = filtered_df[list(rename_dict.keys())].rename(columns=rename_dict)
    
    # --- 莫兰迪视觉增强：格式化表格与进度条展示 ---
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "整改率(%)": st.column_config.ProgressColumn(
                "整改率(%)",
                help="隐患整改完成进度",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "安全得分": st.column_config.NumberColumn(
                "安全得分",
                format="%.1f 分"
            ),
            "风险等级": st.column_config.SelectboxColumn(
                "风险等级",
                options=["低风险", "中风险", "高风险"],
                required=True
            )
        }
    )

    # --- 模块 3：一键导出当前报表 ---
    csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 导出当前筛选报表 (CSV/Excel)",
        data=csv_data,
        file_name="深圳分部_安全运营数据汇总.csv",
        mime="text/csv"
    )