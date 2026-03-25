import streamlit as st
from fpdf import FPDF
import pandas as pd
import plotly.express as px

# --- 页面设置 ---
st.set_page_config(page_title="教练专业评估系统", layout="centered")

st.title("🏃‍♂️ 新客户体能评估系统")

# --- 1. 数据获取模块 ---
with st.form("assessment_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("客户姓名")
        goal = st.selectbox("训练目标", ["减脂", "增肌", "疼痛缓解", "运动表现"])
    with col2:
        age = st.number_input("年龄", 18, 80, 30)
        gender = st.radio("性别", ["男", "女"], horizontal=True)

    st.subheader("物理评估")
    left_aic = st.toggle("左侧 AIC 模式 (Left AIC Pattern)")
    shoulder_rom = st.slider("肩屈曲活动度 (度)", 90, 180, 170)
    
    submitted = st.form_submit_button("生成评估报告")

# --- 2. 自动化诊断逻辑 ---
if submitted:
    issues = []
    recommendations = []
    
    if left_aic:
        status = "存在典型 Left AIC 模式"
        issues.append("骨盆排列：左侧前倾/外旋")
        recommendations.append("1. 90/90 呼吸练习 (激活左侧腘绳肌)")
        recommendations.append("2. 右侧内收肌激活训练")
    else:
        status = "骨盆排列基本中立"

    if shoulder_rom < 165:
        issues.append("上肢受限：肩关节活动度不足")
        recommendations.append("3. 胸廓后侧扩张呼吸感官训练")

    # --- 3. 可视化展示 (iPad 端预览) ---
    st.divider()
    st.header(f"{name} 的评估结果")
    
    st.info(f"**当前状态：** {status}")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.write("**待改善问题：**")
        for issue in issues:
            st.write(f"❌ {issue}")
    with col_res2:
        st.write("**针对性建议：**")
        for rec in recommendations:
            st.write(f"✅ {rec}")

# --- 4. PDF 生成与下载 ---
from fpdf import FPDF
import os

# 在生成 PDF 的逻辑块里
pdf = FPDF()
pdf.add_page()

# --- 关键修改点：加载中文字体 ---
# 确保 simhei.ttf 就在 app.py 同级目录下
font_path = "simhei.ttf" 

if os.path.exists(font_path):
    pdf.add_font('ChineseFont', '', font_path)
    pdf.set_font('ChineseFont', size=12)
else:
    # 如果没找到字体，先用普通字体防止报错，但中文会乱码
    pdf.set_font("Arial", size=12) 
    st.error("未找到字体文件 simhei.ttf，PDF 中文将显示异常")

# --- 写入内容 ---
pdf.cell(40, 10, f"姓名: {name}") # 现在可以正常写入中文了
pdf.ln(10)
pdf.cell(40, 10, f"目标: {goal}")

