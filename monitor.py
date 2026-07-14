import json
import os
import requests

API_URL = "https://corleonemarket.vercel.app/api/stocks"

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

with open("estado.json", "r", encoding="utf-8") as f:
    ESTADO = json.load(f)


def salvar_estado():
    with open("estado.json", "w", encoding="utf-8") as f:
        json.dump(ESTADO, f, indent=2)


def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": texto
        }
    )


def main():
    resposta = requests.get(API_URL)
    acoes = resposta.json()

    alterou_estado = False

    for acao in acoes:
        ticker = acao["sym"]

        if ticker not in CONFIG:
            continue

        preco = acao["price"]

        buy = CONFIG[ticker]["buy"]
        sell = CONFIG[ticker]["sell"]

        # ===== COMPRA =====

        if preco <= buy:

            if not ESTADO[ticker]["buy_sent"]:

                mensagem = (
                    "🟢 OPORTUNIDADE DE COMPRA\n\n"
                    f"Ação: {ticker}\n"
                    f"Preço Atual: R$ {preco:.2f}\n"
                    f"Preço Alvo: R$ {buy:.2f}"
                )

                enviar_mensagem(mensagem)

                ESTADO[ticker]["buy_sent"] = True
                alterou_estado = True

        else:
            if ESTADO[ticker]["buy_sent"]:
                ESTADO[ticker]["buy_sent"] = False
                alterou_estado = True

        # ===== VENDA =====

        if preco >= sell:

            if not ESTADO[ticker]["sell_sent"]:

                mensagem = (
                    "🔔 CORLEONE ALERT\n\n"
                    f"Ação: {ticker}\n"
                    f"Preço Atual: R$ {preco:.2f}\n"
                    f"Preço Alvo: R$ {sell:.2f}\n\n"
                    "Hora de avaliar uma venda."
                )

                enviar_mensagem(mensagem)

                ESTADO[ticker]["sell_sent"] = True
                alterou_estado = True

        else:
            if ESTADO[ticker]["sell_sent"]:
                ESTADO[ticker]["sell_sent"] = False
                alterou_estado = True

    if alterou_estado:
        salvar_estado()


if __name__ == "__main__":
    main()
