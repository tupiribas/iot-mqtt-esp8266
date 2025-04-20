# IoT-MQTT-ESP8266

[![Status do Projeto](https://img.shields.io/badge/Status-Em%20Discuss%C3%A3o-yellow.svg?style=for-the-badge)](https://shields.io/)
[![Linguagens](https://img.shields.io/badge/MicroPython-Python-blueviolet.svg?style=for-the-badge)](https://www.python.org/)
[![Plataformas](https://img.shields.io/badge/ESP8266-Servidor%20Local-orange.svg?style=for-the-badge)](https://micropython.org/)
[![Protocolos](https://img.shields.io/badge/MQTT-brightgreen.svg?style=for-the-badge)](https://mqtt.org/)
[![Licença](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

## Descrição

Este projeto implementa um sistema de **telemetria** utilizando o protocolo MQTT para coletar dados de sensores (simulados em um ESP8266) e transmiti-los para um servidor local para monitoramento e visualização.

## Tecnologias e Conceitos Utilizados

* **ESP8266:** Microcontrolador utilizado para simular a coleta de dados de um sensor e publicar essas informações.
* **MicroPython:** Firmware Python rodando no ESP8266.
* **MQTT (Message Queuing Telemetry Transport):** Protocolo de publicação/subscrição leve para comunicação entre o ESP8266, o broker local e o servidor local.
* **Broker MQTT Local:** Servidor MQTT rodando na rede local da indústria, responsável por intermediar a comunicação MQTT.
* **Broker MQTT na Nuvem (Opcional):** Servidor MQTT hospedado na nuvem para possibilitar acesso remoto aos dados. O broker local pode ser configurado para fazer um "bridge" com este broker.
* **Servidor Local:** Um servidor (potencialmente rodando Python com Flask ou outra framework web) que atua como um cliente MQTT (assinando os dados do broker local) e como um servidor HTTP (servindo os dados para o painel de visualização).
* **HTTP (Hypertext Transfer Protocol):** Protocolo utilizado para a comunicação entre o servidor local e o painel de visualização (interface web).
* **Painel de Visualização:** Uma interface web para exibir os dados dos sensores em tempo real.
* **Qualidade de Serviço (QoS):** Mecanismo do MQTT para garantir diferentes níveis de confiabilidade na entrega das mensagens.

## Arquitetura do Sistema

![Diagrama da Arquitetura do Sistema](https://i.imgur.com/SEu4K1n.png)

1.  **Coleta de Dados (ESP8266):** O ESP8266 (simulando um sensor) coleta dados (ex: status de uma porta) e os publica como mensagens MQTT no **Broker MQTT Local** em um tópico específico (ex: `/dev/porta/`).
2.  **Comunicação Local (MQTT):** O **Servidor Local** se inscreve no tópico `/dev/porta/` do **Broker MQTT Local** via MQTT para receber os dados em tempo real.
3.  **Integração com a Nuvem (Opcional - Bridging MQTT):** O **Broker MQTT Local** pode ser configurado para enviar (fazer um "bridge") dados específicos para um **Broker MQTT na Nuvem**, permitindo acesso remoto.
4.  **Visualização (HTTP):** O **Servidor Local**, após receber os dados via MQTT, os disponibiliza através de uma interface web (servidor HTTP). Um **Painel de Visualização** (executado em um navegador) consome esses dados via requisições HTTP para exibir as informações do sensor.

## Fluxo de Dados Detalhado

1.  O ESP8266 (publicador) envia dados do sensor para o Broker MQTT Local via Wi-Fi usando o protocolo MQTT.
2.  O Broker MQTT Local recebe a mensagem e a encaminha para todos os assinantes interessados.
3.  O Servidor Local (assinante) recebe a mensagem do Broker MQTT Local via MQTT.
4.  (Opcional) O Broker MQTT Local, se configurado, envia uma cópia da mensagem para o Broker MQTT na Nuvem.
5.  O Servidor Local processa os dados recebidos e os disponibiliza através de sua interface HTTP.
6.  Um navegador (Painel de Visualização) faz uma requisição HTTP ao Servidor Local para obter os dados e os exibe.

## Próximos Passos e Considerações

* Implementação do código MicroPython no ESP8266 para simular a leitura do sensor e a publicação MQTT.
* Configuração e execução de um Broker MQTT Local (ex: Mosquitto).
* (Opcional) Configuração de um Broker MQTT na Nuvem (ex: AWS IoT Core, Google Cloud IoT Core) e o "bridging" entre os brokers.
* Desenvolvimento do Servidor Local (em Python com Flask ou outra framework) para atuar como cliente MQTT e servidor HTTP.
* Criação do Painel de Visualização (HTML, CSS, JavaScript) para exibir os dados consumidos do Servidor Local via HTTP.
* Exploração dos diferentes níveis de Qualidade de Serviço (QoS) no MQTT para garantir a confiabilidade da entrega dos dados.

Este README fornece um panorama da arquitetura de monitoramento industrial utilizando MQTT e HTTP, conforme discutido. A implementação prática envolverá a configuração de cada componente de software e hardware detalhadamente.