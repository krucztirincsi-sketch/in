import os
import json
from openai import OpenAI

# The DeepSeek API base URL is usually "https://api.deepseek.com/v1" or "https://api.deepseek.com"
# For this PoC, we rely on standard OpenAI client configured for DeepSeek.
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL) if DEEPSEEK_API_KEY else None

# Provide the LLM with the context of what tools it has available
ATOMIC_FUNCTIONS_DOC = """
Available Atomic Functions:

1. `aggregate_by_category(data: list, category_field: str, amount_field: str) -> dict`
   Aggregates an amount field by a category field.

2. `calculate_total(data: list, amount_field: str) -> float`
   Calculates the sum of an amount field across data.

3. `render_bar_chart(title: str, data_dict: dict) -> str`
   Renders a Bar Chart. 'data_dict' must be the output of aggregate_by_category.

4. `render_pie_chart(title: str, data_dict: dict) -> str`
   Renders a Pie Chart. 'data_dict' must be the output of aggregate_by_category.

5. `render_summary_text(title: str, text: str, sentiment: str) -> str`
   Renders a text box. sentiment can be "positive", "negative", "neutral", "calm", "anxious".

6. `render_table(title: str, data: list) -> str`
   Renders a data table from raw data list.
"""

def generate_execution_plan(intent: str, context: dict, data_schema: dict) -> dict:
    """
    Calls the DeepSeek LLM to map user intent and context into an execution plan.
    """
    if not client:
        # MOCK MODE if no API key is provided
        return _mock_execution_plan(intent, context)

    prompt = f"""
You are the Logic-to-Ontology Mapper (LOM) of the Subjective Logic Compiler.
Your job is to translate the user's fuzzy intent and emotional context into a strict sequence of atomic function calls to build a dynamic UI.

User Intent: {intent}
User Context (Emotion/State): {json.dumps(context)}
Input Data Schema: {json.dumps(data_schema)}

{ATOMIC_FUNCTIONS_DOC}

Respond ONLY with a valid JSON object representing the execution plan. The JSON should have a "steps" array.
Each step should have:
- "id": a unique string ID for the step.
- "function": the name of the atomic function to call.
- "inputs": a dictionary of inputs to the function.
  - To pass the raw input data, use the special string "$RAW_DATA" for the 'data' argument.
  - To pass the output of a previous step, use the special string "$STEP_<id>".
- "is_ui": boolean, true if the function returns HTML to be rendered.

Choose the UI elements and sentiment based on the user's intent and context. For example, if they are anxious, maybe use calmer text or simpler charts.

Example Output format:
{{
  "steps": [
    {{
      "id": "step1",
      "function": "calculate_total",
      "inputs": {{"data": "$RAW_DATA", "amount_field": "amount"}},
      "is_ui": false
    }},
    {{
      "id": "step2",
      "function": "render_summary_text",
      "inputs": {{"title": "Total Spent", "text": "$STEP_step1", "sentiment": "calm"}},
      "is_ui": true
    }}
  ]
}}
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a compiler that outputs ONLY valid JSON execution plans. No markdown formatting, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        content = response.choices[0].message.content.strip()
        # Clean up markdown block if the model included it despite instructions
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]

        return json.loads(content.strip())
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return _mock_execution_plan(intent, context)


def _mock_execution_plan(intent: str, context: dict) -> dict:
    """A fallback mock execution plan if DeepSeek is not configured."""
    emotion = context.get("emotion", "neutral")
    sentiment = "calm" if emotion in ["anxious", "stressed"] else "neutral"

    # A generic plan for testing based on common expense data structure
    plan = {
        "steps": [
            {
                "id": "calc_total",
                "function": "calculate_total",
                "inputs": {"data": "$RAW_DATA", "amount_field": "amount"},
                "is_ui": False
            },
            {
                "id": "render_total",
                "function": "render_summary_text",
                "inputs": {
                    "title": "Total Value",
                    "text": "$STEP_calc_total",
                    "sentiment": sentiment
                },
                "is_ui": True
            },
            {
                "id": "agg_cat",
                "function": "aggregate_by_category",
                "inputs": {"data": "$RAW_DATA", "category_field": "category", "amount_field": "amount"},
                "is_ui": False
            },
            {
                "id": "render_chart",
                "function": "render_pie_chart",
                "inputs": {"title": "Breakdown by Category", "data_dict": "$STEP_agg_cat"},
                "is_ui": True
            }
        ]
    }
    return plan
