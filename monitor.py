
import os
import json
import requests

API_URL = "https://corleonemarket.com/api/stocks"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": texto
        },
        timeout=20
    )

def obter_acoes():
    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    acoes = obter_acoes()

    for acao in acoes:
        ticker = acao["sym"]

        if ticker not in CONFIG:
            continue

        preco = acao["price"]
        alvo = CONFIG[ticker]["sell"]

        if preco >= alvo:

            mensagem = (
                "🔔 CORLEONE ALERT\n\n"
                f"Ação: {ticker}\n"
                f"Preço Atual: R$ {preco:.2f}\n"
                f"Preço Alvo: R$ {alvo:.2f}\n\n"
                "Hora de avaliar uma venda."
            )

            enviar_mensagem(mensagem)

if __name__ == "__main__":
    main()
