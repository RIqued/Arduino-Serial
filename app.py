from flask import Flask, render_template, request, jsonify
import serial
import time

app = Flask(__name__)

# Configuração da porta serial (aberta uma vez)
try:
    ser = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)  # Espera a inicialização da porta serial
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")

# Função para enviar comando para o Arduino
def enviar_comando(comando):
    ser.write(f'{comando}\n'.encode('utf-8'))
    time.sleep(1)
    resposta = None
    while True:
        if ser.in_waiting > 0:
            resposta = ser.readline().decode('utf-8').rstrip()
            break
    return resposta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controlar', methods=['POST'])
def controlar():
    comando = request.form.get('comando')
    if comando:
        resposta = enviar_comando(comando)
        return jsonify({'status': resposta})
    return jsonify({'status': 'Comando não enviado'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
