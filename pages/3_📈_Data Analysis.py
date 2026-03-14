import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm, binom
import plotly.express as px
import plotly.graph_objects as go
from openpyxl import load_workbook
from streamlit_extras.dataframe_explorer import dataframe_explorer
from plotnine import ggplot, aes, geom_histogram, geom_line, theme_minimal

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_excel("Produto_bruto.xlsx", engine="openpyxl")
    return df

df = load_data()

st.image("3.jpg", width=650) 

st.title("Análise da Produção Mineral no Brasil")
st.markdown("""
Este dashboard tem como objetivo analisar a produção mineral de ferro no Brasil, explorando padrões de distribuição, 
identificando estados com maior produção e utilizando modelos estatísticos para compreensão dos dados. 
A análise inclui visualizações interativas e cálculos estatísticos que permitem insights sobre o setor mineral.
""")

st.subheader("Apresentação dos Dados e Tipos de Variáveis")
st.markdown("""
O conjunto de dados utilizado foi disponibilizado pela Agência Nacional de Mineração (ANM), e contém informações sobre a produção bruta de minérios no Brasil, 
com detalhes sobre estados produtores, classes minerais e quantidades extraídas.

- **Ano base**: Ano da produção (numérica discreta).
- **UF**: Estado onde ocorreu a extração (categórica nominal).
- **Classe**: Tipo de substância mineral (ex.: Metálicos) (categórica nominal).
- **Substância**: Nome do minério extraído (categórica nominal).
- **Substância Mineral**: Nome detalhado da substância extraída (categórica nominal).
- **Quantidade produção - minério rom (t)**: Volume total extraído em toneladas (numérica contínua).
""")

# Exibir a tabela completa dos dados
st.subheader("Visualização da Tabela de Dados")
st.dataframe(df)

st.subheader("Perguntas-chave da Análise")
st.markdown("""
1. Quais são estados que possuem os maiores índices de extração de minério de ferro?
2. A distribuição dos dados segue um padrão específico?
3. É possível utilizar o threshold para determinar quais estados devem possuir mais investimentos na extração de ferro ?
4. Como as distribuições probabilísticas ajudam a entender a produção?
5. A produção mineral apresenta uma distribuição simétrica ou há um viés para estados altamente produtivos?
6. Se um estado já teve alta produção em um ano, qual a chance de repetir esse desempenho no ano seguinte?
7. Existe uma concentração de valores próximos à média ou há uma dispersão elevada?
8. A produção mineral apresenta caudas longas, indicando eventos extremos de produção?
""")

# Exibir estatísticas descritivas
st.subheader("Estatísticas Descritivas")
media = df["Quantidade Produção - Minério ROM (t)"].mean()
mediana = df["Quantidade Produção - Minério ROM (t)"].median()
moda = df["Quantidade Produção - Minério ROM (t)"].mode()[0]
desvio_padrao = df["Quantidade Produção - Minério ROM (t)"].std()
variancia = df["Quantidade Produção - Minério ROM (t)"].var()

# Criar um DataFrame para exibir as estatísticas em uma tabela
estatisticas_df = pd.DataFrame({
    "Estatística": ["Média", "Mediana", "Moda", "Desvio Padrão", "Variância"],
    "Valor": [f"{media:.2f} toneladas", f"{mediana:.2f} toneladas", f"{moda:.2f} toneladas", f"{desvio_padrao:.2f} toneladas", f"{variancia:.2e} toneladas²"]
})

st.table(estatisticas_df)

st.subheader("1. Quais são estados que possuem os maiores índices de extração de minério de ferro?")
st.markdown("""
A análise da produção total por estado mostrou que alguns estados se destacam na extração minério de ferro.
O estado com a maior produção foi identificado no gráfico abaixo, no qual é possível visualizado no gráfico de barras da produção total por UF.

Os dois maiores produtores de minério de ferro no Brasil são os estados do **Pará** e de **Minas Gerais**.
Porém, como é possível observar no gráfico, o estado de **Minas Gerais** possui a maior produção de ferro nacional.
""")

