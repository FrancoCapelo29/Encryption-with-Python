from flask import Flask, render_template, request, session
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para las sesiones

# Genera una clave y la devuelve como string
def generar_clave():
    return Fernet.generate_key()

# Encripta el mensaje
def encriptar_mensaje(mensaje, clave):
    fernet = Fernet(clave)
    mensaje_encriptado = fernet.encrypt(mensaje.encode())
    return mensaje_encriptado

# Desencripta el mensaje
def desencriptar_mensaje(mensaje_encriptado, clave):
    fernet = Fernet(clave)
    mensaje_desencriptado = fernet.decrypt(mensaje_encriptado).decode()
    return mensaje_desencriptado

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encriptar', methods=['POST'])
def encriptar():
    mensaje = request.form['mensaje']
    clave = generar_clave()
    mensaje_encriptado = encriptar_mensaje(mensaje, clave)
    session['mensaje_encriptado'] = mensaje_encriptado
    return render_template('index.html', mensaje_encriptado=mensaje_encriptado.decode(), clave=clave.decode())

@app.route('/desencriptar', methods=['POST'])
def desencriptar():
    clave = request.form['clave'].encode()
    mensaje_encriptado = session.get('mensaje_encriptado')
    if not mensaje_encriptado:
        return render_template('desencriptar.html', error="No hay mensaje encriptado en la sesión.")
    try:
        mensaje_desencriptado = desencriptar_mensaje(mensaje_encriptado, clave)
        return render_template('desencriptar.html', mensaje_desencriptado=mensaje_desencriptado)
    except Exception as e:
        return render_template('desencriptar.html', error="Clave incorrecta o mensaje dañado")

@app.route('/desencriptar_form')
def desencriptar_form():
    return render_template('desencriptar.html')

if __name__ == '__main__':
    app.run(debug=True)
