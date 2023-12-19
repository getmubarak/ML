"""Python file to serve as the frontend"""
import sys
import os

sys.path.append(os.path.abspath('.'))

import streamlit as st
import time
import tiktoken
import openai

from classic_cars.components.sidebar import sidebar
from sqlalchemy import create_engine, text

from llama_index import VectorStoreIndex, SQLDatabase
from llama_index.objects import ObjectIndex, SQLTableNodeMapping, SQLTableSchema
from llama_index.callbacks import CallbackManager, TokenCountingHandler
from llama_index.indices.struct_store import SQLTableRetrieverQueryEngine
from llama_index import ServiceContext

def load_chain():
    db_user = "root"
    db_password = "abc"
    db_host = "mysql"
    db_name = "classicmodels" #sampleDB
    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    engine = create_engine(connection_string)
    table_details = {
        "customers": "stores customer’s data.",
        "products": "stores a list of scale model cars.",
        "productlines": "stores a list of product line categories.",
        "orders": "stores sales orders placed by customers.",
        "orderdetails": "stores sales order line items for each sales order.",
        "payments": "stores payments made by customers based on their accounts.",
        "employees": "stores all employee information as well as the organization structure such as who reports to whom.",
        "offices": "stores sales office data."
    }
    sql_database = SQLDatabase(engine)
    tables = list(sql_database._all_tables)
    table_node_mapping = SQLTableNodeMapping(sql_database)
    table_schema_objs = []
    for table in tables:
        table_schema_objs.append((SQLTableSchema(table_name = table, context_str = table_details[table])))

    token_counter = TokenCountingHandler(
        tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
    )
    callback_manager = CallbackManager([token_counter])
    # chain = ConversationChain(llm=llm)
    openai.api_key = st.session_state.get("OPENAI_API_KEY")
    service_context = ServiceContext.from_defaults(
        llm=llm,callback_manager=callback_manager
    )
    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex,
        service_context=service_context
    )
    query_engine = SQLTableRetrieverQueryEngine(
        sql_database, obj_index.as_retriever(similarity_top_k=3), service_context=service_context
    )
    
    return query_engine

def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


if __name__ == "__main__":

    st.set_page_config(
        page_title="Classic Cars",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded", )
    st.header("Classic Cars Interactive Dashboard")
    sidebar()

    if not st.session_state.get("open_api_key_configured"):
        st.error("Please configure your API Keys!")
    else:
        chain = load_chain()

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("What is your question?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner('CHAT-BOT is at Work ...'):
                    assistant_response = chain.query(user_input)
                message_placeholder.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

