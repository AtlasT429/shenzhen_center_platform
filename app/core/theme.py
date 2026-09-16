# -------------------------------------------------------------
# 深圳分部·深安智巡 - 莫兰迪商务视觉规范 (Design System)
# -------------------------------------------------------------

# 图表配色
COLOR_TOP = "#2563eb"       # 标杆高亮：精炼高雅蓝
COLOR_MID = "#cbd5e1"       # 平稳项目：清爽冰灰蓝
COLOR_LOW = "#94a3b8"       # 待提升项目：沉稳石墨灰
COLOR_LINE = "#64748b"      # 基准虚线 / 辅助线
TEXT_COLOR = "#334155"      # 主文字色：深板岩灰
TEXT_MUTED = "#64748b"      # 次要文字色：中灰

# Plotly 全局 Layout 配置
PLOTLY_THEME = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_COLOR, family="Microsoft YaHei, Sans-Serif")
)