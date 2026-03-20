


# IMPORTAR AAS BIBLIOTECAS
import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate



# CRIAR O TITULO
st.title("My ChatBot IA")


with st.sidebar:

    st.markdown("##  Configurações")
    st.markdown("---")

    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Crie sua chave em console.groq.com/keys"
    )

    st.markdown("---")

    # Criar Contexto

    contexto = st.text_area(
        "Contexto do Assistente",
        value="Você é um assistente acadêmico da Univille especialista em Inteligência Artificial. "
              "Explique conceitos de forma clara, didática e em português.",
        height=150
    )

    # Seleção de modelos
    modelo = st.selectbox(
        "Modelo Groq",
        [
            "llama-3.3-70b-versatile",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "Novo modelo"
        ]
    )

    # Temperatura do modelo
    temperatura = st.slider(
        "Temperatura (criatividade)",
        0.0, 1.0, 0.3
    )

    # Criar memória da conversa do modelo e o usuário
    st.markdown("---")

    if st.button(" Limpar conversa"):
        st.session_state.mensagens = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small>IA</small>",
        unsafe_allow_html=True
    )



# FUNÇÃO DO BOT
def resposta_bot(mensagens):

    chat = ChatGroq(
        model=modelo,
        api_key=groq_key,
        temperature=temperatura
    )

    mensagens_modelo = [("system", contexto)]
    mensagens_modelo += mensagens

    resposta = chat.invoke(mensagens_modelo)

    return resposta.content


# MEMÓRIA DO CHAT

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        ("assistant", "Olá!  Sou o assistente de IA da Univille. Como posso ajudar?")
    ]


# MOSTRAR HISTÓRICO

for role, content in st.session_state.mensagens:

    with st.chat_message(role):
        st.markdown(content)


# INPUT DO USUÁRIO
pergunta = st.chat_input("Digite sua pergunta...")


if pergunta:

    if not groq_key:
        st.warning(" Informe sua Groq API Key no menu lateral.")
        st.stop()

    st.session_state.mensagens.append(("user", pergunta))
    st.chat_message("user").markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):

            resposta = resposta_bot(st.session_state.mensagens)

            st.markdown(resposta)

    st.session_state.mensagens.append(("assistant", resposta))