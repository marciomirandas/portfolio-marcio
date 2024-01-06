import requests


url = 'http://localhost:8000/api/v1/cursos/'
token = '6e72e4c6dc37e4dd7deb93ea7bb208cb5e2f0f59'

headers = {
    "Authorization": f"Token {token}"
}

curso_atualizado = {
    "titulo": "Django3",
    "url": "http://www.django3.com.br",
    "ativo": True
}

id = '2'

resultado = requests.put(url=f'{url}{id}/', headers=headers, data=curso_atualizado)

# Testando o código de status HTTP
assert resultado.status_code == 200


# Testando se o nome do curso é o mesmo do informado
assert resultado.json()['titulo'] == curso_atualizado['titulo']