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

# Check if session is new
if "session_started" not in st.session_state:
    st.session_state.session_started = True
    DB.clear_chat_history()  # Clears chat history at the start of a new session

# Retrieve chat history from database
st.subheader("Chat History")
chat_history = DB.get_chat_history()
for user_msg, bot_msg, timestamp in chat_history:
    st.write(f"🧑 {user_msg} (at {timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
    st.write(f"🤖 {bot_msg}")
    st.write("---")

# Input text box
user_input = st.text_input("You:", "")

# If user enters text, generate a response
if user_input:
    response = chatbot(user_input, max_length=100, do_sample=True)
    bot_response = response[0]["generated_text"]

    # Save chat in database
    DB.save_chat_to_db(user_input, bot_response)

    # Display response
    st.write("🤖 Chatbot:", bot_response)

