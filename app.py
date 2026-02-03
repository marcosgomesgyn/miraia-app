import streamlit as st
import datetime
from streamlit_mic_recorder import mic_recorder

# Configuração da Página
st.set_page_config(page_title="MiraIA - Agendamento", page_icon="📅", layout="centered")

# CSS para visual mobile
st.markdown("""
    <style>
    .stApp { max-width: 450px; margin: 0 auto; border: 1px solid #ddd; border-radius: 20px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'agenda' not in st.session_state:
    st.session_state.agenda = []

st.title("✨ MiraIA Estética V2")

tab1, tab2 = st.tabs(["Agendar", "Painel Admin"])

with tab1:
    with st.form("form_agendamento"):
        nome = st.text_input("Seu Nome")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        servico = st.selectbox("Serviço", ["Corte Masculino", "Lash Design", "Manicure", "Pedicure"])
        data = st.date_input("Data", datetime.date.today())
        hora = st.time_input("Horário", datetime.time(9, 0))
        enviar = st.form_submit_button("Confirmar Agendamento")
        if enviar:
            st.session_state.agenda.append({"nome": nome, "zap": whatsapp, "servico": servico, "data": data, "hora": hora})
            st.success(f"Agendado para {nome}!")

with tab2:
    st.subheader("🎙️ Comando de Voz")
    # Este é o componente que resolve o problema do microfone
    audio = mic_recorder(start_prompt="Clique para falar", stop_prompt="Parar", key='recorder')
    
    if audio:
        st.audio(audio['bytes'])
        st.success("Áudio capturado! Agora vamos conectar ao cérebro do Gemini no Passo 2.")

    st.divider()
    st.write("### 📋 Agenda")
    for item in st.session_state.agenda:
        st.write(f"**{item['hora']}** - {item['nome']} ({item['servico']})")

