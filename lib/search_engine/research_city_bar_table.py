import os
from rapidfuzz import process, fuzz
from lib.model_IA.bert.camenBert_ner import get_city_name
from lib.postgresSQL.table_function import get_bar_name, get_all_french_cities


def rectify_city_name(city_name:list)->list:
    """
    overcome typing error by trying to find a match with all the cities in the postgresSQLdatabase 
    --- Explanation ---
    scorer: This parameter allows you to specify a custom scoring function to determine how similar two strings are.
    fuzz.token_set_ratio: This is a specific scoring function provided by the fuzzywuzzy (or rapidfuzz) library.
    It calculates the similarity between two strings by considering the set of tokens (words) in each string.
    It is particularly useful when the order of words doesn't matter, as it ignores duplicate words and focuses on the unique set of words in each string.
    limit=5:
    This parameter specifies the maximum number of top matches to return. In this case, it will return up to 5 of the most similar city names from the correct_city_names list.
    """
    correct_city_names = get_all_french_cities()
    for city in city_name:
        matches = process.extract(city, correct_city_names, scorer=fuzz.token_set_ratio, limit=5)
        best_match = [match for match in matches if match[1] >= 75]  # 80% threshold
        if best_match:
            return [best_match[0][0]]
    raise ValueError("La ville entrée a une erreur de frappe")
            


def process_user_input_for_bar_info(input_user: str)->dict:
    """
    get information related to the bar association
    input_user: user question
    """
    city_name = get_city_name(input_user)
    bar_name = retrieve_bar_info_by_city(city_name)
    if bar_name==[]:
        city_name_corrected=rectify_city_name(city_name)
        bar_name = retrieve_bar_info_by_city(city_name_corrected)
    return bar_name[0]
    
