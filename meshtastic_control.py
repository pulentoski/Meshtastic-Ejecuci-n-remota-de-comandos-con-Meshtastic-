#!/usr/bin/env python3
import glob
import subprocess
import meshtastic
import meshtastic.serial_interface
from datetime import datetime
import time
import logging
from pubsub import pub
import serial

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meshtastic_control.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

def buscar_puerto_serial():
    """Busca un puerto serial válido y retorna el primero que esté libre"""
    posibles_puertos = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
    for puerto in posibles_puertos:
        if not puerto_ocupado(puerto):
            logger.info(f"Puerto detectado: {puerto}")
            return puerto
        else:
            logger.warning(f"⚠️ Puerto {puerto} está ocupado.")
    if posibles_puertos:
        logger.error("Todos los puertos detectados están en uso. Finaliza los procesos que los ocupan antes de continuar.")
    else:
        logger.error("⚠️ No se detectaron dispositivos Meshtastic conectados (ttyUSB* o ttyACM*)")
    return None

def puerto_ocupado(puerto):
    """Devuelve True si el puerto está ocupado, False si está libre"""
    try:
        s = serial.Serial(puerto)
        s.close()
        return False
    except serial.SerialException:
        return True

def execute_command(command):
    """Ejecuta comandos en el sistema con manejo de errores"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return f"✅ {datetime.now().strftime('%H:%M:%S')}:\n{result.stdout[:200]}"
    except subprocess.CalledProcessError as e:
        return f"❌ {datetime.now().strftime('%H:%M:%S')}:\n{e.stderr[:200]}"

def on_receive(packet, interface):
    """Maneja mensajes entrantes manteniendo conectividad inalámbrica"""
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message = packet['decoded']['text']
            if message.startswith("cmd:"):
                logger.info(f"Comando recibido: {message}")
                response = execute_command(message[4:])
                interface.sendText(response)
    except Exception as e:
        logger.error(f"Error procesando mensaje: {str(e)}")

def main():
    interface = None
    puerto = buscar_puerto_serial()
    
    if not puerto:
        logger.error("No hay puertos disponibles para conectar. Saliendo...")
        return  # Sale si no hay puerto disponible o si está ocupado

    try:
        logger.info(f"Iniciando conexión Meshtastic en {puerto}...")
        interface = meshtastic.serial_interface.SerialInterface(
            devPath=puerto,
            noProto=False
        )
        pub.subscribe(on_receive, "meshtastic.receive")
        logger.info(f"\nConfiguración del nodo:\n{interface.nodes}\n")
        logger.info("Sistema listo. Envía comandos con formato: cmd:tu_comando")

        while True:
            time.sleep(1)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        if interface:
            interface.close()
        logger.info("Conexión cerrada")

if __name__ == "__main__":
    main()
