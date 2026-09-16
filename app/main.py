import sys
from pathlib import Path

# 将项目根目录添加到系统路径中
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from app.core.style import inject_custom_css
from app.modules.safety.views.p01_dashboard import render_p01
from app.modules.safety.views.p02_list import render_p02
from app.modules.safety.views.p03_profile import render_p03

st.set_page_config(
    page_title="深圳分部 · 深安智巡 区域运营数据指挥中心",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入 CSS 美化样式
inject_custom_css()

# --- 顶部大标题与系统标识 ---
st.markdown("## 🛡️ 深圳分部 · 深安智巡 区域运营数据指挥中心")
st.markdown("<p style='color: #64748b; margin-top: -15px; font-size: 0.85rem;'>Shenzhen Branch · Operational Data Command Center | V1.0 Dynamic Demo</p>", unsafe_allow_html=True)
st.markdown("---")

# 侧边栏导航
DOMAIN_OPTIONS = {
    "🛡️ 安全数据驾驶舱": "safety",
    "🍃 环境数据驾驶舱 (规划中)": "environment",
    "🎧 客服数据驾驶舱 (规划中)": "customer"
}

selected_domain = st.sidebar.selectbox("业务板块", list(DOMAIN_OPTIONS.keys()))

if DOMAIN_OPTIONS[selected_domain] == "safety":
    page = st.sidebar.radio("功能页面", ["安全驾驶舱 (P01)", "安全板块 (P02)", "项目安全画像 (P03)"])
    
    if "P01" in page:
        render_p01()
    elif "P02" in page:
        render_p02()
    elif "P03" in page:
        render_p03()
else:
    st.warning("该业务板块为未来扩展模块，V1.0 暂未开放。")