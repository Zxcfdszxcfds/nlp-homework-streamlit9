import streamlit as st
import jieba
import jieba.posseg as pseg
import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# ---------------------- 页面配置 ----------------------
st.set_page_config(
    page_title="中文词法分析器",
    page_icon="🔤",
    layout="wide"
)

# ---------------------- 工具函数 ----------------------
def text_normalization(text):
    """文本规范化：去除特殊符号、全角转半角、简体化"""
    # 去除特殊符号
    text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)
    # 全角转半角
    text = text.replace('，', ',').replace('。', '.').replace('；', ';').replace('：', ':')
    text = text.replace('（', '(').replace('）', ')').replace('、', ',').replace('！', '!')
    return text

def jieba_cut(text, mode="default"):
    """不同模式的jieba分词"""
    if mode == "精准模式":
        return list(jieba.cut(text))
    elif mode == "全模式":
        return list(jieba.cut(text, cut_all=True))
    elif mode == "搜索引擎模式":
        return list(jieba.cut_for_search(text))

def pos_tagging(text):
    """词性标注，返回带词性的词列表"""
    return [(word, flag) for word, flag in pseg.cut(text)]

def get_word_freq(words, top_n=5):
    """统计词频"""
    freq = Counter(words)
    return freq.most_common(top_n)

# ---------------------- 主界面 ----------------------
st.title("🔤 中文词法分析器")
st.markdown("---")

# 输入框
input_text = st.text_area("输入中文文本", value="南京市长江大桥是一座宏伟的桥梁。", height=100)

if st.button("开始分析"):
    # 区块1：文本规范化
    st.subheader("📝 文本规范化结果")
    norm_text = text_normalization(input_text)
    st.code(norm_text, language="text")

    # 区块2：多算法分词对比
    st.subheader("✂️ 多算法分词对比")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**精准模式**")
        seg1 = jieba_cut(norm_text, "精准模式")
        st.write(" ".join(seg1))
    with col2:
        st.markdown("**全模式**")
        seg2 = jieba_cut(norm_text, "全模式")
        st.write(" ".join(seg2))
    with col3:
        st.markdown("**搜索引擎模式**")
        seg3 = jieba_cut(norm_text, "搜索引擎模式")
        st.write(" ".join(seg3))

    # 词频统计与可视化
    st.subheader("📊 词频统计（Top5）")
    all_words = seg1
    freq = get_word_freq(all_words)
    freq_df = pd.DataFrame(freq, columns=["词", "频次"])
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(freq_df, use_container_width=True)
    with col2:
        fig, ax = plt.subplots()
        ax.bar(freq_df["词"], freq_df["频次"], color="#1f77b4")
        st.pyplot(fig)

    # 区块3：词性标注可视化
    st.subheader("🏷️ 词性标注结果")
    pos_result = pos_tagging(norm_text)
    # 词性颜色映射
    pos_colors = {
        "n": "red",      # 名词
        "v": "blue",     # 动词
        "a": "green",    # 形容词
        "d": "orange",   # 副词
        "p": "purple"    # 介词
    }
    # 生成带颜色的HTML文本
    html_text = ""
    for word, flag in pos_result:
        color = pos_colors.get(flag[0], "black")
        html_text += f'<span style="color:{color};">{word}</span> '
    st.markdown(html_text, unsafe_allow_html=True)

st.markdown("---")
st.markdown("© 2025 NLP 课程实验 | 中文词法分析器")
