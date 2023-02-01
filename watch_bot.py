import time
import requests
import random
import json
import discord
from discord.ext import tasks 
from bs4 import BeautifulSoup

required_part = "product-form__inventory inventory"
url = "https://www.citymoments.com/products/seiko-mens-casual-analog-metal-watch-snk063j5?_pos=2&_sid=4782a3bd4&_ss=r"
# url = "https://www.citymoments.com/collections/watches/products/seiko-snk809k2-automatic-analog-nylon-black-mens-watch"

name = "SEIKO_SNK063J5"

def run_discord_bot():

    ### Give more rights to the bot ###
    intents = discord.Intents.all()
    client = discord.Client(intents = intents)

    ### Loading Token ###
    with open('config.json') as config_file:
        token = json.load(config_file)['token']

    ### Print on a terminal that it's ok ###
    @client.event
    async def on_ready():
        print(f"Connected to Discord as {client.user}")
        if not speak_on_channel.is_running():
            speak_on_channel.start()

    @client.event
    async def on_message(message):
        # Debug part 
        # Get the Discord channel = str(message.channel)
        # username = str(message.author)
        # print(f"{username} said : {user_message} ({channel})")
        # print(message)

        # Get the Discord channel you want to send the message to
        user_message = str(message.content)

        ### avoid bot considering it own messages as users' ###
        if (message.author.id == client.user.id):
            return

        ### get channel ###
        channel = discord.utils.get(client.get_all_channels(), name="test-test")
                
        if user_message == '!dispo':
            print("hello")

            ### chargement du texte ###
            response = requests.get(url)
            html_content = response.text

            ### extraction du texte ###
            soup = BeautifulSoup(html_content, "html.parser")
            # product_list = soup.find("span", class_=required_part)
            product_list = soup.select('span[class*="product-form__inventory inventory"]')[0]

            print(product_list)
            
            if product_list.text == "Sold out":
                output_message = f"Product is sold out rn."
                await message.channel.send(output_message)

            else:
                # Send the message to the channel
                output_message = f"{name} is now in stock!"
                await message.channel.send(output_message)

    @tasks.loop(seconds=3600)
    async def speak_on_channel():

        ### chargement du texte ###
        response = requests.get(url)
        html_content = response.text

        ### Comme il s'agit d'une requête réguilière, permet le monitoring dans l'interface de déploiement du modèle ###
        print(response.status_code)

        ### extraction du texte ###
        soup = BeautifulSoup(html_content, "html.parser")
        product_list = soup.select('span[class*="product-form__inventory inventory"]')[0]
        
        ### récupère l'ID du channel dans lequel on souhaite publier ###
        channel = discord.utils.get(client.get_all_channels(), name="test-test")
        
        if product_list.text == "Sold out":
            output_message = f"Product is sold out rn."
            await channel.send(output_message)

        else:
            # Send the message to the channel
            output_message = f"{name} is now in stock!"
            await channel.send(output_message)
            await channel.send("@everyone")

        next_time = random.randrange(2700, 4500)
        speak_on_channel.change_interval(seconds=next_time)
    
    client.run(token)
                
