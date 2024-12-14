import openai
import os
from lib.model_IA.gpt.prompt_function import load_prompt_from_file, replace_rag_info_in_prompt, select_prompt_path

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
    

def process_answer(flag_prompt:int, rag_info:dict, user_input :str, temperature :float, token: int, history_interaction: str)->str:
    """
    Process the answer by selecting the appropriate prompt, replacing placeholders, and calling the chat API.
    
    flag_prompt: An integer indicating which prompt to use.
    rag_info: A dictionary containing information to replace placeholders in the prompt.
    user_input: The user's question or input as a string.
    temperature: The temperature setting for the model, affecting randomness.
    token: The maximum number of tokens for the response.
    history_interaction: A string containing previous interaction history to include in the prompt.
    """
    prompt_path = select_prompt_path(flag_prompt)
    raw_prompt = load_prompt_from_file(prompt_path)
    prompt = replace_rag_info_in_prompt(rag_info, raw_prompt)
    answer = call_chat_api(user_input, temperature, token, prompt, history_interaction)
    return answer



