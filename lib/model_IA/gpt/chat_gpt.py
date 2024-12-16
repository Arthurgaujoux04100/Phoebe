import openai
import os

def call_chat_api(user_input :str, temperature :float, token: int, prompt: str, history_interaction: str) -> str:
    """
    user_input : question utilisateur
    temperature: temperature modele
    token: nombre token max
    prompt: promt a utiliser
    Return : string
    """

    messages = [
        {"role": "system", "content": prompt + history_interaction},
     #   {"role": "user", "content": history_interaction},
        {"role": "user", "content": user_input} 
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages, 
        max_tokens=token,
        temperature = temperature
    )
    return response['choices'][0]['message']['content']






