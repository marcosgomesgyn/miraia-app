import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from audio_recorder_streamlit import audio_recorder

# 1. DESIGN EXTRAORDINÁRIO (Ajustado para Mobile e Desktop)
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
        # O motor 2.0 que sua chave já confirmou ter acesso [cite: 2026-02-04]
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        st.subheader("⚡ Ação Rápida")
        col_audio, col_txt, col_file = st.columns([0.6, 2, 1])
        
        with col_audio:
            # Componente de voz otimizado [cite: 2026-02-04]
            audio_bytes = audio_recorder(text="Falar", icon_size="2x", neutral_color="#3b82f6")
        
        with col_txt:
            comando = st.text_input("Comando de texto:", placeholder="Ex: Agendar reunião amanhã às 10h")
        
        with col_file:
            arquivo = st.file_uploader("Subir Print", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        # DISPARO: Só executa se houver áudio OU se clicar no botão
        botao_executar = st.button("🚀 Executar MiraAI")
        
        if botao_executar or audio_bytes:
            with st.spinner("MiraAI processando sua solicitação..."):
                # Define a instrução base
                instrucao = f"Aja como MiraAI. Instrução do usuário: {comando if comando else 'Processar entrada multimodal.'}"
                conteudo_para_ia = [instrucao]
                
                # Adiciona Imagem se houver [cite: 2026-02-04]
                if arquivo:
                    img = Image.open(arquivo)
                    conteudo_para_ia.append(img)
                
                # Adiciona Áudio se houver [cite: 2026-02-04]
                if audio_bytes:
                    conteudo_para_ia.append({"mime_type": "audio/wav", "data": audio_bytes})

                # Chamada oficial para a API
                response = model.generate_content(conteudo_para_ia)
                
                # Exibição do Resultado
                st.success("Análise concluída!")
                st.markdown(f"**Resposta da IA:** {response.text}")
                
                # Atualização automática da Agenda
                texto_tarefa = comando if comando else "Comando via Voz/Imagem"
                nova_tarefa = pd.DataFrame([{'Prioridade': 'Alta', 'Horário': 'Pendente', 'Tarefa/Evento': texto_tarefa, 'Status': 'Novo'}])
                st.session_state.agenda = pd.concat([st.session_state.agenda, nova_tarefa], ignore_index=True)

    except Exception as e:
        if "429" in str(e):
            st.warning("⚠️ O Google pediu um tempo (Limite de Cota). Aguarde 60 segundos e tente o próximo comando. [cite: 2026-02-04]")
        else:
            st.error(f"Erro na conexão: {e}")

# 4. DASHBOARD DE AGENDA
st.divider()
st.subheader("📅 Sua Jornada de Hoje")
st.session_state.agenda = st.data_editor(st.session_state.agenda, num_rows="dynamic", use_container_width=True)

st.markdown("---")
st.caption("MiraAI v2.0 - Tecnologia Omni Digital")
