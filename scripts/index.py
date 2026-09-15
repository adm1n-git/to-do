# import python3 modules

import streamlit as st



def main():
    # configure streamlit page

    st.set_page_config(
        page_title = "Study & Writing Tools",
        page_icon = ":dolphin:",
        layout = "wide"
    )

    with st.container(border=True):
        
        st.markdown(
            """
            # Study & Writing Tools

            A collection of applications to help you learn effectively and write with confidence.

            ---

            ## Recall — Spaced Repetition Study Tracker

            Recall is a study companion designed to support long-term retention of learned material, extending beyond exam preparation.

            Rather than relying on last-minute intensive study, which often results in rapid forgetting, Recall prompts users to revisit topics at optimal intervals, informed by the natural patterns of memory decay over time. Users may input the material they are studying, and Recall subsequently manages a review schedule — ranging from the following day to as long as a year later — to support durable, long-term retention of the content.

            ---

            ## Fix Grammar and Rephrase Sentence

            Write with confidence. Fix Grammar and Rephrase Sentence helps you clean up your writing in one simple place. Paste any text to get it corrected for spelling, grammar, and punctuation errors, so your writing reads clean and professional — then get alternate versions with different tone and phrasing, useful for rewording awkward sentences, avoiding repetition, or finding the right voice for your message.

            """
        )

if __name__ == "__main__":
    main()
