import discord
import os

client = discord.Client()

@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
client.run('ODU3Mzc3MzE4Mzc2MDQ2NjAz.YNOs2g.PZ_eRHenWDv91MXIcfOe8zsb-cU')