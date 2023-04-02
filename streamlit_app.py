import os
import streamlit as st
import openai
import chardet

openai.api_key = os.environ.get("OPENAI_API_KEY")

def corregir_gramatica_y_estilo(texto_ensayo):
    prompt = f"Por favor, corrige la gramática y el estilo del siguiente ensayo:\n\n{texto_ensayo}\n\nEnsayo corregido:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    ensayo_corregido = response.choices[0].text.strip()
    return ensayo_corregido

st.title("Corrector de Gramática y Estilo")
archivo_subido = st.file_uploader("Sube tu ensayo", type=["txt", "docx", "pdf"])

if archivo_subido is not None:
    deteccion = chardet.detect(archivo_subido.read())
    codificacion = deteccion['encoding'] or 'latin-1'
    archivo_subido.seek(0)
    
    texto_ensayo = archivo_subido.read().decode(codificacion)

    st.write("Contenido del ensayo:")
    st.write(texto_ensayo)

    if st.button("Corregir Gramática y Estilo"):
        ensayo_corregido = corregir_gramatica_y_estilo(texto_ensayo)
        st.write("Ensayo corregido:")
        st.write(ensayo_corregido)

        with open("ensayo_corregido.txt", "w") as f:
            f.write(f"Ensayo original:\n\n{texto_ensayo}\n\nEnsayo corregido:\n\n{ensayo_corregido}")

        st.download_button(
            label="Descargar Ensayo Corregido",
            data=open("ensayo_corregido.txt", "rb"),
            file_name="ensayo_corregido.txt",
            mime="text/plain",
        )
