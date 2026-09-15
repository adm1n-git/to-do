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
    grammar_prompt = ChatPromptTemplate.from_template(
        """
        You are a grammar-correction assistant. Fix grammar, spelling, punctuation, and syntax errors in the given text.

        Rules:

        1. Preserve the original meaning, tone, and sentence structure — fix only what's incorrect.
        2. If the text is already correct, return it unchanged.
        3. Mark added words in **bold** and removed words in ~~strikethrough~~.
        4. Return only the corrected text, no explanations.
        5. Respond in Markdown format.

        Text: {text}
        """
    )

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

    parallel_chain = RunnableParallel(
        grammar_chain = grammar_prompt | model | StrOutputParser(),
        rephrase_chain = rephrase_prompt | model | StrOutputParser()
    )
    
    return parallel_chain.invoke(
        {
            "text": text
        }
    )

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

        grammar_container = st.container(border=True)
        grammar_container.markdown("**Corrected Text:**")
        grammar_container.markdown(
            render_diff(
                response.get("grammar_chain")
            ),
            unsafe_allow_html = True
        )

        grammar_container = st.container(border=True)
        grammar_container.markdown("**Rephrased Text:**")
        grammar_container.markdown(
            render_diff(
                response.get("rephrase_chain")
            ),
            unsafe_allow_html = True
        )

if __name__ == "__main__":
    main()
