import streamlit as st
import socket
import numpy as np
from encoding_module import decode_line_code, decrypt_message
from visualization import plot_signal_waveform, plot_binary_signal

# Initialize session state
if "listening" not in st.session_state:
    st.session_state.listening = False
if "port" not in st.session_state:
    st.session_state.port = 65432
if "received_message" not in st.session_state:
    st.session_state.received_message = False
if "reset_requested" not in st.session_state:
    st.session_state.reset_requested = False


def request_reset():
    # Instead of calling rerun directly, set a flag to do it later
    st.session_state.reset_requested = True
    st.session_state.listening = False
    st.session_state.received_message = False


st.title("Host B - Receptor")

# Check for reset request from previous run
if st.session_state.reset_requested:
    st.session_state.reset_requested = False
    # Don't need to do anything else, state has already been reset

# Port configuration
col1, col2 = st.columns([3, 1])
with col1:
    port = st.number_input(
        "Porta de conexão:",
        min_value=1024,
        max_value=65535,
        value=st.session_state.port,
        key="port_input",
        disabled=st.session_state.listening,
    )
    st.session_state.port = int(port)

# Control buttons
col1, col2 = st.columns(2)

with col1:
    listen_button = st.button(
        "Aguardar Mensagem", disabled=st.session_state.listening, key="listen_button"
    )

with col2:
    reset_button = st.button(
        "Reiniciar",
        on_click=request_reset,
        disabled=st.session_state.listening and not st.session_state.received_message,
    )

# Status indicator
if st.session_state.listening and not st.session_state.received_message:
    status = st.empty()
    status.info(
        f"Servidor escutando na porta {st.session_state.port}... Aguardando conexão..."
    )

# Server logic
if listen_button:
    st.session_state.listening = True

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", st.session_state.port))
            s.listen()
            s.settimeout(1.0)  # Set a timeout so we can update the UI

            status = st.empty()
            placeholder = st.empty()

            # Keep trying to accept a connection until successful
            while st.session_state.listening and not st.session_state.received_message:
                try:
                    status.info(
                        f"Servidor escutando na porta {st.session_state.port}... Aguardando conexão..."
                    )
                    conn, addr = s.accept()

                    with conn:
                        placeholder.success(f"Conectado por {addr}")
                        data = conn.recv(
                            8192
                        )  # Increased buffer size for larger messages

                        if data:
                            received_signal = np.frombuffer(data, dtype=np.float32)
                            st.session_state.received_message = True

                            # T2: Mostrar forma de onda recebida
                            st.subheader("Sinal Recebido")
                            fig = plot_signal_waveform(
                                received_signal, title="Forma de onda do sinal recebido"
                            )
                            st.pyplot(fig)

                            # T8: Processo inverso
                            binary_msg = decode_line_code(received_signal)

                            # Visualize binary data
                            st.subheader("Representação Binária")
                            binary_fig = plot_binary_signal(
                                binary_msg[
                                    : min(64, len(binary_msg))
                                ],  # Show first 64 bits for clarity
                                title="Amostra dos primeiros bits recebidos",
                            )
                            st.pyplot(binary_fig)

                            st.subheader("Binário Recuperado")
                            formatted_binary = " ".join(
                                [
                                    binary_msg[i : i + 8]
                                    for i in range(0, len(binary_msg), 8)
                                ]
                            )
                            st.text(formatted_binary)

                            # Converter binário para texto
                            try:
                                encrypted_msg = "".join(
                                    [
                                        chr(int(binary_msg[i : i + 8], 2))
                                        for i in range(0, len(binary_msg), 8)
                                    ]
                                )

                                st.subheader("Mensagem Criptografada")
                                st.text(encrypted_msg)

                                # Decriptografar
                                original_msg = decrypt_message(encrypted_msg)

                                st.subheader("Mensagem Decodificada")
                                st.success(original_msg)
                            except ValueError as e:
                                st.error(f"Erro ao decodificar a mensagem: {e}")

                            break
                except socket.timeout:
                    # This is normal, just keep trying
                    continue
                except Exception as e:
                    st.error(f"Erro ao escutar: {e}")
                    st.session_state.listening = False
                    break
    except Exception as e:
        st.error(f"Erro ao iniciar o servidor: {e}")
        st.session_state.listening = False

# Shows message history
if st.session_state.received_message:
    st.info(
        "Mensagem recebida com sucesso! Clique em 'Reiniciar' para escutar novamente."
    )
