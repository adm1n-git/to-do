# import python3 modules

import streamlit as st

def login():
    st.set_page_config(
        page_title="Login", 
        page_icon="🔒", 
        layout = "wide"
    )

    st.title("🔒 Login")
    st.write("Please log in with your Microsoft account to continue.")
    st.button("Log in with Microsoft", on_click=st.login)

def main():
    st.set_page_config(
        page_title = "Study & Writing Tools", 
        page_icon = ":dolphin:", 
        layout = "wide"
    )

    st.navigation(
        {
            "Home": [
                st.Page(page="scripts/index.py", title="Home")
            ],
            "Recall Pages": [
                st.Page(page="scripts/recall/update.py", title="Update"),
                st.Page(page="scripts/recall/tasks.py", title="Tasks")
            ],         
            "Other Pages": [
                st.Page(page="scripts/others/fix-text.py", title="Fix Text")
            ]
        },
        position = "top"
    ).run()

if __name__ == "__main__":
    if not st.user.is_logged_in:
        login()
        
    else:
        main()
