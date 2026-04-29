import streamlit as st
from chatbot_logic import obter_resposta

# Configuração da Página
st.set_page_config(page_title="Chatbot Operadora", page_icon="💳")
st.title("🤖 Chatbot - Operadora de Cartão")
st.markdown("Bem-vindo ao atendimento automático!")

# Inicializa o histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Como posso ajudar com seu cartão?"):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lógica de saída (Obrigado / Sair não são necessários no Web, mas vamos tratar)
    if "obrigado" in prompt.lower():
        resposta_final = "Eu que agradeço! Posso ajudar em mais alguma coisa?"
    else:
        # Chama a lógica do modelo da professora
        resposta_final, confianca = obter_resposta(prompt)
        if confianca > 0:
            resposta_final = f"{resposta_final} \n\n *(Confiança: {round(confianca*100, 2)}%)*"

    # Exibe resposta do bot
    with st.chat_message("assistant"):
        st.markdown(resposta_final)
    st.session_state.messages.append({"role": "assistant", "content": resposta_final})