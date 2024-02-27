import requests

# Função para obter o token
def get_token():
    token_url = 'http://localhost:8000/api/token/pair'
    user_data = {
        "username": "admin",
        "password": "admin"
    }
    response = requests.post(token_url, json=user_data)
    if response.ok:
        return response.json()['access']
    else:
        print('Erro ao obter token:', response.text)
        return None

# Função para desativar o superusuário
def deactivate_superuser(username, token):
    endpoint_url = f'http://localhost:8000/api/superuser/deactivate_superuser?username={username}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(endpoint_url, headers=headers)
    if response.ok:
        print('Superusuário desativado com sucesso')
    else:
        print('Erro ao desativar superusuário:', response.text)

# Obtém o token
token = get_token()
if token:
    # Chama a função para desativar o superusuário
    deactivate_superuser('string', token)  # Substitua 'string' pelo username desejado
