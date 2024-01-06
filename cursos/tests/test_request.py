import requests

url = 'http://localhost:8000/api/v1/cursos'
token = '6e72e4c6dc37e4dd7deb93ea7bb208cb5e2f0f59'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

resultado = requests.get(url, headers=headers)

if resultado.status_code == 200:
    resultado = resultado.json()
else:
    resultado = f'Erro {resultado.status_code}: {resultado.text}'

print(resultado)