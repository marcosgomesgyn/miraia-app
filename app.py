import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# 1. CONFIGURAÇÃO E ESTILO (CORREÇÃO TOTAL)
st.set_page_config(page_title="Vozia - MiraIA", layout="wide")

# CSS Corrigido para o Dark Mode e botões azuis
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    div[st-sidebar-width] { background-color: #1A1C23; }
    .stButton>button { 
        background-color: #007BFF !important; color: white !important; 
        border-radius: 8px; border: none; padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True) # Agora está correto!

# 2. INICIALIZAÇÃO DA AGENDA
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Hora/Data', 'Tarefa/Evento', 'Status'])

st.title("🚀 Omni Digital - Vozia/MiraIA")

# Barra lateral
api_key = st.sidebar.text_input("Cole sua API Key aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # MUDANÇA CRÍTICA: Chamamos o modelo sem o prefixo 'models/' 
        # para forçar a biblioteca a achar a rota certa.
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
                    
                    # Chamada simplificada
                    response = model.generate_content(conteudo)
                    
                    if response.text:
                        st.success(f"✅ Sucesso!")
                        st.write(response.text)
                        nova_linha = pd.DataFrame([{'Hora/Data': 'Confirmar', 'Tarefa/Evento': comando, 'Status': 'Novo'}])
                        st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

    except Exception as e:
        st.error(f"Erro: {e}")
        # Se der 404 de novo, vamos mostrar quais modelos sua chave REALMENTE pode usar
        if "404" in str(e):
            st.info("Tentando listar modelos disponíveis para sua chave...")
            models = [m.name for m in genai.list_models()]
            st.write(models)

# Sempre mostra a agenda, mesmo sem API Key, para não ficar "vazio"
st.divider()
st.subheader("📅 Agenda de Hoje")
st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)
