# import Python and Streamlit modules

from dotenv import load_dotenv
load_dotenv()

import os
PROJECT_DIR=os.environ.get("PROJECT_DIR")
DB_DIR=os.environ.get("DB_DIR")

from datetime import datetime
import streamlit as st

import sys
sys.path.append(PROJECT_DIR)
from support import sqlite_database, dt2str, str2dt

def add(topic: str):
    """
    The function will create an SQLite table called to_do and then add the topic into the database.
    """

    # create an SQLite table called to_do with id, topic, created_at, and recall_days columns

    db.exec_query(
        query = 
            """
            CREATE TABLE IF NOT EXISTS to_do (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                created_at TEXT,
                day_1 INTEGER DEFAULT 0,
                day_3 INTEGER DEFAULT 0,
                day_7 INTEGER DEFAULT 0,
                day_14 INTEGER DEFAULT 0,
                day_30 INTEGER DEFAULT 0,
                day_90 INTEGER DEFAULT 0,
                day_180 INTEGER DEFAULT 0,
                day_365 INTEGER DEFAULT 0
            )
            """
    )

    # add the topic to the database

    db.exec_query(
        query = 
            """
            INSERT INTO to_do (topic, created_at) VALUES (:topic, :created_at)
            ON CONFLICT(topic) DO NOTHING
            """,

        parameters = {
            "topic": topic,
            "created_at" : dt2str(datetime.now())  
        }
    )

def get(topic: str):
    """
    The function will retrieve the list of database records related to the topic.
    """

    # get the records related to the topic

    records = db.exec_query(
        query = 
            """
            SELECT * FROM to_do WHERE topic=:topic LIMIT 1
            """,

        parameters = {
            "topic": topic
        }
    )

    return records

def main():
    """
    The function will get the topic and add it to the database.
    Finally, the script will retrieve the DB record for the inserted topic and display it. 
    """

    # configure the streamlit page

    st.set_page_config(
        page_title = "Recall — Spaced Repetition Study Tracker",
        page_icon = ":dolphin:",
        layout = "wide"
    )

    inner_container = st.container(border=True)
    topic = inner_container.text_input(label="**Recall Topic:**")

    if inner_container.button("Submit"):
        # add the topic to the database

        add(topic)

        # get the db records related to the topic

        record = get(topic)[0]
        st.info(
            f"""
            **ID:** {record.get("id")}

            **Recall Topic**: {record.get("topic")}
            
            **Created At**: {record.get("created_at")}
            """
        )

if __name__ == "__main__":
    db = sqlite_database(DB_DIR)
    main()
    _ = db.close
