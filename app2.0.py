import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import json
import random

# 页面配置
st.set_page_config(page_title="智能数据分析Agent", layout="wide", page_icon="📊")

# 自定义CSS美化
st.markdown("""
<style>
    .css-1r6slb0, .css-1v3fvcr {
        background-color: #f9f9fb;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
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
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
    hr {
        margin: 1rem 0;
    }
    .card-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session_state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'ai_advice' not in st.session_state:
    st.session_state.ai_advice = ""
if 'ai_chart_config' not in st.session_state:
    st.session_state.ai_chart_config = None
if 'show_ai_chart_card' not in st.session_state:
    st.session_state.show_ai_chart_card = False

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/data-configuration.png", width=80)
    st.title("⚙️ 配置")
    
    st.markdown("### 📂 1. 上传数据")
    uploaded_file = st.file_uploader("Excel 或 CSV", type=["xlsx", "csv"])
    
    st.markdown("### 🔑 2. DeepSeek API")
    api_key_input = st.text_input("API Key", type="password", placeholder="sk-...")
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    
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
                        st.session_state.ai_advice = advice
                        st.success(advice)
                    except Exception as e:
                        st.error(f"调用失败: {e}")
        else:
            if st.session_state.ai_advice:
                st.success(st.session_state.ai_advice)

# ========== 读取数据 ==========
if uploaded_file is not None:
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            st.error("不支持的文件类型，请上传 CSV 或 Excel 文件")
            st.stop()
        st.session_state.df = df
        st.toast("✅ 数据加载成功！", icon="🎉")
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        st.stop()

if st.session_state.df is not None:
    df = st.session_state.df
    
    st.title("📊 智能数据分析Agent")
    st.caption("支持多维度透视、多图表类型、自然语言生成图表")
    
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
    
    # ========== AI 智能生成图表（多样化） ==========
    st.subheader("🤖 AI 智能生成图表")
    col_btn, _ = st.columns([1, 5])
    with col_btn:
        if st.button("✨ AI 自动生成图表", use_container_width=True):
            if not st.session_state.api_key:
                st.error("请先在侧边栏配置 API Key")
            else:
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                date_cols = [col for col in df.columns if 'date' in col.lower() or '时间' in col or '日期' in col]
                sample = df.head(10).to_string()
                # 随机选择分析角度
                perspectives = ["盈利能力分析", "销售趋势分析", "渠道对比分析", "产品成本结构", "销量分布", "时间序列预测"]
                perspective = random.choice(perspectives)
                prompt = f"""
                数据列名：{list(df.columns)}
                数值列：{numeric_cols}
                日期列：{date_cols}
                数据样例：
                {sample}
                请从「{perspective}」的角度出发，推荐一个最能揭示该角度业务洞察的图表配置，输出JSON格式：
                {{
                    "chart_type": "柱状图/折线图/饼图/散点图/箱线图",
                    "x": "X轴字段名",
                    "y": "Y轴字段名（字符串，如果是多指标则用数组）",
                    "color": "颜色分组字段名（可选，如果没有则为null）",
                    "reason": "为什么推荐这个图表"
                }}
                只输出JSON，不要其他解释。
                """
                client = OpenAI(api_key=st.session_state.api_key, base_url="https://api.deepseek.com/v1")
                with st.spinner("AI 正在分析数据并推荐图表..."):
                    try:
                        resp = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.8  # 增加随机性
                        )
                        config = json.loads(resp.choices[0].message.content)
                        st.session_state.ai_chart_config = config
                        st.session_state.show_ai_chart_card = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"AI 推荐失败: {e}")
    
    if st.session_state.show_ai_chart_card and st.session_state.ai_chart_config:
        config = st.session_state.ai_chart_config
        with st.container():
            st.markdown("#### 📈 AI 推荐图表")
            st.caption(f"**推荐理由**: {config.get('reason', '')}")
            try:
                chart_type = config.get("chart_type")
                x = config.get("x")
                y = config.get("y")
                color = config.get("color") if config.get("color") != "null" else None
                if x in df.columns and (y in df.columns if isinstance(y, str) else all(col in df.columns for col in y)):
                    if chart_type == "柱状图":
                        fig = px.bar(df, x=x, y=y, color=color)
                    elif chart_type == "折线图":
                        if x in df.columns and pd.api.types.is_datetime64_any_dtype(df[x]):
                            df_sorted = df.sort_values(by=x)
                        else:
                            df_sorted = df
                        fig = px.line(df_sorted, x=x, y=y, color=color)
                    elif chart_type == "饼图":
                        if isinstance(y, str):
                            pie_data = df.groupby(x)[y].sum().reset_index()
                            fig = px.pie(pie_data, names=x, values=y)
                        else:
                            st.warning("饼图只支持一个数值字段")
                            fig = None
                    elif chart_type == "散点图":
                        fig = px.scatter(df, x=x, y=y, color=color)
                    elif chart_type == "箱线图":
                        fig = px.box(df, x=x, y=y, color=color)
                    else:
                        fig = px.bar(df, x=x, y=y, color=color)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(f"AI 推荐的字段 {x} 或 {y} 不在数据中")
            except Exception as e:
                st.error(f"生成图表失败: {e}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ 保留", key="keep_ai_chart"):
                    st.session_state.show_ai_chart_card = False
                    st.success("已保留AI推荐配置（可手动在下方图表分析中调整）")
                    st.rerun()
            with col2:
                if st.button("🔄 重新生成", key="regenerate_ai_chart"):
                    st.session_state.ai_chart_config = None
                    st.session_state.show_ai_chart_card = False
                    st.rerun()
            with col3:
                if st.button("❌ 放弃", key="discard_ai_chart"):
                    st.session_state.show_ai_chart_card = False
                    st.rerun()
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
    
    # ========== 图表分析（优化版） ==========
    st.subheader("📈 图表分析")
    col1, col2 = st.columns(2)
    with col1:
        chart_type = st.selectbox("图表类型", ["柱状图", "折线图", "饼图", "散点图", "箱线图"])
        date_cols = [col for col in df.columns if 'date' in col.lower() or '时间' in col or '日期' in col]
        default_x = date_cols[0] if date_cols else df.columns[0]
        x_axis = st.selectbox("X轴（类别/时间）", options=df.columns, index=list(df.columns).index(default_x))
    with col2:
        y_axis = st.multiselect("Y轴（数值字段，可多选）", options=numeric_cols, default=numeric_cols[0] if numeric_cols else [])
        color_by = st.selectbox("颜色分组（可选）", options=["无"] + list(df.columns), index=0)
    
    if x_axis and y_axis:
        try:
            if chart_type == "折线图" and x_axis in df.columns:
                try:
                    df[x_axis] = pd.to_datetime(df[x_axis])
                    df_sorted = df.sort_values(by=x_axis)
                except:
                    df_sorted = df
            else:
                df_sorted = df
            
            fig = None
            if chart_type == "柱状图":
                if color_by != "无":
                    fig = px.bar(df_sorted, x=x_axis, y=y_axis, color=color_by, barmode="group")
                else:
                    fig = px.bar(df_sorted, x=x_axis, y=y_axis)
            elif chart_type == "折线图":
                if color_by != "无":
                    fig = px.line(df_sorted, x=x_axis, y=y_axis, color=color_by)
                else:
                    fig = px.line(df_sorted, x=x_axis, y=y_axis)
            elif chart_type == "饼图":
                if len(y_axis) == 1:
                    pie_data = df.groupby(x_axis)[y_axis[0]].sum().reset_index()
                    fig = px.pie(pie_data, names=x_axis, values=y_axis[0])
                else:
                    st.warning("饼图只能选择一个数值字段")
            elif chart_type == "散点图":
                if len(y_axis) == 1:
                    fig = px.scatter(df_sorted, x=x_axis, y=y_axis[0], color=color_by if color_by!="无" else None)
                else:
                    st.warning("散点图只能选择一个Y轴字段")
            elif chart_type == "箱线图":
                fig = px.box(df_sorted, x=x_axis, y=y_axis[0] if y_axis else None, color=color_by if color_by!="无" else None)
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"图表生成失败: {e}")
    else:
        st.info("请选择X轴和至少一个Y轴字段")
    
    st.markdown("---")
    
    # ========== 自然语言生成图表（支持聚合） ==========
    with st.expander("🗣️ 自然语言生成图表（实验性）"):
        nl_query = st.text_input("用自然语言描述你想看的图表", 
                                 placeholder="例如：按月份和渠道的销售额柱状图")
        if st.button("✨ 生成图表") and nl_query:
            if not st.session_state.api_key:
                st.error("请先配置 API Key")
            else:
                # 定义内部函数
                def generate_chart_from_nl(df, nl_query, api_key):
                    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
                    prompt = f"""
                    数据列名：{list(df.columns)}
                    数值列：{numeric_cols}
                    用户需求：{nl_query}
                    请输出一个 JSON 对象，包含以下字段：
                    - "x": X轴字段名（如果需要按月/年聚合，使用 "month(字段名)" 或 "year(字段名)"）
                    - "y": Y轴字段名（如果需要聚合，使用 "sum(字段名)" 或 "mean(字段名)"）
                    - "color": 颜色分组字段名（可选，没有则为null）
                    - "chart_type": 图表类型（折线图/柱状图/饼图/散点图/箱线图）
                    - "group_by": 分组字段列表（如果需要对数据进行分组聚合，例如 ["month(order_date)", "channel"]）
                    - "agg": 聚合方式字典，如 {{"revenue": "sum"}}
                    只输出 JSON，不要其他解释。
                    """
                    resp = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0
                    )
                    config = json.loads(resp.choices[0].message.content)
                    
                    # 处理分组聚合
                    if "group_by" in config and config["group_by"]:
                        df_agg = df.copy()
                        group_cols = []
                        for g in config["group_by"]:
                            if g.startswith("month("):
                                field = g[6:-1]
                                df_agg["month"] = pd.to_datetime(df_agg[field]).dt.to_period("M").astype(str)
                                group_cols.append("month")
                            elif g.startswith("year("):
                                field = g[5:-1]
                                df_agg["year"] = pd.to_datetime(df_agg[field]).dt.year
                                group_cols.append("year")
                            else:
                                group_cols.append(g)
                        agg_dict = config.get("agg", {})
                        if not agg_dict:
                            # 默认对y字段求和
                            agg_dict = {config["y"]: "sum"}
                        grouped = df_agg.groupby(group_cols).agg(agg_dict).reset_index()
                        # 重命名聚合列
                        for k, v in agg_dict.items():
                            grouped.rename(columns={k: f"{v}_{k}"}, inplace=True)
                        x_col = config["x"] if config["x"] not in ["month(?)", "year(?)"] else group_cols[0]
                        y_col = config["y"] if config["y"] not in ["sum(?)", "mean(?)"] else f"{list(agg_dict.values())[0]}_{list(agg_dict.keys())[0]}"
                        color_col = config.get("color") if config.get("color") != "null" else None
                        data = grouped
                    else:
                        data = df
                        x_col = config["x"]
                        y_col = config["y"]
                        color_col = config.get("color") if config.get("color") != "null" else None
                    
                    chart_type = config.get("chart_type", "折线图")
                    if chart_type == "折线图":
                        fig = px.line(data, x=x_col, y=y_col, color=color_col)
                    elif chart_type == "柱状图":
                        fig = px.bar(data, x=x_col, y=y_col, color=color_col)
                    elif chart_type == "饼图":
                        if isinstance(y_col, str):
                            pie_data = data.groupby(x_col)[y_col].sum().reset_index()
                            fig = px.pie(pie_data, names=x_col, values=y_col)
                        else:
                            fig = None
                    else:
                        fig = px.line(data, x=x_col, y=y_col, color=color_col)
                    return fig
                
                with st.spinner("解析并生成图表中..."):
                    try:
                        fig = generate_chart_from_nl(df, nl_query, st.session_state.api_key)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("无法生成图表，请尝试更简单的描述")
                    except Exception as e:
                        st.error(f"生成失败: {e}")

else:
    st.info("👈 请在左侧侧边栏上传 Excel 或 CSV 文件开始分析")
