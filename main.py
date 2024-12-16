import openai
import argparse
import sqlite3
import os
from elevenlabs import ElevenLabs, VoiceSettings, play
from lib.sqlite_db.functions import initialize_db, insert_chat, delete_db
from lib.user_interaction.functions import switch_session, shutdown_pheobe, wrong_imput_user, get_summary
#from lib.model_IA.text_to_speech.elevenlabs import text_to_speech
from lib.processing.interaction_processing import get_history_interaction, process_answer
from lib.processing.initialization import set_initialisation_variables, get_api_key


openai.api_key = get_api_key('API_GPT_PHOEBE')

def main(temperature: float, token: int):
    print()
#    play(text_to_speech())
    print("""Démarrage de la conversation avec l'IA Phoebé. Dites 'autre analyse' pour ouvrir une autre session, avoir le résumé pour avoir le résumé complet de l'interaction, 'merci' ou 'stop' pour terminer la session.""")
    initialize_db()
    flag_prompt, session, flag_resume = set_initialisation_variables()
    print("Bonjour Maître")
    while True:
        user_input = input("Comment puis-je vous aider ?: ")

        if switch_session(user_input):
            session+=1
            flag_prompt = 0
            continue

        if shutdown_pheobe(user_input):
            delete_db()
            break

        if wrong_imput_user(user_input):
            continue

        if get_summary(user_input):
            flag_prompt = 2
            flag_resume = True
            
        history_interaction = get_history_interaction(session=session, get_summary_flag=flag_resume)
        response = process_answer(flag_prompt, user_input, temperature, token, history_interaction)
        insert_chat(user_input, response, session)
        flag_prompt=1
        flag_resume = False
        print()
        print()
        print("Phoebé: ", response)
        print()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--temperature", help="Set temperature (default is 1.0)", type=float, required=False, default=1.0)
    parser.add_argument("-tok", "--token", help="Set temperature (default is 1.0)", type=int, required=False, default=3000)
    args = parser.parse_args()
    main(args.temperature, args.token)
