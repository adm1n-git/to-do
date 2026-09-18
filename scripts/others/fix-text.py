# import python3 modules

from dotenv import load_dotenv
import os
load_dotenv()
MODEL = os.environ.get("MODEL")

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import streamlit as st
import re

def render_diff(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<span style="color:green; font-weight:bold;">\1</span>', text)
    text = re.sub(r'~~(.*?)~~', r'<span style="color:red; text-decoration:line-through;">\1</span>', text)
    return text

def interact_with_language_model(text: str):
    rephrase_prompt = ChatPromptTemplate.from_template(
        """
        You are a writing assistant. Fix grammar, spelling, punctuation, and syntax errors in the given text, and rephrase it only where needed to improve clarity, flow, or naturalness.

        Rules:

        1. Correct all grammatical, spelling, and punctuation errors.
        2. Rephrase awkward, unclear, or unnatural sentences, but preserve the original meaning, tone, and intent.
        3. Do not rephrase sentences that are already clear and correct — only change what needs improvement.
        4. Mark added words in **bold** and removed words in ~~strikethrough~~.
        5. Return only the corrected/rephrased text, no explanations.
        6. Respond in Markdown format.

        Text: {text}
        """
    )

    model = init_chat_model(
        model = MODEL,
        temperature = 0.3,
        max_tokens = 1_000,
        timeout = 30,
        max_retries = 2
    )

    rephrase_chain = rephrase_prompt | model | StrOutputParser()
    return rephrase_chain.invoke({"text": text})

def main():
    # configure streamlit page

    st.set_page_config(
        page_title = "Fix Grammar and Rephrase Sentence",
        page_icon = ":dolphin:",
        layout = "wide"
    )

    text_container = st.container(border=True)
    text_container.markdown("**Text:**")
    text = text_container.text_area(label="**Text:**", label_visibility="collapsed")
    if text_container.button("**Fix Text**", type="primary"):
        with text_container.spinner(text="**Analyzing text with AI model..**"):
            response = interact_with_language_model(text)

        response_container = st.container(border=True)
        response_container.markdown("**Corrected Text:**")
        response_container.markdown(
            render_diff(response),
            unsafe_allow_html = True
        )

if __name__ == "__main__":
    main()
