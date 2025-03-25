from google import genai

client = genai.Client(api_key="AIzaSyDwXgFl1zHt2jECuhpl0TF6lEIWZTd5s_I")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)