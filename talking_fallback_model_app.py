"""This is a Streamlit app that demonstrates how to use a fallback model in a
LangChain Expression Language (LCEL) chain."""

import streamlit as st
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.llms.fake import FakeStreamingListLLM
from langchain_core.output_parsers import StrOutputParser
from text import get_fallback_message


DEFAULT_MODEL_NAME = "Click 'Start Streaming' to see how LangChain can do fallback from a model that is not working."
TIME_OUT = 0.03
DEFAULT_TOPIC = 'bears'


def initialize_session_state():
    if 'start_streaming' not in st.session_state:
        st.session_state['start_streaming'] = False
    if 'streamed_text' not in st.session_state:
        st.session_state['streamed_text'] = ""


def create_streaming_chain(openai_api_key, model_name, topic):
    """Creates a chain that returns a joke on the provided topic. The LLM has
    a fallback to a fake model that does not reason."""
    
    prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    ai_model = ChatOpenAI(api_key=openai_api_key, 
                          model=model_name)
    fallback_model = FakeStreamingListLLM(responses=[get_fallback_message(topic)])
    output_parser = StrOutputParser()
    return prompt | ai_model.with_fallbacks([fallback_model]) | output_parser


def run_chain_and_stream_to_ui(chain, text_area, topic):
    for s in chain.stream({"topic": topic}):
        st.session_state['streamed_text'] += s
        text_area.markdown(st.session_state['streamed_text'])
        time.sleep(TIME_OUT)


def main():
    st.title("A fallback model that explains LCEL, fallbacks and streaming.")
    topic = st.text_input("Tell me a joke about:", value=DEFAULT_TOPIC)
    model_name = st.text_input("Using OpenAI model:", value=DEFAULT_MODEL_NAME)
    text_area = st.empty()   
    
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", 
                                       value='invalid api key',
                                       key="chatbot_api_key", 
                                       type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    initialize_session_state()

    if st.button("Start Streaming"):
        st.session_state['start_streaming'] = True
        st.session_state['streamed_text'] = ""

    if st.session_state['start_streaming']:
        chain = create_streaming_chain(openai_api_key, model_name, topic)
        run_chain_and_stream_to_ui(chain, text_area, topic)


if __name__ == '__main__':
    main()
