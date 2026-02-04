import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# CONFIGURAÇÃO DE DESIGN EXTRAORDINÁRIO
st.set_page_config(page_title="MiraAI - Gestão Inteligente", layout="wide", initial_sidebar_state="expanded")

# CSS Personalizado para Estilo High-Tech
st.markdown("""
    <style>
    /* Fundo Principal */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Estilização da Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid #334155;
    }
    
    /* Botão Principal Neon */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }

    /* Input de Texto */
    .stTextInput>div>div>input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #475569;
        border-radius: 8px;
    }

    /* Tabela de Agenda */
    div[data-testid="stDataFrame"] {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Prioridade', 'Horário', 'Tarefa/Evento', 'Status'])

# CABEÇALHO
col_tit1, col_tit2 = st.columns([1, 4])
with col_tit1:
    st.write("# 🤖")
with col_tit2:
    st.title("MiraAI")
    st.caption("Seu Assistente Multimodal de Alta Performance")

# BARRA LATERAL
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
st.sidebar.title("Configurações")
api_key = st.sidebar.text_input("Conectar com Google Cloud (API Key):", type="password")

# CORPO DO APP
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos o 2.0 que sua chave já liberou!
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        container_comando = st.container()
        with container_comando:
            st.subheader("⚡ Ação Rápida")
            col1, col2 = st.columns([2, 1])
            with col1:
                comando = st.text_input("O que deseja agendar ou analisar?", placeholder="Ex: Analisar este print de horários e agendar amanhã")
            with col2:
                arquivo = st.file_uploader("Subir Print/Foto", type=['png', 'jpg', 'jpeg'])

            if st.button("Executar com Gemini 2.0"):
                with st.spinner("Processando inteligência..."):
                    conteudo = [f"Aja como Vozia/MiraAI. Agende ou responda: {comando}"]
                    if arquivo:
                        conteudo.append(Image.open(arquivo))
                    
                    response = model.generate_content(conteudo)
                    st.success("Comando Processado!")
                    st.info(response.text)
                    
                    # Logica simples de inserção na agenda
                    nova_linha = pd.DataFrame([{'Prioridade': 'Alta', 'Horário': 'A confirmar', 'Tarefa/Evento': comando, 'Status': 'Pendente'}])
                    st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

    except Exception as e:
        if "429" in str(e):
            st.warning("⚠️ O Google está respirando... Tente novamente em 30 segundos.")
        else:
            st.error(f"Conexão: {e}")

# ÁREA DA AGENDA (DESIGN DE DASHBOARD)
st.divider()
st.subheader("📅 Sua Jornada de Hoje")
st.session_state.agenda = st.data_editor(
    st.session_state.agenda, 
    num_rows="dynamic", 
    use_container_width=True
)

st.markdown("---")
st.caption("MiraAI v2.0 - Desenvolvido para Omni Digital")
