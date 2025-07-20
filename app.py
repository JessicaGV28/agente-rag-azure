# app.py

import streamlit as st
from main import preguntar_al_agente  # <-- importa la función que filtra y llama al agente

st.set_page_config(page_title="Agente RAG + Wikipedia", layout="wide")

st.title("Agente conversacional RAG + Wikipedia")

st.markdown("Escribe tu pregunta abajo. El agente decidirá si usar el contexto local o buscar en Wikipedia.")

# Inicializa el historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = []

# Lista simple de palabras o temas sensibles que no queremos procesar
palabras_prohibidas = ["sexo", "violencia", "terrorismo", "drogas", "insultos", "racismo"]

pregunta = st.text_input("Haz tu pregunta:")

if pregunta:
    # Validación ética simple en frontend
    if any(p in pregunta.lower() for p in palabras_prohibidas):
        st.warning("Lo siento, no puedo procesar preguntas que contengan contenido inapropiado o sensible.")
    else:
        with st.spinner("Pensando..."):
            # Ahora llama a la función filtrada en main.py
            respuesta = preguntar_al_agente(pregunta)

            # Guarda en el historial
            st.session_state.historial.append({"usuario": pregunta, "agente": respuesta})

# Muestra la conversación
if st.session_state.historial:
    st.subheader("Conversación:")
    for turno in reversed(st.session_state.historial):
        st.markdown(f"**Tú:** {turno['usuario']}")
        st.markdown(f"**Agente:** {turno['agente']}")
        st.markdown("---")
