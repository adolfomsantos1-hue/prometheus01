"""
PROMETHEUS 01 - SERVIDOR ANDROID
"""

import socket
import threading
import json
import time
import struct
from datetime import datetime

CONTROL_PORT = 5000
BROADCAST_PORT = 5001
DEVICE_NAME = "Meu Celular"
DEVICE_TYPE = "Android"

class PrometheusServer:
    def __init__(self):
        self.running = False
        
    def start(self):
        self.running = True
        threading.Thread(target=self._broadcast_loop, daemon=True).start()
        self._start_tcp_server()
        
    def _start_tcp_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', CONTROL_PORT))
        server.listen(5)
        print(f"🚀 Servidor rodando na porta {CONTROL_PORT}")
        
        while self.running:
            try:
                client, addr = server.accept()
                print(f"📱 Cliente conectado: {addr}")
                threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()
            except:
                break
                
    def _handle_client(self, client):
        try:
            while self.running:
                size_data = client.recv(4)
                if not size_data:
                    break
                size = struct.unpack('>I', size_data)[0]
                data = client.recv(size)
                command = json.loads(data.decode())
                response = self._process_command(command)
                json_response = json.dumps(response).encode()
                client.send(struct.pack('>I', len(json_response)) + json_response)
        except:
            pass
        finally:
            client.close()
            
    def _process_command(self, command):
        cmd = command.get('cmd', '')
        
        if cmd == 'IDENTIFY':
            return {'status': 'success', 'data': f'PROMETHEUS|{DEVICE_NAME}|{DEVICE_TYPE}'}
        elif cmd == 'get_info':
            return {'status': 'success', 'data': {'name': DEVICE_NAME, 'type': DEVICE_TYPE, 'time': str(datetime.now())}}
        elif cmd == 'ping':
            return {'status': 'success', 'data': {'ping': 'pong'}}
        else:
            return {'status': 'error', 'message': 'Comando desconhecido'}
            
    def _broadcast_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.running:
            try:
                msg = f"PROMETHEUS_ANNOUNCE|name:{DEVICE_NAME}|type:{DEVICE_TYPE}|port:{CONTROL_PORT}"
                sock.sendto(msg.encode(), ('255.255.255.255', BROADCAST_PORT))
                time.sleep(5)
            except:
                time.sleep(1)

if __name__ == "__main__":
    server = PrometheusServer()
    print("🚀 Servidor Prometheus rodando na porta 5000")
    server.start()
