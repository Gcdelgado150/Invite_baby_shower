import streamlit as st
import pandas as pd
import base64
import os
from helpers.sidebar import create_sidebar
from helpers import read_table, write_table
from time import sleep

st.set_page_config(page_title="Luigi", page_icon=":spades:", layout="wide")
st.markdown("<h1 style='text-align: center;'>Charraiá do Luigi</h1>", unsafe_allow_html=True)

# Função para converter imagem local para Base64
def get_base64_of_image(image_path):
    if not os.path.exists(image_path):
        st.error(f"Imagem '{image_path}' não encontrada!")
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Aplica imagem de fundo repetida
img_base64 = get_base64_of_image("charraia.jpg")

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-repeat: repeat;
            background-size: 150px;
            background-color: rgba(255, 255, 255, 0.4);  /* White overlay with 40% opacity */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

if "companions" not in st.session_state:
    st.session_state.companions = []
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = True
if "my_list" not in st.session_state:
    st.session_state.my_list = []

df = read_table()

def get_percentage():
    total_fraldas = len(df[(df['Acompanhante'] == 'Não')])
    fraldas_m = len(df[(df['Fralda'] == 'M') & (df['Acompanhante'] == 'Não')])
    fraldas_g = len(df[(df['Fralda'] == 'G') & (df['Acompanhante'] == 'Não')])

    percentage_M = 70
    percentage_P = 10
    percetange_G = 100 - (percentage_M + percentage_P)

    if fraldas_m/total_fraldas * 100 < percentage_M:
        return "Se puder leve fraldas M"
    elif fraldas_m/total_fraldas * 100 > percentage_M:
        if fraldas_g/total_fraldas * 100 < percetange_G:
            return "Se puder leve fraldas G"
        else:
            return "À sua escolha"

# Function to close the dialog
def close_dialog():
    st.session_state.show_dialog = False

# Function to add a new companion slot
def add_companion():
    st.session_state.companions.append({"name": "", "type": "Adult"})

def enviar(nome, presenca, fralda):
    write_table(nome, presenca, fralda, acompanhantes=st.session_state.my_list)
    close_dialog()
    confirmed()

@st.dialog("🎉 Presença Confirmada")
def confirmed():
    st.write("Presença confirmada!! Obrigado e nos vemos lá!")

# CSS FOR EXPANDER
st.markdown("""
    <style>
    /* Background color of the whole expander block */
    details {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 8px;
    }

    /* Header of the expander */
    summary {
        background-color: #4CAF50 !important;
        color: white !important;
        padding: 10px;
        font-size: 18px;
        border-radius: 8px;
    }

    /* Optional: adjust width */
    .st-expander {
        max-width: 600px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

# CSS FOR INPUT TEXT
st.markdown("""
    <style>
    /* Target the input boxes */
    input[type="text"] {
        border: 2px solid #4CAF50 !important;  /* Green border */
        border-radius: 6px !important;
        padding: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# CSS FOR selectbox
st.markdown("""
    <style>
    select {
        border: 2px solid #4CAF50 !important;
        border-radius: 6px;
        padding: 6px;
    }

    select:focus {
        border-color: #388E3C !important;  /* darker green on focus */
        outline: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Use st.markdown to style the text
styled_text = f"""
<div style='color:#2E8B57; font-size:22px; font-weight:bold;'>
    {get_percentage()}
</div>
"""

# Define the popup dialog
with st.expander("🎉 Confirmar presença"):
    if st.session_state.show_dialog:
        st.subheader("📋 Confirmação de Presença")
        st.markdown(styled_text, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            nome = st.text_input("Nome")
        with col2:
            presenca = st.radio("Você confirma presença?", ["Sim", "Não"], horizontal=False)
        with col3:
            fralda = st.selectbox("Tamanho da fralda que irá levar", ["P", "M", "G"])


        st.divider()
        st.write("Adicionar acompanhantes (Clique no botão de adicionar após preencher)")
        for dnames in st.session_state.my_list:
            col1, col2 = st.columns(2)
            with col1: 
                st.write(dnames["name"])
            with col2: 
                st.write(dnames["Type"])

        col1, col2, col3 = st.columns(3)
        with col1:
            nome_acompanhante = st.text_input("Nome", key="nome_acompanhante")
        with col2:
            type = st.selectbox("Criança ou Adulto?", ["Criança","Adulto"])
        with col3:
            if st.button("Adicionar", key='add_button'):
                if len(nome_acompanhante) > 0:
                    obj = {"name": nome_acompanhante, "Type": type}
                    st.session_state.my_list.append(obj)
                    st.rerun()
                else:
                    st.warning("Coloque o nome do acompanhante")

        st.divider()
        if st.button("Enviar", on_click=enviar, args=(nome, presenca, fralda,)):
            st.rerun()

event_info_html = """
<div style="
    background-color: white; 
    padding: 25px 30px; 
    border-radius: 12px; 
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 30px auto;
    color: #333;
">
    <h2 style="margin-top: 0;">📅 Informações do Evento</h2>
    <ul style="list-style-type:none; padding-left: 0; font-size: 16px;">
        <li><strong>Data:</strong> 13 de Junho de 2025</li>
        <li><strong>Horário:</strong> 18:00</li>
        <li><strong>Confirme sua presença abaixo ↓ até 10 de Junho</strong></li>
    </ul> </div>
<div style="
    background-color: white; 
    padding: 25px 30px; 
    border-radius: 12px; 
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 30px auto;
    color: #333;
">
    <h2 style="margin-top: 30px;">📍 Localização</h2>
    <p style="font-size: 16px; margin-bottom: 0;">
        Rua Professor Aníbal de Matos, 290. Belo Horizonte
    </p>
</div>
"""

st.markdown(event_info_html, unsafe_allow_html=True)

# Use a container to wrap the map with styles in one block
with st.container():
    st.markdown("""
    <div style="
        max-width: 700px;
        margin: 0 auto 30px auto;  /* centers horizontally */
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    ">
    """, unsafe_allow_html=True)
    
    df = pd.DataFrame({
        'lat': [-19.948176],
        'lon': [-43.944153]
    })
    st.map(df, zoom=15, size=15)
    
    st.markdown("</div>", unsafe_allow_html=True)
