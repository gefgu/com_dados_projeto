# Communication Data Project - README

## 📡 Projeto de Comunicação de Dados

Este projeto implementa um sistema de comunicação entre dois hosts (transmissor e receptor) com codificação de linha, criptografia e visualização interativa de sinais.

### 🚀 Funcionalidades

- **Host A (Transmissor)**: Envia mensagens criptografadas e codificadas
- **Host B (Receptor)**: Recebe, decodifica e descriptografa mensagens
- **Visualização Interativa**: Gráficos Plotly para análise de sinais
- **Codificação de Linha**: Conversão de dados binários para sinais analógicos
- **Criptografia**: Sistema de criptografia de mensagens (placeholder)
- **Interface Web**: Interface Streamlit intuitiva

---

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conexão de rede entre os computadores

### 1. Clone/Download do Projeto

```bash
# Clone o repositório ou baixe os arquivos
git clone <repository-url>
cd com_dados_projeto
```

### 2. Configuração do Ambiente Virtual

#### 🐧 Linux/macOS

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install streamlit matplotlib numpy plotly

# Verificar instalação
pip list
```

#### 🪟 Windows

```cmd
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install streamlit matplotlib numpy plotly

# Verificar instalação
pip list
```

### 3. Estrutura de Arquivos

Certifique-se de que todos os arquivos estão presentes:

```
com_dados_projeto/
├── host.py              # Aplicação transmissora
├── receptor.py          # Aplicação receptora
├── encoding_module.py   # Módulo de codificação/criptografia
├── visualization.py     # Módulo de visualização
├── venv/               # Ambiente virtual
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Este arquivo
```

---

## 🔧 Configuração de Rede

### Encontrar Endereços IP

#### 🐧 Linux/macOS

```bash
# Método 1
ip addr show

# Método 2
ifconfig

# Método 3
hostname -I

# Procure por endereços como: 192.168.x.x ou 10.x.x.x
```

#### 🪟 Windows

```cmd
# Método 1
ipconfig

# Método 2
ipconfig /all

# Procure por "IPv4 Address": 192.168.x.x ou 10.x.x.x
```

### Configuração de Firewall

#### 🐧 Linux (UFW)

```bash
# Verificar status do firewall
sudo ufw status

# Permitir portas necessárias
sudo ufw allow 8501    # Streamlit Receptor
sudo ufw allow 8502    # Streamlit Transmissor
sudo ufw allow 65432   # Porta de comunicação (personalizável)

# Habilitar firewall se necessário
sudo ufw enable
```

#### 🪟 Windows Defender

1. **Abrir Firewall do Windows:**

   - Pressione `Win + R`, digite `firewall.cpl`
   - Clique em "Permitir um aplicativo ou recurso através do Firewall do Windows Defender"

2. **Adicionar Exceção:**

   - Clique em "Alterar configurações"
   - Clique em "Permitir outro aplicativo..."
   - Procure por `python.exe` no diretório do seu ambiente virtual
   - Marque "Particular" e "Público"

3. **Configuração Alternativa:**
   ```cmd
   # Execute como Administrador
   netsh advfirewall firewall add rule name="Streamlit" dir=in action=allow protocol=TCP localport=8501-8502
   netsh advfirewall firewall add rule name="Python Communication" dir=in action=allow protocol=TCP localport=65432
   ```

#### 🍎 macOS

```bash
# Verificar status do firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Adicionar Python às aplicações permitidas
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /usr/bin/python3
```

---

## 🚀 Execução das Aplicações

### Configuração de Rede de Exemplo

- **Computador A (Transmissor)**: `192.168.1.100`
- **Computador B (Receptor)**: `192.168.1.101`
- **Porta de Comunicação**: `65432`

### 1. Iniciar o Receptor (Computador B)

#### 🐧 Linux/macOS

```bash
# Navegar para o diretório do projeto
cd /caminho/para/com_dados_projeto

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar aplicação receptora
streamlit run receptor.py --server.address 0.0.0.0 --server.port 8501
```

#### 🪟 Windows

```cmd
# Navegar para o diretório do projeto
cd C:\caminho\para\com_dados_projeto

# Ativar ambiente virtual
venv\Scripts\activate

# Iniciar aplicação receptora
streamlit run receptor.py --server.address 0.0.0.0 --server.port 8501
```

### 2. Iniciar o Transmissor (Computador A)

#### 🐧 Linux/macOS

```bash
# Em um novo terminal
cd /caminho/para/com_dados_projeto
source venv/bin/activate

# Iniciar aplicação transmissora
streamlit run host.py --server.address 0.0.0.0 --server.port 8502
```

#### 🪟 Windows

```cmd
# Em um novo prompt de comando
cd C:\caminho\para\com_dados_projeto
venv\Scripts\activate

