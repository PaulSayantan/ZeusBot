from time import sleep
import os
import discord
from discord.ext import commands
from googlesearch import search


class ZeusBot:
    bot = commands.Bot(command_prefix="$")

    def __init__(self):
        print('ZeusBot initialized...')

    def start(self, key):
        print('ZeusBot Running...')
        self.bot.run(key)

    @bot.command()
    async def hello(ctx: commands.Context, *args: str):
        greet = 'Hi ' + str(ctx.author.display_name) + '!'
        await ctx.send(content=greet)

    # ask the bot about something, and it will search about it on google
    @bot.command()
    async def search(ctx: commands.Context, *args):
        query = ' '.join(args)
        # search the query in google
        result = '\n'.join(search(query, safe='on', stop=10))
        output = 'Google Search Results:\n' + result
        await ctx.send(output)

    # music playback using ytdl [NOT IMPLEMENTED]
    @bot.command()
    async def play(ctx: commands.Context, *args):
        music_query = ' '.join(args)
        # play music from youtube
        await ctx.send('This command is not yet implemented by the developer. Will be available in the near future.')


    

 
if __name__ == '__main__':
    token: str = os.getenv('BOT_TOKEN')
    zbot = ZeusBot()
    zbot.start(token)
