import discord
from discord.ext import tasks
from pycoingecko import CoinGeckoAPI
from datetime import datetime



gc = CoinGeckoAPI()
# perms: 2147616768
client = discord.Client()
global CURRENT_PRICE,CURRENT_VALUE


def api():
    api_return = gc.get_price(ids='shiba-inu', vs_currencies='usd')
    return format(float(api_return["shiba-inu"]["usd"]), '.8f'), float(api_return["shiba-inu"]["usd"])

def returnMessage():
    return f"@everyone current Shiba Inu price is `${api()[0]}`"

@client.event
async def on_message(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if message.author == client.user:
        return
    if message.content.startswith('$shib'):
        ret_message = returnMessage()
        print(f'[{current_time}] User requested price.\n\t   Returned: {ret_message}')
        await message.channel.send(ret_message)

@tasks.loop(minutes=5)
async def timerMessage():
    global CURRENT_PRICE, CURRENT_VALUE
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    temp_price, temp_value = api()
    print(f"[{current_time}] Current price is: {temp_price}")
    if CURRENT_VALUE * 1.05 < temp_value:
        CURRENT_PRICE = temp_price
        CURRENT_VALUE = temp_value
        message = f"@everyone PRICE INCREASE! Current price of Shiba Inu: ${temp_price}"
        channel = client.get_channel(877544339159535618)
        await channel.send(message)
        print(f"[{current_time}] Chat updated with message:\n{message}")

    elif CURRENT_VALUE * .95 > temp_value:
        CURRENT_PRICE = temp_price
        CURRENT_VALUE = temp_value
        message = f"@everyone PRICE DECREASE. Current price of Shib: ${temp_price}"
        channel = client.get_channel(877544339159535618)
        await channel.send(message)
        print(f"[{current_time}] Chat updated with message:\n{message}")


@client.event
async def on_ready():
    global CURRENT_PRICE, CURRENT_VALUE
    CURRENT_PRICE, CURRENT_VALUE = api()
    if not timerMessage.is_running():
        timerMessage.start()

client.run("")
