import snscrape.modules.twitter as sntwitter
import requests
import time

# Lista de cuentas que quieres trackear
users = ['adrianaia_', 'otracuenta', 'mascuentas']

# Webhook de Make (el tuyo aquí)
make_webhook_url = 'https://hook.us1.make.com/TU-WEBHOOK-AQUI'

# Diccionario para guardar los últimos tweets enviados
last_tweets = {}

def scrape_and_send():
    for user in users:
        print(f"Buscando tweets de @{user}...")
        tweets = list(sntwitter.TwitterUserScraper(user).get_items())
        if tweets:
            latest_tweet = tweets[0]
            tweet_id = latest_tweet.id
            tweet_url = f'https://x.com/{user}/status/{tweet_id}'

            # Si es un tweet nuevo, lo enviamos
            if user not in last_tweets or last_tweets[user] != tweet_id:
                last_tweets[user] = tweet_id

                # Enviar a Make
                payload = {'tweet_url': tweet_url}
                response = requests.post(make_webhook_url, json=payload)

                if response.status_code == 200:
                    print(f'✅ Enviado a Make: {tweet_url}')
                else:
                    print(f'❌ Error enviando {tweet_url}: {response.status_code}')

while True:
    scrape_and_send()
    print("Esperando 5 minutos antes de volver a comprobar...")
    time.sleep(300)
