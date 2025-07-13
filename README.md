# Agente Conversacional con Function Calling y Retrieval-Augmented Generation (RAG) usando Azure OpenAI

Este proyecto implementa un agente conversacional avanzado que combina:

- **Function Calling**: permite que el modelo haga llamadas a funciones externas.  
- **Retrieval-Augmented Generation (RAG)**: integra recuperación de información desde un contexto local y fuentes externas para generar respuestas precisas y actualizadas.

El agente utiliza el servicio de Azure OpenAI junto con LangChain y la API de Wikipedia para enriquecer las respuestas cuando la información local pueda estar desactualizada.

---

## Características principales

- Uso de embeddings para indexar un documento de contexto (normativa LOPD) local.  
- Recuperación de información relevante del contexto para responder preguntas.  
- Llamadas a Wikipedia para obtener información externa actualizada cuando la pregunta lo requiere.  
- Flujo conversacional con memoria para mantener el contexto del diálogo.  
- Interfaz web sencilla desarrollada con **Streamlit** para interactuar con el agente.  

---

## Estructura del proyecto

```
├── data/
│   └── contexto.txt        # Documento de contexto local (normativa LOPD)
├── main.py                 # Código principal del agente conversacional
├── app.py                  # Interfaz gráfica con Streamlit
├── requirements.txt        # Dependencias Python necesarias
├── .env.example            # Ejemplo de variables de entorno para Azure
├── .gitignore              # Ignorar archivos innecesarios en Git
└── README.md               # Documentación del proyecto
```

---

## Requisitos previos

- Cuenta activa en Azure con acceso al servicio Azure OpenAI.
- Claves y configuraciones de despliegue (deployment name, endpoint, API key, versión API).
- Python 3.9+ instalado.
- Conexión a Internet.

---

## Configuración

1. Copia el archivo `.env.example` y renómbralo a `.env`.

2. Rellena las variables con los datos de tu cuenta Azure:

```env
AZURE_DEPLOYMENT_NAME=tu_nombre_de_deployment
AZURE_OPENAI_API_KEY=tu_api_key
AZURE_OPENAI_ENDPOINT=https://tu_endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-05-15
```

3. Asegúrate de que el archivo `data/contexto.txt` contiene el texto de referencia para el RAG.

---

## Instalación de dependencias

Ejecuta en la terminal:

pip install -r requirements.txt


---

## Uso

Para ejecutar el agente conversacional, ejecuta:

python3 main.py

Luego, podrás hacer preguntas en la consola. Para salir, escribe `salir` o `exit`.

El agente responderá utilizando:

- Información del contexto local para preguntas relacionadas con la normativa LOPD.
- Wikipedia para preguntas con términos que sugieran información reciente o no cubierta en el contexto.

Para ejecutar con interfaz web Streamlit, ejecuta:

streamlit run app.py

Accede luego a http://localhost:8501 en tu navegador para interactuar con la aplicación gráfica.

---

## Flujo del agente

1. El usuario hace una pregunta.
2. El agente intenta responder usando el índice de contexto local (RAG).
3. Si la pregunta parece requerir información actualizada (palabras clave como "último", años recientes), el agente busca en Wikipedia.
4. Devuelve la respuesta combinada y mantiene la memoria conversacional.

---

## Notas

- El proyecto usa `langchain`, `langchain_community` y `langchain_openai` para integrarse con Azure OpenAI.
- Wikipedia se consulta mediante `wikipediaapi` con un user-agent personalizado.
- La memoria conversacional se mantiene para dar continuidad a la conversación.
- La interfaz web con Streamlit permite una experiencia de usuario más amigable y persistente.

---

## Enlace al repositorio

[https://github.com/JessicaGV28/agente-rag-azure]

---

