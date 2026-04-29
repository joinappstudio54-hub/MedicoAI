import json
import re

def safe_parse_json(text: str):
    """
    Cleans and safely parses LLM output into JSON
    """

    if not text:
        raise ValueError("Empty response from model")

    text = text.strip()

    # remove markdown blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format from model: {str(e)}")