import streamlit as st
import datetime
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

# Forçamos a conexão com a versão estável
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configure sua GOOGLE_API_KEY nos Secrets do Streamlit!")

# Definimos o modelo estável
MODELO_ESTAVEL = 'models/gemini-1.5-flash'

st.set_page_config(page_title="MiraIA - Agendamento", page_icon="📅", layout="centered")

if 'agenda' not in st.session_state:
    st.session_state.agenda = []

st.title("✨ MiraIA Estética V2")

tab1, tab2 = st.tabs(["Agendar", "Painel Admin"])

with tab1:
    st.subheader("📝 Cadastro Manual")
    with st.form("form_agendamento"):
        nome = st.text_input("Seu Nome")
        whatsapp = st.text_input("WhatsApp")
        servico = st.selectbox("Serviço", ["Corte Masculino", "Lash Design", "Manicure"])
        data = st.date_input("Data", datetime.date.today())
        enviar = st.form_submit_button("Confirmar Agendamento")
        
        if enviar:
            st.session_state.agenda.append({
                "nome": nome, 
                "zap": whatsapp, 
                "servico": servico, 
                "data": data.strftime('%d/%m/%Y')
            })
            st.success(f"Agendado para {nome}!")

with tab2:
    st.subheader("🎙️ Comando de Voz Inteligente")
    st.write("Diga algo como: 'Agendar Manicure para Julia amanhã'")
    
    # 1. BOTÃO DE GRAVAÇÃO
    audio = mic_recorder(
        start_prompt="Clique para Falar", 
        stop_prompt="Parar e Processar", 
        key='recorder'
    )
    
    if audio:
        st.audio(audio['bytes'])
        
        with st.spinner("IA interpretando sua voz..."):
            try:
                # 2. DIAGNÓSTICO: Mostra o que a chave realmente alcança
                modelos_disponiveis = [m.name for m in genai.list_models()]
                st.write(f"DEBUG - Sua chave enxerga: {modelos_disponiveis}")
                
                # 3. CHAMADA DA IA
                model = genai.GenerativeModel(MODELO_ESTAVEL)
                
                prompt = "Você é um assistente de recepção. Extraia Nome, Serviço e Data deste áudio. Responda APENAS no formato: Nome: [nome], Serviço: [servico], Data: [data]"
                
                audio_data = {
                    "mime_type": "audio/wav",
                    "data": audio['bytes']
                }
                
                response = model.generate_content([prompt, audio_data])
                st.info(f"✅ Resultado da IA:\n{response.text}")
                
            except Exception as e:
                st.error(f"Erro detalhado: {e}")

st.divider()
st.write("### 📋 Agenda de Hoje")
if not st.session_state.agenda:
    st.write("Nenhum agendamento para hoje.")
else:
    for item in st.session_state.agenda:
        st.write(f"🔹 **{item['nome']}** - {item['servico']} ({item['data']})")

