# 数据分析Agent部署指南

## 项目简介

这是一个基于Streamlit的网页版数据分析Agent，使用智谱AI的API进行智能分析，支持Excel和CSV文件上传、自动数据摘要、智能问答和数据可视化功能。

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
streamlit run app.py
```

### 3. 配置智谱AI API密钥

- 访问 [智谱AI开放平台](https://open.bigmodel.cn/) 注册账号并获取API密钥
- 在应用的侧边栏输入API密钥

## 部署到Streamlit Community Cloud

### 1. 准备工作

- 确保你有一个GitHub账号
- 创建一个新的GitHub仓库，将项目文件（app.py和requirements.txt）上传到仓库中

### 2. 部署步骤

1. 访问 [Streamlit Community Cloud](https://share.streamlit.io/)
2. 点击 "New app" 按钮
3. 选择你的GitHub仓库
4. 选择分支（通常是main/master）
5. 指定主文件路径：`app.py`
6. 点击 "Deploy!" 按钮

### 3. 配置环境变量（可选）

为了安全起见，你可以在Streamlit Community Cloud中设置环境变量来存储API密钥：

1. 在Streamlit应用管理页面，点击 "Settings"
2. 在 "Secrets" 部分，添加以下内容：
   ```
   api_key = "你的智谱AI API密钥"
   ```
3. 修改app.py文件，使用环境变量获取API密钥：
   ```python
   import os
   st.session_state.api_key = os.getenv("api_key", "")
   ```

### 4. 分享应用

部署完成后，你将获得一个公开的URL，可以分享给任何人访问。

## 使用说明

1. 在侧边栏上传Excel或CSV文件
2. 查看数据预览和基本信息
3. 输入智谱AI API密钥
4. 点击 "开始AI分析" 按钮
5. 查看侧边栏中的分析报告
6. 查看主区域中的可视化图表
7. 在智能问答区域输入问题，获得AI回答

## 功能特点

- **文件处理**：支持Excel (xlsx) 和 CSV 文件上传
- **数据预览**：自动显示数据前10行和基本信息
- **AI智能分析**：使用智谱AI的glm-4-flash模型生成分析报告
- **智能问答**：支持针对数据的自然语言提问
- **数据可视化**：自动生成合适的交互式图表
- **一键部署**：支持部署到Streamlit Community Cloud

## 注意事项

- 确保你的智谱AI API密钥有足够的配额
- 对于大型数据集，分析可能需要较长时间
- 请遵守智谱AI的使用条款和数据隐私政策
