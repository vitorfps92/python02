from flask import Flask, jsonify, send_file
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

# Criar o app do Flask
app = Flask(__name__)







# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)