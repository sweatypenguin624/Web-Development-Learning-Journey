import mimetypes, os
from geminiVision import caption
from geminiAudio import captionAudio
from main import checkAllClaims

def preprocessor(input_data):
    if isinstance(input_data, str):
        if os.path.isfile(input_data):
            # This is a file path
            mime_type, _ = mimetypes.guess_type(input_data)
            if mime_type:
                if mime_type.startswith('image'):
                    return mime_type + "\n" + caption(input_data)
                elif mime_type.startswith('audio'):
                    return mime_type + "\n" + captionAudio(input_data)
            else:
                # Treat as text content
                return input_data
        else:
            # This is text content
            return input_data
    else:
        return "Invalid input type"

def processor(*args):
    query = ""
    for arg in args:
        query += preprocessor(arg)
    return checkAllClaims(query)