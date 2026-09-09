# import python3 modules

from dotenv import load_dotenv
load_dotenv()

import os
PROJECT_DIR=os.environ.get("PROJECT_DIR")
DB_DIR=os.environ.get("DB_DIR")

from datetime import datetime, timedelta
import streamlit as st

import sys
sys.path.append(PROJECT_DIR)
from support import sqlite_database

def dt2str(dt):
    return dt.strftime(r"%Y-%m-%d %H:%M:%S")

def str2dt(str):
    return datetime.strptime(str, r"%Y-%m-%d %H:%M:%S")

def get():
    # get the records from the table to_do

    records = db.exec_query(
        query = 
            """
            SELECT * FROM to_do
            """
    )

    return records

def change_recall_day_flag(day: str, id: int):
    # update the day flag for the record id

    db.exec_query(
        query = 
            f"""
            UPDATE to_do SET {day}=1 WHERE id=:id
            """,

        parameters = {
            "id": id
        }
    )

def reset_recall_day_flag(id: int):
    # update the day flags for the given row

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
                day_365=0
            WHERE id=:id
            """,

        parameters= {
            "id": id
        }
    )

def main():
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
            recall_day_flag = record.get(day_str)

            if (recall_dt <= today_dt) and (recall_day_flag != 1):
                inner_container = st.container(border=True)
                inner_container.info(
                    f"""
                    **Recall Topic**: {record.get("topic")}

                    **Created At**: {record.get("created_at")}

                    **Recall Schedule:** {day_str.title().replace("_", "-")}
                    """
                )

                if inner_container.button("**I Remembered**", type="primary", key=f"remembered_{id}"):
                    change_recall_day_flag(day=day_str, id=id)
                    st.rerun()

                if inner_container.button("**I Forgot**", type="secondary", key=f"forgot_{id}"):
                    reset_recall_day_flag(id=id)
                    st.rerun()

                break

if __name__ == "__main__":
    db = sqlite_database(DB_DIR)
    main()
    _ = db.close
