# Agente Conversacional RAG con Function Calling usando Azure OpenAI

Este proyecto implementa un agente conversacional avanzado que combina:

- Generación de respuestas usando Azure OpenAI con deployment GPT-4o.
- Recuperación de información local (contexto.txt) mediante un índice vectorial FAISS.
- Búsqueda externa en Wikipedia para consultas que pueden necesitar información actualizada o no presente en el contexto.
- Uso de memoria conversacional para mantener el contexto en la conversación.

---

## Estructura del proyecto

- `main.py`: código principal del agente.
- `contexto.txt`: archivo con información local para RAG.
- `requirements.txt`: dependencias necesarias para ejecutar el proyecto.
- `.env.example`: variables de entorno necesarias (no contiene claves reales).

---

## Requisitos previos

- Python 3.9 o superior.
- Cuenta Azure con OpenAI habilitado.
- Variables de entorno definidas en un archivo `.env` con tus credenciales Azure.

---

## Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone <URL-del-repo>
   cd <nombre-repo>
