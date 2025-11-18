import os
from llama_cpp import Llama

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "Phi-3-mini-4k-instruct-IQ4_NL.gguf")

# Lazy load LLM to avoid loading on import
_llm = None

def _get_llm():
    """Lazy initialization of LLM."""
    global _llm
    if _llm is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}\n"
                "Please download Phi-3-mini-4k-instruct-IQ4_NL.gguf and place it in the project directory."
            )
        _llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,
            n_threads=6,
            n_gpu_layers=35,
            verbose=False
        )
    return _llm

def roast(context):
    """Generate a roast based on user's current activity context."""
    llm = _get_llm()
    prompt = f"""<|system|>
You output one short roast. Tone: toxic, rude, dry, gen-z, sarcastic.
use emojis contextually wisely at the end mostly. No kindness. No questions. No compliments. No positivity.
Max 10 words. Exactly one line. Never give explanations.
</|system|>

<|user|>
The user is currently: {context}
Roast be mean.
</|user|>

<|assistant|>
"""
    try:
        out = llm(
            prompt.strip(),
            max_tokens=40,
            temperature=0.7,
            top_p=0.9,
            stop=["<|user|>", "<|system|>", "</|assistant|>", "</|user|>", "\n\n"]
        )
        return out["choices"][0]["text"].strip().strip('"').strip("'")
    except Exception as e:
        return f"Error generating roast: {str(e)}"

def roast_reply(context, conversation_history=None):
    """Generate a roast response to user's message with conversation context."""
    llm = _get_llm()
    
    # Build conversation context if available
    history_text = ""
    if conversation_history:
        recent = conversation_history[-3:]  # Last 3 messages for context
        history_parts = []
        for role, msg, _ in recent:
            if role == "user":
                history_parts.append(f"User: {msg}")
            elif role == "roaster":
                history_parts.append(f"Roaster: {msg}")
        if history_parts:
            history_text = "\n".join(history_parts) + "\n"
    
    prompt = f"""<|system|>
You output one short roast in response to the user. Tone: toxic, rude, dry, gen-z, sarcastic.
use emojis contextually wisely at the end mostly. No kindness. No questions. No compliments. No positivity.
Max 15 words. Exactly one line. Never give explanations. Respond to what the user said.
</|system|>

{history_text}<|user|>
{context}
</|user|>

<|assistant|>
"""
    try:
        out = llm(
            prompt.strip(),
            max_tokens=50,
            temperature=0.8,
            top_p=0.9,
            stop=["<|user|>", "<|system|>", "</|assistant|>", "</|user|>", "\n\n"]
        )
        return out["choices"][0]["text"].strip().strip('"').strip("'")
    except Exception as e:
        return f"Error generating reply: {str(e)}"

