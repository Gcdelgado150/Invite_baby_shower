import streamlit as st
from helpers import read_table, write_table

st.set_page_config(page_title="Visão Lista de convidados", page_icon=":spades:", layout="wide")
df = read_table()

st.write(f"Ate o momento temos: {len(df)} pessoas indo")
st.write(f"Sendo: {len(df[df['Tipo'] == 'Adulto'])} adultos")
st.write(f"{len(df[df['Tipo'] == 'Criança'])} Crianças")

total_fraldas = len(df[(df['Acompanhante'] == 'Não')])
fraldas_p = len(df[(df['Fralda'] == 'P') & (df['Acompanhante'] == 'Não')])
fraldas_m = len(df[(df['Fralda'] == 'M') & (df['Acompanhante'] == 'Não')])
fraldas_g = len(df[(df['Fralda'] == 'G') & (df['Acompanhante'] == 'Não')])

st.write(f"Temos {fraldas_p} fraldas P ({fraldas_p/total_fraldas * 100:.1f}%)")
st.write(f"Temos {fraldas_m} fraldas M ({fraldas_m/total_fraldas * 100:.1f}%)")
st.write(f"Temos {fraldas_g} fraldas G ({fraldas_g/total_fraldas * 100:.1f}%)")




