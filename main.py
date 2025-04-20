from network import WLAN, STA_IF
from umqtt.simple import MQTTClient
from time import sleep
from json import dumps


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
MQTT_TOPIC = str(config.get('MQTT_TOPIC'))


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


def gerar_dados():
    return dumps({"temperatura": 25.5, "umidade": 10})


def publicar_mensagem(cliente, mensagem):
    try:
        cliente.publish(MQTT_TOPIC, mensagem)
        print(f'Mensagem publicada no tópico: "{MQTT_TOPIC}": {mensagem}')
        sleep(5)
    except Exception as e:
        print(f'Erro ao publicar: {e}')
    # finally:
        # cliente.disconnect()
        # print('Broker MQTT desconectado.')


conectar_wifi()
cliente_mqtt = conectar_broker()
dados = gerar_dados()

while True:
    if cliente_mqtt:
        publicar_mensagem(cliente_mqtt, mensagem=dados)
    else:
        print(f'Falha ao publicar mensagem: {cliente_mqtt}')
        sleep(5)
