import discord
import random
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

prize = None
duration = None
entries = []

async def end_raffle(message):
    global entries
    winner = random.choice(entries)
    await message.channel.send(f'The winner of the {prize} raffle is: {winner.mention}! Congratulations!')
    entries = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global prize, duration, entries
    if message.content.startswith('!start raffle'):
        await message.channel.send('What is the prize for the raffle?')
        prize_response = await client.wait_for('message', check=lambda response: response.author == message.author)
        prize = prize_response.content
        await message.channel.send('For how long will the raffle run?')
        duration_response = await client.wait_for('message', check=lambda response: response.author == message.author)
        try:
            duration = int(duration_response.content)
        except ValueError:
            await message.channel.send('Invalid duration. Please enter a valid number of seconds.')
            return
        entries = []
        raffle_message = await message.channel.send(f'🎉 A raffle for a {prize} has started! Click the party emoji to enter. 🎉')
        await raffle_message.add_reaction('🎉')
        await asyncio.sleep(duration)
        await end_raffle(message)
    elif message.content.startswith('!reroll'):
        if entries:
            await end_raffle(message)
        else:
            await message.channel.send('No raffle is currently running.')

@client.event
async def on_reaction_add(reaction, user):
    global entries
    if str(reaction.emoji) == '🎉' and user != client.user:
        entries.append(user)

client.run(os.environ.get('TOKEN'))
