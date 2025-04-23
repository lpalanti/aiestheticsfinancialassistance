import streamlit as st
import datetime
import requests

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

# Seu ID do Telegram e token do bot
TELEGRAM_CHAT_ID = '1963421158'  # Substitua com seu ID de usuário
TELEGRAM_BOT_TOKEN = '7971840892:AAH8sIg3iQUI7jQkMSd3YrYPaU4giRDVRQc'  # Substitua com o seu token

# Função para enviar mensagem no Telegram
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            st.success("Alerta enviado no Telegram!")
        else:
            st.error(f"Erro ao enviar alerta no Telegram: {response.status_code}")
    except Exception as e:
        st.warning(f"Erro ao enviar mensagem no Telegram: {e}")

# Função para verificar alertas
def verificar_alertas():
    hoje = datetime.datetime.now().day
    mensagens = []
    for nome, vencimento in despesas.items():
        alerta_dia = (vencimento - 3) % 31 or 30  # 3 dias antes do vencimento
        if hoje == alerta_dia:
            mensagens.append(f"⚠️ Lembrete: '{nome}' vence em 3 dias ({vencimento}/mês)!")
    return mensagens

# Streamlit App
st.set_page_config(page_title="Aiesthetics - Financial Assistance", layout="centered")
st.title("💸 Aiesthetics - Financial Assistance")
st.subheader("📂 Despesas Mensais")

st.markdown("---")

# Controle de despesas pagas
for nome in despesas.keys():
    pago = st.checkbox(f"{nome} - Vence dia {despesas[nome]}", key=nome)
    if pago:
        st.write(f"✔️ {nome} marcado como pago")
    else:
        st.write(f"❌ {nome} ainda não pago")

st.markdown("---")

# Botão para verificar alertas e enviar para Telegram
if st.button("🔔 Verificar alertas e enviar no Telegram"):
    mensagens = verificar_alertas()
    if mensagens:
        for msg in mensagens:
            enviar_telegram(msg)
    else:
        st.info("Nenhum alerta necessário hoje.")

st.markdown("---")

st.caption("© 2025 Aiesthetics App")
