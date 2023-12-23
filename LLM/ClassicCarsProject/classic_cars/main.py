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
from llama_index.llms import OpenAI
import pandas as pd
import numpy as np
from decimal import *
import matplotlib.pyplot as plt

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
    llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
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

data = None

def show_graph():
    column_names, column_values = zip(*data)
    fig, ax = plt.subplots()
    ax.bar(column_names, column_values)
    st.pyplot(fig)  
    
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
        chart_type = st.selectbox("Select a Visualization Type: ",['None', 'Bar', 'Pie'])
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
                
                with st.spinner('CHAT-BOT is at Work ...'):
                    assistant_response = chain.query(user_input)                    
                    st.write('1. Natural Language Question send to LLM')
                    st.write('2. LLM Generated SQL Query')
                    st.write(assistant_response.metadata['sql_query'])
                    st.write('3. SQL Query send to database server')
                    st.write('4. SQL query result')
                    st.table(assistant_response.metadata['result'])
                    st.write('5. LLM converting SQL Query Result in to Natural Language')
                    st.write('6. Natural Language response from LLM')
                    st.markdown(assistant_response)
                    data = assistant_response.metadata['result']
                    column_names, column_values = zip(*data)
                    if(chart_type == 'Bar'):
                        fig, ax = plt.subplots()
                        ax.bar(column_names, column_values)
                        st.pyplot(fig)  
                    
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
          
