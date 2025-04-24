import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Configurações iniciais
st.set_page_config(page_title="Assistente Financeiro Valerio", layout="wide")

st.title("📊 Assistente Financeiro Valerio 3.1")

# Lista de ativos monitorados
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
    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df.index, df['Close'], label=f'{ativo}')
        ax.set_xlabel("Data")
        ax.set_ylabel("Preço (R$)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning(f"Sem dados disponíveis para {ativo} nos últimos 6 meses.")

# Simulação básica de carteira (valores atuais)
st.sidebar.header("Sua carteira")

# Carteira exemplo (ajuste conforme sua posição real)
carteira = {
    'IVVB11': 1,  # cota
    'GOLD11': 5,  # cotas
    'BOVA11': 0,
    'DOL11': 0,
    'SMAL11': 0,
    'PETR4': 0
}

# Coletar preços atuais com segurança
valores_atuais = {}
for ativo in ativos_selecionados:
    df = yf.Ticker(ativos[ativo]).history(period="1d")
    if not df.empty:
        valores_atuais[ativo] = df['Close'].iloc[0]
    else:
        valores_atuais[ativo] = None  # Sem dados

# Calcular o valor total da carteira
valor_total = 0
for ativo in ativos_selecionados:
    qtd = carteira.get(ativo, 0)
    preco = valores_atuais.get(ativo)
    if preco is not None:
        valor_total += qtd * preco

# Exibir valores
if valor_total > 0:
    st.sidebar.metric(label="Valor atual da carteira", value=f"R$ {valor_total:,.2f}")
else:
    st.sidebar.warning("Sem dados de preço disponíveis para calcular o valor da carteira.")

# Mostrar preços atuais
st.sidebar.subheader("Preços Atuais")
for ativo in ativos_selecionados:
    preco = valores_atuais.get(ativo)
    if preco is not None:
        st.sidebar.write(f"{ativo}: R$ {preco:,.2f}")
    else:
        st.sidebar.write(f"{ativo}: Dados indisponíveis")


