import os, logging
import google.generativeai as genai
from dotenv import load_dotenv  


# silence the ALTS noise
logging.getLogger("absl").setLevel(logging.ERROR)
# 0.  Config -----------------------------------------------------------------
load_dotenv()
# 1.  Key ------------------------------------------------------------------
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if not GEMINI_KEY:
    raise RuntimeError("GEMINI_API_KEY env-var is empty")

genai.configure(api_key=GEMINI_KEY)
# 3.  Model ----------------------------------------------------------------
MODEL = genai.GenerativeModel("gemini-2.0-flash")   # or gemini-2.0-flash-exp

# 4.  Helper ---------------------------------------------------------------
def call_gemini(prompt: str) -> str:
    """Call Gemini LLM with a prompt and return the response text."""

    try:
        response = MODEL.generate_content(
            prompt,
            generation_config={"temperature": 0.0, "max_output_tokens": 10}
        )
        return response.text.strip().lower()
    except Exception as exc: 
        return f"error:{exc}"