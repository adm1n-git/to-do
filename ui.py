# import python3 modules

import streamlit as st

# configure streamlit pages

st.set_page_config(
    page_title = "Recall — Spaced Repetition Study Tracker",
    page_icon = ":dolphin:",
    layout = "wide" 
)

def main():
    # construct navigation pages

    st.navigation(
        {
            "Home": [
                st.Page(page="scripts/index.py", title="Home")
            ],
            "Recall Pages": [
                st.Page(page="scripts/update.py", title="Update"),
                st.Page(page="scripts/tasks.py", title="Tasks")
            ]
        },
        position = "top"
    ).run()

if __name__ == "__main__":
    main()
