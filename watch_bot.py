import time
import requests
import random
import json
import discord
from discord.ext import tasks 
from bs4 import BeautifulSoup

required_part = "product-form__inventory inventory"
url = "https://www.citymoments.com/products/seiko-mens-casual-analog-metal-watch-snk063j5?_pos=2&_sid=4782a3bd4&_ss=r"


def run_discord_bot():

    intents = discord.Intents.all()
    client = discord.Client(intents = intents)
    with open('config.json') as config_file:
        token = json.load(config_file)['token']

    @client.event
    async def on_ready():
        print(f"Connected to Discord as {client.user}")
        if not speak_on_channel.is_running():
              speak_on_channel.start()
                
    @client.event
    async def on_message(message):
        # Get the Discord channel you want to send the message to
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        if(message.author.id == client.user.id):
            return
    
        print(f"{username} said : {user_message} ({channel})")
        print(message)
        
        ### get channel ###
        channel = discord.utils.get(client.get_all_channels(), name="test-test")
                
        if user_message == '!check_dispo':
            ### chargement du texte ###
            response = requests.get(url)
            html_content = response.text

            ### extraction du texte ###
            soup = BeautifulSoup(html_content, "html.parser")
            product_list = soup.find("span", class_=required_part)
            
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
                
        response = requests.get(url)
        html_content = response.text

        ### extraction du texte ###
        soup = BeautifulSoup(html_content, "html.parser")
        product_list = soup.find("span", class_=required_part)
        
        channel = discord.utils.get(client.get_all_channels(), name="test-test")
        
        if product_list.text == "Sold out":
            output_message = f"Product is sold out rn."
            await channel.send(output_message)

        else:
            # Send the message to the channel
            output_message = f"{name} is now in stock!"
            await channel.send(output_message)
        
        next_time = random.randrange(2700, 4500)
        speak_on_channel.change_interval(minutes=next_time)
    
    client.run(token)
                
                




