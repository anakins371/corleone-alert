import json
import os
import requests

API_URL = "https://corleonemarket.com/api/stocks"

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
        fair_price = CONFIG[ticker]["fair_price"]

        desconto = ((fair_price - preco) / fair_price) * 100

        # ====================
        # COMPRA
        # ====================

        if preco <= buy:

            if not ESTADO[ticker]["buy_sent"]:

                mensagem = (
    "━━━━━━━━━━━━━━━━━━\n\n"
    "🟢 OPORTUNIDADE DE COMPRA\n\n"
    f"📌 {ticker}\n\n"
    f"💵 Preço Atual: R$ {preco:.2f}\n"
    f"🎯 Preço Alvo: R$ {buy:.2f}\n\n"
    "⟡ Ativo negociado abaixo da zona de entrada.\n\n"
    "━━━━━━━━━━━━━━━━━━"
                )
                
                enviar_mensagem(mensagem)

                ESTADO[ticker]["buy_sent"] = True
                alterou_estado = True

        else:

            if ESTADO[ticker]["buy_sent"]:
                ESTADO[ticker]["buy_sent"] = False
                alterou_estado = True

        # ====================
        # GRANDE OPORTUNIDADE
        # ====================

        if desconto >= 30:

            if not ESTADO[ticker]["great_sent"]:

                mensagem = (
    "━━━━━━━━━━━━━━━━━━\n\n"
    "🔥 GRANDE OPORTUNIDADE\n\n"
    f"📌 {ticker}\n\n"
    f"💵 Preço Atual: R$ {preco:.2f}\n"
    f"🎯 Preço Justo: R$ {fair_price:.2f}\n"
    f"📉 Desconto: {desconto:.1f}%\n\n"
    "⟡ Ativo sendo negociado muito abaixo do valor estimado.\n\n"
    "━━━━━━━━━━━━━━━━━━"
                )

                enviar_mensagem(mensagem)

                ESTADO[ticker]["great_sent"] = True
                alterou_estado = True

        else:

            if ESTADO[ticker]["great_sent"]:
                ESTADO[ticker]["great_sent"] = False
                alterou_estado = True

        # ====================
        # DESCONTO INSANO
        # ====================

        if desconto >= 50:

            if not ESTADO[ticker]["insane_sent"]:

                mensagem = (
    "━━━━━━━━━━━━━━━━━━\n\n"
    "🚨 DESCONTO INSANO\n\n"
    f"📌 {ticker}\n\n"
    f"💵 Preço Atual: R$ {preco:.2f}\n"
    f"🎯 Preço Justo: R$ {fair_price:.2f}\n"
    f"📉 Desconto: {desconto:.1f}%\n\n"
    "⟡ Possível barganha extrema detectada.\n"
    "⟡ Condição rara de mercado.\n\n"
    "━━━━━━━━━━━━━━━━━━"
                )

                enviar_mensagem(mensagem)

                ESTADO[ticker]["insane_sent"] = True
                alterou_estado = True

        else:

            if ESTADO[ticker]["insane_sent"]:
                ESTADO[ticker]["insane_sent"] = False
                alterou_estado = True

        # ====================
        # OPORTUNIDADE LENDÁRIA
        # ====================

        if desconto >= 70:

            if not ESTADO[ticker]["legendary_sent"]:

                mensagem = (
    "━━━━━━━━━━━━━━━━━━\n\n"
    "💎 OPORTUNIDADE LENDÁRIA\n\n"
    f"📌 {ticker}\n\n"
    f"💵 Preço Atual: R$ {preco:.2f}\n"
    f"🎯 Preço Justo: R$ {fair_price:.2f}\n"
    f"📉 Desconto: {desconto:.1f}%\n\n"
    "⟡ Condição extremamente rara.\n"
    "⟡ Possível ponto de entrada excepcional.\n"
    "⟡ Verifique o ativo imediatamente.\n\n"
    "━━━━━━━━━━━━━━━━━━"
                )

                enviar_mensagem(mensagem)

                ESTADO[ticker]["legendary_sent"] = True
                alterou_estado = True

        else:

            if ESTADO[ticker]["legendary_sent"]:
                ESTADO[ticker]["legendary_sent"] = False
                alterou_estado = True
                
        # ====================
        # VENDA
        # ====================

        if preco >= sell:

            if not ESTADO[ticker]["sell_sent"]:

                mensagem = (
    "━━━━━━━━━━━━━━━━━━\n\n"
    "🔔 CORLEONE ALERT\n\n"
    f"📌 {ticker}\n\n"
    f"💵 Preço Atual: R$ {preco:.2f}\n"
    f"🎯 Preço Alvo: R$ {sell:.2f}\n\n"
    "⟡ Hora de avaliar realização de lucro.\n\n"
    "━━━━━━━━━━━━━━━━━━"
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
