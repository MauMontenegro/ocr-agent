tank_task_prompt = """You are an agent specialized in analyzing OCR-extracted text about the state of fuel tanks.  
    Your task is to extract the tank data and structure it into a JSON file according to the following schema:"""

tank_additional_prompt = """Return only the structured JSON, with no additional explanations. If a field is missing in the OCR text, set its value to 0."""


oxxo_task_prompt= """Extract product details and prices from OXXO purchase tickets.  
    Structure the data in JSON format.If there are repeated product, add them."""

oxxo_additional_prompt= """Return only the JSON, with no extra text."""