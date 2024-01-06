import requests


url = 'http://localhost:8000/api/v1/cursos'
token = '6e72e4c6dc37e4dd7deb93ea7bb208cb5e2f0f59'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

resultado = requests.get(url, headers=headers)


# Testando se o endpoint está correto
assert resultado.status_code == 200

# Testando a quantidade de registro
assert resultado.json()['count'] == 3

# Testando o título do primeiro curso está correto
assert resultado.json()['results'][0]['titulo'] == 'Java'