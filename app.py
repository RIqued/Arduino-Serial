from flask import Flask, render_template, request
import serial
import time

app = Flask(__name__)

# Configuração da porta serial para o Arduino
ser = serial.Serial('COM5', 9600, timeout=1)  # Substitua 'COM5' pela porta correta
time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')  # Isso vai renderizar o arquivo index.html

@app.route('/controlar', methods=['POST'])
def controlar():
    comando = request.form.get('comando')
    if comando:
        ser.write(f'{comando}\n'.encode('utf-8'))  # Envia o comando para o Arduino
        return f'Comando {comando} enviado ao Arduino!', 200
    return 'Comando inválido', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
