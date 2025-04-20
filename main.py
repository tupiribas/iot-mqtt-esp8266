from network import WLAN, STA_IF
from umqtt.simple import MQTTClient
from time import sleep
from machine import Pin
from gc import mem_free, mem_alloc


def carregar_arquivo(filename="config.txt"):
    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except OSError:
        print(f'Problemas ao ler o arquivo de configuração "{filename}".')
    finally:
        print('\nLeitura do arquivo finalizada.')
    return config


config = carregar_arquivo()

SSID = str(config.get('SSID'))
SENHA = str(config.get('SENHA'))

MQTT_BROKER = str(config.get('MQTT_BROKER'))
MQTT_PORTA = int(config.get('MQTT_PORTA'))
MQTT_CLIENTE_ID = str(config.get('MQTT_CLIENTE_ID'))
MQTT_USUARIO = str(config.get('MQTT_USUARIO'))
MQTT_SENHA = str(config.get('MQTT_SENHA'))
MQTT_TOPIC_WIFI = str(config.get('MQTT_TOPIC_WIFI'))
MQTT_TOPIC_MEMORIA = str(config.get('MQTT_TOPIC_MEMORIA'))


def conectar_wifi():
    # Cria a estação de interface (wi-fi)
    wlan = WLAN(STA_IF)
    if not wlan.isconnected():
        print('Agora você está conectado a rede Wifi!\r\n\n')
    else:
        print("Você ja está conectado!")
    try:
        # Ativa a interface Wi-fi
        wlan.active(True)
        # Testa a conexão de rede
        wlan.connect(SSID, SENHA)
        sleep(10)
    except Exception as e:
        print(f'Falha ao conectar ao Wi-Fi. Erro: {e}')
    return wlan


led = Pin(2, Pin.OUT)


def conectar_broker():
    cliente = MQTTClient(client_id=MQTT_CLIENTE_ID,
                         server=MQTT_BROKER,
                         port=MQTT_PORTA,
                         user=MQTT_USUARIO,
                         password=MQTT_SENHA)
    sleep(5)
    try:
        cliente.connect()
        print('Conectado ao broker MQTT!')
        return cliente
    except Exception as e:
        print(f'Erro ao conectar ao bkoker: {e}')
        return None


def get_wifi_info(wlan):
    sta_if = wlan
    if sta_if.isconnected():
        return {
            "Conectado": True,
            "Nome_Rede": sta_if.config('essid'),
            "Sinal_wifi": sta_if.status('rssi'),
            "IP": sta_if.ifconfig()[0],
            "Endereco_MAC": sta_if.config('mac').hex(':')
        }
    else:
        return {"Conectado": False}


def get_memory_info():
    return {
        "Memoria_Livre": mem_free(),
        "Memoria_Usada": mem_alloc()
    }


def publicar_mensagem(cliente, wifi_info, memoria_info):
    try:
        cliente.publish(MQTT_TOPIC_WIFI, str(wifi_info), qos=0)
        print(
            f'Mensagem publicada no tópico: "{MQTT_TOPIC_WIFI}": {wifi_info}')
        cliente.publish(MQTT_TOPIC_MEMORIA, str(memoria_info), qos=0)
        print(
            f'''Mensagem publicada no tópico: "{MQTT_TOPIC_MEMORIA}":
            {memoria_info}'''
        )
        for _ in range(4):
            led.value(1)
            sleep(0.2)
            led.value(0)
            sleep(0.2)
    except Exception as e:
        print(f'Erro ao publicar: {e}')
    # finally:
        # cliente.disconnect()
        # print('Broker MQTT desconectado.')


wlan = conectar_wifi()
cliente_mqtt = conectar_broker()
INTERVALO = 2

while True:
    if cliente_mqtt:
        wifi_info = get_wifi_info(wlan)
        memoria_info = get_memory_info()
        publicar_mensagem(cliente_mqtt, wifi_info=wifi_info,
                          memoria_info=memoria_info)
        sleep(INTERVALO)
    else:
        print('Falha ao publicar mensagem. Cliente MQTT não conectado.')
        wlan = conectar_wifi()
        cliente_mqtt = conectar_broker()
        sleep(INTERVALO)
