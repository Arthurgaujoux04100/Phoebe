import os


def set_initialisation_variables():
    """
    initialisation of variables
    """
    flag_prompt = 0
    session = 0
    flag_resume = False
    return flag_prompt, session, flag_resume

def get_api_key(api:str)->str:
    """
    Retrieve the API key from environment variables based on the specified API name.

    Parameters:
    api (str): The name of the API for which the key is requested. 
               It should be either 'API_GPT_PHOEBE' or 'ELEVENLABS_API_KEY'.

    Returns:
    str: The API key as a string if the environment variable is set; otherwise, None.
    """
    if api=='API_GPT_PHOEBE':
        return os.getenv('API_GPT_PHOEBE')
    elif api=='ELEVENLABS_API_KEY':
        return os.getenv('ELEVENLABS_API_KEY')
