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


def formatResponse(
    response, computer, result
):  #formats the response so that the results are aligned and look nice
    return "\n" + "You".rjust(
        10) + "|EncourageBot" + "\n" + f"{response}".rjust(
            10) + f"|{computer}" + "\n" + f"You {result}!".rjust(15)

def clearRPSData(user):
    with open('rps_stats.txt') as fp:
        stats = json.load(fp)
        stringuser = str(user)
        if stringuser in stats:
            del stats[stringuser]
    # print("stats", stats)
    if stats == {}:
      stats = {'a':1}
    with open('rps_stats.txt', 'w') as outfile:
        json.dump(stats, outfile)
    


def retriveData(author):
    stringauthor = str(author)
    with open('rps_stats.txt') as fp:
        stats = json.load(fp)
        if stringauthor in stats:
            wins, losses, ties = map(int, stats[stringauthor])
            return '{}, your stats are: {} wins, {} losses, {} ties, for a win percentage of {}%.'.format(
                author.mention, wins, losses, ties,
                (2 * wins + ties) * 100 / (2 * (wins + losses + ties)))

        else:
            return '{}, you have not played any matches yet!'.format(
                author.mention)

def rockPaperScissors(user, response):
    itemlist = ['rock', 'paper', 'scissors']
    winsAgainst = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    uniDict = {
        'rock': '\U0001FAA8',
        'paper': '\U0001F4F0',
        'scissors': '\U00002702'
    }  # unicode emojis for r/p/s
    computer = computerinput = itemlist[random.randint(
        0, 2)]  # get random response from computer

    # logic for the matchups
    if computer == response.lower():
        result = 'tied'
    elif computer == winsAgainst[response.lower()]:
        result = "won"  # computer lost
    else:
        result = "lost"  # computer won

    with open('rps_stats.txt') as fp:
        stats = json.load(fp)


    # storing the data from rps match
    # print(f"Storing data: {user}:{result}")
    stringname = str(user)
    if stringname in stats:
        (wins, losses, ties) = stats[stringname]
        if result == "won":
            wins += 1
        elif result == "lost":
            losses += 1
        elif result == "tied":
            ties += 1

    else:
        # print('else')
        (wins, losses, ties) = (0, 0, 0)
        if result == "won":
            wins += 1
        elif result == "lost":
            losses += 1
        elif result == "tied":
            ties += 1

    stats[str(user)] = (wins, losses, ties)
    with open('rps_stats.txt', 'w') as outfile:
        # print(f"Wrote data: {user}:{result}")
        json.dump(stats, outfile)

    return formatResponse(uniDict[response], uniDict[computer], result)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$"):
        if message.channel.name != "stuffbot":
            await message.channel.send(
                "Please only use this bot in <#857377863941357568>")

        elif message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        elif message.content.startswith('$inspire'):
            await message.channel.send(get_quote())

        elif message.content.startswith("$rps"):
            if message.content.startswith("$rps stats"):
                await message.channel.send(retriveData(message.author))
            elif message.content.startswith("$rps clear"):
                clearRPSData(message.author)
                await message.channel.send("Cleared your Rock Paper Scissors data!")
            else:
                response = message.content.split(" ")[1]  # get the user input
                # print(response)
                await message.channel.send(
                    rockPaperScissors(message.author,response
                                      ))  # send the message

        elif message.content.startswith("$dog"):
            await message.channel.send(get_dog())

        elif message.content.startswith("$help"):
            commands = """
            
            $hello: returns Hello!
            $inspire: returns random inspirational quote
            $rps rock/paper/scissors: Rock paper scissors 
            $rps stats: returns your rock paper scissors stats
            $rps clear: clears your rock paper scissors data
            $dog: returns a random dog photo
            """
            await message.channel.send(commands)


token = os.environ['TOKEN']

keep_alive()
client.run(token)
