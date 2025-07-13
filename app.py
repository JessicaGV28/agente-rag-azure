# app.py

import streamlit as st
from main import qa_chain, buscar_en_web
import datetime

st.set_page_config(page_title="Agente RAG + Wikipedia", layout="wide")

st.title("Agente conversacional RAG + Wikipedia")

st.markdown("Escribe tu pregunta abajo. El agente usará primero el contexto local, y si es necesario, buscará información externa en Wikipedia.")

# Inicializa el historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = []

pregunta = st.text_input("Haz tu pregunta:")

if pregunta:
    hoy = datetime.datetime.now().year
    usar_wikipedia = any(palabra in pregunta.lower() for palabra in ["último", "reciente", str(hoy), str(hoy - 1)])

    # Ejecuta el agente RAG
    with st.spinner("Pensando..."):
        respuesta_completa = qa_chain.invoke({"question": pregunta})
        respuesta = respuesta_completa["answer"]

        if usar_wikipedia:
            respuesta_extra = buscar_en_web(pregunta)
            respuesta += f"\n\nBúsqueda externa:\n{respuesta_extra}"

        # Guarda en el historial
        st.session_state.historial.append({"usuario": pregunta, "agente": respuesta})

# Muestra la conversación
if st.session_state.historial:
    st.subheader("Conversación:")
    for turno in reversed(st.session_state.historial):
        st.markdown(f"**Tú:** {turno['usuario']}")
        st.markdown(f"**Agente:** {turno['agente']}")
        st.markdown("---")
