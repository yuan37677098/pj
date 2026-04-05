import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from openai import OpenAI

st.set_page_config(page_title="数据分析Agent", layout="wide")
st.title("📊 数据分析Agent")

# 初始化 session_state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# 侧边栏：文件上传 + API配置
with st.sidebar:
    st.header("文件上传")
    uploaded_file = st.file_uploader("上传 Excel 或 CSV 文件", type=["xlsx", "csv"])
    
    st.header("API 配置")
    api_key_input = st.text_input("DeepSeek API Key", type="password", 
                                  placeholder="输入你的 DeepSeek API Key")
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    st.markdown("**提示**：上传数据后，可以手动选择图表坐标轴，并自定义度量值。")

# 读取文件
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
        st.success("文件加载成功！")
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        st.stop()

# 如果有数据，显示交互界面
if st.session_state.df is not None:
    df = st.session_state.df
    
    # 数据预览
    st.subheader("数据预览")
    st.dataframe(df.head(10))
    
    # 显示基本信息
    st.subheader("数据信息")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"行数: {df.shape[0]}")
        st.write(f"列数: {df.shape[1]}")
    with col2:
        st.write("列名:")
        st.write(list(df.columns))
    
    # ---------- 自定义度量值 ----------
    st.subheader("自定义度量值")
    st.markdown("你可以输入一个 Python 表达式来创建新列，例如：`revenue - cost_goods`")
    col_expr, col_new = st.columns([3,1])
    with col_expr:
        expr = st.text_input("表达式（使用已有列名）", key="expr_input")
    with col_new:
        new_col_name = st.text_input("新列名", key="new_col_name")
    
    if st.button("创建度量值"):
        if expr and new_col_name:
            try:
                # 安全执行表达式（只允许基本运算，禁用危险函数）
                allowed_names = {col: df[col] for col in df.columns}
                allowed_names.update({"pd": pd, "np": __import__("numpy")})
                # 使用 eval 但限制全局和局部变量
                result = eval(expr, {"__builtins__": {}}, allowed_names)
                df[new_col_name] = result
                st.session_state.df = df
                st.success(f"已创建列 '{new_col_name}'")
                st.dataframe(df[[new_col_name]].head())
            except Exception as e:
                st.error(f"表达式错误: {e}")
        else:
            st.warning("请输入表达式和新列名")
    
    # ---------- 交互式图表 ----------
    st.subheader("交互式图表")
    # 获取所有列名，区分数值列和日期列
    all_cols = list(df.columns)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    date_cols = [col for col in all_cols if 'date' in col.lower() or '时间' in col or '日期' in col]
    
    # 如果没有日期列，用索引
    x_options = date_cols if date_cols else ['index']
    y_options = numeric_cols if numeric_cols else all_cols
    
    x_axis = st.selectbox("选择 X 轴（通常为日期）", x_options)
    y_axis = st.selectbox("选择 Y 轴（数值）", y_options)
    
    if st.button("生成图表"):
        if x_axis == 'index':
            x_data = df.index
            x_label = "行索引"
        else:
            x_data = df[x_axis]
            x_label = x_axis
            # 如果是日期列，尝试转换为 datetime
            if x_axis in date_cols:
                x_data = pd.to_datetime(x_data, errors='coerce')
        
        if y_axis not in numeric_cols:
            st.warning("Y 轴必须是数值列")
        else:
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(x_data, df[y_axis], marker='o', linestyle='-')
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_axis)
            ax.set_title(f"{y_axis} 随时间变化")
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    # ---------- 智能问答（使用 DeepSeek API）----------
    st.subheader("智能问答")
    user_question = st.text_area("输入你想问的问题", 
                                 placeholder="例如：哪个产品的销量最高？总利润是多少？")
    if st.button("提交问题"):
        if not st.session_state.api_key:
            st.error("请先在侧边栏输入 DeepSeek API Key")
        elif not user_question:
            st.warning("请输入问题")
        else:
            # 准备数据摘要（避免超长）
            sample = df.head(20).to_string()
            col_info = ", ".join(df.columns)
            prompt = f"""
            用户问题：{user_question}
            数据列名：{col_info}
            数据样例（前20行）：
            {sample}
            请基于数据回答用户问题，给出具体数值和分析建议。
            """
            client = OpenAI(api_key=st.session_state.api_key, 
                            base_url="https://api.deepseek.com/v1")
            try:
                with st.spinner("AI 思考中..."):
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    answer = response.choices[0].message.content
                    st.success(answer)
            except Exception as e:
                st.error(f"调用失败：{e}")

else:
    st.info("请先在侧边栏上传 Excel 或 CSV 文件")