from aip import AipImageClassify, AipOcr
import streamlit as st
from PIL import Image
import os

# ====================== 配置百度API密钥 ======================
APP_ID = '122689279'
API_KEY = 'cVIy9EdGHF395RGvdxu1CAoa'
SECRET_KEY = 'LjCgtyDepr653msDgcG4JLTJmSfZgX8S'

# 初始化百度AI客户端
client_tag = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)  # 图像标签识别
client_ocr = AipOcr(APP_ID, API_KEY, SECRET_KEY)  # 文字OCR识别

# ====================== 页面配置 ======================
st.set_page_config(page_title="智能图像识别工具", page_icon="📷")
st.title("📷 智能图像识别工具")
st.subheader("学号：202335020643 | 姓名：吴志轩")
st.divider()


# ====================== 核心工具函数 ======================
def get_file_content(file_path):
    """读取图片二进制数据"""
    with open(file_path, 'rb') as fp:
        return fp.read()


def recognize_image_tag(image_path):
    """调用百度AI识别图像标签"""
    image = get_file_content(image_path)
    # 调用通用物体识别接口
    result = client_tag.advancedGeneral(image)
    return result


def recognize_text_ocr(image_path):
    """调用百度AI识别图片文字"""
    image = get_file_content(image_path)
    # 调用通用文字识别接口
    result = client_ocr.basicGeneral(image)
    return result


# ====================== 界面交互 ======================
st.write("### 1. 上传图片（支持jpg/png/jpeg）")
uploaded_file = st.file_uploader("选择图片", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 保存临时图片
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 显示上传的图片
    image = Image.open(temp_path)
    st.image(image, caption='上传的图片', use_column_width=True)

    # 1. 图像标签识别结果
    st.write("### 2. 图像识别结果（物体标签+置信度）")
    tag_result = recognize_image_tag(temp_path)
    if 'result' in tag_result:
        for item in tag_result['result']:
            st.write(f"🏷️ 标签：{item['keyword']} | 置信度：{round(item['score'], 4)}")
    else:
        st.error("❌ 图像标签识别失败，请检查API密钥或网络")

    # 2. 文字OCR识别结果
    st.write("### 3. 图片文字提取（OCR）")
    text_result = recognize_text_ocr(temp_path)
    if 'words_result' in text_result:
        if text_result['words_result']:
            for item in text_result['words_result']:
                st.write(f"📝 识别文字：{item['words']}")
        else:
            st.info("ℹ️ 图片中未识别到文字")
    else:
        st.error("❌ 文字OCR识别失败，请检查API密钥或网络")

    # 删除临时文件
    os.remove(temp_path)