import os
import streamlit as st
import requests
from datetime import datetime
from history_manager import add_to_json, read_from_json

def get_response_with_prompt(user_input):
    url = "http://localhost:8000/generate_with_prompt/"
    data = {"question": user_input, "document_path": None}
    response = requests.post(url, json=data)
    answer_text = response.json()['answer']
    res = answer_text.replace('<eod>', '').strip()
    return res

def get_response_with_rag(user_input, document_path):
    url = "http://localhost:8000/generate_with_rag/"
    data = {"question": user_input, "document_path": document_path}
    response = requests.post(url, json=data)
    answer_text = response.json()['answer']
    res = answer_text.replace('<eod>', '').strip()
    return res

def fetch_content_from_api(url):
    api_url = "http://101.200.73.250:7860/fetch-content/"
    params = {"url": url}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json().get("content", "")
    else:
        return "无法获取内容，请检查输入的url是否正确"

    
st.set_page_config(layout="wide")
st.title("博客阅读助手")

# 创建两个列布局，一个用于显示爬虫内容，一个用于显示大模型输出
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 爬虫预览")

    url_input = st.text_input("输入URL")
    file_name = st.text_input("输入要保存的文件名", value="default")
    current_date = datetime.now().strftime("-%Y-%m-%d")
    file_name = file_name + current_date + ".txt"
    file_path = f"./{file_name}"
    
    if st.button("提交URL", key="submit_url"):
        content = fetch_content_from_api(url_input)
    
        if not content:
            content = "没有抓取到内容。"
    
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    
        add_to_json(file_name)  # 将文件名添加到JSON中
    
        st.write("爬虫文本预览:")
        st.write(content)

        # 将文件内容作为输入，调用 get_response_with_prompt
        answer = get_response_with_prompt(content)
        
        with col2:
            st.markdown("## 文章评价")
            st.write(answer)

        # 将返回的response写入JSON文件
        add_to_json(file_name, answer)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            saved_content = file.read()
    else:
        saved_content = "没有找到对应的内容。"
    
    st.write("已保存的爬虫内容:")
    st.write(saved_content)

with col2:
    st.markdown("## 文章问答")
    # 添加下拉展示框
    saved_files = read_from_json().keys()  # 获取所有已保存的文件名
    selected_file = st.selectbox("选择已保存的文件", saved_files)
    
    user_input = st.text_input("用户输入", key="user_input")
    if st.button("输入问题", key="input_button"):
        answer = get_response_with_rag(user_input, selected_file)
        if not answer:
            answer = "没有生成回答。"
        
        st.write("大模型输出:")
        st.write(answer)

st.markdown("## 历史记录")

# 读取 JSON 中的所有数据
history_data = read_from_json()

# 格式化历史记录
history_text = ""
for file_name, output in history_data.items():
    history_text += f"文件名: {file_name}\n大模型输出: {output}\n\n"

# 在文本区域中显示历史记录
st.text_area("历史记录", history_text, height=50)

# 导出设置
with st.expander("导出设置"):
    st.markdown("在这里选择导出选项")
    if st.button("导出 JSON 数据"):
        st.write("导出功能尚未实现")