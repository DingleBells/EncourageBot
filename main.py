import discord
import os
import requests
import json
import random
import webscraper
import getMatchResults
from mlbstandings import returnstandings as mlb
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
):  # formats the response so that the results are aligned and look nice
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
        stats = {'a': 1}
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
    computer = itemlist[random.randint(
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

def testEmbed():
    embed = discord.Embed(
        title="Title",
        description='This is a description that is very very very very very very very very long',
        color=discord.Colour.blue()
    )
    embed.set_footer(text='This is a footer')
    embed.set_image(url='https://images.blz-contentstack.com/v3/assets/blt321317473c90505c/blt582a5af067ad863f/5ce855808339428f06fdb327/logo.svg?auto=webp')
    embed.set_thumbnail(url='https://images.blz-contentstack.com/v3/assets/blt321317473c90505c/blt582a5af067ad863f/5ce855808339428f06fdb327/logo.svg?auto=webp')
    embed.set_author(name='Author Name', icon_url='https://images.blz-contentstack.com/v3/assets/blt321317473c90505c/blt582a5af067ad863f/5ce855808339428f06fdb327/logo.svg?auto=webp')
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    return embed

def owlSchedule(response):
    west, east = webscraper.getStandings(int(response))
    tourneyDict = {0:'```2021 Regular Season Standings```',
                   1:"```May Melee Qualifier Standings```",
                   2:'```June Joust: Qualifier Standings```',
                   3:'```Summer Showdown: Qualifier Standings```',
                   4:'```Countdown Cup: Qualifier Standings```'}

    west = "```"+str(west)+"```"
    east = "```"+str(east)+"```"

    return west, east, tourneyDict[int(response)]


def helpCommand():
    commands = discord.Embed(
        title="StuffBot Commands",
        description='List of StuffBot Commands',
        color=discord.Colour.gold()
    )
    commands.add_field(name='$dog', value='Returns a random dog photo')
    commands.add_field(name='$hello', value='Returns Hello!')
    commands.add_field(name='$inspire', value='Returns a random inspirational quote')
    commands.add_field(name='$rps clear', value='Clears your rock paper scissors data')
    commands.add_field(name='$rps rock/paper/scissors', value='Play rock paper scissors with StuffBot!')
    commands.add_field(name='$rps stats', value='Returns your rock paper scissors data')
    commands.add_field(name='$owl standings {number}', value='''Returns the current Overwatch League standings. Use 0 for
     the Reg. Season, 1 for May Melee, 2 for June Joust, 3 for Summer Showdown, and 5 for Countdown Cup''')
    return commands


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

        elif message.content.startswith("$embed"):
            await message.channel.send(embed=testEmbed())

        elif message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        elif message.content.startswith('$inspire'):
            await message.channel.send(get_quote())

        elif message.content.startswith("$owl scores"):
            await message.channel.send(embed=getMatchResults.getScoreEmbed(getMatchResults.getScores()))

        elif message.content.startswith("$owl standings"):
            response = message.content.split()[2]
            west, east, tourney = owlSchedule(response)
            print(len(west), len(east))
            await message.channel.send(tourney)
            await message.channel.send(west)
            await message.channel.send(east)

        elif message.content.startswith("$mlb standings"):
            restofmessage = message.content.split('$mlb standings ')[1].split()
            [league, division] = restofmessage
            if division.lower() not in ['east', 'central', 'west']:
                await message.channel.send('That is not an official MLB Division!')
            elif league.lower() == 'al':
                await message.channel.send(f"```AL {division.title()} Standings:```")
                await message.channel.send(mlb(0, division.lower()))
            elif league.lower() == 'nl':
                await message.channel.send(f"```NL {division.title()} Standings:```")
                await message.channel.send(mlb(1,division.lower()))
            else:
                await message.channel.send("That is not an official MLB League!")

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
                    rockPaperScissors(message.author, response
                                      ))  # send the message

        elif message.content.startswith("$dog"):
            await message.channel.send(get_dog())


        elif message.content.startswith("$help"):
            await message.channel.send(embed=helpCommand())

token = os.environ['TOKEN']

keep_alive()
client.run(token)
