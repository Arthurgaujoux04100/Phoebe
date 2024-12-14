import os

def select_prompt_path(flag_prompt: int)->str:
    """
    return the good prompt
    flag_prompt: prompt number : int
    return
        prompt str : str
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    prompt_dir = os.path.join(base_path, 'prompts')  
    if flag_prompt == 0:
        return os.path.join(base_path, 'prompts', 'Phoebe_analyse_detailed.txt')
    elif flag_prompt == 1:
        return os.path.join(base_path, 'prompts', 'Phoebe_2nd_round.txt')
    elif flag_prompt == 2:
        return os.path.join(base_path, 'prompts', 'Phoebe_summary.txt')


def load_prompt_from_file(prompt:str)->str:
    """
    prompt: path of the prompt
    """
    with open(f'{prompt}', 'r') as file:
        return file.read()


def replace_rag_info_in_prompt(rag_info:dict, prompt:str)->str:
    """
    replace the RAG information in the prompt 
    """
    for placeholder, value in rag_info.items():
        prompt = prompt.replace(f"{{{placeholder}}}", value)
    return system_message