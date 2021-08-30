from time import sleep
import os
import discord
from discord.ext import commands
# from googlesearch.googlesearch import GoogleSearch as google




class ZeusBot:
    bot = discord.Client()
    
    def __init__(self) -> None:
        print('ZeusBot Initialized...')

    def start(self, key):
        print('ZeusBot Running...')
        self.bot.run(key)

    @bot.event
    async def on_message(msg: discord.Message):
        # convert the whole message into lowercase
        msg.content = msg.content.lower()

        # bot must not talk with itself, that's really bad
        if msg.author == ZeusBot.bot.user:
            return
        
        # greet
        if msg.content.startswith('$hello') or msg.content.startswith('$hi'):
            greet = 'Hi! ' + str(msg.author.display_name) + ' nice to meet you !' 
            await msg.channel.send(greet)
        # if anybody writes/send something unneccessary in any particular channel, delete the text and warn him/her
        elif str(msg.channel) == 'general':
            await msg.channel.purge(limit=5)
            warning = 'Hey ' + str(msg.author.display_name) + ' you are not allowed to text here'
            await msg.channel.send(warning)
            sleep(5)
            await msg.channel.purge(limit=5)

        elif msg.content.startswith('$ask'):
            search_query = msg.content.split('$ask')[1]
            result = 'nil'
            output = 'Google Search Results for Query: ' + search_query +'\n' + result
            await msg.channel.send(output)

    @bot.event
    async def on_ask(msg: discord.Message):
        msg.content = msg.content.lower()

        if msg.author == ZeusBot.bot.user:
            return

        if msg.content.startswith('$ask'):
            search_query = msg.content.split('$ask')[1]
            result = 'nil'
            output = 'Google Search Results for Query: ' + search_query +'\n' + result
            await msg.channel.send(output)





class ZeusCommands(commands.Cog):
    # greet
    @commands.command()
    async def hello(ctx: commands.Context, *args: str):
        greet = 'Hi ' + str(ctx.author) + '! So, do you want me to do something ?'
        await ctx.send(content=greet)
    
    # ask the bot about something, and it will search about it on google
    @commands.command()
    async def ask(ctx: commands.Context, *args: str):
        query = ' '.join(str(args))
        # search the query in google
        result = ''
        output = 'Google Search Results for Query: ' + query +'\n' + result
        await ctx.send(output)

    # music playback using ytdl [NOT IMPLEMENTED]
    @commands.command()
    async def play(ctx: commands.Context, *args):
        music_query = ' '.join(args)
        # play music from youtube
        await ctx.send('This command is not yet implemented by the developer. Will be available in the near future.')
    
 
if __name__ == '__main__':
    token: str = os.getenv('BOT_TOKEN')
    zbot = ZeusBot()
    zbot.start(token)
