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
You output one short roast. Tone: toxic, rude, dry, gen-z, sarcastic.
use emojis contextually wisely at the end mostly. No kindness. No questions. No compliments. No positivity.
Max 10 words. Exactly one line. Never give explanations.</|system|>

<|user|>
The user is currently: {context}
Roast be mean.
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
    return out["choices"][0]["text"].strip().strip('"').strip("'")

