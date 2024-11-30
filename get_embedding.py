import re
import numpy as np
import google.generativeai as genai



def get_embedding(text, model="models/text-embedding-004"):
    # Convert non-string input to an empty string
    if not isinstance(text, str):
        text = ""

    # Return a default vector if the text is empty or whitespace only
    if not text.strip():
        return np.zeros(768)  # Assuming a 768-dimensional vector as default
    # Pre-process text to remove newline characters
    text = text.replace("\n", " ")
    # Remove email addresses
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '', text)
    # Remove content inside parentheses
    text = re.sub(r"\([^()]*\)", "", text)
    # Remove "From: " and "Subject: " prefixes
    # text = text.replace("From: ", "").replace("\nSubject: ", "")
    # Remove newlines, curly braces, and any special characters
    text = re.sub(r"[\n@(){}]", " ", text)
    # Remove other non-word characters and extra spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Generate the embedding using the specified model
    result = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document",
        title="Embedding of Email Phishing"
    )

    # Extract the embedding vector from the response
    embedding_results = result['embedding']

    return embedding_results

