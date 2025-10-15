

TARGET_TYPE_PROMPT = (
    "You are a classifier.\n"
    "I will give you a single target string.\n"
    "Reply with exactly one word from this list:\n"
    '["person", "email", "phone", "other"]\n'
    "Do not add spaces, punctuation, or explanations."
)
DEEP_SEARCH_CLEANING_PROMPT = (
    "Clean this JSON data from an OSINT search on a target (type: person/email/phone). "
    "Extract only key target info into a structured JSON, adapting fields to the type "
    "(e.g., for person: name/job/profiles; for email: associated persons/breaches; "
    "for phone: owner/location). Ignore metadata, summaries, and irrelevant results. "
    "Output just the JSON—no extra text.\n\n"
    "Output format (use null/empty if no data; customize per type):\n"
    "{\n"
    "  \"target_type\": \"string (person/email/phone)\",\n"
    "  \"target_value\": \"string (e.g., name/email/phone)\",\n"
    "  \"primary_details\": \"object with 2-4 key-value pairs specific to type (e.g., for person: {'location': '...', 'occupation': '...'} ) or null\",\n"
    "  \"profiles_mentions\": {\"platform\": \"URL/handle/array\" for each relevant platform} or null,\n"
    "  \"associated_entities\": {\"emails\": [\"list\"] or null, \"phones\": [\"list\"] or null, \"persons\": [\"list\"] or null},\n"
    "  \"timeline_events\": [{\"date\": \"YYYY-MM-DD\", \"event\": \"string\"}] or null,\n"
    "  \"contacts\": {\"emails\": [\"list\"] or null, \"phones\": [\"list\"] or null},\n"
    "  \"notes\": \"string (insights/gaps) or null\"\n"
    "}\n\n"
    "Be concise and relevant. Ensure valid JSON output.\n"
    "JSON data:\n"
)

