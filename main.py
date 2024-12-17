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
    state = set_initialisation_variables()
    print("Bonjour Maître")
    while True:
        user_input = input("Comment puis-je vous aider ?: ")
        action = session_manager.handle_user_input(user_input, state)
        if action == "break":
            break
        elif action == "continue":
            continue
        elif action =="process":
            bar_info = session_manager.get_rag_info()
            history_interaction = get_history_interaction(session, state["flag_resume"])
            response = process_answer(state["flag_prompt"], user_input, temperature, token, history_interaction, bar_info)
            insert_chat(user_input, response, state["session"])
            state = session_manager.update_state_flags(state, prompt=1, resume=False, session=state['session'])
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
