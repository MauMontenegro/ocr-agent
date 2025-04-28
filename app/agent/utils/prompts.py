tank_task_prompt = """
Extract information from this fuel tanks document.
Extract the following information for each tank:
    - Tank name
    - Volumen
    - tc combustible
    - 100% vacío
    - altura
    - volumen de agua
    - temperatura   

Return the information in a form of a list of variables for each field described above. I f a field is missing add it with 0.
"""

purchase_ticket_task_prompt = """
Extract information from this purchase receipt.
Extract the following information:
- Store information
- Date and time of purchase
- List of purchased items with name, quantity and price
- Total amount
- Payment information (method, amount, change)

Return the information in a structured format.
"""

edenred_task_prompt = """
Extract information from this Edenred fuel purchase receipt.  
Extract the following details:  
- Terminal name and ID  
- Date and time of purchase  
- Authorization number  
- Product name  
- Quantity in liters  
- Unit price  
- Importe (subtotal before discounts)  
- Discount amount  
- Total amount after discounts  

Ensure accuracy in extracted values. If any field is missing, return an empty string ("").  
"""

dinamica_facebook_prompt ="""You are an information extraction agent specialized in gas station receipts.
Extract the following structured information from the OCR-processed text:

Extract the following fields:
- **Station**: Name or branch of the gas station
- **Address**: Complete address of the station
- **Date**: Transaction date in YYYY-MM-DD format
- **Volume**: Amount of fuel in liters/gallons
- **Total_Amount**: Total amount charged for the transaction

Only return these fields. If any information is not found, return an empty string for that field.
"""

# Document classifier prompt
classifier_prompt = """You are a document classifier specializing in OCR text.
Examine the following OCR text and determine which category it belongs to:

1. "tank_schematizer" - Tank monitoring reports with volume, temperature, and fuel levels
2. "oxxo_schematizer" - OXXO store receipts with product sales
3. "edenred_schematizer" - Transport Unit Purchase 
4. "facebook_schematizer" - Gas station receipts showing fuel purchases with volume, price per unit, and total amount
5. "unknown" - If the document doesn't clearly fit either category

Return ONLY the category name without any explanation.
"""