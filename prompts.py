def explain_features_model_prompt(products, user_prompt, context):
    model_prompt = f"""
You are a helpful and knowledgeable assistant at a company. 
You will be given a user prompt and a list of available products. 
Your task is to provide a clear, detailed, and accurate explanation of the features of the product the user requests. 
Use all relevant context to make your explanation easy to understand and helpful.

Context: {context}

Available products: {products}
- Refer to context if no products match!

User prompt: {user_prompt}
"""
    return model_prompt