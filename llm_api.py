import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_core.chat_history import  BaseChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory

from db import get_products_str
from few_shot import get_fewshot


if not os.environ.get('OPENAI_API_KEY'):
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

llm = ChatOpenAI(
    openai_api_base='https://api.proxyapi.ru/openai/v1',
    model_name="gpt-4o-mini",
    temperature=0.0,
)

def get_session_history() -> BaseChatMessageHistory:
    return StreamlitChatMessageHistory()

def get_order_process_chain():
    # Шаблон для подсказок
    example_prompt = PromptTemplate.from_template(
        "Запрос пользователя: {Question}\nРаспознанные товары: {Products_name}"
    )

    # Шаблон для блока few-shot
    few_shot_prompt_template = FewShotPromptTemplate(
        examples=[],
        example_prompt=example_prompt,
        prefix="Ниже приведены подсказки для неоднозначных запросов:",
        suffix="",
        input_variables=["user_request"]
    )
   
    system_message = """Ты - умный ИИ помощник - помогаешь сформировать корзину в интернет-магазине.
Если не удается определить подходящие товары - используй подсказки или предложи одну маленькую пиццу и напиток.
Исходя из перечня доступных товаров и запроса пользователя , сформируй список товаров с указанием их количества.
Если пользователь указал конкретное количество, используй его.
Если количество не указано явно, оцени его на основании контекста.
Если контекста недостаточно, укажи "1" по умолчанию.

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
"""

    prompt = ChatPromptTemplate([
            ("system", system_message),
            MessagesPlaceholder(variable_name="history", n_messages=5, optional=True),
            ("human", "{user_request}"),
    ])

    chain = (
        RunnablePassthrough.assign(
            products=lambda _: get_products_str(),
            few_shot=lambda inputs: few_shot_prompt_template.model_copy(
                update={"examples": get_fewshot(inputs["user_request"])}
            ).format(user_request=inputs["user_request"])
        )
        | prompt
        | llm
    )

    parser = JsonOutputParser()

    rwmh = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="user_request",
        history_messages_key="history",
    ) | parser

    return rwmh