# Análise por Estado e Classe Mineral
st.subheader("Produção Total por Estado e Classe Mineral")
df_estado = df.groupby("UF")["Quantidade Produção - Minério ROM (t)"].sum().reset_index()
df_classe = df.groupby("Classe Substância")["Quantidade Produção - Minério ROM (t)"].sum().reset_index()

st.plotly_chart(px.bar(df_estado, x="UF", y="Quantidade Produção - Minério ROM (t)", title="Produção Total de Minério por Estado"))
st.plotly_chart(px.bar(df_classe, x="Classe Substância", y="Quantidade Produção - Minério ROM (t)", title="Produção Total de Minério por Classe Mineral"))

st.subheader("2.A distribuição dos dados segue um padrão específico?")
st.markdown("""
A produção mineral no Brasil apresenta grandes variações entre os estados, como é possível ver no gráfico, porém é possível analisar certos padrões de mineração. Como respondido na questão anterior Minas Gerais se destaca como o maior produtor nacional de minério de ferro, seguido pelo estado do Pará. Essa liderança pode ser explicada pela presença do Quadrilátero Ferrífero, região localizada no centro-sul do estado de Minas Gerais uma das mais importantes províncias minerais do mundo, onde a exploração de ferro remonta ao período colonial.

No Pará, a produção é impulsionada pelo Projeto Carajás, uma das maiores jazidas de minério de ferro de alta qualidade do planeta, explorada desde a década de 1980. No entanto, a infraestrutura logística e a distância dos principais mercados consumidores dificultam o escoamento da produção paraense, o que pode influenciar a diferença na produção total.

Além disso, fatores como investimentos em tecnologia de extração, políticas ambientais e demanda global pela commoditie afetam a produção de cada estado ao longo do tempo. Essa variação pode ser observada nos gráficos, que evidenciam a discrepância na produção mineral estadual.
""")

st.subheader("Estados com Produção Acima do Threshold")
thresh = st.slider("Defina um limite mínimo de produção (threshold)", min_value=float(df_estado["Quantidade Produção - Minério ROM (t)"].min()), max_value=float(df_estado["Quantidade Produção - Minério ROM (t)"].max()), value=float(media))
estados_acima_thresh = df_estado[df_estado["Quantidade Produção - Minério ROM (t)"] > thresh]
st.dataframe(estados_acima_thresh)

st.subheader("3.É possível utilizar o threshold para determinar quais estados devem possuir mais investimentos na extração de ferro ?")
st.markdown("""     
Sim, pois se utilizarmos um threshold baseado na média de produção nacional ou em um percentil elevado, como por exemplo o dos 10% dos maiores produtores, podemos identificar quais estados consistentemente ultrapassam esse valor e quais ficam abaixo. Estados como Minas Gerais e Pará, que possuem produção significativamente acima do threshold, já são líderes no setor e podem se beneficiar de investimentos para otimizar processos, melhorar infraestrutura e ampliar a capacidade produtiva.

Além disso, a análise do threshold ao longo do tempo pode mostrar se determinados estados estão crescendo ou estagnados na produção, auxiliando na tomada de decisão sobre onde alocar recursos para maximizar a eficiência e o retorno do investimento.
             
""")



st.subheader("4.Como as distribuições probabilísticas ajudam a entender a produção?")
st.markdown("""
Para compreender melhor os padrões de produção mineral no Brasil, foi utilizado duas distribuições probabilísticas que ajudam a interpretar os dados de maneira mais intuitiva:

- **Distribuição Binomial**: Essa distribuição foi escolhida pois é útil para analisar a probabilidade de um estado ter uma produção acima da média. Como há uma variação significativa entre os estados, essa abordagem permite quantificar a frequência com que altos volumes de produção ocorrem.

- **Distribuição Normal**: Foi escolhida esta distribuição porque a produção de minério, quando analisada em grandes volumes, tende a seguir um comportamento aproximadamente normal. Isso nos ajuda a identificar padrões e a prever valores dentro de uma faixa esperada.
""")

