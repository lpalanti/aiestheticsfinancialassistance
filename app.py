import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

# Configurações iniciais
st.set_page_config(page_title="Assistente Financeiro Valerio", layout="wide")

st.title("Assistente Financeiro Valerio 3.1")

# Lista de ativos monitorados
ativos = {
    'IVVB11': 'IVVB11.SA',
    'BOVA11': 'BOVA11.SA',
    'GOLD11': 'GOLD11.SA',
    'DOL11': 'DOL11.SA',
    'SMAL11': 'SMAL11.SA',
    'PETR4': 'PETR4.SA'
}

# Caminho do arquivo CSV para persistência
csv_file = "carteira.csv"

# Dados iniciais se o CSV não existir
dados_iniciais = pd.DataFrame([
    {'ativo': 'IVVB11', 'quantidade': 1, 'preco': 348.25, 'data': pd.to_datetime('2025-04-24'), 'tipo': 'compra'},
    {'ativo': 'GOLD11', 'quantidade': 5.05, 'preco': 19.78, 'data': pd.to_datetime('2025-04-24'), 'tipo': 'compra'}
])

# Carregar carteira do CSV, se existir
if os.path.exists(csv_file):
    df_carteira = pd.read_csv(csv_file, parse_dates=['data'])
else:
    df_carteira = dados_iniciais.copy()
    df_carteira.to_csv(csv_file, index=False)

# Inicialização da carteira no session_state
if 'carteira' not in st.session_state:
    st.session_state.carteira = df_carteira.copy().to_dict('records')

# Gerenciamento manual da carteira
st.sidebar.header("Gerenciar Carteira")
operacao = st.sidebar.radio("Escolha uma operação:", ["Adicionar", "Excluir"])
ativo_escolhido = st.sidebar.selectbox("Ativo (lista):", list(ativos.keys()))
ativo_manual = st.sidebar.text_input("Ou digite o código do ativo manualmente:")
ativo_final = ativo_manual.upper() if ativo_manual else ativo_escolhido
quantidade = st.sidebar.number_input("Quantidade:", min_value=0.0, step=1.0)
preco = st.sidebar.number_input("Preço por cota (R$):", min_value=0.0, step=0.01)
data_operacao = st.sidebar.date_input("Data da operação:", value=date.today())

if st.sidebar.button("Confirmar Operação"):
    nova_operacao = {
        'ativo': ativo_final,
        'quantidade': quantidade if operacao == "Adicionar" else -quantidade,
        'preco': preco,
        'data': data_operacao,
        'tipo': 'compra' if operacao == "Adicionar" else 'venda'
    }
    st.session_state.carteira.append(nova_operacao)
    # Atualizar CSV
    df_atualizado = pd.DataFrame(st.session_state.carteira)
    df_atualizado.to_csv(csv_file, index=False)
    st.sidebar.success("Operação registrada e salva com sucesso!")

# Exibir histórico da carteira
st.sidebar.subheader("Histórico de Operações")
if st.session_state.carteira:
    df_carteira = pd.DataFrame(st.session_state.carteira)
    st.sidebar.dataframe(df_carteira)
else:
    st.sidebar.write("Nenhuma operação registrada.")

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
    st.subheader(f"{ativo} - Últimos 6 meses")
    if not df.empty:
        fig, ax = plt.subplots(figsize=(3, 1.5))  # Tamanho ainda menor
        ax.plot(df.index, df['Close'], label=f'{ativo}', linewidth=0.8)
        ax.set_xlabel("Data", fontsize=6)
        ax.set_ylabel("Preço (R$)", fontsize=6)
        ax.legend(fontsize=6)
        ax.tick_params(axis='both', labelsize=6)
        st.pyplot(fig)
    else:
        st.warning(f"Sem dados disponíveis para {ativo} nos últimos 6 meses.")

# Calcular valor atual da carteira
valores_atuais = {}
for ativo in ativos_selecionados:
    df = yf.Ticker(ativos[ativo]).history(period="1d")
    if not df.empty:
        valores_atuais[ativo] = df['Close'].iloc[0]
    else:
        valores_atuais[ativo] = None

# Calcular valor total com base na carteira registrada
valor_total = 0
if st.session_state.carteira:
    df_carteira = pd.DataFrame(st.session_state.carteira)
    for ativo in df_carteira['ativo'].unique():
        preco = valores_atuais.get(ativo)
        if preco is not None:
            qtd_total = df_carteira[df_carteira['ativo'] == ativo]['quantidade'].sum()
            valor_total += qtd_total * preco

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
st.header("Simulação de Cenários Econômicos")
cenario = st.selectbox("Escolha um cenário:", ["Crise Fiscal no Brasil", "Recessão Global", "Crescimento Global Acelerado"])

# Variações percentuais dos cenários
variacoes = {
    "Crise Fiscal no Brasil": {"IVVB11": 0.15, "GOLD11": 0.10, "BOVA11": -0.15, "DOL11": 0.12, "SMAL11": -0.20, "PETR4": -0.10},
    "Recessão Global": {"IVVB11": -0.15, "GOLD11": 0.10, "BOVA11": -0.20, "DOL11": 0.08, "SMAL11": -0.25, "PETR4": -0.10},
    "Crescimento Global Acelerado": {"IVVB11": 0.20, "GOLD11": -0.10, "BOVA11": 0.15, "DOL11": -0.05, "SMAL11": 0.25, "PETR4": 0.15}
}

# Calcular carteira simulada
valor_simulado = 0
if st.session_state.carteira:
    df_carteira = pd.DataFrame(st.session_state.carteira)
    for ativo in df_carteira['ativo'].unique():
        preco = valores_atuais.get(ativo)
        variacao = variacoes[cenario].get(ativo, 0)
        if preco is not None:
            preco_simulado = preco * (1 + variacao)
            qtd_total = df_carteira[df_carteira['ativo'] == ativo]['quantidade'].sum()
            valor_simulado += qtd_total * preco_simulado

if valor_simulado > 0:
    st.success(f"Valor simulado da carteira no cenário '{cenario}': R$ {valor_simulado:,.2f}")
else:
    st.info("Nenhum ativo com valor para simulação.")
