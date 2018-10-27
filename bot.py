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
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


@bot.event
async def on_ready():
    print("Ready when you are!")
    print("I am running on " + bot.user.name)
    print("with ID " + bot.user.id)


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("Pong!")


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    await bot.say("The username is: {}".format(user.name))


@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)


@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()


@bot.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()


@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@bot.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()


@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()


@bot.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await bot.say(f'Total {len(queues[server.id])} video(s) queued.')


bot.run(TOKEN)
