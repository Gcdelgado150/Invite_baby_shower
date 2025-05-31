import streamlit as st
import pandas as pd
import base64
import os
from helpers.sidebar import create_sidebar
from helpers import read_table, write_table
from time import sleep

# Reset logic BEFORE the widget is declared
if "reset_nome" not in st.session_state:
    st.session_state.reset_nome = False

if "nome_acompanhante" not in st.session_state:
    st.session_state.nome_acompanhante = ""

if "type" not in st.session_state:
    st.session_state.type = "Adulto"  # default

if "my_list" not in st.session_state:
    st.session_state.my_list = []

# If reset flag is True, reset the input value
if st.session_state.reset_nome:
    st.session_state["nome_acompanhante_input"] = ""  # Reset input via widget key
    st.session_state.reset_nome = False  # Reset the flag

st.set_page_config(page_title="Luigi", page_icon=":spades:", layout="wide")

# title = """
# <div style="
#     background-color: white; 
#     padding: 25px 10px; 
#     border-radius: 12px; 
#     box-shadow: 0 6px 15px rgba(0,0,0,0.1);
#     max-width: 500px;
#     margin: 30px auto;
#     color: #333;
#     text-align: center;
# ">
#     <h2 style="margin-top: 0;">Charraiá do Luigi</h2>
# </div>
# """
# st.markdown(title, unsafe_allow_html=True)
st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
# st.markdown("<h1 style='text-align: center; color: lightgreen;'></h1>", unsafe_allow_html=True)

# Função para converter imagem local para Base64
def get_base64_of_image(image_path):
    if not os.path.exists(image_path):
        st.error(f"Imagem '{image_path}' não encontrada!")
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Aplica imagem de fundo repetida
img_base64 = get_base64_of_image("Charraia_oficial.png")

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        @media only screen and (max-width: 768px) {{
            .stApp {{
                background-size: contain;
                background-position: top;
                background-attachment: scroll;
            }}
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
    fraldas_p = len(df[(df['Fralda'] == 'P') & (df['Acompanhante'] == 'Não')])

    percentage_M = 50
    percetange_G = 50

    return 1, "Sugestão de fralda:  Pampers Comfort Sec ou Personal Premium"

    if fraldas_p < 6:
        return 0, "Sugestão de fralda para você:  Pampers Comfort Sec ou Personal Premium P"

    if fraldas_m/total_fraldas * 100 < percentage_M:
        return 1, "Sugestão de fralda para você: Pampers Comfort Sec ou Personal Premium M"
    elif fraldas_m/total_fraldas * 100 > percentage_M:
        if fraldas_g/total_fraldas * 100 < percetange_G:
            return 2, "Sugestão de fralda para você:  Pampers Comfort Sec ou Personal Premium G"
        else:
            return 0, "Sugestão de fralda para você:  À sua escolha"

# Function to close the dialog
def close_dialog():
    st.session_state.show_dialog = False

# Function to add a new companion slot
def add_companion():
    st.session_state.companions.append({"name": "", "type": "Adult"})

def enviar(nome, presenca, fralda, lista):
    write_table(nome, presenca, fralda, acompanhantes=lista)
    close_dialog()
    confirmed(nome, st.session_state.my_list)

@st.dialog("🎉 Presença Confirmada")
def confirmed(nome, acompanhantes):
    st.write("Presença confirmada!! Obrigado e nos vemos lá!")

# CSS FOR EXPANDER
st.markdown("""
    <style>
    /* Background color of the whole expander block */
    details {
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Header of the expander */
    summary {
        background-color: #4CAF50  !important;
        color: black !important;
        padding: 10px;
        font-size: 25px;
        font-weight: bold;
        border-radius: 8px;
    }

    /* Optional: adjust width */
    .st-expander {
        max-width: 600px;
        margin: auto;
        font-weight: bold;
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

# Inject CSS to target the container div around the selectbox
st.markdown("""
    <style>
    /* Target selectbox outer container */
    div[data-baseweb="select"] {
        border: 2px solid #4CAF50 !important;
        border-radius: 6px !important;
        padding: 6px !important;
    }

    /* Add a green border when focused */
    div[data-baseweb="select"]:focus-within {
        border-color: #388E3C !important;
    }
    </style>
""", unsafe_allow_html=True)

# Define the popup dialog
with st.expander("🎉 Confirme sua presença e a fralda que vai levar, clicando aqui!".upper()):
    if st.session_state.show_dialog:
        st.subheader("📋 Confirmação de Presença")
        suggestion, phrase = get_percentage()

        col1, col2, col3 = st.columns(3)
        with col1:
            nome_text = f"""
            <div style='color:#2E8B57; font-size:22px; font-weight:bold;'>
                Nome:
            </div>
            """
            st.markdown(nome_text, unsafe_allow_html=True)
            nome_convidado = st.text_input("")
        with col2:
            presenca = st.radio("Você confirma presença?", ["Sim", "Não"], horizontal=False)
        
        # Use st.markdown to style the text
        styled_text = f"""
        <div style='color:#2E8B57; font-size:22px; font-weight:bold;'>
            {phrase}
        </div>
        """
        st.markdown(styled_text, unsafe_allow_html=True)
        fralda = st.selectbox("Tamanho da fralda que irá levar", ["P", "M", "G"], index=suggestion)

        st.divider()
        st.write("Adicionar acompanhantes (Clique no botão de adicionar após preencher)")
        for i in range(len(st.session_state.my_list)):
            col1, col2 = st.columns(2)
            with col1: 
                st.write(f"Acompanhante {i+1} : {st.session_state.my_list[i]['name']}")
            with col2: 
                st.write(st.session_state.my_list[i]["Type"])

        col1, col2, col3 = st.columns(3)
        with col1:
            nome = st.text_input("Nome", key="nome_acompanhante_input")

        with col2:
            st.session_state.type = st.selectbox(
                "Criança ou Adulto?", ["Criança", "Adulto"], 
                index=1 if st.session_state.type == "Adulto" else 0,
                key="type_select"
            )

        if st.button("Adicionar mais acompanhante"):
            if len(st.session_state.nome_acompanhante.strip()) > 0:
                st.session_state.my_list.append({
                    "name": st.session_state.nome_acompanhante.strip(),
                    "Type": st.session_state.type
                })
                st.session_state.reset_nome = True  # Set reset flag
                st.rerun()
            else:
                st.warning("Coloque o nome do acompanhante")

        st.divider()
        if st.button("Confirmar"):
            if len(nome_convidado.strip()) > 0:
                st.warning("Coloque seu nome!")
            if len(st.session_state.nome_acompanhante.strip()) > 0:
                st.session_state.my_list.append({
                    "name": st.session_state.nome_acompanhante.strip(),
                    "Type": st.session_state.type
                })

            # Use the final list of acompanhantes
            enviar(nome_convidado, presenca, fralda, st.session_state.my_list)
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
        <li><strong>Horário:</strong> 19:00</li>
        <li><strong>Confirme sua presença até 10 de Junho</strong></li>
    </ul> 
    <h2 style="margin-top: 30px;">📍 Localização</h2>
    <p style="font-size: 16px; margin-bottom: 0;">
        Rua Gastão da Cunha, 50. Gutierrez, Belo Horizonte
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
        'lat': [-19.940738281785094],
        'lon': [-43.96217765187213]
    })
    st.map(df, zoom=15, size=15)
    
    st.markdown("</div>", unsafe_allow_html=True)
