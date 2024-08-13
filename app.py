import socket
import json
from flask import Flask, jsonify, render_template
import threading

app = Flask(__name__)

# Store the received data globally to be accessed by the web page
received_data = {}

class SocketClient:
    def __init__(self, host='192.168.4.33', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Failed to connect to the server. Is the server running?")
            return False
        return True

    def receive_data(self):
        global received_data
        try:
            while True:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                parsed_data = json.loads(data)
                received_data = parsed_data
                print("Data received:", received_data)  # Debugging
        except ConnectionResetError:
            print("Connection lost.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.client_socket.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    global received_data
    return jsonify(received_data)

def start_socket_client():
    client = SocketClient(host='192.168.4.33', port=12345)
    if client.connect():
        client.receive_data()

if __name__ == '__main__':
    # Start the socket client in a separate thread
    socket_thread = threading.Thread(target=start_socket_client)
    socket_thread.daemon = True
    socket_thread.start()
    
    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000, debug=True)
