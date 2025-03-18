import time
import psutil
import pygetwindow as gw
import os
from pypresence import Presence

# Configura el ID de tu aplicación en Discord Developer Portal
CLIENT_ID = "1351548975567736923"
rpc = Presence(CLIENT_ID)
rpc.connect()

# Nombre del proceso de Packet Tracer en Windows
PACKET_TRACER_PROCESS = "PacketTracer.exe"

def is_packet_tracer_running():
    """Verifica si Packet Tracer está en ejecución."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == PACKET_TRACER_PROCESS:
            return True
    return False

def get_packet_tracer_file_name():
    """Obtiene el nombre del archivo abierto en Packet Tracer sin la ruta."""
    for window in gw.getWindowsWithTitle("Packet Tracer"):
        if window.title:
            title = window.title.replace(" - Cisco Packet Tracer", "").strip()
            file_name = os.path.basename(title)  # Extrae el nombre del archivo del titulo de la ventana
            return file_name
    return "Proyecto desconocido"

while True:
    if is_packet_tracer_running():
        project_name = get_packet_tracer_file_name()
        print(f"Packet Tracer en ejecución: {project_name}")

        rpc.update(
            state=f"Editando {project_name}",
            details="Tracing Packets",
            large_image="packet_tracer",
            small_image="cisco",
            start=time.time()
        )
    else:
        print("Packet Tracer no está en ejecución.")
        rpc.clear()

    time.sleep(15)  # Discord limita las actualizaciones a cada 15 segundos
