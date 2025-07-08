# agente_rag_function_calling/main.py

import os
import sys
import datetime

try:
    from dotenv import load_dotenv
    from langchain_community.chat_models import AzureChatOpenAI
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import TextLoader
    from langchain_openai import AzureOpenAIEmbeddings
    from langchain.indexes import VectorstoreIndexCreator
    import wikipediaapi
except ModuleNotFoundError as e:
    print("\n[ERROR] Falta un módulo necesario. Asegúrate de ejecutar:")
    print("    pip install -r requirements.txt\n")
    print("Módulo no encontrado:", e.name)
    sys.exit(1)

# Carga de variables de entorno (Azure credentials)
load_dotenv()

AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

missing_vars = [k for k, v in {
    "AZURE_DEPLOYMENT_NAME": AZURE_DEPLOYMENT_NAME,
    "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
    "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
    "AZURE_OPENAI_API_VERSION": AZURE_OPENAI_API_VERSION
}.items() if not v]

if missing_vars:
    print("\n[ERROR] Faltan variables de entorno:", ", ".join(missing_vars))
    print("Por favor revisa tu archivo .env\n")
    sys.exit(1)

# Configuración del modelo de Azure OpenAI
llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0
)

# Función para búsqueda externa en Wikipedia
wiki = wikipediaapi.Wikipedia(user_agent='AgenteRAGJessGPT/1.0 (https://jessicagarrido_webfake.com)', language='es')

def buscar_en_web(query):
    import wikipedia  
    wikipedia.set_lang("es")
    wikipedia.set_user_agent("AgenteRAGJessGPT/1.0 (https://jessicagarrido_webfake.com)")

    try:
        resultados = wikipedia.search(query)
        if resultados:
            page_title = resultados[0]
            page = wikipedia.page(page_title)
            return f"[Wikipedia] {page.summary[:500]}..."
        else:
            return f"No encontré resultados relevantes en Wikipedia para: '{query}'."
    except Exception as e:
        return f"[Wikipedia] Error al buscar: {str(e)}"


# Cargar contexto local (RAG)
file_path = "data/contexto.txt"
if not os.path.exists(file_path):
    print(f"\n[ERROR] Archivo '{file_path}' no encontrado. Asegúrate de crearlo antes de ejecutar este script.\n")
    sys.exit(1)

loader = TextLoader(file_path)
docs = loader.load()

# Crear índice vectorial FAISS con embeddings de Azure
index = VectorstoreIndexCreator(
    embedding=AzureOpenAIEmbeddings(
        deployment="text-embedding-3-large",
        model="text-embedding-3-large",
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
        chunk_size=1000
    ),
    vectorstore_cls=FAISS
).from_loaders([loader])

# Memoria conversacional
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

# Cadena con RAG
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=index.vectorstore.as_retriever(),
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

print("\nAgente conversacional con RAG + Function Calling (Wikipedia). Escribe 'salir' para terminar.\n")

while True:
    try:
        pregunta = input("Tú: ")
        if pregunta.lower() in ["salir", "exit"]:
            break

        # 1. Intenta responder con RAG
        respuesta_completa = qa_chain.invoke({"question": pregunta})
        respuesta_rag = respuesta_completa["answer"]

        # 2. Detecta si falta información reciente (condicional simple)
        hoy = datetime.datetime.now().year
        if any(palabra in pregunta.lower() for palabra in ["último", "reciente", str(hoy), str(hoy - 1)]):
            print("\n[RAG] Puede que la información esté desactualizada. Usando búsqueda externa en Wikipedia...\n")
            respuesta_web = buscar_en_web(pregunta)
            print("Agente:", respuesta_web)
        else:
            print("Agente:", respuesta_rag)

    except KeyboardInterrupt:
        print("\nInterrupción por teclado. Saliendo...")
        break
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}\n")
