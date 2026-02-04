import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from audio_recorder_streamlit import audio_recorder # Importação no topo [cite: 2026-02-04]

# 1. CONFIGURAÇÃO DE DESIGN EXTRAORDINÁRIO
st.set_page_config(page_title="MiraAI - Gestão Inteligente", layout="wide", initial_sidebar_state="expanded")

# CSS High-Tech [cite: 2026-02-04]
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    section[data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.8); border-right: 1px solid #334155; }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white; border: none; padding: 12px; border-radius: 8px;
        font-weight: 600; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    .stTextInput>div>div>input { background-color: #1e293b; color: #f8fafc; border: 1px solid #475569; }
    div[data-testid="stDataFrame"] { background-color: #1e293b; border-radius: 12px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DA AGENDA
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Prioridade', 'Horário', 'Tarefa/Evento', 'Status'])

# 3. CABEÇALHO
col_tit1, col_tit2 = st.columns([1, 4])
with col_tit1:
    st.write("# 🤖")
with col_tit2:
    st.title("MiraAI")
    st.caption("Seu Assistente Multimodal de Alta Performance [cite: 2026-02-04]")

# 4. BARRA LATERAL
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
st.sidebar.title("Configurações")
api_key = st.sidebar.text_input("Conectar com Google Cloud (API Key):", type="password")

# 5. CORPO DO APP (AÇÃO RÁPIDA)
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') # Motor 2.0 [cite: 2026-02-04]
        
        container_comando = st.container()
        with container_comando:
            st.subheader("⚡ Ação Rápida")
            
            # Layout de 3 colunas para incluir o MICROFONE [cite: 2026-02-04]
            col_audio, col_txt, col_file = st.columns([0.5, 2, 1])
            
            with col_audio:
                # O botão de voz neon [cite: 2026-02-04]
                audio_bytes = audio_recorder(text="", icon_size="2x", neutral_color="#3b82f6")
            
            with col_txt:
                comando = st.text_input("O que deseja agendar?", placeholder="Fale ou digite aqui...")
            
            with col_file:
                arquivo = st.file_uploader("Subir Print", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

            if st.button("Executar com Gemini 2.0") or audio_bytes:
                with st.spinner("Processando inteligência..."):
                    conteudo = [f"Aja como Vozia/MiraAI. Usuário quer: {comando}"]
                    
                    if audio_bytes:
                        conteudo.append({"mime_type": "audio/wav", "data": audio_bytes}) [cite: 2026-02-04]
                    if arquivo:
                        conteudo.append(Image.open(arquivo))
                    
                    response = model.generate_content(conteudo)
                    st.success("Comando Processado!")
                    st.info(response.text)
                    
                    # Inserção na agenda
                    nova_linha = pd.DataFrame([{'Prioridade': 'Alta', 'Horário': 'A confirmar', 'Tarefa/Evento': comando if comando else "Comando de Voz", 'Status': 'Pendente'}])
                    st.session_state.agenda = pd.concat([st.session_state.agenda, nova_linha], ignore_index=True)

    except Exception as e:
        if "429" in str(e):
            st.warning("⚠️ O Google está respirando... Tente novamente em 30 segundos. [cite: 2026-02-04]")
        else:
            st.error(f"Conexão: {e}")

# 6. TABELA DE AGENDA (DASHBOARD)
st.divider()
st.subheader("📅 Sua Jornada de Hoje")
st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

st.markdown("---")
st.caption("MiraAI v2.0 - Desenvolvido para Omni Digital")