# Iniciar aplicação transmissora
streamlit run host.py --server.address 0.0.0.0 --server.port 8502
```

---

## 📱 Uso das Aplicações

### 1. Configurar o Receptor

1. **Acessar Interface:**

   - Abra navegador em: `http://192.168.1.101:8501`
   - Ou localmente: `http://localhost:8501`

2. **Configurar Porta:**

   - Defina porta de escuta: `65432`

3. **Iniciar Escuta:**
   - Clique em "Aguardar Mensagem"
   - Aguarde mensagem: "Servidor escutando na porta 65432..."

### 2. Configurar o Transmissor

1. **Acessar Interface:**

   - Abra navegador em: `http://192.168.1.100:8502`
   - Ou localmente: `http://localhost:8502`

2. **Configurar Conexão:**

   - IP do Host B: `192.168.1.101`
   - Porta de conexão: `65432`

3. **Enviar Mensagem:**
   - Digite uma mensagem
   - Visualize os gráficos gerados
   - Clique em "Enviar Mensagem"

### 3. Verificar Comunicação

- **No Receptor**: Deve aparecer os sinais recebidos e a mensagem decodificada
- **No Transmissor**: Deve aparecer "Mensagem enviada com sucesso!"

---

## 🔍 Resolução de Problemas

### Problemas de Conectividade

#### Testar Conectividade de Rede

**🐧 Linux/macOS:**

```bash
# Testar ping
ping 192.168.1.101

# Testar porta específica
telnet 192.168.1.101 65432

# Verificar portas abertas
netstat -tuln | grep 65432
```

**🪟 Windows:**

```cmd
# Testar ping
ping 192.168.1.101

# Testar porta específica
Test-NetConnection -ComputerName 192.168.1.101 -Port 65432

# Verificar portas abertas
netstat -an | findstr 65432
```

### Problemas Comuns e Soluções

| Problema                 | Causa Provável      | Solução                                            |
| ------------------------ | ------------------- | -------------------------------------------------- |
| "Connection refused"     | Firewall bloqueando | Configurar firewall ou desabilitar temporariamente |
| "Address already in use" | Porta ocupada       | Usar porta diferente (ex: 65433)                   |
| "No route to host"       | IP incorreto        | Verificar IP com `ipconfig`/`ifconfig`             |
| Streamlit não abre       | Porta ocupada       | Usar `--server.port` diferente                     |

### Soluções Alternativas

#### Usar Hotspot Móvel

Se a rede local bloquear comunicação entre dispositivos:

1. **Criar hotspot** em um celular
2. **Conectar ambos computadores** ao hotspot
3. **Seguir mesmo procedimento** com os novos IPs

#### Teste Local (Um Computador)

Para testar em um único computador:

1. **Terminal 1:**

   ```bash
   streamlit run receptor.py --server.port 8501
   ```

2. **Terminal 2:**

   ```bash
   streamlit run host.py --server.port 8502
   ```

3. **Configuração:**
   - IP: `127.0.0.1` (localhost)
   - Portas diferentes para cada aplicação

---

## 📋 Comandos Úteis

### Verificar Status dos Serviços

```bash
# Verificar processos Streamlit rodando
ps aux | grep streamlit

# Matar processo específico
kill -9 <PID>

# Verificar portas em uso
lsof -i :8501
lsof -i :65432
```

### Atualizar Dependências

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Atualizar pip
pip install --upgrade pip

# Atualizar pacotes
pip install --upgrade streamlit matplotlib numpy plotly
```

---

## 🤝 Desenvolvimento

### Adicionar Novas Funcionalidades

1. **Codificação de Linha:** Editar encoding_module.py
2. **Visualizações:** Editar visualization.py
3. **Interface:** Editar host.py ou receptor.py

### Estrutura dos Módulos

- **encoding_module.py**: Funções de codificação/decodificação
- **visualization.py**: Gráficos interativos com Plotly
- **host.py**: Interface do transmissor
- **receptor.py**: Interface do receptor

---

## 📞 Suporte

### Logs de Debug

Para obter mais informações sobre erros:

```bash
# Executar com logs detalhados
streamlit run receptor.py --logger.level debug
```

### Informações do Sistema

```bash
# Versão Python
python --version

# Versões dos pacotes
pip list

# Informações do sistema
uname -a  # Linux/macOS
systeminfo  # Windows
```

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.

---

## 🔄 Histórico de Versões

- **v1.0**: Implementação básica com Matplotlib
- **v1.1**: Migração para Plotly (gráficos interativos)
- **v1.2**: Melhorias na interface e tratamento de erros

---

**Desenvolvido para o curso de Comunicação de Dados** 📡
