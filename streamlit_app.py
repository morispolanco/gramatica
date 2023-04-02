import os
import streamlit as st
import openai
import chardet

openai.api_key = os.environ.get("OPENAI_API_KEY")

def dividir_texto(texto, max_tokens):
    palabras = texto.split()
    fragmentos = []
    fragmento_actual = []

    tokens_actual = 0
    for palabra in palabras:
        tokens_palabra = len(palabra) + 1  # Contar el espacio en blanco antes de la palabra
        if tokens_actual + tokens_palabra > max_tokens:
            fragmentos.append(' '.join(fragmento_actual))
            fragmento_actual = []
            tokens_actual = 0

        fragmento_actual.append(palabra)
        tokens_actual += tokens_palabra

    if fragmento_actual:
        fragmentos.append(' '.join(fragmento_actual))

    return fragmentos

def corregir_gramatica_y_estilo(texto_ensayo):
    max_tokens_por_fragmento = 4000
    fragmentos = dividir_texto(texto_ensayo, max_tokens_por_fragmento)
    correcciones = []

    for fragmento in fragmentos:
        prompt = f"Por favor, corrige la gramática y el estilo del siguiente ensayo:\n\n{fragmento}\n\nEnsayo corregido:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        correccion = response.choices[0].text.strip()
        correcciones.append(correccion)

    ensayo_corregido = ' '.join(correcciones)
    return ensayo_corregido

    st.download_button(
        label="Descargar Ensayo Corregido",
        data=open("ensayo_corregido.txt", "rb"),
        file_name="ensayo_corregido.txt",
        mime="text/plain",
    )
