import streamlit as st
from transformers import pipeline
from database_conn import DB



# Title of the web app
st.title("🤖 Chatbot Support")

# Load the chatbot model (cache to avoid reloading)
@st.cache_resource
def load_chatbot():
    return pipeline("text-generation", model="facebook/blenderbot-400M-distill")

chatbot = load_chatbot()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Check if session is new
if "session_started" not in st.session_state:
    st.session_state.session_started = True
    DB.clear_chat_history()  # Clears chat history at the start of a new session

# Load chat history from database **only once** at the start
if not st.session_state.chat_history:
    st.session_state.chat_history = DB.get_chat_history()

# Custom CSS for chat bubbles
st.markdown(
    """
    <style>
        .chat-container { max-width: 600px; margin: auto; }
        .user-msg { background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: right; }
        .bot-msg { background-color: #EAEAEA; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: left; }
        .timestamp { font-size: 12px; color: #888; margin-bottom: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat history in WhatsApp style
for user_msg, bot_msg, timestamp in st.session_state.chat_history:
    st.markdown(f"<div class='user-msg'>{user_msg}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='timestamp'>{timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='bot-msg'>{bot_msg}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='timestamp'>{timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# Input text box
user_input = st.text_input("You:", "")

# If user enters text, generate a response
if user_input:
    response = chatbot(user_input, max_length=100, do_sample=True)
    bot_response = response[0]["generated_text"]

    # Save chat in database
    DB.save_chat_to_db(user_input, bot_response)

     # Refresh page to display the new message
    st.rerun()

