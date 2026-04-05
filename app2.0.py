def execute_nl_query(df, nl_query, api_key):
    """根据自然语言生成图表，支持分组聚合"""
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    prompt = f"""
数据列名：{list(df.columns)}
用户需求：{nl_query}
请输出一个 JSON 对象，包含以下字段：
- "x": 用于X轴的字段名（如果需要对日期按月聚合，请使用 "month(字段名)" 形式）
- "y": 用于Y轴的字段名（如果是聚合值，如销售额总和，请用 "sum(字段名)"）
- "color": 用于颜色分组的字段名（可选）
- "chart_type": 图表类型（折线图/柱状图等）
- "aggregation": 是否需要分组聚合，若需要则描述分组字段和聚合方式，例如 {{"group_by": ["month(order_date)", "channel"], "agg": {{"revenue": "sum"}} }}
只输出 JSON，不要其他解释。
"""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    config = json.loads(resp.choices[0].message.content)
    
    # 处理聚合逻辑
    if "aggregation" in config and config["aggregation"]:
        group_by = config["aggregation"]["group_by"]
        agg_dict = config["aggregation"]["agg"]
        # 转换 group_by 中的 month(字段) 表达式
        df_agg = df.copy()
        for g in group_by:
            if g.startswith("month("):
                field = g[6:-1]  # 提取字段名
                df_agg["month"] = pd.to_datetime(df_agg[field]).dt.to_period("M").astype(str)
                group_by = [ "month" if g == f"month({field})" else g for g in group_by ]
        grouped = df_agg.groupby(group_by).agg(agg_dict).reset_index()
        # 重命名聚合后的列
        for k, v in agg_dict.items():
            grouped.rename(columns={k: f"{v}_{k}"}, inplace=True)
        x_col = config.get("x", group_by[0])
        y_col = config.get("y", list(agg_dict.values())[0] + "_" + list(agg_dict.keys())[0])
        color_col = config.get("color") if config.get("color") != "null" else None
        chart_type = config.get("chart_type", "折线图")
        # 使用 grouped 数据绘图
        if chart_type == "折线图":
            fig = px.line(grouped, x=x_col, y=y_col, color=color_col)
        elif chart_type == "柱状图":
            fig = px.bar(grouped, x=x_col, y=y_col, color=color_col)
        else:
            fig = px.line(grouped, x=x_col, y=y_col, color=color_col)
        return fig
    else:
        # 简单绘图（无聚合）
        x = config["x"]
        y = config["y"]
        color = config.get("color")
        chart_type = config.get("chart_type", "折线图")
        if chart_type == "折线图":
            fig = px.line(df, x=x, y=y, color=color)
        elif chart_type == "柱状图":
            fig = px.bar(df, x=x, y=y, color=color)
        else:
            fig = px.line(df, x=x, y=y, color=color)
        return fig

# 在自然语言生成图表的按钮逻辑中调用
if st.button("✨ 生成图表") and nl_query:
    with st.spinner("解析并生成中..."):
        try:
            fig = execute_nl_query(df, nl_query, st.session_state.api_key)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"生成失败: {e}")
