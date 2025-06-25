import streamlit as st
import socket
import numpy as np
import subprocess
import platform
from encoding_module import decode_line_code, decrypt_message
from visualization import plot_signal_waveform, plot_binary_signal


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to connect to a remote server (doesn't actually connect)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def get_all_network_interfaces():
    """Get all available network interfaces and their IPs"""
    interfaces = []
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            lines = result.stdout.split("\n")
            current_interface = None
            for line in lines:
                if "adapter" in line.lower() and ":" in line:
                    current_interface = line.split(":")[0].strip()
                elif "IPv4 Address" in line and current_interface:
                    ip = line.split(":")[1].strip()
                    if not ip.startswith("127."):
                        interfaces.append((current_interface, ip))
        else:  # Linux/macOS
            result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
            ips = result.stdout.strip().split()
            for i, ip in enumerate(ips):
                if not ip.startswith("127."):
                    interfaces.append((f"Interface {i+1}", ip))
    except Exception:
        pass
    return interfaces


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
    st.session_state.reset_requested = True
    st.session_state.listening = False
    st.session_state.received_message = False


st.title("Host B - Receptor")

# Get network information
local_ip = get_local_ip()
all_interfaces = get_all_network_interfaces()

# Quick IP display (always visible)
st.info(f"📡 **IP Principal:** `{local_ip}` | **Porta:** `{st.session_state.port}`")

# Network Information Section in an Accordion
with st.expander("📡 Informações Detalhadas de Rede"):
    # Display main IP prominently
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success(f"**IP Principal deste Receptor:** `{local_ip}`")
    with col2:
        if st.button("🔄 Atualizar IP"):
            st.experimental_rerun()

    # Show all available interfaces
    if all_interfaces:
        st.write("**Todas as interfaces de rede disponíveis:**")
        for interface, ip in all_interfaces:
            st.write(f"• {interface}: `{ip}`")
    else:
        st.warning("Não foi possível detectar outras interfaces de rede")

    # Connection instructions
    st.markdown("### 📋 Instruções para o Transmissor")
    st.code(
        f"""
No Host A (Transmissor), configure:
IP do Host B: {local_ip}
Porta: {st.session_state.port}
"""
    )

    # Copy configuration button
    if st.button("📋 Copiar Configuração", key="copy_config_detailed"):
        config_text = f"IP: {local_ip}\nPorta: {st.session_state.port}"
        st.code(config_text)
        st.success("Configuração exibida! Copie manualmente.")

st.markdown("---")

# Check for reset request from previous run
if st.session_state.reset_requested:
    st.session_state.reset_requested = False

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
        help="Porta que o receptor irá escutar por conexões",
    )
    st.session_state.port = int(port)

# Advanced network settings in an expander
with st.expander("⚙️ Configurações Avançadas de Rede"):
    col1, col2 = st.columns(2)

    with col1:
        bind_address = st.selectbox(
            "Interface de escuta:",
            options=["0.0.0.0 (Todas)", "127.0.0.1 (Local apenas)"]
            + [f"{ip} (Específica)" for _, ip in all_interfaces],
            index=0,
            disabled=st.session_state.listening,
            help="Escolha qual interface de rede usar para escutar conexões",
        )

        # Extract actual IP from selection
        if "Todas" in bind_address:
            selected_bind_ip = "0.0.0.0"
        elif "Local" in bind_address:
            selected_bind_ip = "127.0.0.1"
        else:
            selected_bind_ip = bind_address.split()[0]

    with col2:
        timeout_seconds = st.number_input(
            "Timeout (segundos):",
            min_value=1,
            max_value=30,
            value=1,
            disabled=st.session_state.listening,
            help="Tempo limite para aceitar conexões",
        )

# Control buttons
col1, col2, col3 = st.columns(3)

with col1:
    listen_button = st.button(
        "🎧 Aguardar Mensagem",
        disabled=st.session_state.listening,
        key="listen_button",
        use_container_width=True,
    )

with col2:
    reset_button = st.button(
        "🔄 Reiniciar",
        on_click=request_reset,
        disabled=st.session_state.listening and not st.session_state.received_message,
        use_container_width=True,
    )

with col3:
    if st.button("📋 Configuração Rápida", use_container_width=True):
        config_text = f"IP: {local_ip}\nPorta: {st.session_state.port}"
        st.code(config_text)
        st.success("Use estes valores no transmissor!")

# Status indicator
if st.session_state.listening and not st.session_state.received_message:
    status = st.empty()
    status.info(
        f"🎧 Servidor escutando em `{selected_bind_ip}:{st.session_state.port}`\n\n"
        f"**Aguardando conexão do transmissor...**"
    )

# Server logic
if listen_button:
    st.session_state.listening = True

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )  # Allow reuse of address
            s.bind((selected_bind_ip, st.session_state.port))
            s.listen()
            s.settimeout(timeout_seconds)

            status = st.empty()
            placeholder = st.empty()

            # Keep trying to accept a connection until successful
            while st.session_state.listening and not st.session_state.received_message:
                try:
                    status.info(
                        f"🎧 Servidor escutando em `{selected_bind_ip}:{st.session_state.port}`\n\n"
                        f"**Aguardando conexão...**"
                    )
                    conn, addr = s.accept()

                    with conn:
                        placeholder.success(
                            f"✅ **Conectado!** Cliente: `{addr[0]}:{addr[1]}`"
                        )
                        data = conn.recv(65536)  # Increased buffer size

                        if data:
                            received_signal = np.frombuffer(data, dtype=np.float32)
                            st.session_state.received_message = True

                            # Clear status messages
                            status.empty()
                            placeholder.empty()

                            # Display results
                            st.success(
                                f"📨 **Mensagem recebida de:** `{addr[0]}:{addr[1]}`"
                            )

                            # T2: Show received waveform
                            st.subheader("📊 Sinal Recebido")
                            fig = plot_signal_waveform(
                                received_signal, title="Forma de onda do sinal recebido"
                            )
                            st.pyplot(fig)

                            # T8: Reverse process
                            binary_msg = decode_line_code(received_signal)

                            # Visualize binary data
                            st.subheader("🔢 Representação Binária")
                            binary_fig = plot_binary_signal(
                                binary_msg,
                                title="Bits recebidos",
                            )
                            st.pyplot(binary_fig)

                            st.subheader("💾 Binário Recuperado")
                            formatted_binary = " ".join(
                                [
                                    binary_msg[i : i + 8]
                                    for i in range(0, len(binary_msg), 8)
                                ]
                            )
                            st.text(formatted_binary)

                            # Convert binary to text
                            try:
                                encrypted_msg = "".join(
                                    [
                                        chr(int(binary_msg[i : i + 8], 2))
                                        for i in range(0, len(binary_msg), 8)
                                    ]
                                )

                                st.subheader("🔐 Mensagem Criptografada")
                                st.text(encrypted_msg)

                                # Decrypt
                                original_msg = decrypt_message(encrypted_msg)

                                st.subheader("✅ Mensagem Decodificada")
                                st.success(f"**{original_msg}**")

                            except ValueError as e:
                                st.error(f"❌ Erro ao decodificar a mensagem: {e}")

                            break

                except socket.timeout:
                    continue
                except Exception as e:
                    st.error(f"❌ Erro ao escutar: {e}")
                    st.session_state.listening = False
                    break

    except Exception as e:
        st.error(f"❌ Erro ao iniciar o servidor: {e}")
        st.session_state.listening = False

# Show message history
if st.session_state.received_message:
    st.info(
        "✅ **Mensagem recebida com sucesso!** Clique em 'Reiniciar' para escutar novamente."
    )
