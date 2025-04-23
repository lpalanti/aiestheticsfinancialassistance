import streamlit as st
import datetime
import requests

# Dados do Telegram
CHAT_ID = "1963421158"
BOT_TOKEN = "7971840892:AAH8sIg3iQUI7jQkMSd3YrYPaU4giRDVRQc"

# Despesas e datas de vencimento
despesas = {
    "Enel": 26,
    "Nubank": 30,
    "Cartão Carrefour": 30,
    "Vivo Fibra": 30,
    "Celular (Vivo)": 30,
    "Celular (Claro)": 30,
    "Pensão": 6,
    "Empréstimo": 30,
    "Aluguel": 30,
    "MEI 1": 30,
    "MEI 2": 30,
}

# Função para enviar mensagem no Telegram
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensagem}
    try:
        requests.post(url, data=data)
    except:
        st.warning("Erro ao enviar mensagem no Telegram.")

# Função para verificar alertas
def verificar_alertas():
    hoje = datetime.datetime.now().day
    mensagens = []
    for nome, vencimento in despesas.items():
        alerta_dia = (vencimento - 3) % 31 or 30
        if hoje == alerta_dia:
            mensagens.append(f"⚠️ Lembrete: '{nome}' vence em 3 dias ({vencimento}/mês)!")
    return mensagens

# Streamlit App
st.set_page_config(page_title="Aiesthetics - Financial Assistance", layout="centered")
st.title("💸 Aiesthetics - Financial Assistance")
st.subheader("📂 Despesas Mensais")

st.markdown("---")

# Inicializar session_state para as despesas, se não existir
for nome in despesas.keys():
    if nome not in st.session_state:
        st.session_state[nome] = False  # Inicializando o estado como False (não pago)

# Controle de despesas pagas
for nome in despesas.keys():
    pago = st.checkbox(f"{nome}", key=nome, value=st.session_state[nome])
    st.session_state[nome] = pago

st.markdown("---")

# Botão para verificar alertas
if st.button("🔔 Verificar alertas e enviar"):
    mensagens = verificar_alertas()
    if mensagens:
        for msg in mensagens:
            enviar_telegram(msg)
        st.success("Alertas enviados no Telegram!")
    else:
        st.info("Nenhum alerta necessário hoje.")

# Rodapé
st.markdown("---")
st.caption("© 2025 Aiesthetics App")
