import json
import re

def clean(raw_str, filename="cleaned_oxxo_data.json"):
    # Remove unnecessary newlines and whitespace
    print(f"Saving {filename} Schema",flush=True)
    raw_str = raw_str.strip()  
    # Convert single quotes to double quotes
    raw_str = re.sub(r"'", '"', raw_str)    
    raw_str.encode("utf-8").decode("utf-8")
    print(raw_str)    
    data = json.loads(raw_str)   

    print("Now is saving")
    # Save to a JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"JSON saved successfully as {filename}")