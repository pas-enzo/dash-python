import serial
import serial.tools.list_ports
import time

def find_microcontroller_port(baudrate=9600, timeout=1, test_command=b'PING\n', expected_response=b'PONG\n'):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate, timeout=timeout)
            ser.write(test_command)
            time.sleep(0.1)  # pausa para dar tempo de resposta ao microcontrolador
            if ser.in_waiting > 0:
                response = ser.readline().strip()
                if response == expected_response:
                    ser.close()
                    return port.device
            ser.close()
        except:
            continue
    return None

def process_serial_data(input):
    global pressao_linha_dianteira, pressao_linha_traseira, velocidade_dianteira, bateria, temperatura
    global rpm_dezena, rpm_unidade, combustivel, velocidade_traseira, aceleracao_em_x, aceleracao_em_y, aceleracao_em_z
    global giro_em_x, giro_em_y, giro_em_z, tep1, pres1, tep2, pres2, tep3, pres3, tep4, pres4
    global posicao_acelerador, posicao_freio, posicao_volante, botao_piloto1, botao_piloto2, botao_piloto3, x, y
    global velocidade, rpm, forca_g_x, forca_g_y, forca_g_z

    valores = input.split(',')
    
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
    
    # Calculo da velocidade
    velocidade = (velocidade_dianteira + velocidade_traseira) // 2
    
    # Função que junta as partes do RPM
    rpm = (rpm_dezena * 100) + rpm_unidade
    
    # Cálculo da força G
    forca_g_x = aceleracao_em_x / 10.0
    forca_g_y = aceleracao_em_y / 10.0
    forca_g_z = aceleracao_em_z / 10.0

def receive_serial():
    port = find_microcontroller_port()
    if port is None:
        print("Nenhuma porta serial com o microcontrolador encontrada.")
        return

    print(f"Conectando à porta serial: {port}")
    ser = serial.Serial(port, 9600, timeout=1)
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                process_serial_data(line)
                # print para testes
                print(f'Velocidade: {velocidade}, RPM: {rpm}, Força G (X, Y, Z): ({forca_g_x}, {forca_g_y}, {forca_g_z})')

# if __name__ == "__main__":
#     receive_serial()
