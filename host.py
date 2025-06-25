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
if "test_mode" not in st.session_state:
    st.session_state.test_mode = False

st.title("Host A - Transmissor")


# Function to reset input fields
def request_reset():
    st.session_state.reset_requested = True
    st.session_state.reset = True
    st.session_state.receiver_ip = "127.0.0.1"
    st.session_state.message = ""


# Check for reset request
if st.session_state.reset_requested:
    st.session_state.reset_requested = False

# Connection settings in two columns
col1, col2 = st.columns(2)
with col1:
    receiver_ip = st.text_input(
        "IP do Host B:", key="receiver_ip", value=st.session_state.receiver_ip
    )
with col2:
    port = st.number_input(
        "Porta de conexão:",
        min_value=1024,
        max_value=65535,
        value=st.session_state.port,
        key="port_input",
    )

# Test mode toggle
st.markdown("---")
st.session_state.test_mode = st.toggle(
    "🧪 Modo Teste (enviar sequência: 1100001000000000)",
    value=st.session_state.test_mode,
)

# Message input (only show if not in test mode)
if not st.session_state.test_mode:
    message = st.text_input("Digite a mensagem:", key="message")
else:
    message = None

# Process if there's content to process
if message or st.session_state.test_mode:

    if st.session_state.test_mode:
        # Test mode: use binary sequence directly
        test_binary = "1100001000000000"

        # Show test sequence
        st.subheader("📝 Sequência Binária de Teste")
        st.write(test_binary)

        # Skip encryption
        st.subheader("🔐 Criptografia")
        st.write("❌ Pulada no modo de teste")

        # Use test binary directly
        binary_msg = " ".join(
            test_binary[i : i + 8] for i in range(0, len(test_binary), 8)
        )
        final_binary = test_binary

    else:
        # Normal mode: process message
        # Show original message
        st.subheader("📝 Mensagem Original")
        st.write(message)

        # Encrypt
        encrypted = encrypt_message(message)
        st.subheader("🔐 Mensagem Criptografada")
        st.write(encrypted)

        # Convert to binary
        binary_msg = " ".join(format(ord(c), "08b") for c in encrypted)
        final_binary = binary_msg.replace(" ", "")

    # Show binary representation
    st.subheader("🔢 Representação Binária")
    st.write(binary_msg)

    # Visualize binary data
    binary_fig = plot_binary_signal(
        binary_msg,
        title=(
            "Bits da mensagem"
            if not st.session_state.test_mode
            else "Bits da sequência de teste"
        ),
    )
    st.pyplot(binary_fig)

    # Apply line coding
    encoded_signal = encode_line_code(final_binary)
    st.subheader("⚡ Sinal Codificado")

    # Show waveform
    fig = plot_signal_waveform(
        encoded_signal,
        (
            "📊 Forma de onda do sinal codificado"
            if not st.session_state.test_mode
            else "📊 Forma de onda do sinal de teste"
        ),
    )
    st.pyplot(fig)

    # Send buttons
    button_col1, button_col2 = st.columns(2)

    with button_col1:
        send_label = (
            "📡 Enviar Mensagem"
            if not st.session_state.test_mode
            else "📡 Enviar Sequência de Teste"
        )
        if st.button(send_label):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((receiver_ip, st.session_state.port_input))
                    s.sendall(encoded_signal.tobytes())

                success_msg = (
                    f"Mensagem enviada com sucesso para {receiver_ip}:{st.session_state.port_input}!"
                    if not st.session_state.test_mode
                    else f"Sequência de teste enviada com sucesso para {receiver_ip}:{st.session_state.port_input}!"
                )
                st.success(success_msg)
            except Exception as e:
                st.error(f"Erro ao enviar: {e}")

    with button_col2:
        st.button("🔄 Reset", on_click=request_reset)

else:
    # Show reset button if there was previous input
    if st.session_state.get("reset", False):
        st.button("🔄 Reset", on_click=request_reset)
