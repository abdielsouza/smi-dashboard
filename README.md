# 🏭 SMI - Sistema de Monitoramento Industrial

Este projeto simula um cenário industrial real de monitoramento de máquinas, com foco em **análise de dados**, **estatística aplicada** e **previsão de falhas**.
A aplicação foi desenvolvida em **Python** com **Streamlit**, permitindo a exploração interativa dos dados e a extração de insights operacionais.

A ideia central é representar como dados de sensores industriais podem ser usados para **acompanhar desempenho**, **identificar comportamentos anômalos** e **antecipar falhas**, algo comum em contextos de manutenção preditiva.

---

## 🎯 Objetivo do projeto

* Simular dados industriais de máquinas operando ao longo do tempo
* Analisar estatisticamente variáveis de processo
* Visualizar indicadores operacionais (KPIs)
* Aplicar controle estatístico de processo (SPC)
* Construir um modelo simples de Machine Learning para **previsão de falhas**

---

## 🧱 Estrutura do projeto

```
industrial_dashboard/
│
├── data/
│   └── dados_maquinas.csv
│
├── generate_data.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🗂️ Dados simulados

Os dados representam leituras horárias de sensores industriais:

* `temperature` – temperatura da máquina (°C)
* `vibration` – nível de vibração
* `energy_kwh` – consumo energético
* `production_units` – produção por hora
* `failure` – indicação de falha (0 ou 1)
* `status` – Operando ou Falha

As variáveis não são totalmente independentes. Por exemplo:

* Temperatura e vibração influenciam diretamente o consumo de energia
* Níveis elevados desses sensores aumentam a probabilidade de falha

Isso torna o conjunto de dados mais próximo de um ambiente industrial real.

---

## 📊 Análises realizadas

### Estatística descritiva

* Média, desvio padrão e quartis
* Coeficiente de variação (CV), amplamente utilizado na indústria para avaliar estabilidade do processo

### Correlação entre variáveis

* Identificação de relações entre sensores
* Apoio à interpretação do comportamento operacional das máquinas

### Controle Estatístico de Processo (SPC)

* Carta de controle da temperatura
* Limites superior e inferior (UCL e LCL – ±3σ)
* Identificação visual de pontos fora de controle

### Comparação estatística

* Teste t para comparação entre operação normal e estado de falha
* Avaliação de significância estatística das diferenças observadas

---

## 🤖 Machine Learning – Previsão de falhas

Foi implementado um modelo de **Regressão Logística**, escolhido por ser:

* Simples
* Interpretável
* Adequado para aplicações industriais

### Características do modelo:

* Variáveis de entrada: temperatura, vibração, consumo energético e produção
* Classe desbalanceada tratada com `class_weight="balanced"`
* Avaliação utilizando:

  * Relatório de classificação
  * Matriz de confusão

Os coeficientes do modelo são apresentados para facilitar a **interpretação da influência de cada variável** na previsão de falhas, algo essencial em contextos industriais.

---

## 📈 Dashboard interativo

A aplicação desenvolvida em Streamlit permite:

* Filtrar dados por máquina
* Visualizar KPIs operacionais
* Explorar gráficos temporais
* Avaliar estatísticas e correlações
* Analisar o desempenho do modelo de Machine Learning
* Exportar os dados filtrados em formato CSV

Tudo de forma interativa e em tempo real.

---

## 🚀 Como executar o projeto

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Gerar os dados simulados

```bash
python generate_data.py
```

### 3. Executar a aplicação

```bash
streamlit run app.py
```

---

## 🧠 Possíveis extensões

* Curva ROC e AUC
* Ajuste de threshold por risco operacional
* Detecção automática de anomalias
* Simulação de manutenção preditiva
* Exportação automática de relatórios

---

## 📌 Observação final

Este projeto foi desenvolvido com foco em **portfólio**, buscando simular análises e decisões comuns em ambientes industriais reais, indo além de visualizações básicas e explorando estatística aplicada e modelagem de dados de forma prática.