import streamlit as st
from fpdf import FPDF
import pandas as pd
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="数字化体能评估系统", layout="wide")

# --- 2. 界面标题 ---
st.title("🛡️ 数字化体能评估 & 报告系统")
st.caption("适用场景：新客户入场评估、定期体测跟踪")

# --- 3. 第一步：基本信息记录 ---
st.header("第一步：基础信息采集")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("客户姓名", "张三")
        gender = st.radio("性别", ["男", "女"], horizontal=True)
    with col2:
        age = st.number_input("年龄", 18, 80, 25)
        height = st.number_input("身高 (cm)", 140, 210, 175)
    with col3:
        weight = st.number_input("体重 (kg)", 40, 150, 70)

    exp = st.text_area("近期三个月运动经历", placeholder="例如：每周2次慢跑，无力量训练")
    medical_history = st.text_area("过往病史/损伤史", placeholder="例如：半月板旧伤，腰椎间盘突出")

# --- 4. 第二步：运动需求分析 ---
st.header("第二步：运动需求了解")
needs = st.multiselect(
    "选择客户的主要目标 (可多选)",
    ["增肌", "减脂", "运动表现提升", "体态改善", "疼痛缓解", "产后恢复", "压力管理"]
)

# --- 5. 第三步：全方位评估 ---
st.header("第三步：多维度综合评估")

# 5.1 静态体位评估
with st.expander("📸 静态体位评估 (记录观察结果)"):
    st.info("请观察客户在自然站立状态下的排列情况")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        posture_front = st.text_input("正侧观 (Front View)", "头偏、高低肩、骨盆旋转等")
        posture_back = st.text_input("背侧观 (Back View)", "足弓塌陷、脊柱侧弯等")
    with s_col2:
        posture_left = st.text_input("左侧观 (Left View)", "圆肩、头前引、骨盆前倾等")
        posture_right = st.text_input("右侧观 (Right View)", "同上")

# 5.2 灵活性动作评估
with st.expander("🤸 灵活性动作评估"):
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        toe_touch = st.select_slider("站姿摸脚尖", options=["无法触碰", "手指触地", "手掌触地"])
        shoulder_oh = st.select_slider("站姿肩屈过头举", options=["受限", "代偿", "正常"])
        rot_test = st.select_slider("站姿旋转测试", options=["明显受限", "轻度受限", "正常"])
    with f_col2:
        wall_flex = st.checkbox("靠墙肩屈测试 (正常)")
        wall_in_rot = st.checkbox("靠墙肩外展90度内旋 (正常)")
        wall_out_rot = st.checkbox("靠墙肩外展90度外旋 (正常)")

# 5.3 功能动作评估 (FMS 逻辑)
with st.expander("⚙️ 功能动作评估"):
    func_col1, func_col2 = st.columns(2)
    with func_col1:
        oh_squat = st.select_slider("过头深蹲评分", options=[1, 2, 3], help="1分代偿严重，3分动作完美")
        push_up_stab = st.select_slider("躯干稳定性俯卧撑", options=[1, 2, 3])
    with func_col2:
        aslr = st.select_slider("主动直膝抬腿", options=[1, 2, 3])

# 5.4 心肺 & 肌耐力测试
with st.expander("🫀 体能素质测试"):
    fit_col1, fit_col2 = st.columns(2)
    with fit_col1:
        step_test = st.number_input("三分钟台阶测试 (心率次/分)", 40, 200, 100)
    with fit_col2:
        st.write("**肌耐力表现 (记录完成次数/时间)**")
        push_up_count = st.number_input("上肢：俯卧撑 (次)", 0, 100, 0)
        crunch_count = st.number_input("躯干：仰卧卷腹 (次)", 0, 100, 0)
        wall_sit_time = st.number_input("下肢：静蹲 (秒)", 0, 300, 0)

# --- 6. 报告生成与下载 ---
st.divider()
if st.button("📝 生成评估报告"):
    # 报告逻辑处理
    st.success("报告已在后台生成！")
    
    # PDF 生成部分
    pdf = FPDF()
    pdf.add_page()
    
    font_path = "simhei.ttf"
    if os.path.exists(font_path):
        pdf.add_font('Chinese', '', font_path)
        pdf.set_font('Chinese', size=16)
    else:
        pdf.set_font('Arial', size=16)

    # 写入内容
    pdf.cell(200, 10, txt=f"体能评估报告: {name}", ln=True, align='C')
    pdf.set_font('Chinese' if os.path.exists(font_path) else 'Arial', size=10)
    pdf.ln(10)
    
    # 基础数据
    pdf.cell(0, 10, txt=f"性别: {gender} | 年龄: {age} | 身高: {height}cm | 体重: {weight}kg", ln=True)
    pdf.multi_cell(0, 10, txt=f"运动目标: {', '.join(needs)}")
    pdf.multi_cell(0, 10, txt=f"损伤史: {medical_history}")
    pdf.ln(5)
    
    # 评估结果摘要
    pdf.cell(0, 10, txt="--- 评估要点 ---", ln=True)
    pdf.multi_cell(0, 10, txt=f"静态表现: {posture_front}, {posture_left}")
    pdf.cell(0, 10, txt=f"心肺心率: {step_test} bpm", ln=True)
    pdf.cell(0, 10, txt=f"肌耐力: 俯卧撑 {push_up_count}次, 卷腹 {crunch_count}次, 静蹲 {wall_sit_time}秒", ln=True)

    pdf_output = pdf.output(dest='S')
    st.download_button(
        label="📥 下载 PDF 详细报告",
        data=pdf_output,
        file_name=f"{name}_Assessment.pdf",
        mime="application/pdf"
    )