# Distribuição Binomial
st.subheader("Distribuição Binomial")
p_sucesso = len(df[df["Quantidade Produção - Minério ROM (t)"] > media]) / len(df)
n = len(df)
k = np.arange(0, n, 1)
binomial = binom.pmf(k, n, p_sucesso)
fig_binom = go.Figure()
fig_binom.add_trace(go.Scatter(x=k, y=binomial, mode='lines+markers', name='Distribuição Binomial'))
fig_binom.update_layout(title="Distribuição Binomial da Produção de Minério", xaxis_title="Amostras", yaxis_title="Probabilidade")
st.plotly_chart(fig_binom)

st.subheader("5. Se um estado já teve alta produção em um ano, qual a chance de repetir esse desempenho no ano seguinte?")
st.markdown("""
 A chance de um estado manter um alto volume de produção no ano seguinte é bastante elevada, especialmente para estados líderes. Isso ocorre porque a extração mineral depende de fatores estruturais e geológicos que não mudam drasticamente em curtos períodos de tempo.

 Além disso, os contratos de exploração, investimentos e demanda do mercado impactam diretamente as empresas garantindo uma estabilidade na produção. No entanto, oscilações podem ocorrer devido a fatores econômicos, ambientais ou regulatórios, que podem impactar a continuidade da produção em níveis elevados.
                   
""")
st.subheader("6.Se um estado já teve alta produção em um ano, qual a chance de repetir esse desempenho no ano seguinte? ")
st.markdown("""    
A chance de um estado manter um alto volume de produção no ano seguinte é bastante elevada, especialmente para estados líderes. Isso ocorre porque a extração mineral depende de fatores estruturais e geológicos que não mudam drasticamente em curtos períodos de tempo. Além disso, os contratos de exploração, investimentos e demanda do mercado impactam diretamente as empresas, como respondido na questão anterior, garantindo uma estabilidade na produção. No entanto, oscilações podem ocorrer devido a fatores econômicos, ambientais ou regulatórios, que podem impactar a continuidade da produção em níveis elevados.              
""")

# Distribuição Normal
st.subheader("Distribuição Normal")
x = np.linspace(media - 3*desvio_padrao, media + 3*desvio_padrao, 100)
y = norm.pdf(x, media, desvio_padrao)
fig_norm = go.Figure()
fig_norm.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', name='Distribuição Normal'))
fig_norm.update_layout(title="Distribuição Normal da Produção de Minério", xaxis_title="Produção", yaxis_title="Densidade")
st.plotly_chart(fig_norm)


st.subheader("7.Existe uma concentração de valores próximos à média ou há uma dispersão elevada?")
st.markdown("""   
 A análise da distribuição da produção mineral revela uma dispersão elevada dos valores. Embora a média forneça um ponto de referência, há estados com produção muito acima e outros com volumes bem menores, indicando uma grande variabilidade nos dados. Isso sugere que poucos estados concentram a maior parte da produção, enquanto a maioria apresenta valores menores e mais dispersos.               
""")


st.subheader("8. A produção mineral apresenta caudas longas, indicando eventos extremos de produção?")
st.markdown("""     
Sim, a distribuição da produção mineral apresenta caudas longas, o que indica a existência de eventos extremos. Estados como Minas Gerais e Pará possuem uma produção muito acima da média nacional, criando uma assimetria na distribuição dos dados. Isso significa que a produção não é distribuída de maneira uniforme entre os estados, mas sim dominada por alguns poucos, enquanto a maioria tem produção significativamente menor.
             
""")


st.subheader("Conclusão")
st.markdown("""
A análise da produção mineral no Brasil revelou que a extração de minério de ferro está fortemente concentrada em poucos estados, especialmente Minas Gerais e Pará. A distribuição da produção apresenta alta dispersão e caudas longas, indicando que alguns estados dominam significativamente a produção enquanto outros possuem valores mais baixos.

A aplicação de distribuições probabilísticas permitiu entender melhor o comportamento da produção, sugerindo padrões que podem auxiliar na tomada de decisões estratégicas para investimentos e otimização da extração. Estados que superam consistentemente um threshold de produção podem ser considerados prioritários para alocação de recursos e infraestrutura.

Por fim, a estabilidade na produção ao longo dos anos sugere que estados com alta produção tendem a manter esse padrão, salvo interferências externas como políticas ambientais, demanda global e investimentos tecnológicos. Essa previsibilidade pode ser explorada para aprimorar a eficiência do setor mineral no Brasil.
""")
