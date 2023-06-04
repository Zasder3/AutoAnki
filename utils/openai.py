import os
import openai

def init_openai_api() -> None:
    # check if SECRET file exists
    if not os.path.exists("SECRET"):
        raise Exception("SECRET file not found. Please run make_secret.py first.")
    # read SECRET file
    with open("SECRET", "r") as f:
        secret = f.read()
    
    openai.api_key = secret

def complete_request(prompt: str) -> dict:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response
