from flask import Flask, jsonify
import pyautogui
import socket
import threading
import time

app = Flask(__name__)

# Variabili globali
bul = False
running = True  # Flag per controllare l'esecuzione del ciclo principale

# Ottenere l'indirizzo IP locale
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()
print(f"Server running at http://{ip}:50000")

port = 50000

@app.route('/start', methods=['GET'])
def start():
    global bul
    bul = not bul
    return jsonify({"status": "OK", "bul": bul}), 200

@app.route('/stop', methods=['GET'])
def stop():
    global running
    running = False  # Segnale per fermare il ciclo principale
    return jsonify({"status": "Stopping server"}), 200

# Funzione per il ciclo principale
def main_loop():
    global bul, running
    while running:  # Controlla se il server deve continuare a girare
        if bul:
            pyautogui.press('1')
            pyautogui.press('space')
            time.sleep(0.1)  # Per evitare cicli troppo veloci

# Esegui il server Flask e il ciclo principale in parallelo
if __name__ == '__main__':
    # Esegui il ciclo principale in un thread separato
    thread = threading.Thread(target=main_loop, daemon=True)
    thread.start()

    # Avvia il server Flask
    try:
        app.run(host=ip, port=port)
    finally:
        running = False  # Interrompi il ciclo quando il server Flask si chiude
        thread.join()  # Aspetta che il thread si fermi
