import streamlit as st
import plotly.graph_objects as go
from app.modules.safety.dao import SafetyDAO

def render_p01():
    st.subheader("📊 安全驾驶舱核心指标 (P01)")
    
    df = SafetyDAO.get_project_safety_list()
    if df.empty:
        st.info("暂无数据")
        return
        
    avg_score = round(df['safety_score'].mean(), 1)
    avg_rate = round(df['rectification_rate'].mean(), 1)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("监控项目总数", f"{len(df)} 个")
    with col2:
        st.metric("累计发现隐患", f"{df['hazard_count'].sum()} 项")
    with col3:
        st.metric("已完成整改", f"{df['rectified_count'].sum()} 项")
    with col4:
        st.metric("平均安全得分", f"{avg_score} 分")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 各项目安全指标对比")
    
    col_chart1, col_chart2 = st.columns(2)
    
    # -------------------------------------------------------------
    # 麦肯锡经典同色系单色调（Monochrome Gradient Palette）
    # -------------------------------------------------------------
    COLOR_TOP = "#2563eb"       # Top 3 标杆：精炼高雅蓝
    COLOR_MID = "#cbd5e1"       # 中间平稳项目：清爽冰灰蓝
    COLOR_LOW = "#94a3b8"       # 待提升项目：沉稳低调石墨灰（替代刺眼红，做深浅区隔）
    TEXT_COLOR = "#475569"      # 文字色
    
    # --- 图 1：项目安全综合得分 ---
    df_score = df.sort_values(by="safety_score", ascending=True)
    total_len = len(df_score)
    
    colors_score = []
    for idx in range(total_len):
        if idx >= total_len - 3:    # Top 3
            colors_score.append(COLOR_TOP)
        elif idx < 2:               # 倒数 2 名（深灰降调）
            colors_score.append(COLOR_LOW)
        else:                       # 中间正常项
            colors_score.append(COLOR_MID)
    
    fig_score = go.Figure(go.Bar(
        x=df_score['safety_score'],
        y=df_score['project_name'],
        orientation='h',
        marker=dict(color=colors_score, cornerradius=3),
        text=df_score['safety_score'],
        textposition='outside',
        textfont=dict(color=TEXT_COLOR, size=10),
        width=0.55
    ))
    
    fig_score.add_vline(
        x=avg_score, 
        line_dash="dot", 
        line_color="#94a3b8",
        annotation_text=f"均线: {avg_score}分", 
        annotation_position="top right",
        annotation_font=dict(size=10, color="#64748b")
    )
    
    fig_score.update_layout(
        title="<b>项目安全综合得分 (分)</b><br><sup style='color:#64748b;font-size:11px'>蓝色高亮为 Top3 标杆项目</sup>",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=680,
        margin=dict(l=10, r=45, t=60, b=20),
        xaxis=dict(showgrid=False, range=[0, 120], visible=False),
        yaxis=dict(tickfont=dict(size=10, color=TEXT_COLOR))
    )
    
    # --- 图 2：隐患整改完成率 ---
    df_rate = df.sort_values(by="rectification_rate", ascending=True)
    colors_rate = []
    for idx in range(total_len):
        if idx >= total_len - 3:
            colors_rate.append(COLOR_TOP)
        elif idx < 2:
            colors_rate.append(COLOR_LOW)
        else:
            colors_rate.append(COLOR_MID)
            
    fig_rate = go.Figure(go.Bar(
        x=df_rate['rectification_rate'],
        y=df_rate['project_name'],
        orientation='h',
        marker=dict(color=colors_rate, cornerradius=3),
        text=[f"{r}%" for r in df_rate['rectification_rate']],
        textposition='outside',
        textfont=dict(color=TEXT_COLOR, size=10),
        width=0.55
    ))
    
    fig_rate.add_vline(
        x=avg_rate, 
        line_dash="dot", 
        line_color="#94a3b8",
        annotation_text=f"均线: {avg_rate}%", 
        annotation_position="top right",
        annotation_font=dict(size=10, color="#64748b")
    )
    
    fig_rate.update_layout(
        title="<b>隐患整改完成率 (%)</b><br><sup style='color:#64748b;font-size:11px'>蓝色高亮为 Top3 标杆项目</sup>",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=680,
        margin=dict(l=10, r=45, t=60, b=20),
        xaxis=dict(showgrid=False, range=[0, 125], visible=False),
        yaxis=dict(tickfont=dict(size=10, color=TEXT_COLOR))
    )
    
    with col_chart1:
        st.plotly_chart(fig_score, use_container_width=True, config={'displayModeBar': False})
    with col_chart2:
        st.plotly_chart(fig_rate, use_container_width=True, config={'displayModeBar': False})