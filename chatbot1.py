import streamlit as st
from database_conn import DB
from datasets import load_dataset
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, AutoModelForSequenceClassification
import torch
import pandas as pd
from huggingface_hub import login
import asyncio

# Replace 'your_huggingface_token' with your actual token
login(token="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")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load ServiceNow Insight Bench dataset
servicenow_dataset = load_dataset("json", data_files="insight_bench.json")

# Load Incident Management QA dataset
#incident_mgmt_dataset = load_dataset("arsen-r-a/incident-management-qa-test1")

# Print sample data
#print(servicenow_dataset["train"][0])  # First example from ServiceNow dataset
#print(incident_mgmt_dataset["train"][0])  # First example from Incident Management dataset

# Define standard column names (based on dataset inspection)
standard_columns = {
    'sys_updated_by', 'location', 'assignment_group', 'closed_by', 'priority',
    'caller_id', 'sys_updated_on', 'closed_at', 'assigned_to'
}

def normalize_data(example):
    """Ensures each row has the correct columns, filling missing values with 'N/A'"""
    row_data = {col: example.get(col, "N/A") for col in standard_columns}
    return row_data

# Convert to pandas to verify
#df = pd.DataFrame(normalize_data)
#print(df.head())
# Drop any extra columns that are not in the expected schema
#df = df[standard_columns]
#cleaned_dataset = Dataset.from_pandas(df)
# Apply normalization
normalized_dataset = servicenow_dataset.map(normalize_data)


# Load tokenizer
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
#tokenizer = AutoTokenizer.from_pretrained(model_name)

def format_dataset(example):
    """Formats dataset to instruction-response format"""
    instruction = example.get("question", "No question provided")
    response = example.get("answer", "No answer available")
    return {"instruction": instruction, "response": response}


#################
# Title of the web app
st.title("🤖 Chatbot Support")

# Load the chatbot model (cache to avoid reloading)

@st.cache_resource
def load_chatbot_model():
    # This line ensures the model is loaded in memory, preventing repeated API calls
    return pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", tokenizer="mistralai/Mistral-7B-Instruct-v0.1", device=0)

# Call API function (this could be blocking, so we run it in an event loop)
async def call_model_api(user_input):
    chatbot = load_chatbot_model()
    result = chatbot(user_input, max_length=200, num_return_sequences=1)
    return result[0]["generated_text"]

#chatbot = load_chatbot()

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
    try:
        bot_response = call_model_api(user_input)  # No asyncio needed
        DB.save_chat_to_db(user_input, bot_response)
        st.write("🤖 Chatbot:", bot_response)
    except Exception as e:
        st.error(f"Error occurred: {e}")

    # Display response
    st.write("🤖 Chatbot:", bot_response)

