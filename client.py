from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-WxS17ehGk2PnwmzCHcDwT3BlbkFJFMj6bYTk9jG1bqZaFTcj",  # 🔒 Make sure to keep this secret in production
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Edith skilled in general tasks like Alexa and Google Assistant."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(response.choices[0].message.content)
