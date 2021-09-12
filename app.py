import os
from random import choice

import discord
from discord.ext import commands, tasks

from admin import *
from music import *


class ZeusBot:
    bot = commands.Bot(command_prefix="$")
    bot.add_cog(Admin(bot))
    bot.add_cog(Music(bot))

    def __init__(self):
        print('ZeusBot initialized...')

    def start(self, key):
        print('Starting ZeusBot...')
        self.bot.run(key)


    @bot.event
    async def on_ready():
        ZeusBot.change_status.start()
        print('ZeusBot is running on server successfully...')


    @tasks.loop(hours=2)
    async def change_status():
        movies = [] # add some best movie names, mark the ActivityType to watching
        songs = ['93.5 FM Radio', 'Spotify', 'SoundCloud', 'Rap Music']  # add some songs and mark the ActivityType to listening
        games = ['Call of Duty Mobile', 'Valorant', 'PUBG Mobile', 'Counter Strike', 'Krunker.io']  # add some games and mark the ActivityType to gaming
        await ZeusBot.bot.change_presence(activity=discord.Activity(name=choice(games), type=getattr(discord.ActivityType, 'playing')), afk=True)


if __name__ == '__main__':
    token: str = os.getenv('BOT_TOKEN')
    zbot = ZeusBot()
    zbot.start(token)
