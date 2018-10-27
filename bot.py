'''
LonginusBot by kavach

A Discord Bot
'''
import asyncio


from bot_token import TOKEN

import discord
from discord.ext import commands

import youtube_dl

bot = commands.Bot(command_prefix='#')
players = {}
queues = {}


def check_queue(id):
    """
    Check for queue items and play the next song in queue.
    """
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


@bot.event
async def on_ready():
    """
    Print certain state details once the bot is started.
    """
    print("Ready when you are!")
    print("I am running on " + bot.user.name)
    print("with ID " + bot.user.id)


@bot.command(pass_context=True)
async def ping(ctx):
    """
    Ping command

    Returns Pong! on the discord message board.
    """
    await bot.say("Pong!")


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    """
    Info command

    Prints info of any user which is passed as an argument with this command.
    """
    await bot.say("The username is: {}".format(user.name))


@bot.command(pass_context=True)
async def join(ctx):
    """
    Join command

    This command makes the bot join the voice channel where the user is in.
    """
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)


@bot.command(pass_context=True)
async def leave(ctx):
    """
    Leave command

    This commands makes the bot leave the voice channel it is in.
    """
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()


@bot.command(pass_context=True)
async def play(ctx, url):
    """
    Play command

    Plays audio content of youtube videos on a Discord voice channel.
    """
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()


@bot.command(pass_context=True)
async def pause(ctx):
    """
    Pause command

    Pauses the player.
    """
    id = ctx.message.server.id
    players[id].pause()


@bot.command(pass_context=True)
async def stop(ctx):
    """
    Stop command

    Stops the player and clears queue.
    """
    id = ctx.message.server.id
    players[id].stop()


@bot.command(pass_context=True)
async def resume(ctx):
    """
    Resume command

    Resumes a paused player.
    """
    id = ctx.message.server.id
    players[id].resume()


@bot.command(pass_context=True)
async def queue(ctx, url):
    """
    Queue command

    Queues videos on the player.
    """
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await bot.say(f'Total {len(queues[server.id])} video(s) queued.')

# Runs the bot with the discord bot token: TOKEN, which uniquely identifies your bot.
bot.run(TOKEN)
