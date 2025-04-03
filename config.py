# Configurações do nosso sistema

# Configurações dos caminhos dos arquivos e do database
caminho_banco = 'consumo_alcool.db'
caminho_drinks_csv = 'drinks.csv'

# Configurações do Flask
server_config = {
    "DEBUG": True,
    "PORT": 5000,
    "HOST": "0.0.0.0" # pode ser localhost se desejar
}
# No Debug podemos utilizar as seguintes configs:
# Debug como True or False para ligar ou desligar o modo, ou como DEV ou PROD
# DEV é a mesma coisa que Debug True, ou seja, ambiente de desenvolvimento
# PROD é a mesma coisa que False, ou seja, debug desligado e ambiente de produção.

# Outras configurações gerais
semente_aleatoria = 42