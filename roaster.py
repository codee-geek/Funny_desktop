import os
from llama_cpp import Llama

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = "/Users/atharvawakade/Documents/funny01/Phi-3-mini-4k-instruct-IQ4_NL.gguf"


llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=6,
    n_gpu_layers=35,
    verbose=False
)

def roast(context):
    prompt = f"""
<|system|>
You output short, rude, sarcastic one-liner roasts. Max 12 words. No explanations. No multi-sentence. No helpful tone.
</|system|>

<|user|>
The user is currently: {context}
Roast them.
</|user|>

<|assistant|>
"""
    out = llm(
        prompt.strip(),
        max_tokens=40,
        temperature=0.7,
        top_p=0.9,
        stop=["<|user|>", "<|system|>", "</|assistant|>", "</|user|>", "\n\n"]
    )
    return out["choices"][0]["text"].strip()
