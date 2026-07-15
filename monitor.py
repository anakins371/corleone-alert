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


def main():

    try:
        resposta = requests.get(API_URL, timeout=15)
        resposta.raise_for_status()
        acoes = resposta.json()

    except Exception as e:
        print(f"Erro ao acessar API: {e}")
        return

    alterou_estado = False

    for acao in acoes:

        ticker = acao["sym"]

        if ticker not in CONFIG:
            continue

        preco = acao["price"]

        day_high = acao["dayHigh"]
        day_low = acao["dayLow"]
        historical_high = acao["high"]
        historical_low = acao["low"]

        buy = CONFIG[ticker]["buy"]
        sell = CONFIG[ticker]["sell"]
        fair_price = CONFIG[ticker]["fair_price"]

        desconto = ((fair_price - preco) / fair_price) * 100

        # ====================
        # COMPRA
        # ====================

        if preco <= buy:

            mensagem = (
                "━━━━━━━━━━━━━━━━━━\n\n"
                "🟢 OPORTUNIDADE DE COMPRA\n\n"
                f"📌 {ticker}\n\n"
                f"💵 Preço Atual: R$ {preco:.2f}\n"
                f"🎯 Preço Alvo: R$ {buy:.2f}\n\n"
                f"📉 Desconto: {desconto:.1f}%\n\n"
                f"📈 Máxima do Dia: R$ {day_high:.2f}\n"
                f"📉 Mínima do Dia: R$ {day_low:.2f}\n"
                "⟡ Ativo negociado abaixo da zona de entrada.\n\n"
                "━━━━━━━━━━━━━━━━━━"
            )

            enviar_mensagem(mensagem)

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
                    f"📈 Máxima do Dia: R$ {day_high:.2f}\n"
                    f"📉 Mínima do Dia: R$ {day_low:.2f}\n"
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
                    f"📈 Máxima do Dia: R$ {day_high:.2f}\n"
                    f"📉 Mínima do Dia: R$ {day_low:.2f}\n"
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
                    f"📈 Máxima do Dia: R$ {day_high:.2f}\n"
                    f"📉 Mínima do Dia: R$ {day_low:.2f}\n\n"
                    f"🏆 Máxima Histórica: R$ {historical_high:.2f}\n"
                    f"🔻 Mínima Histórica: R$ {historical_low:.2f}\n\n"
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

    if alterou_estado:
        salvar_estado()


if __name__ == "__main__":
    main()


def gerar_scanner(acoes):

    scanner = []

    for acao in acoes:

        ticker = acao["sym"]

        if ticker not in CONFIG:
            continue

        preco = acao["price"]
        fair_price = CONFIG[ticker]["fair_price"]

        desconto = max(
            0,
            ((fair_price - preco) / fair_price) * 100
        )

        scanner.append({
            "ticker": ticker,
            "preco": preco,
            "desconto": desconto
        })

    scanner.sort(
        key=lambda x: x["desconto"],
        reverse=True
    )

    top3 = scanner[:3]

    mensagem = (
        "\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🏆 SCANNER DE MERCADO\n\n"
    )

    medalhas = ["🥇", "🥈", "🥉"]

    for i, ativo in enumerate(top3):

        mensagem += (
            f"{medalhas[i]} {ativo['ticker']}\n"
            f"💵 R$ {ativo['preco']:.2f}\n"
            f"📉 {ativo['desconto']:.1f}%\n\n"
        )

    mensagem += "━━━━━━━━━━━━━━━━━━"

    return mensagem
