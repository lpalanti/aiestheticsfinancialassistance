import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Configurações iniciais
st.set_page_config(page_title="Assistente Financeiro Valerio", layout="wide")

st.title("\ud83d\udcc8 Assistente Financeiro Valerio 3.1")

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
        df = ticker.history(period="6mo")
        dados[ativo] = df
    return dados

dados_carteira = carregar_dados(ativos_selecionados)

# Mostrar gráficos
for ativo, df in dados_carteira.items():
    st.subheader(f"\ud83d\udcc8 {ativo} - Últimos 6 meses")
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
carteira = {
    'IVVB11': 1,  # cota
    'GOLD11': 5,  # cotas
    'BOVA11': 0,
    'DOL11': 0,
    'SMAL11': 0,
    'PETR4': 0
}

valores_atuais = {}
for ativo in ativos_selecionados:
    df = yf.Ticker(ativos[ativo]).history(period="1d")
    if not df.empty:
        valores_atuais[ativo] = df['Close'].iloc[0]
    else:
        valores_atuais[ativo] = None

valor_total = 0
for ativo in ativos_selecionados:
    qtd = carteira.get(ativo, 0)
    preco = valores_atuais.get(ativo)
    if preco is not None:
        valor_total += qtd * preco

if valor_total > 0:
    st.sidebar.metric(label="Valor atual da carteira", value=f"R$ {valor_total:,.2f}")
else:
    st.sidebar.warning("Sem dados de preço disponíveis para calcular o valor da carteira.")

st.sidebar.subheader("Preços Atuais")
for ativo in ativos_selecionados:
    preco = valores_atuais.get(ativo)
    if preco is not None:
        st.sidebar.write(f"{ativo}: R$ {preco:,.2f}")
    else:
        st.sidebar.write(f"{ativo}: Dados indisponíveis")

# Simulação de cenários
st.header("\ud83d\udcca Simulação de Cenários Econômicos")
cenario = st.selectbox("Escolha um cenário:", ["Crise Fiscal no Brasil", "Recessão Global", "Crescimento Global Acelerado"])

# Variações percentuais dos cenários
variacoes = {
    "Crise Fiscal no Brasil": {"IVVB11": 0.15, "GOLD11": 0.10, "BOVA11": -0.15, "DOL11": 0.12, "SMAL11": -0.20, "PETR4": -0.10},
    "Recessão Global": {"IVVB11": -0.15, "GOLD11": 0.10, "BOVA11": -0.20, "DOL11": 0.08, "SMAL11": -0.25, "PETR4": -0.10},
    "Crescimento Global Acelerado": {"IVVB11": 0.20, "GOLD11": -0.10, "BOVA11": 0.15, "DOL11": -0.05, "SMAL11": 0.25, "PETR4": 0.15}
}

# Calcular carteira simulada
valor_simulado = 0
for ativo in ativos_selecionados:
    qtd = carteira.get(ativo, 0)
    preco = valores_atuais.get(ativo)
    variacao = variacoes[cenario].get(ativo, 0)
    if preco is not None:
        preco_simulado = preco * (1 + variacao)
        valor_simulado += qtd * preco_simulado

if valor_simulado > 0:
    st.success(f"Valor simulado da carteira no cenário '{cenario}': R$ {valor_simulado:,.2f}")
else:
    st.info("Nenhum ativo com valor para simulação.")


