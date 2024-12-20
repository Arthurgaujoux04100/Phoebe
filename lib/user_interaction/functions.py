from lib.sqlite_db.functions import *
import os
from lib.search_engine.research_city_bar_table import process_user_input_for_bar_info

class SessionManager:
    def __init__(self):
        self._rag_info = None

    def update_state_flags(self, state: dict, prompt: int, resume: bool, session: int) -> dict:
        """
         Update the session state with new values for 'flag_prompt', 'flag_resume', and 'session'.

         Parameters:
         prompt (int): The new value to set for 'flag_prompt', indicating the current prompt state.
         resume (bool): The new value to set for 'flag_resume', indicating whether a summary is requested.
         session (int): The new value to set for 'session', indicating the current session number.

         Returns:
         dict: The updated state dictionary reflecting the new values for 'flag_prompt', 'flag_resume', and 'session'.
         """
        state["flag_prompt"] = prompt
        state["flag_resume"] = resume
        state["session"] = session
        return state
    
    def wrong_input_user(self, user_input: str, state: dict) -> bool:
        """
        Check for incorrect user input and prompt for correction if necessary.

        Parameters:
        user_input (str): The user's input string to be validated.

        Returns:
        bool: True if the input is incorrect and a prompt is issued, False otherwise.
        """
        if not user_input:
            print("Je n'ai pas reçu de question de votre part, veuillez recommencer.")
            return True
        if state['flag_prompt'] == 0 and not self._rag_info:
            print("Erreur sur l'écriture de la ville, merci de vérifier.")
            return True

    def first_question(self, user_input: str, state: dict) -> bool:
        """
        Update the session state to indicate the first question has been processed.
        first question leads to RAG for the city and first prompt

        Parameters:
        state (dict): The current state of the session, including 'flag_prompt'.

        Returns:
         dict: The updated state with 'flag_prompt' set to 1 if it was initially 0.
        """
        if state['flag_prompt'] == 0:
            if self._rag_info is None: 
                self._rag_info = process_user_input_for_bar_info(user_input)
            return True
    
    def next_question(self, state: dict) -> bool:
        """
        Update the session state to indicate the first question has been processed.
        after the first question leads to other RAG

        Parameters:
        state (dict): The current state of the session, including 'flag_prompt'.
        """
        if state['flag_prompt'] == 1:
            return True

    def switch_session(self, user_input: str, state: dict) -> bool:
        """
        Switch to a new session if the user input matches the trigger phrase.
        
        Parameters:
        user_input (str): The user's input string.
        state (dict): The current state of the session, including 'session' and 'flag_prompt'.
        
        Returns:
        dict: The updated state with incremented session and reset flag_prompt if the condition is met.
        """
        if user_input.lower() in ["autre analyse"]:
            state = self.update_state_flags(state, prompt=0, resume=False, session=state['session'] + 1)
            self._rag_info = None 
            return True

    def shutdown_pheobe(self, user_input: str) -> bool:
        """
        shutdown the software
        user_input: user question :str
        """
        if user_input.lower() in ["merci", "stop"]:
            print("\nFin de la conversation. Au revoir!")
            delete_db()
            return True

    def get_summary(self, user_input: str, state: dict) -> bool:
        """
        Update the session state to indicate that a summary of all interactions is requested.

        Parameters:
        user_input (str): The user's input string.
        state (dict): The current state of the session, including 'flag_prompt' and 'flag_resume'.

        Returns:
        dict: The updated state with 'flag_prompt' set to 2 and 'flag_resume' set to True if the condition is met.
        """
        if user_input.lower() in ['avoir le résumé']:
            state = self.update_state_flags(state, prompt=2, resume=True, session=state['session'])
            return True

    def handle_user_input(self, user_input: str, state: dict) -> bool:
        """Handle the user input and update the session state accordingly."""

        if self.shutdown_pheobe(user_input):
            return "break"

        if self.first_question(user_input, state):
            if self.wrong_input_user(user_input, state):
                return "continue"
            else:
                return "process"
        
        if self.wrong_input_user(user_input, state):
            return "continue"

        if self.switch_session(user_input, state):
            return "continue"

        if self.get_summary(user_input, state):
            return "process"

        if self.next_question(state):
            return "process"


    def get_rag_info(self) -> dict:
        """Return the calculated rag_info."""
        return self._rag_info
    