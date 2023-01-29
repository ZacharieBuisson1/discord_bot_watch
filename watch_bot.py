import time
import requests
import random
from bs4 import BeautifulSoup

required_part = "product-form__inventory inventory"
url = "https://www.citymoments.com/products/seiko-mens-casual-analog-metal-watch-snk063j5?_pos=2&_sid=4782a3bd4&_ss=r"

import discord

def run_discord_bot():

    intents = discord.Intents.default()
    intents.messages = True
    client = discord.Client(intents = intents)
    
    token = "MTA2OTM0NjE1MTg5NzI0Mzc2OQ.GyE8Y1.E6Aum6US9YgnOkmYCWCJBpw0vhKD3lcvolyck4"

    @client.event
    async def on_ready():
        print(f"Connected to Discord as {client.user}")

    @client.event
    async def on_message(message):
        # Get the Discord channel you want to send the message to
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f"{username} said : {user_message} ({channel})")
        print(message)
        
        if user_message == '!check_dispo':
            ### chargement du texte ###
            response = requests.get(url)
            html_content = response.text

            ### extraction du texte ###
            soup = BeautifulSoup(html_content, "html.parser")
            product_list = soup.find("span", class_=required_part)
            
            if product_list.text == "Sold out":
                message = f"Product is sold out rn."
                await message.channel.send()

            else:
                # Send the message to the channel
                message = f"{name} is now in stock!"
                await message.channel.send()
                
    client.run(token)
                
                




