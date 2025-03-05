import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


embeddings_api_model = OpenAIEmbeddings(
    openai_api_base='https://api.proxyapi.ru/openai/v1',
)

fewshot_url = 'https://drive.google.com/uc?id=11SiRepyFjIaMd8NA2eaGo5AWBar7BuYx'
fewshot_file = "KnowledgeBase4FewShot.csv"

# Загрузка датасета для few-shot
if not os.path.exists(fewshot_file):
    #fewshot_file = gdown.download(fewshot_url, quiet=True)
    print(f"Файл загружен: {fewshot_file}")
df = pd.read_csv(fewshot_file)


if os.path.exists('index.faiss'):
    # Загрузка данных векторной базы из бэкапа
    vector_store = FAISS.load_local(
        './',
        embeddings_api_model,
        allow_dangerous_deserialization=True
    )
    print("Загружен бэкап vector_store")
else:
    # Обновление векторной бд из датасета
    vector_store = FAISS.from_texts(
        df['Question'].tolist(), embeddings_api_model,
        ids=df.index.astype(str).tolist()
    )
    vector_store.save_local('./')
    print("vector_store обновлен и сохранен")

def retrieve_examples_ids(user_input, k=3) -> list:
    """Извлекает id k релевантных примеров из датасета."""
    docs = vector_store.similarity_search(user_input, k=k)
    return [doc.id for doc in docs]

def get_fewshot(user_input):
    """Выдает список с примерами, выбранными на основании пользовательского запроса"""
    ids = [int(i) for i in retrieve_examples_ids(user_input)]

    return df.loc[ids].to_dict(orient="records")