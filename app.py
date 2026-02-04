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
        color: white; border-radius: 8px; font-weight: 600; width: 100%;
    }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO
if 'agenda' not in st.session_state:
    st.session_state.agenda = pd.DataFrame(columns=['Prioridade', 'Horário', 'Tarefa/Evento', 'Status'])

st.title("🤖 MiraAI - Assistente Multimodal")

# 3. BARRA LATERAL
api_key = st.sidebar.text_input("Cole sua API Key aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # NOME ABSOLUTO: O padrão que resolve o erro 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')
                
        st.subheader("⚡ Ação Rápida")
        col_audio, col_txt, col_file = st.columns([0.6, 2, 1])
        
        with col_audio:
            audio_bytes = audio_recorder(text="Falar", icon_size="2x", neutral_color="#3b82f6")
        
        with col_txt:
            comando = st.text_input("Comando de texto:", placeholder="Ex: Agendar reunião amanhã às 10h")
        
        with col_file:
            arquivo = st.file_uploader("Subir Print", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        if st.button("🚀 Executar MiraAI"):
            if comando or arquivo or audio_bytes:
                with st.spinner("MiraAI processando sua solicitação..."):
                    instrucao = f"Aja como MiraAI. Instrução do usuário: {comando if comando else 'Analise os dados fornecidos.'}"
                    conteudo_para_ia = [instrucao]
                    
                    if arquivo:
                        conteudo_para_ia.append(Image.open(arquivo))
                    
                    if audio_bytes:
                        conteudo_para_ia.append({"mime_type": "audio/wav", "data": audio_bytes})

                    # Chamada direta
                    response = model.generate_content(conteudo_para_ia)
                    
                    st.success("Análise concluída!")
                    st.markdown(f"**Resposta da IA:** {response.text}")
                    
                    # Atualiza Agenda
                    texto_tarefa = comando if comando else "Comando Multimodal"
                    nova_tarefa = pd.DataFrame([{'Prioridade': 'Alta', 'Horário': 'Ver Resposta', 'Tarefa/Evento': texto_tarefa, 'Status': 'Novo'}])
                    st.session_state.agenda = pd.concat([st.session_state.agenda, nova_tarefa], ignore_index=True)
            else:
                st.warning("Por favor, digite algo antes de executar.")

    except Exception as e:
        if "429" in str(e):
            st.error("Limite de cota atingido. Por favor, aguarde 60 segundos.")
        elif "404" in str(e):
            st.error("Erro de conexão com o modelo. Tentando reestabilizar...")
        else:
            st.error(f"Erro inesperado: {e}")
            
# 4. DASHBOARD DE AGENDA
st.divider()
st.subheader("📅 Sua Jornada de Hoje")
st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

st.markdown("---")
st.caption("MiraAI v2.0 - Tecnologia Omni Digital")

