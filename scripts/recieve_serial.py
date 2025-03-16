import serial
import time

# Inicialização das variáveis globais com valores padrão
pressao_linha_dianteira = pressao_linha_traseira = velocidade_dianteira = bateria = temperatura = 0
rpm_dezena = rpm_unidade = combustivel = velocidade_traseira = aceleracao_em_x = aceleracao_em_y = aceleracao_em_z = 0
giro_em_x = giro_em_y = giro_em_z = tep1 = pres1 = tep2 = pres2 = tep3 = pres3 = tep4 = pres4 = 0
posicao_acelerador = posicao_freio = posicao_volante = botao_piloto1 = botao_piloto2 = botao_piloto3 = x = y = 0
velocidade = rpm = forca_g_x = forca_g_y = forca_g_z = 0

def find_microcontroller_port(baudrate=9600, timeout=1, test_command=b'PING\n', expected_response=b'PONG\r\n'):
    """
    Attempts to find and verify a microcontroller on COM3 using a ping-pong test.
    """
    port_name = 'COM3'
    
    try:
        with serial.Serial(port_name, baudrate, timeout=timeout) as ser:
            print(f"Enviando comando: {test_command.decode('utf-8', errors='ignore').strip()}")
            ser.write(test_command)
            time.sleep(0.5)
            
            if ser.in_waiting > 0:
                response = ser.readline()
                print(f"Resposta recebida: {response}")
                print(f"Tipo da resposta: {type(response)}")
                
                if response == expected_response:
                    print(f"Microcontrolador encontrado em {port_name}")
                    return port_name
                else:
                    print(f"Resposta inesperada. Esperado {expected_response}, recebido {response}")
                    return None
            else:
                print("Nenhum dado recebido do microcontrolador")
                return None
                
    except serial.SerialException as e:
        print(f"Erro de conexão serial em {port_name}: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado em {port_name}: {e}")
        return None

def process_serial_data(input_data):
    global pressao_linha_dianteira, pressao_linha_traseira, velocidade_dianteira, bateria, temperatura
    global rpm_dezena, rpm_unidade, combustivel, velocidade_traseira, aceleracao_em_x, aceleracao_em_y, aceleracao_em_z
    global giro_em_x, giro_em_y, giro_em_z, tep1, pres1, tep2, pres2, tep3, pres3, tep4, pres4
    global posicao_acelerador, posicao_freio, posicao_volante, botao_piloto1, botao_piloto2, botao_piloto3, x, y
    global velocidade, rpm, forca_g_x, forca_g_y, forca_g_z

    # Tenta decodificar os dados como UTF-8, ignorando erros
    try:
        data_str = input_data.decode('utf-8', errors='ignore').strip()
        print(f"Dados decodificados: {data_str}")
        
        # Remove o prefixo "Variáveis recebidas: " se presente
        if data_str.startswith("Variáveis recebidas: "):
            data_str = data_str.replace("Variáveis recebidas: ", "")
        
        # Verifica se os dados estão no formato esperado (separados por vírgulas)
        if ',' not in data_str:
            print("Formato inválido: dados não contêm vírgulas.")
            return
        
        valores = data_str.split(',')
        
        # Verifica se há pelo menos 32 valores esperados
        if len(valores) < 32:
            print(f"Erro: número insuficiente de valores recebidos ({len(valores)}). Esperado: 32.")
            return
        
        # Atribuir valores aos parâmetros
        pressao_linha_dianteira = int(valores[0])
        pressao_linha_traseira = int(valores[1])
        velocidade_dianteira = int(valores[2])
        bateria = int(valores[3])
        temperatura = int(valores[4])
        rpm_dezena = int(valores[5])
        rpm_unidade = int(valores[6])
        combustivel = int(valores[7])
        velocidade_traseira = int(valores[8])
        aceleracao_em_x = int(valores[9])
        aceleracao_em_y = int(valores[10])
        aceleracao_em_z = int(valores[11])
        giro_em_x = int(valores[12])
        giro_em_y = int(valores[13])
        giro_em_z = int(valores[14])
        tep1 = int(valores[16])
        pres1 = int(valores[17])
        tep2 = int(valores[18])
        pres2 = int(valores[19])
        tep3 = int(valores[20])
        pres3 = int(valores[21])
        tep4 = int(valores[22])
        pres4 = int(valores[23])
        posicao_acelerador = int(valores[24])
        posicao_freio = int(valores[25])
        posicao_volante = int(valores[26])
        botao_piloto1 = int(valores[27])
        botao_piloto2 = int(valores[28])
        botao_piloto3 = int(valores[29])
        x = int(valores[30])
        y = int(valores[31])
        
        # Cálculo da velocidade
        velocidade = (velocidade_dianteira + velocidade_traseira) // 2
        
        # Função que junta as partes do RPM
        rpm = (rpm_dezena * 100) + rpm_unidade
        
        # Cálculo da força G
        forca_g_x = aceleracao_em_x / 10.0
        forca_g_y = aceleracao_em_y / 10.0
        forca_g_z = aceleracao_em_z / 10.0
        
    except (ValueError, IndexError) as e:
        print(f"Erro ao processar dados: {e}")
        return

def receive_serial():
    port = find_microcontroller_port()
    if port is None:
        print("Nenhuma porta serial com o microcontrolador encontrada.")
        return

    print(f"Conectando à porta serial: {port}")
    try:
        with serial.Serial(port, 9600, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline()  # Lê os bytes brutos
                    if line:
                        print(f"Dados brutos recebidos: {line}")
                        process_serial_data(line)
                        print(f'Velocidade: {velocidade}, RPM: {rpm}, Força G (X, Y, Z): ({forca_g_x}, {forca_g_y}, {forca_g_z})')
    except serial.SerialException as e:
        print(f"Erro na comunicação serial: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

#if __name__ == "__main__":
 #   receive_serial()