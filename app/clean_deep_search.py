from utils.gemini_llm import call_gemini
from lib.prompts import DEEP_SEARCH_CLEANING_PROMPT
import json



def clean_deep_search(deep_search_results):
    FULL_PROMPT = f"{DEEP_SEARCH_CLEANING_PROMPT}\n\n{deep_search_results}"
    cleaned_data = call_gemini(FULL_PROMPT)
    try:
        return json.loads(cleaned_data)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_output": cleaned_data}