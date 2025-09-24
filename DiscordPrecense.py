import time
import psutil
import pygetwindow as gw
import os
import subprocess
import sys
from pypresence import Presence, exceptions

CLIENT_ID = "1351548975567736923"
rpc = None
start_time = None

PACKET_TRACER_PROCESS = "PacketTracer.exe"
# Ajustar esta ruta según la instalación de Packet Tracer (alguien lo cambia?)
PACKET_TRACER_PATH = r"C:\Program Files\Cisco Packet Tracer 8.2.2\bin\PacketTracer.exe"

# Contador para detectar si Packet Tracer lleva cerrado demasiado tiempo
missing_time = 0
CHECK_INTERVAL = 5       # cada 5 segundos
EXIT_TIMEOUT = 30        # salir si no detecta Packet Tracer en 30s

def connect_rpc():
    """Intenta conectar con Discord RPC, devuelve el objeto rpc o None."""
    global rpc
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        print("✅ Conectado a Discord RPC")
        return rpc
    except exceptions.DiscordNotFound:
        print("⚠️ Discord no está abierto o no se detecta. Reintentando...")
        return None

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

def launch_packet_tracer():
    """Lanza Packet Tracer si no está ya abierto."""
    if not is_packet_tracer_running():
        try:
            subprocess.Popen([PACKET_TRACER_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("🚀 Packet Tracer iniciado")
        except Exception as e:
            print(f"❌ No se pudo iniciar Packet Tracer: {e}")

# ---- PROGRAMA PRINCIPAL ----
launch_packet_tracer()

while True:
    if rpc is None:
        rpc = connect_rpc()

    if rpc:
        try:
            if is_packet_tracer_running():
                missing_time = 0
                if start_time is None:
                    start_time = time.time()

                window = get_packet_tracer_window()
                if window:
                    project_name = get_packet_tracer_file_name(window.title)

                    print(f"Minimized: {window.isMinimized}, Title: {window.title}")
                    is_minimized = window.isMinimized

                    status = "En pausa" if is_minimized else f"Editando {project_name}"
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
                missing_time += CHECK_INTERVAL
                print(f"⚠️ Packet Tracer no está en ejecución ({missing_time}/{EXIT_TIMEOUT}s)")

                try:
                    rpc.clear()
                except Exception:
                    pass
                start_time = None

                if missing_time >= EXIT_TIMEOUT:
                    print("⏹ Packet Tracer no detectado por 30s. Cerrando script...")
                    sys.exit(0)

        except (exceptions.PipeClosed, BrokenPipeError):
            print("⚠️ Se perdió la conexión con Discord. Reintentando...")
            rpc = None  # Forzar reconexión

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            rpc = None  # Mejor forzar reconexión

    time.sleep(CHECK_INTERVAL)
