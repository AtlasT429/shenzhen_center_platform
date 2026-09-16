import streamlit as st
import plotly.graph_objects as go
from app.modules.safety.dao import SafetyDAO
from app.core.theme import COLOR_TOP, COLOR_MID, COLOR_LOW, COLOR_LINE, TEXT_COLOR, PLOTLY_THEME

def render_p03():
    st.subheader("🔍 单项目安全画像深度分析 (P03)")
    
    # 获取所有项目数据
    df = SafetyDAO.get_project_safety_list()
    
    if df.empty:
        st.info("暂无项目数据")
        return
        
    # 下拉框选择目标项目
    project_names = list(df["project_name"].unique())
    selected_project_name = st.selectbox("选择要查看的项目", project_names)
    
    # 筛选出当前选中项目的数据
    proj_data = df[df["project_name"] == selected_project_name].iloc[0]
    
    st.markdown("---")
    
    # 1. 项目基础信息横幅
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    with col_info1:
        st.markdown(f"**项目名称**: {proj_data['project_name']}")
        st.markdown(f"**项目ID**: {proj_data['project_id']}")
    with col_info2:
        st.markdown(f"**业态类型**: {proj_data['business_type']}")
        st.markdown(f"**项目负责人**: {proj_data['manager']}")
    with col_info3:
        st.markdown(f"**统计日期**: {proj_data['record_date']}")
        
        # 风险等级柔和提示
        risk = proj_data['risk_level']
        if risk == "高风险":
            st.error(f"风险等级: {risk}")
        elif risk == "中风险":
            st.warning(f"风险等级: {risk}")
        else:
            st.success(f"风险等级: {risk}")
            
    with col_info4:
        st.metric("安全综合得分", f"{proj_data['safety_score']} 分")
        
    st.markdown("---")
    
    # 2. 隐患与整改数据指标
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("累计发现隐患", f"{proj_data['hazard_count']} 项")
    with col_m2:
        st.metric("已完成整改", f"{proj_data['rectified_count']} 项")
    with col_m3:
        st.metric("整改完成率", f"{proj_data['rectification_rate']}%")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 隐患整改分布")
    
    # 莫兰迪色系环形图 (Donut Chart - 修正 textinfo 格式)
    rectified = int(proj_data['rectified_count'])
    unrectified = max(0, int(proj_data['hazard_count']) - rectified)
    
    fig = go.Figure(data=[go.Pie(
        labels=["已整改", "未整改"],
        values=[rectified, unrectified],
        hole=0.65,
        marker=dict(colors=[COLOR_TOP, COLOR_LOW]),
        textposition='outside',  # 标签线引到外侧，避免挤在盘面上
        textinfo='label+value+percent',  # 修正：用 + 号连接属性
        textfont=dict(color=TEXT_COLOR, size=12),
        hoverinfo='label+value'
    )])
    
    fig.update_layout(
        **PLOTLY_THEME,
        title=f"<b>{selected_project_name} - 隐患整改完成情况</b>",
        height=380,
        showlegend=False,  # 隐藏底部冗余图例
        margin=dict(l=40, r=40, t=50, b=30)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # 3. 巡查与抽检异常备注
    st.markdown("### 📝 巡查 / 抽检异常记录")
    detail_text = proj_data['inspection_detail'] if proj_data['inspection_detail'] else "暂无异常记录"
    st.info(detail_text)