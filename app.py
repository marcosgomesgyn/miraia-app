import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from audio_recorder_streamlit import audio_recorder

# 1. DESIGN EXTRAORDINÁRIO
st.set_page_config(page_title="MiraAI - Gestão Inteligente", layout="wide")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    .stButton>button { 
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); 
        color: white; border-radius: 8px; font-weight: 600; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Prioridade', 'Horário', 'Tarefa/Evento', 'Status'])

st.title("🤖 MiraAI - Assistente Multimodal")

# 3. BARRA LATERAL E API
api_key = st.sidebar.text_input("API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # 4. AÇÃO RÁPIDA (Voz, Texto e IMAGEM)
        st.subheader("⚡ Ação Rápida")
        col_audio, col_txt, col_file = st.columns([0.5, 2, 1])
        
        with col_audio:
            audio_bytes = audio_recorder(text="", icon_size="2x", neutral_color="#3b82f6")
        with col_txt:
            comando = st.text_input("O que o MiraAI deve analisar?", placeholder="Ex: 'Organize este print na minha agenda'")
        with col_file:
            arquivo = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        if st.button("Executar com Gemini 2.0") or audio_bytes:
            with st.spinner("MiraAI analisando..."):
                # O segredo da visão: passamos o comando + a imagem para a IA
                conteudo_para_ia = [f"Aja como MiraAI. Instrução: {comando if comando else 'Analise esta imagem e me ajude.'}"]
                
                if arquivo:
                    img = Image.open(arquivo)
                    conteudo_para_ia.append(img) # Aqui a IA "vê" o print [cite: 2026-02-04]
                
                if audio_bytes:
                    conteudo_para_ia.append({"mime_type": "audio/wav", "data": audio_bytes})

                response = model.generate_content(conteudo_para_ia)
                st.info(response.text)
                
                # Adiciona na tabela
                nova_tarefa = pd.DataFrame([{'Prioridade': 'Alta', 'Horário': 'Ver resposta', 'Tarefa/Evento': comando if comando else "Análise de Imagem", 'Status': 'Pendente'}])
                st.session_state.agenda = pd.concat([st.session_state.agenda, nova_tarefa], ignore_index=True)

    except Exception as e:
        st.error(f"Erro: {e}")

# 5. DASHBOARD DE HOJE
st.divider()
st.subheader("📅 Sua Jornada de Hoje")
st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)
