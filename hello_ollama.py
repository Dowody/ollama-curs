import ollama

MODEL = "qwen3:1.7b"

for chunk in ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "In one sentence, what is a vector embedding?"}],
    stream=True,
):
    print(chunk.message.content, end="", flush=True)
print()