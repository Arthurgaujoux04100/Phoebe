import os
import pandas as pd
from sqlalchemy import create_engine
from lib.postgresSQL.connexion import connexion_postresql


def retrieve_bar_info_by_city(city_user:list)->dict:
    """
    get the bar name from the postgresql database
    to_dict(orient='records'): This method converts each row of the DataFrame into a dictionary, where the keys are the column names and the values are the corresponding values of the row.
     The parameter orient='records' specifies that each row should be a separate dictionary.
    Returns a list of dictionaries: The function returns a list where each element is a dictionary representing a row from the city_bar table.
    city_user = city from the user
    return :list
    """
    if len(city_user)>1:
        city = tuple(city_user)
    else:
        city =  "('" + ', '.join(city_user) + "')"
    engine = connexion_postresql()
    query = f"""
        select 
            city_name,
            bar_name
        from city_bar
        where city_name in {city}"""
    return  pd.read_sql(query, engine).to_dict(orient='records')


def get_all_french_cities()->list:
    """get all the french cities from the postgresql database"""
    engine = connexion_postresql()
    return (
        pd.read_sql("""
            select
                city_name 
            from city_bar
            """,
            engine
            )['city_name'].tolist()
    )