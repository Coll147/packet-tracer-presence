@echo off
start "" "..\..\PacketTracer.exe"
timeout /t 5 /nobreak >nul
start /B pythonw ".\discord_rp.py" 
exit