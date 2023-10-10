import pandas as pd
import requests
import json
import openai

# Lê os IDs de usuário da planilha
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()

# URL da API Santander
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# Função para obter dados do usuário da API Santander
def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

# Obtém os dados dos usuários
users = [user for id in user_ids if (user := get_user(id)) is not None]

# Filtra os usuários com saldo positivo para investimento
filtered_users = [user for user in users if user.get('account').get('balance', 0) > 0.0]

# Configura a chave da API da OpenAI (substitua com sua própria chave)
openai_api_key = 'Minha chave API'
openai.api_key = openai_api_key

# Função para gerar mensagens personalizadas da OpenAI
def generate_ai_news(user, instruction):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Crie uma mensagem para {user['name']} sobre a importância de investir 20% do capital. (máximo de 100 caracteres)",
        max_tokens=50,
        temperature=0.7
    )
    return completion.choices[0].text.strip()

# Envia mensagens personalizadas para os clientes com potencial de investimento
for user in filtered_users:
    news = generate_ai_news(user, "Por favor, invista seu dinheiro com sabedoria para um futuro seguro.")
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })
    print(f"Mensagem gerada para {user['name']}: {news}")

# Agora você pode atualizar os dados na API Santander com as mensagens geradas
# Implemente essa parte conforme a documentação da API Santander

# Salva os dados atualizados em um arquivo JSON
with open('users_data.json', 'w') as outfile:
    json.dump(users, outfile, indent=2)
