import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *

# Configuração da página
st.set_page_config(page_title="Dashboard de Distribuições Probabilísticas", layout="wide")

# Criando as sub-abas (pages)
pages = st.selectbox("Escolha a sua seção:", [
    "Quem sou eu?",
    "Formação e Experiências Profissionais",
    "Skills",
])

# Renderizar conteúdo da página selecionada
if pages == "Quem sou eu?":
    st.image("FotoGabriel.png", width=350)  # Certifique-se de que o caminho da imagem esteja correto
    st.header("Jeferson Gabriel de Mendonça")
    st.write("Meu nome é Jeferson Gabriel de Mendonça, sou estudante do quarto semestre de Engenharia de Software na FIAP. Tenho grande interesse por música, arte e tecnologia, e busco atuar profissionalmente na área de design gráfico, UX/UI ou desenvolvimento de software.")
    st.write("Desde cedo, sempre fui curioso e interessado em diversas áreas, o que me levou a desenvolver habilidades tanto técnicas quanto artísticas. Programação, design gráfico e modelagem 3D são algumas das minhas maiores paixões, e gosto de explorar como essas áreas podem se complementar para criar projetos impactantes.")
    st.write("Acredito que a tecnologia tem o poder de transformar a maneira como interagimos com o mundo, e quero fazer parte dessa transformação.")

elif pages == "Formação e Experiências Profissionais":
    st.header("🎓 Formação e Experiências Profissionais")
    st.write("""
    - **Formação Acadêmica:**
        - Atualmente, curso Engenharia de Software na FIAP, onde desenvolvo conhecimentos técnicos e práticos sobre desenvolvimento de software, análise de dados e design. Além da graduação, estou realizando diversos cursos nas plataformas de ensino digital para aprimorar minhas habilidades em design gráfico e desenvolvimento de software.
    - **Experiência Profissional:**
        - Minha experiência profissional inclui o trabalho como assistente administrativo em um banco, onde desenvolvi habilidades organizacionais e analíticas, auxiliando na estruturação de processos internos.
    - **Projetos Acadêmicos:**
        - Criação de um projeto para uma estação de trem inteligente, utilizando Autodesk Maya para modelagem 3D.
        - Implementação de redes no Packet Tracer, configurando servidores e roteadores para simular ambientes reais.
        - Desenvolvimento de um projeto de análise de orçamento para redução da conta de luz, aplicando conceitos de análise de dados.
    - **Certificações:**
        - Certificações em **programação** e **soft skills** através de **FIAP Nano-Courses** e **Alura**.
    """)

elif pages == "Skills":
    st.header("🚀 Skills")
    st.write("""Ao longo da minha trajetória acadêmica e profissional, desenvolvi diversas habilidades técnicas e interpessoais. Entre minhas principais competências estão:
             
    Hard Skills:
        🔹 Programação: Python, Java, SQL e JavaScript.
        🔹 Ferramentas: Streamlit, Packet Tracer, Autodesk Maya. 
        🔹 Desenvolvimento Web: HTML, CSS e princípios de UX/UI.
        🔹 Design: UX/UI, diagramação, identidade visual e prototipagem com Figma.
        🔹 Modelagem 3D: Criação e estruturação de objetos no Autodesk Maya.
        🔹 Redes de Computadores: Configuração de redes, criação de sub-redes e 
        simulação de ambientes no Packet Tracer.
        🔹 Metodologias Ágeis: Kanban, Scrum e Trello para organização de projetos.
             
    Soft Skills:
        🔹 Comunicação eficiente em português e inglês.
        🔹 Organização e gestão de tarefas com foco em produtividade.
        🔹 Criatividade na resolução de problemas e design thinking.
        🔹 Trabalho em equipe e colaboração multidisciplinar.
        🔹 Capacidade analítica para interpretação e 
        extração de insights a partir de dados.
        🔹 Aprendizado rápido e adaptação a novas tecnologias.
    """)
