# import Python and Streamlit modules

from dotenv import load_dotenv
load_dotenv()

import os
PROJECT_DIR=os.environ.get("PROJECT_DIR")
DB_DIR=os.environ.get("DB_DIR")

from datetime import datetime, timedelta
import streamlit as st

import sys
sys.path.append(PROJECT_DIR)
from support import sqlite_database, dt2str, str2dt

def get():
    """
    The function will retrieve and return the database records.
    """

    # create an SQLite table called to_do with id, topic, created_at and recall days columns

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

    # get the records from the table to_do

    records = db.exec_query(
        query = 
            """
            SELECT * FROM to_do
            """
    )

    return records

def update(day: str, id: int):
    """
    The function will change the remember flag from 0 to 1 for the given day.
    """

    # update the day flag for the record ID

    db.exec_query(
        query = 
            f"""
            UPDATE to_do SET {day}=1 WHERE id=:id
            """,

        parameters = {
            "id": id
        }
    )

def drop(id: int):
    """
    The function will delete the database record of the given record ID.
    """

    # delete the rows that are not required

    db.exec_query(
        query = 
            f"""
            DELETE FROM to_do WHERE id=:id
            """,

        parameters = {
            "id": id
        }
    )

def reset(id: int):
    """
    The function will reset the remember flag from 1 to 0 for the given record ID.
    """

    # reset the day flags for the given row

    db.exec_query(
        query = 
            """
            UPDATE to_do 
            SET day_1=0, 
                day_3=0,
                day_7=0,
                day_14=0,
                day_30=0,
                day_90=0,
                day_180=0,
                day_365=0,
                created_at=:created_at
            WHERE id=:id
            """,

        parameters= {
            "id": id,
            "created_at": dt2str(datetime.now())
        }
    )

def main():
    """
    The function will initially retrieve all database records.
    A database record will be displayed if the record's created_at + recall cycle < current time.
    The function provides Remembered, Forgot and Reset buttons to update the respective DB fields.
    """

    # configure the streamlit page

    st.set_page_config(
        page_title = "Recall — Spaced Repetition Study Tracker",
        page_icon = ":dolphin:",
        layout = "wide"
    )

    for record in get():
        for day_str, day_int in [
            ("day_1", 1), 
            ("day_3", 3), 
            ("day_7", 7), 
            ("day_14", 14), 
            ("day_30", 30), 
            ("day_90", 90), 
            ("day_180", 180), 
            ("day_365", 365)
            ]:

            id = record.get("id")
            recall_dt = str2dt(record.get("created_at")) + timedelta(days=day_int)
            today_dt = datetime.now()
            flag = record.get(day_str)

            if (recall_dt <= today_dt) and (flag != 1):
                inner_container = st.container(border=True)
                inner_container.info(
                    f"""
                    **Recall Topic**: {record.get("topic")}

                    **Created At**: {record.get("created_at")}

                    **Recall Schedule:** {day_str.title().replace("_", "-")}
                    """
                )

                if inner_container.button("**Remembered**", key=f"remembered_{id}"):
                    update(day=day_str, id=id)
                    st.rerun()

                if inner_container.button("**Forgot**", key=f"forgot_{id}"):
                    reset(id=id)
                    st.rerun()

                if inner_container.button("**Drop**", key=f"drop_{id}"):
                    drop(id=id)
                    st.rerun()

                break

if __name__ == "__main__":
    db = sqlite_database(DB_DIR)
    main()
    _ = db.close
