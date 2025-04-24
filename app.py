import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Configurações iniciais
st.set_page_config(page_title="Assistente Financeiro Valerio", layout="wide")

st.title("📊 Assistente Financeiro Valerio 3.1")

# Lista de ativos que vamos monitorar
ativos = {
    'IVVB11': 'IVVB11.SA',
    'BOVA11': 'BOVA11.SA',
    'GOLD11': 'GOLD11.SA',
    'DOL11': 'DOL11.SA',
    'SMAL11': 'SMAL11.SA',
    'PETR4': 'PETR4.SA'
}

# Seção de seleção de ativos
st.sidebar.header("Selecione os ativos para análise")
ativos_selecionados = st.sidebar.multiselect("Escolha os ativos:", list(ativos.keys()), default=list(ativos.keys()))

# Baixar dados das cotações
@st.cache_data
def carregar_dados(ativos_selecionados):
    dados = {}
    for ativo in ativos_selecionados:
        ticker = yf.Ticker(ativos[ativo])
        df = ticker.history(period="6mo")  # Últimos 6 meses
        dados[ativo] = df
    return dados

dados_carteira = carregar_dados(ativos_selecionados)

# Mostrar gráficos
for ativo, df in dados_carteira.items():
    st.subheader(f"📈 {ativo} - Últimos 6 meses")
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'], label=f'{ativo}')
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (R$)")
    ax.legend()
    st.pyplot(fig)

# Simulação básica de carteira (valores atuais)
st.sidebar.header("Sua carteira")
carteira = {
    'IVVB11': 1,  # cota
    'GOLD11': 5,  # cotas
    'BOVA11': 0,
    'DOL11': 0,
    'SMAL11': 0,
    'PETR4': 0
}

valores_atuais = {ativo: yf.Ticker(ativos[ativo]).history(period="1d")['Close'].iloc[0] for ativo in ativos_selecionados}
valor_total = sum(carteira[ativo] * valores_atuais.get(ativo, 0) for ativo in ativos_selecionados)

st.sidebar.metric(label="Valor atual da carteira", value=f"R$ {valor_total:,.2f}")

