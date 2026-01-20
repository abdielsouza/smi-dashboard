import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

from generate_data import generate_data

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Dashboard Industrial",
    layout="wide"
)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/dados_maquinas.csv",
        parse_dates=["timestamp"]
    )

df = load_data()

# ===============================
# HEADER
# ===============================
st.title("SMI - Sistema de Monitoramento Industrial")
st.markdown("""
Dashboard para **análise estatística, controle de processo e previsão de falhas**
em ambiente industrial simulado.
""")

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("🔧 Filtros")

machine = st.sidebar.selectbox(
    "Selecione a máquina",
    sorted(df["machine_id"].unique())
)

# ===============================
# REGENERAR DADOS
# ===============================

st.sidebar.subheader("🔄 Dados")

if st.sidebar.button("Regenerar dados"):
    with st.spinner("Gerando novos dados industriais..."):
        generate_data()
        st.cache_data.clear()
        st.rerun()

df_full = df.copy()
df_m = df_full[df_full["machine_id"] == machine]

# ===============================
# JANELA DE ANÁLISE
# ===============================

st.sidebar.subheader("⏱️ Janela de Análise")

start_time = st.sidebar.date_input(
    "Data inicial",
    value=df_m["timestamp"].min(),
    min_value=df_m["timestamp"].min(),
    max_value=df_m["timestamp"].max()
)

end_time = st.sidebar.date_input(
    "Data final",
    value=df_m["timestamp"].max(),
    min_value=df_m["timestamp"].min(),
    max_value=df_m["timestamp"].max()
)

start_time = pd.Timestamp(start_time)
end_time = pd.Timestamp(end_time)

df_m = df_m[df_m["timestamp"].between(start_time, end_time)]

# ===============================
# KPIs PRINCIPAIS
# ===============================
st.subheader("📌 Indicadores Operacionais")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Produção Média (unid/h)",
    f"{df_m['production_units'].mean():.1f}"
)

col2.metric(
    "Temperatura Média (°C)",
    f"{df_m['temperature'].mean():.1f}"
)

col3.metric(
    "Consumo Médio (kWh)",
    f"{df_m['energy_kwh'].mean():.1f}"
)

col4.metric(
    "Falhas Registradas",
    int(df_m["failure"].sum())
)

# ===============================
# ANÁLISE ESTATÍSTICA
# ===============================
st.subheader("📊 Estatísticas Descritivas")

stats_df = (
    df_m[["temperature", "vibration", "energy_kwh", "production_units"]]
    .describe()
    .T
)

st.markdown("""
- **temperature**: A temperatura da máquina.
- **vibration**: O nível de vibração da máquina.
- **energy_kwh**: O consumo de energia da máquina (kW/h).
- **production_units**: Unidade fictícia de produção de uma máquina. Maior número representa maior nível de produção.
""")

stats_df["cv_%"] = (stats_df["std"] / stats_df["mean"]) * 100

st.dataframe(stats_df.round(2), use_container_width=True)

# ===============================
# CORRELAÇÃO
# ===============================
st.subheader("🔗 Correlação entre Sensores")

corr = df_m[
    ["temperature", "vibration", "energy_kwh", "production_units"]
].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Matriz de Correlação"
)

st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("""
- ⚠️ Números mais próximos de -1 indicam uma relação **inversamente proporcional** mais forte.
- ⚠️ Números mais próximos de 1 indicam uma relação **diretamente proporcional** mais forte.
- ⚠️ Números mais próximos de 0 indicam uma **correlação fraca ou inexistente** entre as variáveis.
""")

# ===============================
# EVOLUÇÃO TEMPORAL
# ===============================
st.subheader("📈 Evolução Temporal")

fig_temp = px.line(
    df_m,
    x="timestamp",
    y="temperature",
    title="Temperatura ao Longo do Tempo"
)

fig_prod = px.line(
    df_m,
    x="timestamp",
    y="production_units",
    title="Produção por Hora"
)

st.plotly_chart(fig_temp, use_container_width=True)
st.plotly_chart(fig_prod, use_container_width=True)

# ===============================
# CONTROLE ESTATÍSTICO DE PROCESSO (SPC)
# ===============================
st.subheader("📉 Controle Estatístico de Processo (Temperatura)")

mean_temp = df_m["temperature"].mean()
std_temp = df_m["temperature"].std()

df_m["UCL"] = mean_temp + 3 * std_temp
df_m["LCL"] = mean_temp - 3 * std_temp

fig_spc = px.line(
    df_m,
    x="timestamp",
    y="temperature",
    title="Carta de Controle - Temperatura"
)

fig_spc.add_hline(
    y=mean_temp,
    line_dash="dash",
    annotation_text="Média"
)

fig_spc.add_hline(
    y=df_m["UCL"].iloc[0],
    line_dash="dot",
    annotation_text="UCL"
)

fig_spc.add_hline(
    y=df_m["LCL"].iloc[0],
    line_dash="dot",
    annotation_text="LCL"
)

st.plotly_chart(fig_spc, use_container_width=True)

# ===============================
# COMPARAÇÃO OPERANDO vs FALHA
# ===============================
st.subheader("⚠️ Comparação Estatística: Operação x Falha")

operando = df_m[df_m["failure"] == 0]["temperature"]
falha = df_m[df_m["failure"] == 1]["temperature"]

t_stat, p_value = stats.ttest_ind(
    operando,
    falha,
    equal_var=False
)

st.write(f"**Teste t para Temperatura:** p-value = `{p_value:.5f}`")

if p_value < 0.05:
    st.success("Diferença estatisticamente significativa ✔️")
else:
    st.warning("Diferença NÃO significativa ❌")

# ===============================
# BOXPLOT INDUSTRIAL
# ===============================
st.subheader("📦 Distribuição de Temperatura por Status")

fig_box = px.box(
    df_m,
    x="status",
    y="temperature",
    color="status",
    title="Temperatura por Status da Máquina"
)

st.plotly_chart(fig_box, use_container_width=True)

# ===============================
# MACHINE LEARNING
# ===============================
st.subheader("🤖 Modelo de Machine Learning – Previsão de Falhas")

features = [
    "temperature",
    "vibration",
    "energy_kwh",
    "production_units"
]

X = df_m[features]
y = df_m["failure"]

class_counts = y.value_counts()

# Checagem de segurança
if len(class_counts) < 2 or class_counts.min() < 2:
    st.warning(
        "Não há dados suficientes de falha neste recorte "
        "para treinar o modelo de Machine Learning."
    )
    st.info(
        "Tente ampliar a janela de tempo, selecionar outra máquina "
        "ou regenerar os dados."
    )

else:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        stratify=y,
        random_state=42
    )

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=500
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    st.text("📄 Relatório de Classificação")
    st.text(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)

    fig_cm = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Previsto", y="Real"),
        title="Matriz de Confusão"
    )

    st.plotly_chart(fig_cm, use_container_width=True)

    coef_df = pd.DataFrame({
        "Variável": features,
        "Importância": model.coef_[0]
    }).sort_values(by="Importância", ascending=False)

    fig_imp = px.bar(
        coef_df,
        x="Importância",
        y="Variável",
        orientation="h",
        title="Importância das Variáveis no Modelo"
    )

    st.plotly_chart(fig_imp, use_container_width=True)

# ===============================
# DOWNLOAD
# ===============================
st.sidebar.subheader("⬇️ Exportação")

st.sidebar.download_button(
    label="Baixar dados filtrados",
    data=df_m.to_csv(index=False),
    file_name=f"dados_{machine}.csv",
    mime="text/csv"
)