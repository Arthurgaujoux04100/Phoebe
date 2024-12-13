import openai
import argparse
import sqlite3
import os
import argparse
from elevenlabs import ElevenLabs, VoiceSettings
from elevenlabs import play
from lib.sqlite_db.functions import *
from lib.model_IA.gpt.chat_gpt import get_response
from lib.user_interaction.functions import *
from lib.model_IA.text_to_speech.elevenlabs import text_to_speech


openai.api_key = os.getenv('API_GPT_PHOEBE')

def main(temperature: float, token: int):
    print()
    play(text_to_speech())
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
            
        prompt = prompt_choice(flag_prompt)
        history_interaction = get_history_interaction(session=session, get_summary_flag=flag_resume)
        response = get_response(user_input, temperature, token, prompt, history_interaction)
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
