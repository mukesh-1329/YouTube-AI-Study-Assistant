from huggingface_hub import InferenceClient
from config import HF_API_KEY , MODEL_NAME

#MODEL_NAME= "meta-llama/Meta-Llama-3-8B-Instruct"
# Initialize client
client = InferenceClient(
    model=MODEL_NAME,
    token=HF_API_KEY
)


def query_hf(prompt):
    try:
        output = ""

        for message in client.chat_completion(
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            stream=True,
        ):
            if message.choices and len(message.choices) > 0:
                content = message.choices[0].delta.content
                if content:
                    output += content

        return output

    except Exception as e:
        return f"LLM Error: {str(e)}"