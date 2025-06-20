import streamlit as st
import socket
import numpy as np
from encoding_module import encode_line_code, encrypt_message
from visualization import plot_signal_waveform, plot_binary_signal

# Initialize session state for reset functionality
if "reset" not in st.session_state:
    st.session_state.reset = False
if "reset_requested" not in st.session_state:
    st.session_state.reset_requested = False
if "port" not in st.session_state:
    st.session_state.port = 65432
if "receiver_ip" not in st.session_state:
    st.session_state.receiver_ip = "127.0.0.1"

st.title("Host A - Transmissor")


# Function to reset input fields
def request_reset():
    st.session_state.reset_requested = True
    st.session_state.reset = True
    # Set the text input value directly
    st.session_state.receiver_ip = "127.0.0.1"
    st.session_state.message = ""


# Check for reset request
if st.session_state.reset_requested:
    st.session_state.reset_requested = False
    # Values already reset in the request_reset function

# Connection settings in two columns
col1, col2 = st.columns(2)
with col1:
    # Use the value from session state WITHOUT updating the session state afterward
    receiver_ip = st.text_input(
        "IP do Host B:", key="receiver_ip", value=st.session_state.receiver_ip
    )
    # Don't update session state here - Streamlit will handle this automatically
with col2:
    port = st.number_input(
        "Porta de conexão:",
        min_value=1024,
        max_value=65535,
        value=st.session_state.port,
        key="port_input",
    )
    # No need to update session state here either
    # st.session_state.port = int(port)  # Remove this line

# Message input
message = st.text_input("Digite a mensagem:", key="message")

# Layout for action buttons in a row
button_col1, button_col2 = st.columns(2)

send_button = None

if message:
    # T1: Mostrar mensagem original
    st.subheader("Mensagem Original")
    st.write(message)

    # T4: Criptografar
    encrypted = encrypt_message(message)
    st.subheader("Mensagem Criptografada")
    st.write(encrypted)

    # T5: Converter para binário (ASCII estendido)
    binary_msg = " ".join(format(ord(c), "08b") for c in encrypted)
    #binary_msg = "1100001000000000" # Sequência binária da aula de apresentação sem a criptografia.

    st.subheader("Mensagem em Binário")
    st.write(binary_msg)

    # Visualize binary data
    binary_fig = plot_binary_signal(
        binary_msg[: min(64, len(binary_msg.replace(" ", "")))],
        title="Amostra dos primeiros bits da mensagem",
    )
    st.pyplot(binary_fig)

    # T6: Aplicar algoritmo de codificação de linha
    encoded_signal = encode_line_code(binary_msg.replace(" ", ""))
    st.subheader("Sinal Codificado")

    # T2: Mostrar forma de onda
    fig = plot_signal_waveform(encoded_signal, "Forma de onda do sinal codificado")
    st.pyplot(fig)

    # T7: Enviar pela rede
    with button_col1:
        send_button = st.button("Enviar Mensagem")

    with button_col2:
        reset_button = st.button("Nova Mensagem", on_click=request_reset)

    if send_button:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Use the configured port from session state
                s.connect((receiver_ip, st.session_state.port_input))
                s.sendall(encoded_signal.tobytes())
            st.success(
                f"Mensagem enviada com sucesso para {receiver_ip}:{st.session_state.port_input}!"
            )
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
else:
    # Only show reset button if there was previous input
    if st.session_state.get("reset", False):
        st.button("Nova Mensagem", on_click=request_reset)
