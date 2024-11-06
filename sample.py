from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "あなたは役に立つアシスタントです。"},
    {"role": "user", "content": "こんにちは！"}
  ]
)

print(completion.choices[0].message)