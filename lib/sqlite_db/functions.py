import sqlite3
import os

def initialize_db():
    """
    initialize a db connection plus creation of chat_history if not exists
    """
    conn = sqlite3.connect('chat_phoebe_history.db')
    cursor = conn.cursor()
    cursor.execute("""
        create table if not exists chat_history (
            id integer primary key autoincrement,
            session integer,
            user_input text,
            gpt_reponse text,
            timestamp datetime default current_timestamp
        )
    """)
    conn.commit()
    conn.close()

def insert_chat(user_input: str, gpt_reponse: str, session: int):
    """
    Insert requests from user anf gpt's response into the table chat_history
    args:
        user_input: user's question :str
        gpt_reponse: gpt's reponse :str
        session: session of analyse (at each start of a session we start by prompt 1) :int
    """
    conn = sqlite3.connect('chat_phoebe_history.db')
    cursor = conn.cursor()
    cursor.execute(
        """insert into chat_history (user_input, gpt_reponse, session) values (?, ?, ?) """,
        (user_input, gpt_reponse, session)
    )
    conn.commit()
    conn.close()

def delete_db():
    """
    db table chat_history deleting
    """
    if os.path.exists('chat_phoebe_history.db'):
        os.remove('chat_phoebe_history.db')

def get_table():
    """
    Display all records from the chat_history table
    """
    conn = sqlite3.connect('chat_phoebe_history.db')
    cursor = conn.cursor()
    cursor.execute("""
        select
            user_input,
            gpt_reponse
        from chat_history
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
        
def display_chat_history():
    """
    Display all records from the chat_history table
    """
    conn = sqlite3.connect('chat_phoebe_history.db')
    cursor = conn.cursor()
    cursor.execute("select * from chat_history")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def get_last_query(session)->tuple:
    """
    get the last question/response
    return:
        last question/response : tuple 

    """
    conn = sqlite3.connect('chat_phoebe_history.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        select
            user_input,
            gpt_reponse
        from chat_history
        where id=(select max(id) from chat_history)
        and session = {session};
    """)
    row = cursor.fetchone()
    conn.close()
    return row