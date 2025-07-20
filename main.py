# main.py

from dotenv import load_dotenv
import os

load_dotenv() 

from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.agents import AgentExecutor
from langchain_community.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory

# Lee variables Azure de entorno
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

if not all([AZURE_DEPLOYMENT_NAME, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION]):
    raise ValueError("Faltan variables de entorno de Azure. Revisa tu .env")

# Lista simple de palabras o temas sensibles para filtro ético
palabras_prohibidas = ["sexo", "violencia", "terrorismo", "drogas", "insultos", "racismo"]

# Función herramienta para búsqueda externa en Wikipedia
@tool
def buscar_en_wikipedia(query: str) -> str:
    """Busca información en Wikipedia en español sobre un tema dado"""
    wrapper = WikipediaAPIWrapper(lang="es")
    return wrapper.run(query)

# Definir herramientas disponibles para el agente
tools = [buscar_en_wikipedia]

# Crear el modelo de lenguaje Azure Chat
llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0
)

# Crear memoria de conversación
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Inicializar el agente con herramientas
qa_chain: AgentExecutor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    memory=memory
)

# Función que actúa de wrapper para filtrar preguntas antes de enviarlas al agente
def preguntar_al_agente(pregunta: str) -> str:
    if any(p in pregunta.lower() for p in palabras_prohibidas):
        return "Lo siento, no puedo procesar preguntas que contengan contenido inapropiado o sensible."
    else:
        resultado = qa_chain.invoke({"input": pregunta})
        return resultado["output"]
