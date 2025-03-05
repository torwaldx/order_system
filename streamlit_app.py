import streamlit as st
import json
import os

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain

from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

import db
import few_shot

# Show title and description.
st.title("💬 Чат бот для размещения заказов в пиццерии")


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management


os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
llm = ChatOpenAI(
    openai_api_base='https://api.proxyapi.ru/openai/v1',
    model_name="gpt-4o-mini",
    temperature=0.0,
)


def debug_prompt(inputs):
    print("=== Полный промпт ===")
    print(inputs.text)
    print("=====================")
    return inputs  # Пропускаем дальше без изменений

def get_order_process_chain():
    # Шаблон для подсказок
    example_prompt = PromptTemplate.from_template(
        "Запрос пользователя: {Question}\nРаспознанные товары: {Products_name}"
    )

    # Шаблон для few-shot подсказок
    few_shot_prompt_template = FewShotPromptTemplate(
        examples=[],
        example_prompt=example_prompt,
        prefix="Ниже приведены подсказки для неоднозначных запросов:",
        suffix="",
        input_variables=["user_request"]
    )

    # Основной шаблон для формирования запроса
    get_products_template = """Ты - умный ИИ помощник - помогаешь сформировать корзину в интернет-магазине.
    Если не удается определить подходящие товары - используй подсказки или предложи одну маленькую пиццу и напиток.
    Исходя из перечня доступных товаров и запроса пользователя , сформируй список товаров с указанием их количества.
    Если пользователь указал конкретное количество, используй его.
    Если количество не указано явно, оцени его на основании контекста.
    Если контекста недостаточно, укажи "1" по умолчанию.
    Ты можешь выбирать товары только из перечня доступных товаров с ценами, никаких посторонних продуктов.

    Формат ответа: JSON-объект с ключом "items", содержащим список словарей с полями "name" (название товара) и "quantity" (количество).
    Ответ должен быть строго JSON-объектом без пояснений и дополнительного текста.
    Пример ответа:
    Запрос пользователя: "Две больших пеперрони и 3 напитка"
    Ответ:
    {{
        "items": [
            {{"name": "Пепперони Large", "quantity": 2}},
            {{"name": "Добрый Кола Small", "quantity": 3}}
        ]
    }}

    {few_shot}

    Вот перечень доступных товаров (товар | тип | цена):
    {products}

    Текущий запрос пользователя: {user_request}
    """

    base_prompt = PromptTemplate.from_template(get_products_template)

    
    chain = (
        RunnablePassthrough.assign(
            products=lambda _: db.get_products_str(),
            few_shot=lambda inputs: few_shot_prompt_template.copy(
                update={"examples": few_shot.get_fewshot(inputs["user_request"])}
            ).format(user_request=inputs["user_request"])
        )
        | base_prompt
        # | RunnableLambda(debug_prompt)  # Выводит полный промпт перед отправкой в LLM
        | llm
    )
    return chain



# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
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
