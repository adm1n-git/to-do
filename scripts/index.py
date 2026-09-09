# import python3 modules

import streamlit as st

# configure streamlit page

st.set_page_config(
    page_title = "Recall — Spaced Repetition Study Tracker",
    page_icon = ":dolphin:",
    layout = "wide" 
)

def main():
    with st.container(border=True):
        
        st.markdown(
            """
            # Recall — Spaced Repetition Study Tracker

            Recall is a study companion designed to support long-term retention of learned material, extending beyond exam preparation.

            Rather than relying on last-minute intensive study, which often results in rapid forgetting, Recall prompts users to revisit topics at optimal intervals, informed by the natural patterns of memory decay over time. Users may input the material they are studying, and Recall subsequently manages a review schedule — ranging from the following day to as long as a year later — to support durable, long-term retention of the content.
            """
        )

if __name__ == "__main__":
    main()
