import streamlit as st
import datetime
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

# 1. Configuração de Estabilidade da API
# Forçamos a conexão com a versão estável para evitar o erro 404
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Adicione isso temporariamente para ver o que sua chave enxerga:
    # st.write(genai.list_models())
else:
    st.error("Configure sua GOOGLE_API_KEY nos Secrets do Streamlit!")

# Definimos o modelo uma única vez aqui no topo
MODELO_ESTAVEL = 'gemini-2.0-flash-exp'

st.set_page_config(page_title="MiraIA - Agendamento", page_icon="📅", layout="centered")

# Inicializa a agenda se não existir
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
    
    # Componente de gravação
    audio = mic_recorder(
        start_prompt="Clique para Falar", 
        stop_prompt="Parar e Processar", 
        key='recorder'
    )
    
    if audio:
        # Mostra o player para você conferir se o som ficou bom
        st.audio(audio['bytes'])
        
        with st.spinner("IA interpretando sua voz..."):
            try:
                # Agora sim, usando a variável que criamos no topo!
                model = genai.GenerativeModel(MODELO_ESTAVEL)
                
                prompt = "Você é um assistente de recepção. Extraia Nome, Serviço e Data deste áudio. Responda APENAS no formato: Nome: [nome], Serviço: [servico], Data: [data]"
                
                audio_data = {
                    "mime_type": "audio/wav",
                    "data": audio['bytes']
                }
                
                # O comando abaixo agora usa o modelo da variável lá de cima
                response = model.generate_content([prompt, audio_data])
                
                st.info(f"✅ Resultado da IA:\n{response.text}")
                
            except Exception as e:
                st.error(f"Erro na IA: {e}")

                
    st.divider()
    st.write("### 📋 Agenda de Hoje")
    if not st.session_state.agenda:
        st.write("Nenhum agendamento para hoje.")
    else:
        for item in st.session_state.agenda:
            st.write(f"🔹 **{item['nome']}** - {item['servico']} ({item['data']})")


