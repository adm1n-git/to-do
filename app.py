# import Python and Streamlit modules

import streamlit as st

def login():
    """
    The function will display the login page for the application.
    """
 
    st.set_page_config(
        page_title = "Login",
        page_icon = ":dolphin:",
        layout = "centered",
        initial_sidebar_state = "collapsed"
    )
 
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&display=swap');
 
        /* hide all Streamlit chrome: header, toolbar, menu, deploy button, footer, sidebar */
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        div[data-testid="stSidebar"],
        div[data-testid="collapsedControl"],
        div[data-testid="stSidebarCollapsedControl"],
        .stAppDeployButton,
        #MainMenu,
        footer {
            display: none !important;
        }
 
        /* the CSS-only element should not take up space in the layout */
        div[data-testid="stElementContainer"]:has(> div[data-testid="stMarkdown"] style),
        div.stElementContainer:has(style) {
            display: none !important;
        }
 
        .stApp {
            background: #E9F0F3;
        }
 
        /* centre the card vertically and horizontally in the window */
        div[data-testid="stMainBlockContainer"] {
            max-width: 30rem;
            min-height: 100vh;
            padding: 1.5rem !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
 
        div[data-testid="stMainBlockContainer"] > div[data-testid="stVerticalBlock"] {
            flex: 0 0 auto;
            justify-content: center;
        }
 
        /* the card: every login element lives inside it */
        .st-key-login-card {
            width: 100%;
            box-sizing: border-box;
            background: #FFFFFF;
            border: 1px solid #D2DEE4;
            border-radius: 16px;
            padding: 2.5rem 2rem;
            box-shadow: 0 10px 30px rgba(18, 48, 63, 0.08);
            align-items: center;
            text-align: center;
        }
 
        .st-key-login-card,
        .st-key-login-card * {
            font-family: 'Manrope', 'Source Sans', 'Segoe UI', sans-serif;
        }
 
        /* centre the text blocks inside the card */
        .st-key-login-card div[data-testid="stMarkdownContainer"],
        .st-key-login-card div[data-testid="stMarkdown"] {
            width: 100%;
            text-align: center;
        }
 
        .st-key-login-card .login-icon {
            font-size: 3rem;
            line-height: 1;
            margin-bottom: 1rem;
            text-align: center;
        }
 
        .st-key-login-card .login-title {
            margin: 0 0 0.5rem;
            padding: 0;
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1.25;
            letter-spacing: -0.01em;
            color: #12303F;
            text-align: center;
        }
 
        .st-key-login-card p.login-message {
            margin: 0 auto 0.5rem;
            max-width: 22rem;
            font-size: 1rem;
            line-height: 1.6;
            color: #4F6672;
            text-align: center;
        }
 
        /* the login button, centred inside the card */
        .st-key-login-card div[data-testid="stButton"],
        .st-key-login-card div.stButton {
            display: flex;
            justify-content: center;
            width: 100%;
        }
 
        .st-key-login-card button {
            background: #1F6F8B;
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.75rem;
        }
 
        .st-key-login-card button p {
            color: #FFFFFF;
            font-size: 1rem;
            font-weight: 700;
        }
 
        .st-key-login-card button:hover {
            background: #17566D;
            color: #FFFFFF;
        }
 
        .st-key-login-card button:focus-visible {
            outline: 3px solid #8CC4D8;
            outline-offset: 2px;
        }
        </style>
        """,
        unsafe_allow_html = True
    )
 
    with st.container(key = "login-card"):
 
        st.markdown(
            """
            <div class="login-icon">&#x1F42C;</div>
            <div class="login-title" role="heading" aria-level="1">Study &amp; Writing Tools</div>
            <p class="login-message">Log in with your Microsoft account to continue.</p>
            """,
            unsafe_allow_html = True
        )
 
        st.button("Log in with Microsoft", on_click = st.login)

def main():
    """
    The function will handle the page navigation in the application.
    """

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
