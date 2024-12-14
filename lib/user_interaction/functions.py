from lib.sqlite_db.functions import *
import os

def set_initialisation_variables():
    """
    initialisation of variables
    """
    flag_prompt = 0
    session = 0
    flag_resume = False
    return flag_prompt, session, flag_resume

def switch_session(user_input: str)->bool:
    """
    define the session: a session starts with the prompt 1, set the new session +1 and remove old history interaction from the
    variable history_interaction (but all the interaction remains in the db table)
    user_input: user question :str
    """
    if user_input.lower() in ["autre analyse"]:
        return True

def shutdown_pheobe(user_input:str)->bool:
    """
    shutdown the software
    user_input: user question :str
    """
    if user_input.lower() in ["merci", "stop"]:
        print()
        print("Fin de la conversation. Au revoir!")
        return True

def wrong_imput_user(user_input:str)->bool:
    """
    in case of wrong input, ask again 
    """
    if user_input=='':
        print("j'ai pas reçu de question de votre part, veuillez recommencer")
        return True

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

def get_summary(user_input:str)->bool:
    """
    get the complete summary of all the interactions
    user_input: user question :str
    """
    if user_input.lower() in ['avoir le résumé']:
        return True