import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        /* 顶部 padding 优化 */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        
        /* 清爽白底高亮 KPI 卡片 */
        [data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-top: 4px solid #2563eb !important; /* 顶部分层蓝线 */
            padding: 16px 20px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        }
        [data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricValue"] {
            color: #1e3a8a !important;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
        }
        </style>
    """, unsafe_allow_html=True)