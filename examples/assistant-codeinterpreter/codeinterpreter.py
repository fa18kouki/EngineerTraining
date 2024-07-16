import openai

# OpenAI APIキーを設定
openai.api_key = 'your-api-key'

def run_code_interpreter(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    prompt = "print('Hello, world!')"
    result = run_code_interpreter(prompt)
    print("Code Output:\n", result)
