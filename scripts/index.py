# import python3 modules

import streamlit as st


def main():
    """
    The function will display the home page of the application.
    """

    # configure streamlit page

    st.set_page_config(
        page_title = "Study & Writing Tools",
        page_icon = ":dolphin:",
        layout = "wide"
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&display=swap');

        /* the CSS-only element should not take up space in the layout */
        div[data-testid="stElementContainer"]:has(> div[data-testid="stMarkdown"] style),
        div.stElementContainer:has(style) {
            display: none !important;
        }

        .stApp {
            background: #E9F0F3;
        }

        div[data-testid="stMainBlockContainer"] {
            max-width: 56rem;
            padding-top: 6rem !important;
            padding-bottom: 3rem !important;
        }

        /* make both tool cards the same height */
        div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
            height: 100%;
        }

        div[data-testid="stColumn"] div[data-testid="stLayoutWrapper"] {
            flex: 1 1 auto;
        }

        .home-hero,
        .home-hero * {
            font-family: 'Manrope', 'Source Sans', 'Segoe UI', sans-serif;
            text-align: center;
        }

        .home-hero .home-icon {
            font-size: 3rem;
            line-height: 1;
            margin-bottom: 0.75rem;
        }

        .home-hero .home-title {
            margin: 0 0 0.5rem;
            font-size: 2.25rem;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -0.01em;
            color: #12303F;
        }

        .home-hero .home-intro {
            margin: 0 auto 1.5rem;
            max-width: 34rem;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #4F6672;
        }

        /* one card per tool */
        .st-key-tool-recall,
        .st-key-tool-fix-text {
            box-sizing: border-box;
            height: 100%;
            background: #FFFFFF;
            border: 1px solid #D2DEE4;
            border-radius: 16px;
            padding: 1.75rem;
            box-shadow: 0 10px 30px rgba(18, 48, 63, 0.08);
        }

        .st-key-tool-recall *,
        .st-key-tool-fix-text * {
            font-family: 'Manrope', 'Source Sans', 'Segoe UI', sans-serif;
        }

        .tool-name {
            margin: 0 0 0.25rem;
            font-size: 1.4rem;
            font-weight: 800;
            color: #12303F;
        }

        .tool-tagline {
            margin: 0 0 0.75rem;
            font-size: 0.95rem;
            font-weight: 700;
            color: #1F6F8B;
        }

        .tool-text {
            margin: 0 0 1rem;
            font-size: 1rem;
            line-height: 1.65;
            color: #4F6672;
        }

        .st-key-tool-recall a[data-testid="stPageLink-NavLink"],
        .st-key-tool-fix-text a[data-testid="stPageLink-NavLink"] {
            background: #1F6F8B;
            border-radius: 10px;
            justify-content: center;
            width: 100%;
            padding: 0.6rem 1rem;
        }

        .st-key-tool-recall a[data-testid="stPageLink-NavLink"]:hover,
        .st-key-tool-fix-text a[data-testid="stPageLink-NavLink"]:hover {
            background: #17566D;
        }

        .st-key-tool-recall a[data-testid="stPageLink-NavLink"] *,
        .st-key-tool-fix-text a[data-testid="stPageLink-NavLink"] * {
            color: #FFFFFF;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html = True
    )

    st.markdown(
        """
        <div class="home-hero">
            <div class="home-icon">&#x1F42C;</div>
            <div class="home-title" role="heading" aria-level="1">Study &amp; Writing Tools</div>
            <p class="home-intro">
                Remember what you learn, and write it clearly.
                Pick a tool to get started.
            </p>
        </div>
        """,
        unsafe_allow_html = True
    )

    recall_column, fix_text_column = st.columns(2, gap = "large")

    with recall_column:

        with st.container(key = "tool-recall"):

            st.markdown(
                """
                <div class="tool-name">Recall</div>
                <div class="tool-tagline">Spaced-repetition study tracker</div>
                <p class="tool-text">
                    Add the topics you're learning and Recall schedules reviews
                    at 1, 3, 7, 14, 30, 90, 180, and 365 days. Each review lands
                    just as the memory starts to fade, so what you learn stays
                    with you long after exam week.
                </p>
                """,
                unsafe_allow_html = True
            )

            st.page_link("scripts/recall/update.py", label = "Add a topic")
            st.page_link("scripts/recall/tasks.py", label = "Review your tasks")

    with fix_text_column:

        with st.container(key = "tool-fix-text"):

            st.markdown(
                """
                <div class="tool-name">Fix Text</div>
                <div class="tool-tagline">Fix grammar and rephrase</div>
                <p class="tool-text">
                    Paste any text to correct spelling, grammar, and punctuation.
                    You also get an alternate version with a different tone and
                    phrasing, useful for awkward sentences, repeated words, or
                    finding the right voice for your message.
                </p>
                """,
                unsafe_allow_html = True
            )

            st.page_link("scripts/others/fix-text.py", label = "Fix your text")

if __name__ == "__main__":
    main()
