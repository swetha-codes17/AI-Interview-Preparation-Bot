from groq import Groq
client = Groq(api_key="groq_api_key")
response = client.chat.completions.create(model = "llama-3.1-8b-instant",messages=[
    {"role": "user", "content":"say hello" }
]
)
print(response.choices[0].message.content)
