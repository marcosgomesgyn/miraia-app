import streamlit as st
import datetime

# 1. Configuração da Página (Visual de App)
st.set_page_config(page_title="MiraIA - Agendamento", page_icon="📅", layout="centered")

# CSS para esconder o menu do Streamlit e parecer um App
st.markdown("""
    <style>
    .stApp { max-width: 450px; margin: 0 auto; border: 1px solid #ddd; border-radius: 20px; padding: 10px; }
    button { width: 100%; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Banco de Dados Temporário (Session State)
if 'agenda' not in st.session_state:
    st.session_state.agenda = []

# 3. Cabeçalho
st.title("✨ MiraIA Estética")
st.subheader("Agendamento Rápido")

# 4. Interface de Abas (Cliente e Admin)
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
            novo_agendamento = {"nome": nome, "zap": whatsapp, "servico": servico, "data": data, "hora": hora}
            st.session_state.agenda.append(novo_agendamento)
            st.success(f"Pronto, {nome}! Seu horário para {servico} foi reservado.")

with tab2:
    st.write("### 📋 Agenda de Hoje")
    if not st.session_state.agenda:
        st.info("Nenhum agendamento para hoje.")
    else:
        for item in st.session_state.agenda:
            with st.container():
                st.markdown(f"**{item['hora']} - {item['nome']}**")
                st.caption(f"Serviço: {item['servico']}")
                # Botão que abre o WhatsApp real com mensagem pronta
                msg = f"Olá {item['nome']}, confirmamos seu horário de {item['servico']} hoje às {item['hora']}."
                link_zap = f"https://wa.me/55{item['zap']}?text={msg.replace(' ', '%20')}"
                st.markdown(f"[💬 Chamar no WhatsApp]({link_zap})")
                st.divider()

    # Espaço para o Comando de Voz (Explicação)
    st.warning("🎙️ O comando de voz requer integração com API do Navegador. No Streamlit Cloud, usaremos o componente 'streamlit-mic-recorder' no próximo passo.")