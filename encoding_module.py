import numpy as np

# Criptografa uma mensagem usando a Cifra de César com ASCII estendido (256 caracteres)
def encrypt_message(message, shift=3): #usamos  como deslocamento padrão
    encrypted = ""
    
    for char in message:
        # Pega o código ASCII do caractere (0-255)
        ascii_code = ord(char)
        
        # Aplica o deslocamento no conjunto completo ASCII (0-255)
        shifted_code = (ascii_code + shift) % 256
        
        # Converte de volta para caractere
        encrypted_char = chr(shifted_code)
        encrypted += encrypted_char
    
    return encrypted

# Descriptografa considerando ASCII estendido
def decrypt_message(encrypted_message, shift=3):
    decrypted = ""
    
    for char in encrypted_message:
        # Pega o código ASCII do caractere criptografado
        ascii_code = ord(char)
        
        # Aplica o deslocamento negativo no conjunto completo ASCII (0-255)
        original_code = (ascii_code - shift) % 256
        
        # Converte de volta para caractere original
        decrypted_char = chr(original_code)
        decrypted += decrypted_char
    
    return decrypted

def encode_line_code(binary_string):
    
    signal = [] # Inicializando a lista do sinal
    last_polarity = -1 # Iniciando com polaridade negativa (Mas é apenas uma convenção)
    zero_count = 0 # Contador de zeros consecutivos
    one_count = 0 # Contador dos pulsos

    for bit in binary_string: # Iterando sobre cada bit do string binário
        if bit == '1': # Se ocorrer um pulso
            last_polarity *= -1 # Inverte a polaridade
            signal.append(last_polarity) # Adiciona o sinal com a polaridade invertida
            zero_count = 0 # Reseta o contador de zeros consecutivos
            one_count += 1 # Incrementa o contador de pulsos(pra ver se o número é par ou ímpar)
        else:
            zero_count += 1 # Incrementa o contador de zeros consecutivos
            if zero_count == 4: # Se ocorrerem 4 zeros consecutivos
                if one_count % 2 == 0: # Se o número de pulsos for par
                    last_polarity *= -1 # Inverte a polaridade
                    signal[-3:] = [last_polarity, 0, 0] # Substitui os últimos 3 zeros por B00, sendo B a polaridade invertida
                    signal.append(last_polarity) # Coloca o V com polaridade invertida ao pulso anterior (que é a violação da regra dos 4 zeros consecutivos)
                else: # Se o número de pulsos for ímpar
                    signal[-3:] = [0,0,0] # Substitui os últimos 3 zeros por 000 (porém essa linha só existe para melhor visualização do funcionamento do algoritmo)
                    signal.append(last_polarity) # Coloca o V com a mesma polaridade do pulso anterior(que é a violação da regra dos 4 zeros consecutivos)
                zero_count = 0 
                one_count = 0
            else:
                signal.append(0.0) # Adiciona um zero ao sinal
        
    return np.array(signal, dtype=np.float32) # Retorna o sinal como um array NumPy de float32 para melhor compatibilidade com bibliotecas de processamento de sinal

def decode_line_code(signal):
    
    binary_string = "" # Inicializando a string binária
    zero_count = 0 # Contador de zeros consecutivos
    last_polarity = None # Variável para armazenar a polaridade do último pulso

    i = 0 
    while i < len(signal): # Iterando sobre o sinal

        sample = signal[i]
        if sample == 0: # Se a amostra for zero
            zero_count += 1 # Incrementa o contador de zeros consecutivos
            binary_string += "0" # Adiciona um zero à string binária
            i += 1
        else: # Se a amostra for 1 ou -1
            if (i + 3 < len(signal) and
                signal[i + 1] == 0 and
                signal[i + 2] == 0 and
                signal[i + 3] == sample): # Verifica se é o caso do B00V (com B e V pulsos da mesma polaridade)

                binary_string += "0000" # Adiciona 4 zeros à string binária (que era violação alterada dos 4 zeros consecutivos)
                last_polarity = sample # Atualiza a polaridade do último pulso
                i += 4
                zero_count = 0

            elif zero_count == 3 and sample == last_polarity: # Verifica se é o caso do 000V (com um pulso seguindo os 3 zeros consecutivos)
                binary_string = binary_string[:-3] + "0000" # Coloca os 4 zeros consecutivos na string binária
                i += 1
                zero_count = 0

            else: # Caso seja um pulso isolado ou após zeros sem restrição
                binary_string += "1" # De forma normal adiciona um 1 à string binária
                zero_count = 0
                last_polarity = sample
                i += 1

    return binary_string
