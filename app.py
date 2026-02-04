import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# 1. ESTILO "DARK MODE" PROFISSIONAL
st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { 
        background-color: #007BFF; color: white; border-radius: 10px;
        border: none; padding: 10px 24px; font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_stdio=True)

# 2. INICIALIZAÇÃO DA AGENDA
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

api_key = st.sidebar.text_input("Cole sua API Key aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Forçamos o modelo sem prefixos para evitar o 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.subheader("🎤 O que o Omni deve fazer?")
        comando = st.text_input("Comando:", value="Agendar live no Instagram quarta às 19h")
        arquivo = st.file_uploader("Suba um Print ou Foto", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Executar Comando"):
            if not comando:
                st.warning("Por favor, digite um comando.")
            else:
                with st.spinner("O Omni está processando..."):
                    conteudo = [f"Aja como o assistente Vozia. O usuário quer: {comando}"]
                    if arquivo:
                        img = Image.open(arquivo)
                        conteudo.append(img)
                    
                    # A CHAMADA PURA (O Google decide a versão v1 automaticamente)
                    response = model.generate_content(conteudo)
                    
                    if response.text:
                        st.success(f"✅ Sucesso! Resposta: {response.text}")
                        nova_linha = pd.DataFrame([{'Hora/Data': 'Confirmar', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                        st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

        st.divider()
        st.subheader("📅 Agenda de Hoje")
        st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

    except Exception as e:
        st.error(f"Erro de conexão: {e}")
