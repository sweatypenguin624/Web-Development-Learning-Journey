from main import checkAllClaims

def preprocessor(input_data):
    if isinstance(input_data, str):
        # Only treat as text content, no file checking
        return input_data
    else:
        raise ValueError("Input must be a string (text only), no files allowed")

def processor(text):
    query = preprocessor(text)
    return checkAllClaims(query)