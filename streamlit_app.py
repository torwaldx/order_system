import streamlit as st
import json

import db
from llm_api import get_order_process_chain


st.title("💬 Чат бот для размещения заказов в пиццерии")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Просто напечатайте, что вы хотите"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    chain = get_order_process_chain()
    answer = chain.invoke({"user_request": prompt})

    order = db.get_products_with_prices(json.loads(answer.content))
    order_text = "\n\n".join([f"{item['name']} - {item['quantity']} x {item['price']}" for item in order['items']])

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        st.markdown(order_text)

    st.session_state.messages.append({"role": "assistant", "content": order_text})
