import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag_pipeline import get_response
import streamlit as st

st.set_page_config(
    page_title="AI RAG Chatbot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Animated gradient background */
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Main container */
        .main .block-container {
            padding: 2rem 1rem 120px 1rem;
            max-width: 1000px;
        }
        
        /* Glassmorphic header */
        .header-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 24px;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1),
                        inset 0 1px 0 rgba(255, 255, 255, 0.2);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: fadeInDown 0.6s ease-out;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Title with glow effect */
        .header-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -2px;
            text-shadow: 0 0 40px rgba(255, 255, 255, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }
        
        .emoji-icon {
            font-size: 3rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
            margin-top: 1rem;
            font-weight: 400;
            letter-spacing: 0.5px;
            line-height: 1.6;
        }
        
        /* Chat messages container */
        .stChatMessage {
            background: transparent !important;
            padding: 0.5rem 0;
            margin-bottom: 1rem;
            animation: messageSlideIn 0.4s ease-out;
        }
        
        @keyframes messageSlideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* User message bubble */
        [data-testid="stChatMessage"][data-message-author="user"] > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.25rem 1.75rem;
            border-radius: 24px 24px 4px 24px;
            margin-left: auto;
            margin-right: 0;
            max-width: 70%;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            font-size: 1rem;
            line-height: 1.6;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        [data-testid="stChatMessage"][data-message-author="user"] > div:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
        }
        
        /* Assistant message bubble */
        [data-testid="stChatMessage"][data-message-author="assistant"] > div {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            color: #2d3748;
            padding: 1.25rem 1.75rem;
            border-radius: 24px 24px 24px 4px;
            margin-left: 0;
            margin-right: auto;
            max-width: 70%;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.4);
            font-size: 1rem;
            line-height: 1.7;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        [data-testid="stChatMessage"][data-message-author="assistant"] > div:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
        }
        
        /* Enhanced chat input */
        .stChatInput {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            padding: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.1);
            z-index: 999;
        }
        
        .stChatInput > div {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .stChatInput > div > div {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 28px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 0.75rem 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08),
                        inset 0 1px 0 rgba(255, 255, 255, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stChatInput > div > div:focus-within {
            border-color: #667eea;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
        }
        
        .stChatInput input {
            font-size: 1rem;
            color: #2d3748;
            font-weight: 400;
        }
        
        .stChatInput input::placeholder {
            color: #a0aec0;
            font-weight: 400;
        }
        
        /* Spinner animation */
        .stSpinner > div {
            border-top-color: #667eea !important;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Avatar styling */
        [data-testid="stChatMessage"] [data-testid="stAvatar"] {
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            width: 40px;
            height: 40px;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, 
                rgba(102, 126, 234, 0.6) 0%, 
                rgba(118, 75, 162, 0.6) 100%);
            border-radius: 10px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, 
                rgba(102, 126, 234, 0.9) 0%, 
                rgba(118, 75, 162, 0.9) 100%);
            background-clip: padding-box;
        }
        
        /* Message text styling */
        .stMarkdown {
            line-height: 1.7;
        }
        
        .stMarkdown p {
            margin-bottom: 0.5rem;
        }
        
        .stMarkdown code {
            background: rgba(102, 126, 234, 0.1);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        /* Hide Streamlit branding */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        /* Loading indicator */
        .stSpinner {
            text-align: center;
        }
        
        /* Welcome message for empty state */
        .welcome-message {
            text-align: center;
            padding: 4rem 2rem;
            color: rgba(255, 255, 255, 0.8);
            animation: fadeIn 1s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .welcome-message h2 {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: white;
        }
        
        .welcome-message p {
            font-size: 1.1rem;
            opacity: 0.9;
            line-height: 1.6;
        }
        
        /* Feature cards */
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <div class="header-title">
            <span class="emoji-icon"></span>
            <span>AI CHATBOT</span>
        </div>
        <p class="subtitle">Powered by Advanced RAG Technology • Ask anything about your documents</p>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="welcome-message">
            <h2>Welcome to AI Chatbot</h2>
            <p>I'm here to help you understand your documents. Ask me anything!</p>
        </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask a question about your PDFs..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=""):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=""):
        with st.spinner("Thinking..."):
            response = get_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()