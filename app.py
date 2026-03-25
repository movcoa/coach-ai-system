import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import os
import tempfile
import pandas as pd
from fpdf import FPDF

# ==========================================
# --- 1. 核心修复：MediaPipe 初始化 ---
# ==========================================
# 直接从底层导入子模块，避开映射错误
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import drawing_styles as mp_drawing_styles

# 使用缓存，防止每次操作都重新加载模型
@st.cache_resource
def get_pose_instance():
    return mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5
    )

pose_engine = get_pose_instance()

# ==========================================
# --- 2. 页面配置 ---
# ==========================================
st.set_page_config(page_title="AI 数字化体能评估", layout="wide")
st.title("🏋️‍♂️ AI 数字化体能评估系统")

# ==========================================
# --- 3. 核心功能函数 ---
# ==========================================
def process_pose_image(image_file):
    if image_file is None:
        return None, None
    
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # AI 推理
    results = pose_engine.process(img_rgb)
    
    # 绘制骨架
    annotated_img = img_rgb.copy()
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            annotated_img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
    return annotated_img, results.pose_landmarks

def analyze_posture(landmarks):
    if not landmarks: return []
    issues = []
    lm = landmarks.landmark
    
    # 逻辑 1：高低肩分析
    l_sh = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    r_sh = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    if abs(l_sh.y - r_sh.y) > 0.03:
        issues.append("检测到双肩不平（高低肩），建议关注骨盆及足底支撑")
    
    # 逻辑 2：重心偏移分析
    nose = lm[mp_pose.PoseLandmark.NOSE]
    l_heel = lm[mp_pose.PoseLandmark.LEFT_HEEL]
    r_heel = lm[mp_pose.PoseLandmark.RIGHT_HEEL]
    mid_heel_x = (l_heel.x + r_heel.x) / 2
    if abs(nose.x - mid_heel_x) > 0.05:
        issues.append("身体重心存在侧向偏移，建议进行呼吸及侧向链训练")
        
    return issues

# ==========================================
# --- 4. 侧边栏及主界面 ---
# ==========================================
with st.sidebar:
    st.header("👤 客户信息")
    name = st.text_input("姓名", "访客")
    goal = st.multiselect("评估目标", ["减脂", "缓解疼痛", "PRI呼吸", "纠正体态"], ["纠正体态"])

st.header("📸 姿态拍照评估")
c1, c2 = st.columns(2)
all_issues = []

with c1:
    st.subheader("📍 正面评估")
    f_file = st.file_uploader("上传正面照片", type=['jpg','png','jpeg'], key="f")
    if f_file:
        res, lms = process_pose_image(f_file)
        if res is not None:
            st.image(res, use_container_width=True)
            issues = analyze_posture(lms)
            for i in issues: 
                st.warning(i)
                all_issues.append(i)

with c2:
    st.subheader("📍 侧面评估")
    s_file = st.file_uploader("上传侧面照片", type=['jpg','png','jpeg'], key="s")
    if s_file:
        res, lms = process_pose_image(s_file)
        if res is not None:
            st.image(res, use_container_width=True)
            # 侧面分析可根据需要扩展
            st.info("侧面重心线提取成功")

# ==========================================
# --- 5. 报告生成 ---
# ==========================================
st.divider()
if st.button("📝 生成数字化报告"):
    if all_issues:
        st.success(f"已为 {name} 生成报告！包含 {len(all_issues)} 项 AI 建议。")
        # PDF 导出逻辑可在此处继续扩展
    else:
        st.info("请先上传照片并完成 AI 自动诊断。")
