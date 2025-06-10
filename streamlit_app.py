import streamlit as st
from groq import Groq

st.title("MI CHAT DE IA")
st.sidebar.title("Configuración de la IA")

nombre_usuario= st.sidebar.text_input("¿Cuál es tu nombre?", value="Usuario")

modelos=[ 'llama3-8b-8192', 'llama3-70b-8192', 'mixtral8x7b-32768']
modelo_elegido = st.sidebar.selectbox("Selecciona un modelo", modelos)

tono = st.sidebar.selectbox("Tono del asistente", ["Formal", "Informal", "Amistoso"])
def crea_usuario_groq():
    clave_secreta= st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)


def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        saludo= f'Hola {nombre_usuario}, ¿en qué puedo ayudarte hoy?'
        actualizar_historial("assistant", saludo, "🤖")

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})
    
def mostrar_hiatorial():
    for mensaje in st.session_state.mensajes:
       with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]): st.markdown(mensaje["content"])
           
def area_chat():
    contenedorChat = st.container(height= 400, border= True)
    with contenedorChat: mostrar_hiatorial()


def main():
    clienteUsuario = crea_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribi tu mensaje!!!")
    if mensaje:
        actualizar_historial("user", mensaje, "👩🏻")
        with st.chat_message("assiatant", avatar= "🤖"):
             mensaje_respuesta= st.empty
             respuesta_completa= ""
        respuesta_stream= clienteUsuario.chat.completions.create(
                 model= modelo_elegido,
                 messages= [{"role":"system", "content":f'Eres un asistente con tono {tono.lower()}.'},
                            {"role":"user", "content": mensaje}],
                 stream= True 
             )
        
        for frase in respuesta_stream:
            if frase.choices[0].delta.content:
                respuesta_completa += frase.choices[0].delta.content
        st.markdown(respuesta_completa)
        
        actualizar_historial("assiatant", respuesta_completa, "🤖")
        st.experimental_rerun()
        
if __name__== "__main__":
    main()
