import requests


url = 'http://localhost:8000/api/v1/cursos/'
token = '6e72e4c6dc37e4dd7deb93ea7bb208cb5e2f0f59'

headers = {
    "Authorization": f"Token {token}"
}

novo_curso = {
    "titulo": "Django",
    "url": "http://www.django.com.br",
    "ativo": True
}

resultado = requests.post(url=url, headers=headers, data=novo_curso)

# Testando o código de status HTTP
assert resultado.status_code == 201

# Testando se o nome do curso é o mesmo do informado
assert resultado.json()['titulo'] == novo_curso['titulo']
