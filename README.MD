

# Ejecución Remota de Comandos con Meshtastic

## 📌 Descripción

Este proyecto permite la ejecución remota de comandos en un sistema Linux utilizando Meshtastic, un protocolo de red mesh de largo alcance y código abierto. El sistema escucha mensajes de texto con el prefijo `cmd:` y ejecuta el comando subsiguiente en la máquina host, devolviendo el resultado a través de la red Meshtastic.

## ✨ Características Principales

* Ejecución segura de comandos remotos mediante red mesh Meshtastic
* Transmisión en tiempo real de los resultados (limitado a 200 caracteres)
* Manejo de errores con indicadores claros de éxito/fallo
* Registro de logs persistente (en `meshtastic_control.log` y consola)
* Mantiene conectividad inalámbrica durante la operación

## ⚙️ Requisitos

* Python 3.x
* Meshtastic (`pip install meshtastic`)
* Librería PubSub (`pip install pypubsub`)
* Dispositivo Meshtastic conectado (ej. /dev/ttyUSB0)

## 🚀 Configuración Rápida

1. Instala las dependencias:

```bash
pip install meshtastic pypubsub
```

2. Conecta tu dispositivo Meshtastic (ej. vía USB)

3. Ejecuta el script:

```bash
python3 meshtastic_control.py
```

## 📝 Uso

Envía comandos con el formato:

```
cmd:<tu_comando>
```

Ejemplos:

* `cmd:ls -la` - Lista archivos
* `cmd:df -h` - Muestra espacio en disco
* `cmd:uptime` - Ver tiempo de actividad del sistema

## ⚠️ Seguridad

* ADVERTENCIA: Este script ejecuta comandos directamente en el sistema
* Recomendado solo para redes Mesh privadas/seguras
* Considera implementar autenticación adicional
* Limita el acceso a nodos de confianza

## 📄 Licencia

Este proyecto está bajo licencia MIT. Úsalo bajo tu propio riesgo.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor abre un issue o pull request con tus mejoras.
