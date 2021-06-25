import discord
import os
import requests
import json
import random
from keep_alive import keep_alive


client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def get_dog():
  response = requests.get("https://dog.ceo/api/breeds/image/random")
  json_data = json.loads(response.text)
  dogurl = json_data['message']
  return dogurl

def formatResponse(response, computer, result): #formats the response so that the results are aligned and look nice
    return "\n" + "You".rjust(10) + "|EncourageBot" +"\n" + f"{response}".rjust(10) + f"|{computer}"  +"\n"+ f"You {result}!".rjust(15)


def rockPaperScissors(response):
  itemlist = ['rock', 'paper','scissors']
  winsAgainst = {'rock': 'scissors', 'paper':'rock', 'scissors':'paper'}
  uniDict = {'rock':'\U0001FAA8', 'paper':'\U0001F4F0', 'scissors':'\U00002702'} # unicode emojis for r/p/s
  computer = computerinput = itemlist[random.randint(0,2)] # get random response from computer
  # logic for the matchups
  if computer == response.lower():
    result = 'tied'
  elif computer == winsAgainst[response.lower()]:
    result = "won" # computer lost
  else:
    result = "lost" # computer won

  return formatResponse(uniDict[response], uniDict[computer], result)
  


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

          elif message.content.startswith("$rps"):
            response = message.content.split(" ")[1] # get the user input
            # print(response)
            await message.channel.send(rockPaperScissors(response)) # send the message
          
          elif message.content.startswith("$dog"):
            await message.channel.send(get_dog())
          


token = os.environ['TOKEN']

keep_alive()
client.run(os.environ['TOKEN'])