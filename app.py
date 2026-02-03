import streamlit as st
import datetime
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import io

# Configuração da API (Vamos configurar a chave com segurança depois)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configure sua GOOGLE_API_KEY nos Secrets do Streamlit!")

st.set_page_config(page_title="MiraIA - Agendamento", page_icon="📅", layout="centered")

if 'agenda' not in st.session_state:
    st.session_state.agenda = []

st.title("✨ MiraIA Estética V2")

tab1, tab2 = st.tabs(["Agendar", "Painel Admin"])

with tab1:
    # (O formulário manual continua aqui para segurança)
    with st.form("form_agendamento"):
        nome = st.text_input("Seu Nome")
        whatsapp = st.text_input("WhatsApp")
        servico = st.selectbox("Serviço", ["Corte Masculino", "Lash Design", "Manicure"])
        data = st.date_input("Data", datetime.date.today())
        enviar = st.form_submit_button("Confirmar")
        if enviar:
            st.session_state.agenda.append({"nome": nome, "zap": whatsapp, "servico": servico, "data": data})

with tab2:
    st.subheader("🎙️ Comando de Voz Inteligente")
    audio = mic_recorder(start_prompt="Falar Comando", stop_prompt="Parar e Processar", key='recorder')
    
    if audio:
        st.audio(audio['bytes'])
        with st.spinner("Interpretando comando..."):
            try:
                # O Cérebro: Enviando áudio para o Gemini
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                contents = [
                    "Você é um assistente de recepção. Extraia Nome, Serviço e Data deste áudio. Responda APENAS no formato: Nome: [nome], Serviço: [servico], Data: [data]",
                    {"mime_type": "audio/wav", "data": audio['bytes']}
                ]
                response = model.generate_content(contents)
                st.info(f"IA Entendeu: {response.text}")
                
                # Aqui adicionaremos a lógica para salvar na lista automaticamente no próximo ajuste
            except Exception as e:
                st.error(f"Erro na IA: {e}")

    st.divider()
    st.write("### 📋 Agenda Atual")
    for item in st.session_state.agenda:
        st.write(f"✅ {item['nome']} - {item['servico']}")

