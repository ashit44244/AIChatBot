import pandas as pd
import google.generativeai as genai
import json

# Set Google Gemini API key
genai.configure(api_key="AIzaSyDwXgFl1zHt2jECuhpl0TF6lEIWZTd5s_I")  # Replace with your actual API key
models = genai.list_models()
for model in models:
    print(model.name, "->", model.supported_generation_methods)

# Load the user event data (CSV or JSON)
def load_user_data(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")

# Convert user event logs into a structured prompt for LLM
def format_prompt(user_data):
    sample_logs = user_data[['User_ID', 'Timestamp', 'Event_Type', 'Field_Name', 'Time_Spent (ms)', 'Error_Message', 'Button_Clicked', 'Page_Name', 'Navigation_Pattern', 'Form_Completed']].head(10).to_json(orient='records')
    prompt = f"""
    Analyze the following user interaction logs and identify patterns:
    {sample_logs}
    
    - What fields are causing hesitation?
    - Are there frequent errors in specific fields?
    - Where do users drop off most?
    - Suggestions to improve UX based on these behaviors.
    
    Provide a structured response.
    """
    return prompt

# Function to call Google Gemini LLM
def analyze_with_llm(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# Main execution
if __name__ == "__main__":
    file_path = "c2t_events_data.csv"  # Change this to your dataset file
    user_data = load_user_data(file_path)
    prompt = format_prompt(user_data)
    insights = analyze_with_llm(prompt)
    
    print("\n🔍 User Behavior Insights:")
    print(insights)