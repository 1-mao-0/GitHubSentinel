import streamlit as st
import whisper
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 设置页面标题和布局
st.set_page_config(page_title="ChatPPT Assistant", layout="wide")
st.title("🎤 ChatPPT Assistant: Voice & Text Interaction")

# 初始化会话状态（保存聊天历史）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏：模型选择和配置
with st.sidebar:
    st.header("Settings")
    # 选择输入模式：语音或文本
    input_mode = st.radio("Input Mode", ["Text", "Voice"])

# --- 模型加载（缓存避免重复加载） ---
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")  # 可选 "small", "medium"

@st.cache_resource
def load_minicpm_model():
    model_name = "openbmb/MiniCPM-2B-dpo-fp16"  # 替换为实际模型路径
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
    return model, tokenizer

whisper_model = load_whisper_model()
minicpm_model, minicpm_tokenizer = load_minicpm_model()

# --- 功能函数 ---
def transcribe_audio(audio_path):
    """Whisper 语音转文本"""
    result = whisper_model.transcribe(audio_path)
    return result["text"]

def generate_text(prompt):
    """MiniCPM 生成文本"""
    inputs = minicpm_tokenizer(prompt, return_tensors="pt")
    outputs = minicpm_model.generate(**inputs, max_length=200)
    return minicpm_tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- 主交互逻辑 ---
# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 输入区域
if input_mode == "Voice":
    uploaded_audio = st.file_uploader("Upload Audio", type=["wav", "mp3"])
    if uploaded_audio:
        with st.spinner("Transcribing audio..."):
            text = transcribe_audio(uploaded_audio.name)
            st.session_state.messages.append({"role": "user", "content": text})
            with st.chat_message("user"):
                st.markdown(text)
else:
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

# 生成回复
if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = generate_text(st.session_state.messages[-1]["content"])
            st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
