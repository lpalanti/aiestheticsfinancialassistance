import streamlit as st

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

st.caption("© 2025 Aiesthetics App")
