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

dinamica_facebook_prompt ="""Eres un agente especializado en extracción de información de tickets de gasolina escaneados mediante OCR.

A partir del siguiente texto extraído por OCR, identifica y devuelve exclusivamente los siguientes campos en formato estructurado y con el tipo de dato indicado:

- **Estación**: Nombre o sucursal de la gasolinera (string).  
- **Dirección**: Dirección completa de la estación (string).  
- **Fecha**: Fecha de la transacción, en formato AAAA-MM-DD (date).  
- **Volumen**: Cantidad de combustible cargado (en litros o galones, según se indique) (flotante).  
- **Cantidad o Importe**: Total o importe cobrado por la gasolina (flotante).

Devuelve únicamente estos campos como resultado.  
Si alguno de los datos no puede encontrarse en el texto, devuelve una cadena vacía (`""`) en ese campo.
"""

# Document classifier prompt
classifier_prompt = """You are a document classifier specializing in OCR text.
Examine the following OCR text and determine which category it belongs to:

1. "tank_schematizer" - Tank monitoring reports with volume, temperature, and fuel levels
2. "oxxo_schematizer" - OXXO store receipts with product sales
3. "edenred_schematizer" - Transport Unit Purchase 
4. "facebook_schematizer" - Gas station receipts of 'Dispensarios' machines of redpetroil enterprise and petroplazas showing fuel purchases with volume, address, gas station and total amount
5. "unknown" - If the document doesn't clearly fit either category

Return ONLY the category name without any explanation.
"""