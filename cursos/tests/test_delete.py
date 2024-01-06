import requests


url = 'http://localhost:8000/api/v1/cursos/'
token = '6e72e4c6dc37e4dd7deb93ea7bb208cb5e2f0f59'

headers = {
    "Authorization": f"Token {token}"
}
id = '1'


resultado = requests.delete(url=f'{url}{id}/', headers=headers)

# Testando o código de status HTTP
assert resultado.status_code == 204


# Testando se o tamanho do conteúdo retornado é 0
assert len(resultado.text) == 0