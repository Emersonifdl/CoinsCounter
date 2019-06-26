from datetime import datetime
from decimal import Decimal

import requests

# defining the api-endpoint
API_ENDPOINT = "http://127.0.0.1:8000/api/transacoes/"

# your API key here
API_KEY = "1bfb5cbc25e4450423a10e247a04eb37"

# your source code here
valor = Decimal(0.5)
data_hora = datetime.now()

# data to be sent to api
data = {
    'cofre': API_KEY,
    'data_hora': data_hora,
    'valor': valor
}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)

# extracting response text
data = r.json()
print("JSON is:%s" % data)