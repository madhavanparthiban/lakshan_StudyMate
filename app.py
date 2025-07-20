import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API
#genai.configure(api_key="AIzaSyBbhMS4yL2PypXvZJnol6uGBzWjkMSwi5w")
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
# Initialize the model
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    generation_config=genai.types.GenerationConfig(max_output_tokens=150)
)

# Hide Streamlit's default menu and footer
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(
    page_title="Study Mate",
    page_icon="📚",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    .header {
        color: #2e4057;
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(145deg, #ffffff, #e6e9f0);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .chat-container {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        padding: 1.5rem;
        margin-bottom: 1rem;
        height: 65vh;
        overflow-y: auto;
    }
    .user-message {
        background-color: #e3f2fd;
        border-radius: 15px 15px 0 15px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-message {
        background-color: #f0f4f8;
        border-radius: 15px 15px 15px 0;
        padding: 0.8rem;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .stTextInput>div>div>input {
        background-color: white !important;
    }
    .clear-btn {
        background-color: #ff6b6b !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .timestamp {
        font-size: 0.7rem;
        color: #718096;
        text-align: right;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<div class="header"><h1>📚 Study Mate</h1><p>Your AI learning assistant</p></div>', unsafe_allow_html=True)

# Sidebar for additional features
with st.sidebar:
    st.header("Settings")
    if st.button("🧹 Clear Chat History", key="clear", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()

    st.markdown("- ✏️ Study assistant")
    st.markdown("- 📝 Concept explanations")
    st.markdown("- 🧠 Problem solving")
    st.markdown("- 💬 Q&A support")


# Chat container
with st.container():
   # st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; color: #718096;'>
            <h3>How can I help you study today?</h3>
            <p>Ask questions about any subject!</p>
            <div style='margin-top: 2rem;'>
                <p>Try asking:</p>
                <p>• Explain quantum physics in simple terms</p>
                <p>• Help me solve this calculus problem</p>
                <p>• What's the difference between mitosis and meiosis?</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You</strong>
                    <div>{msg["content"]}</div>
                    <div class="timestamp">{msg.get("time", "")}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <strong>Study Mate</strong>
                    <div>{msg["content"]}</div>
                    <div class="timestamp">{msg.get("time", "")}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Ask a study question...")
if prompt:
    # Add timestamp
    current_time = datetime.now().strftime("%H:%M")
    
    # Add user message
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "time": current_time
    })
    
    # Generate response
    with st.spinner("Thinking..."):
        response = model.generate_content(f"{prompt}. Please respond briefly in 3-4 lines.")
        bot_reply = response.text
    
    # Add bot message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": bot_reply,
        "time": current_time
    })
    
    st.rerun()