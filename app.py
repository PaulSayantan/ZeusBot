import os
import asyncio
import discord
from random import choice
from discord.ext import commands, tasks
from googlesearch import search
from music import *

class ZeusBot:
    bot = commands.Bot(command_prefix="$")
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


    @bot.command(name='$hello', help='the bot greets you')
    async def hello(ctx: commands.Context, *args: str):
        greet = 'Hi ' + str(ctx.author.display_name) + '!'
        await ctx.send(content=greet)


    # ask the bot about something, and it will search about it on google
    @bot.command(name='$search <query>', help='search google and display result in the chat')
    async def search(ctx: commands.Context, *args):
        if str(ctx.channel) in ['general', 'search', 'discussion', 'google'] :
            query = ' '.join(args)
            # search the query in google
            result = '\n'.join(search(query, safe='on', stop=10))
            output = 'Google Search Results:\n' + result
            await ctx.send(output)
        else:
            await ctx.send(str(ctx.author.display_name) + ', you are not allowed to run this command here')
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=2)


    @bot.command(name='$clear <number>', help='remove number of previous messages (including the command message)', pass_context = True)
    async def clear(self, ctx: commands.Context, arg):
        """Clear only number of messages passed as argument"""
        number = int(arg) + 1 #Converting the amount of messages to delete to an integer
        counter = 0
        async for x in self.bot.logs_from(ctx.message.channel, limit = number):
            if counter < number:
                await self.bot.delete_message(x)
                counter += 1
                await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even


    @bot.command()
    @commands.has_role("Admin")
    async def destroy(self, ctx: commands.Context, *args):
        """Erasing all messages present in the channel"""
        await ctx.channel.purge()
    

    @bot.command(pass_context=True, name='$kick <member>', help='remove a user from the guild (also provide reason)')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, cause=None):
        """Kick a member for misconduct"""
        if not member.server_permissions.administrator and str(member) != '★彡belikesayantan彡★#5276':
            if cause:
                try:
                    await member.kick(reason=cause)
                    await ctx.send('Kicked ' + str(member.display_name))
                except:
                    await ctx.send('There is a issue. Please wait...')
                    await asyncio.sleep(2)
            else:
                await ctx.send(str(ctx.author.display_name) + ', please provide a reason to kick ' + str(member.display_name) + '.')
        else:
            await ctx.send('Hey ' + str(ctx.author.display_name) + '!! How dare you try to kick the admin? Are you dumb?')
    
    @kick.error
    async def kick_error(self, error, ctx: commands.Context):
        if isinstance(error, commands.CheckFailure):
            text = 'Sorry {}, you do not have permissions to do that!'.format(ctx.message.author.display_name)
            await self.bot.send_message(ctx.message.channel, text)
        elif isinstance(error, commands.BadArgument):
            await self.bot.send_message(ctx.message.channel, "Could not identify the member to kick")
        elif isinstance(error, commands.MissingPermissions):
            text = 'Sorry {}, you do not have permissions to do that!'.format(ctx.message.author.display_name)
            await self.bot.send_message(ctx.message.channel, text)
        else:
            raise error


    @bot.command(pass_context=True, name='$ban <member>', help='ban a member from the guild')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, cause=None):
        if not member.server_permissions.administrator and str(member) != '★彡belikesayantan彡★#5276':
            if cause:
                try:
                    await member.ban(reason=cause)
                    await ctx.send('Banned ' + str(member.display_name))
                except:
                    await ctx.send('There is a issue. Please wait...')
                    await asyncio.sleep(2)
            else:
                await ctx.send(str(ctx.author.display_name) + ', please provide a reason to kick ' + str(member.display_name) + '.')
        else:
            await ctx.send('Hey ' + str(ctx.author.display_name) + '!! How dare you try to ban the admin? Are you dumb?')

    @ban.error
    async def ban_error(self, error, ctx: commands.Context):
        if isinstance(error, commands.CheckFailure):
            text = 'Sorry {}, you do not have permissions to do that!'.format(ctx.message.author.display_name)
            await self.bot.send_message(ctx.message.channel, text)
        elif isinstance(error, commands.BadArgument):
            await self.bot.send_message(ctx.message.channel, "Could not identify the member to kick")
        elif isinstance(error, commands.MissingPermissions):
            text = 'Sorry {}, you do not have permissions to do that!'.format(ctx.message.author.display_name)
            await self.bot.send_message(ctx.message.channel, text)
        else:
            raise error


    @bot.command(pass_context=True, name='$unban <member>', help='to bring back a banned member into the guild')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx: commands.Context, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

if __name__ == '__main__':
    token: str = os.getenv('BOT_TOKEN')
    zbot = ZeusBot()
    zbot.start(token)
