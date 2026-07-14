
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

# ALERTA DE COMPRA
if "buy" in CONFIG[ticker]:
    alvo_compra = CONFIG[ticker]["buy"]

    if preco <= alvo_compra:
        mensagem = (
            "🟢 OPORTUNIDADE DE COMPRA\n\n"
            f"Ação: {ticker}\n"
            f"Preço Atual: R$ {preco:.2f}\n"
            f"Preço Alvo: R$ {alvo_compra:.2f}\n\n"
            "Ação entrou na zona de compra."
        )

        enviar_mensagem(mensagem)

# ALERTA DE VENDA
if "sell" in CONFIG[ticker]:
    alvo_venda = CONFIG[ticker]["sell"]

    if preco >= alvo_venda:
        mensagem = (
            "🔔 CORLEONE ALERT\n\n"
            f"Ação: {ticker}\n"
            f"Preço Atual: R$ {preco:.2f}\n"
            f"Preço Alvo: R$ {alvo_venda:.2f}\n\n"
            "Hora de avaliar uma venda."
        )

        enviar_mensagem(mensagem)
