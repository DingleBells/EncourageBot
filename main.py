import discord
import os
import requests
import json
from keep_alive import keep_alive


client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$"):
          if message.channel.name != "encourage-bot-testing":
            await message.channel.send("Please only use this bot in <#857377863941357568>")
          
          elif message.content.startswith('$hello'):
              await message.channel.send('Hello!')
          
          elif message.content.startswith('$inspire'):
            await message.channel.send(get_quote())

token = os.environ['TOKEN']

keep_alive()
client.run(os.environ['TOKEN'])