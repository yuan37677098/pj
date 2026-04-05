import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import json

# 页面配置
st.set_page_config(page_title="智能数据分析Agent", layout="wide", page_icon="📊")

# 自定义CSS美化
st.markdown("""
<style>
    /* 卡片样式 */
    .css-1r6slb0, .css-1v3fvcr {
        background-color: #f9f9fb;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    /* 侧边栏背景 */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    /* 按钮样式 */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    /* 标题样式 */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
    hr {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session_state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/data-configuration.png", width=80)
    st.title("⚙️ 配置")
    
    # 文件上传
    st.markdown("### 📂 1. 上传数据")
    uploaded_file = st.file_uploader("Excel 或 CSV", type=["xlsx", "csv"])
    
    # API Key
    st.markdown("### 🔑 2. DeepSeek API")
    api_key_input = st.text_input("API Key", type="password", placeholder="sk-...")
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    
    # AI 建议折叠块
    with st.expander("💡 AI 智能建议（点击展开）"):
        if st.button("🤖 请AI分析数据并推荐图表", use_container_width=True):
            if st.session_state.df is None:
                st.warning("请先上传数据")
            elif not st.session_state.api_key:
                st.error("请先配置 API Key")
            else:
                df = st.session_state.df
                sample = df.head(20).to_string()
                col_info = ", ".join(df.columns)
                prompt = f"""
                你是一个数据分析专家。请基于以下数据信息，给出：
                1. 数据的主要特征（如趋势、分布、异常）
                2. 推荐3个最有价值的图表（说明用什么图表类型，X轴和Y轴分别选什么字段，为什么）
                3. 建议下一步的分析方向
                数据列名：{col_info}
                数据样例（前20行）：
                {sample}
                """
                client = OpenAI(api_key=st.session_state.api_key, base_url="https://api.deepseek.com/v1")
                with st.spinner("AI 分析中..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.3
                        )
                        advice = response.choices[0].message.content
                        st.success(advice)
                    except Exception as e:
                        st.error(f"调用失败: {e}")

# ========== 读取数据 ==========
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
        st.toast("✅ 数据加载成功！", icon="🎉")
    except Exception as e:
        st.error(f"文件读取失败: {e}")

if st.session_state.df is not None:
    df = st.session_state.df
    
    # ========== 主区域 ==========
    st.title("📊 智能数据分析Agent")
    st.caption("支持多维度透视、多图表类型、自然语言生成图表")
    
    # 数据预览（折叠）
    with st.expander("📋 数据概览（点击展开）"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总行数", df.shape[0])
        with col2:
            st.metric("总列数", df.shape[1])
        with col3:
            st.metric("缺失值总数", df.isnull().sum().sum())
        st.dataframe(df.head(10), use_container_width=True)
        st.write("**列名及类型**")
        st.write(pd.DataFrame({"列名": df.columns, "类型": df.dtypes.astype(str)}))
    
    st.markdown("---")
    
    # ========== 数据透视表 ==========
    st.subheader("📊 数据透视表")
    col1, col2 = st.columns(2)
    with col1:
        rows = st.multiselect("行（分组字段）", options=df.columns, default=df.columns[0] if len(df.columns)>0 else [])
    with col2:
        cols = st.multiselect("列（可选交叉表）", options=df.columns, default=[])
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    values = st.multiselect("值（数值字段）", options=numeric_cols, default=numeric_cols[0] if numeric_cols else [])
    agg_func = st.selectbox("聚合方式", ["求和", "均值", "计数", "最大值", "最小值"])
    agg_map = {"求和": "sum", "均值": "mean", "计数": "count", "最大值": "max", "最小值": "min"}
    
    if rows and values:
        try:
            if cols:
                pivot = pd.pivot_table(df, values=values, index=rows, columns=cols, aggfunc=agg_map[agg_func], fill_value=0)
            else:
                pivot = df.groupby(rows)[values].agg(agg_map[agg_func]).reset_index()
            st.dataframe(pivot, use_container_width=True)
        except Exception as e:
            st.warning(f"透视表生成失败: {e}")
    else:
        st.info("请至少选择行字段和值字段")
    
    st.markdown("---")
    
    # ========== 图表生成 ==========
    st.subheader("📈 图表分析")
    col1, col2 = st.columns(2)
    with col1:
        chart_type = st.selectbox("图表类型", ["柱状图", "折线图", "饼图", "散点图", "箱线图"])
        x_axis = st.selectbox("X轴（类别/时间）", options=df.columns, index=0)
    with col2:
        y_axis = st.multiselect("Y轴（数值字段，可多选）", options=numeric_cols, default=numeric_cols[0] if numeric_cols else [])
        color_by = st.selectbox("颜色分组（可选）", options=["无"] + list(df.columns), index=0)
    
    if x_axis and y_axis:
        try:
            fig = None
            if chart_type == "柱状图":
                if color_by != "无":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=color_by, barmode="group")
                else:
                    fig = px.bar(df, x=x_axis, y=y_axis)
            elif chart_type == "折线图":
                fig = px.line(df, x=x_axis, y=y_axis, color=color_by if color_by!="无" else None)
            elif chart_type == "饼图":
                if len(y_axis) == 1:
                    pie_data = df.groupby(x_axis)[y_axis[0]].sum().reset_index()
                    fig = px.pie(pie_data, names=x_axis, values=y_axis[0])
                else:
                    st.warning("饼图只能选择一个数值字段")
            elif chart_type == "散点图":
                if len(y_axis) == 1:
                    fig = px.scatter(df, x=x_axis, y=y_axis[0], color=color_by if color_by!="无" else None)
                else:
                    st.warning("散点图只能选择一个Y轴字段")
            elif chart_type == "箱线图":
                fig = px.box(df, x=x_axis, y=y_axis[0] if y_axis else None, color=color_by if color_by!="无" else None)
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"图表生成失败: {e}")
    else:
        st.info("请选择X轴和至少一个Y轴字段")
    
    st.markdown("---")
    
    # ========== 自然语言生成图表（折叠） ==========
    with st.expander("🗣️ 自然语言生成图表（实验性）"):
        nl_query = st.text_input("用自然语言描述你想看的图表", 
                                 placeholder="例如：按月份和渠道的销售额柱状图")
        if st.button("✨ 生成图表") and nl_query:
            if not st.session_state.api_key:
                st.error("请先配置 API Key")
            else:
                prompt = f"""
                数据列名：{list(df.columns)}
                用户需求：{nl_query}
                请以JSON格式输出以下字段：
                - chart_type: 图表类型，可选 ["柱状图","折线图","饼图","散点图","箱线图"]
                - x: X轴字段名
                - y: Y轴字段名（字符串或列表）
                - color: 颜色分组字段名，如果没有则为null
                只输出JSON，不要其他解释。
                """
                client = OpenAI(api_key=st.session_state.api_key, base_url="https://api.deepseek.com/v1")
                with st.spinner("解析中..."):
                    try:
                        resp = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0
                        )
                        config = json.loads(resp.choices[0].message.content)
                        chart_type = config.get("chart_type")
                        x = config.get("x")
                        y = config.get("y")
                        color = config.get("color")
                        if x in df.columns and y in df.columns:
                            if chart_type == "柱状图":
                                fig = px.bar(df, x=x, y=y, color=color)
                            elif chart_type == "折线图":
                                fig = px.line(df, x=x, y=y, color=color)
                            elif chart_type == "饼图":
                                pie_data = df.groupby(x)[y].sum().reset_index()
                                fig = px.pie(pie_data, names=x, values=y)
                            else:
                                fig = px.scatter(df, x=x, y=y, color=color)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("AI返回的字段名不在数据中")
                    except Exception as e:
                        st.error(f"解析失败: {e}")

else:
    st.info("👈 请在左侧侧边栏上传 Excel 或 CSV 文件开始分析")
