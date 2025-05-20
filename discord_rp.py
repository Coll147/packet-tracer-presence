import time
import psutil
import pygetwindow as gw
import os
from pypresence import Presence

CLIENT_ID = "1351548975567736923"
rpc = Presence(CLIENT_ID)
rpc.connect()

PACKET_TRACER_PROCESS = "PacketTracer.exe"
start_time = None

def is_packet_tracer_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == PACKET_TRACER_PROCESS:
            return True
    return False

def get_packet_tracer_window():
    """Devuelve la ventana activa de Packet Tracer si existe."""
    for window in gw.getWindowsWithTitle("Packet Tracer"):
        return window
    return None

def get_packet_tracer_file_name(title):
    """Extrae el nombre del archivo desde el título de la ventana."""
    title = title.replace(" - Cisco Packet Tracer", "").strip()
    return os.path.basename(title)

while True:
    if is_packet_tracer_running():
        if start_time is None:
            start_time = time.time()

        window = get_packet_tracer_window()
        if window:
            project_name = get_packet_tracer_file_name(window.title)
            print(f"Minimized: {window.isMinimized}, Active: {window.isActive}")
            
            # Solo considera "En pausa" si está minimizado
            is_minimized = window.isMinimized

            status = "Descansando :_v" if is_minimized else f"Editando {project_name}"
            print(f"Packet Tracer en ejecución: {status}")

            rpc.update(
                state=status,
                details="Tracing Packets",
                large_image="packet_tracer",
                small_image="cisco",
                start=start_time
            )
        else:
            print("No se encontró la ventana de Packet Tracer.")
    else:
        print("Packet Tracer no está en ejecución.")
        rpc.clear()
        start_time = None

    time.sleep(15)
