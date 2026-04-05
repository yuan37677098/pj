import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px

# 设置页面标题
st.set_page_config(page_title="数据分析Agent", layout="wide")

# 页面标题
st.title("📊 数据分析Agent")

# 侧边栏 - 文件上传
st.sidebar.header("文件上传")
uploaded_file = st.sidebar.file_uploader("上传Excel或CSV文件", type=["xlsx", "csv"])

# 存储API密钥
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 智谱AI API密钥输入
st.sidebar.header("API配置")
st.session_state.api_key = st.sidebar.text_input("输入智谱AI API密钥", value=st.session_state.api_key, type="password")

# 数据存储
if "df" not in st.session_state:
    st.session_state.df = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "charts" not in st.session_state:
    st.session_state.charts = []

# 处理上传的文件
if uploaded_file is not None:
    try:
        # 读取文件
        if uploaded_file.name.endswith('.csv'):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)
        
        # 显示数据预览
        st.subheader("数据预览")
        st.dataframe(st.session_state.df.head(10))
        
        # 显示数据基本信息
        st.subheader("数据信息")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"行数: {st.session_state.df.shape[0]}")
            st.write(f"列数: {st.session_state.df.shape[1]}")
        with col2:
            st.write("列名:")
            st.write(list(st.session_state.df.columns))
    except Exception as e:
        st.error(f"文件读取失败: {str(e)}")
# 智谱AI API调用函数
def call_chatglm_api(prompt, api_key):
    url = "https://open.bigmodel.cn/api/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "glm-4-flash",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("data", {}).get("messages", [{}])[0].get("content", "")
    except Exception as e:
        st.error(f"API调用失败: {str(e)}")
        return ""

# 开始AI分析按钮
if st.sidebar.button("开始AI分析") and st.session_state.df is not None and st.session_state.api_key:
    with st.sidebar.spinner("正在分析数据..."):
        # 准备数据摘要
        data_summary = f"""数据摘要:
- 数据集形状: {st.session_state.df.shape[0]}行 x {st.session_state.df.shape[1]}列
- 列名: {list(st.session_state.df.columns)}
- 数据类型:
{st.session_state.df.dtypes.to_string()}
- 基本统计信息:
{st.session_state.df.describe().to_string()}
"""
        
        # 生成分析报告的提示词
        analysis_prompt = f"""请分析以下数据集并生成一份详细的分析报告，包括：
1. 数据概览
2. 关键指标和统计信息
3. 数据洞察和发现
4. 可能的业务价值

数据摘要：
{data_summary}

请用中文回答，输出格式清晰易读。"""
        
        # 调用API生成分析报告
        st.session_state.analysis_result = call_chatglm_api(analysis_prompt, st.session_state.api_key)
        
        # 生成可视化建议的提示词
        viz_prompt = f"""基于以下数据集，推荐2-3个最合适的可视化图表类型，并说明推荐理由。

数据摘要：
{data_summary}

请只返回图表类型和简短理由，不要有其他内容。"""
        
        # 调用API获取可视化建议
        viz_suggestions = call_chatglm_api(viz_prompt, st.session_state.api_key)
        
        # 生成图表
        st.session_state.charts = []
        
        # 尝试生成柱状图
        try:
            # 选择数值列
            numeric_cols = st.session_state.df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                # 选择第一个数值列
                value_col = numeric_cols[0]
                # 如果有分类列，使用分类列作为x轴
                categorical_cols = st.session_state.df.select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    x_col = categorical_cols[0]
                    fig1 = px.bar(st.session_state.df, x=x_col, y=value_col, title=f"{x_col} vs {value_col}")
                    st.session_state.charts.append(fig1)
        except Exception as e:
            pass
        
        # 尝试生成折线图
        try:
            # 检查是否有日期列或时序数据
            date_cols = [col for col in st.session_state.df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if len(date_cols) > 0:
                date_col = date_cols[0]
                # 选择数值列
                numeric_cols = st.session_state.df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                    fig2 = px.line(st.session_state.df, x=date_col, y=value_col, title=f"{value_col} 随时间变化")
                    st.session_state.charts.append(fig2)
        except Exception as e:
            pass
        
        # 尝试生成散点图
        try:
            # 选择两个数值列
            numeric_cols = st.session_state.df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) >= 2:
                fig3 = px.scatter(st.session_state.df, x=numeric_cols[0], y=numeric_cols[1], 
                                 title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
                st.session_state.charts.append(fig3)
        except Exception as e:
            pass

# 显示分析报告
if st.session_state.analysis_result:
    st.sidebar.header("分析报告")
    st.sidebar.write(st.session_state.analysis_result)

# 显示可视化图表
if st.session_state.charts:
    st.subheader("数据可视化")
    for i, fig in enumerate(st.session_state.charts):
        st.plotly_chart(fig, use_container_width=True)

# 智能问答功能
st.subheader("智能问答")
user_question = st.text_input("请输入您的问题：")
if user_question and st.session_state.df is not None and st.session_state.api_key:
    with st.spinner("AI正在思考..."):
        # 准备问答提示词
        qna_prompt = f"""请基于以下数据集回答用户问题：

数据集信息：
{st.session_state.df.head().to_string()}

用户问题：{user_question}

请用中文回答，基于数据内容给出准确的答案。"""
        
        # 调用API获取回答
        answer = call_chatglm_api(qna_prompt, st.session_state.api_key)
        
        # 显示回答
        st.write("AI回答：")
        st.write(answer)

# 部署指南链接
st.sidebar.header("部署指南")
st.sidebar.markdown("[点击查看详细部署指南](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)")
