from lib.sqlite_db.functions import *
import os
from lib.model_IA.gpt.chat_gpt import call_chat_api
from lib.model_IA.gpt.prompt_function import load_prompt_from_file, replace_rag_info_in_prompt, select_prompt_path
from lib.search_engine.research_city_bar_table import process_user_input_for_bar_info


def get_history_interaction(session: int, get_summary_flag: bool)->str:
    """
    get the interaction history in a string to send it to gpt
    get_summary_flag: flag
    """
    if get_last_query(session)==None:
        history_interaction =""
        return history_interaction
    else:
        history_interaction = "Voici l'historique de notre conversation :\n"
        if get_summary_flag==True:
            for user_input, gpt in get_table():
                history_interaction += f"Utilisateur: {user_input}\nGPT: {gpt}\n"
            return history_interaction
        else:
            history_interaction += f"Utilisateur: {list(get_last_query(session))[0]}\nGPT: {list(get_last_query(session))[1]}\n"
            return history_interaction

def process_answer(flag_prompt:int, user_input :str, temperature :float, token: int, history_interaction: str)->str:
    """
    Process the answer by selecting the appropriate prompt, replacing placeholders, and calling the chat API.
    
    flag_prompt: An integer indicating which prompt to use.
    user_input: The user's question or input as a string.
    temperature: The temperature setting for the model, affecting randomness.
    token: The maximum number of tokens for the response.
    history_interaction: A string containing previous interaction history to include in the prompt.
    """
    prompt_path = select_prompt_path(flag_prompt)
    if flag_prompt==0:
        raw_prompt = load_prompt_from_file(prompt_path)
        rag_info = process_user_input_for_bar_info(user_input)
        prompt = replace_rag_info_in_prompt(rag_info, raw_prompt)
    else:
        prompt = load_prompt_from_file(prompt_path)
    answer = call_chat_api(user_input, temperature, token, prompt, history_interaction)
    return answer