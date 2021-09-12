import asyncio

import discord
from discord.ext import commands, tasks
from googlesearch import search


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context, *args: str):
        """the bot greets you"""
        greet = 'Hi ' + str(ctx.author.display_name) + '!'
        await ctx.send(content=greet)


    @commands.command()
    async def google_search(self, ctx: commands.Context, *args):
        """search anything, get response like a google search"""
        if str(ctx.channel) in ['general', 'search', 'discussion', 'google', 'bot-testing'] :
            query = ' '.join(args)
            # search the query in google
            result = '\n'.join(search(query, stop=10))
            output = 'Google Search Results:\n' + result
            await ctx.send(output)
        else:
            await ctx.send(str(ctx.author.display_name) + ', you are not allowed to run this command here')
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=2)

    
    @commands.command()
    async def clear(self, ctx: commands.Context, arg):
        """Clear only number of messages passed as argument"""
        number = int(arg) + 1 #Converting the amount of messages to delete to an integer
        counter = 0
        async for x in self.bot.logs_from(ctx.message.channel, limit = number):
            if counter < number:
                await self.bot.delete_message(x)
                counter += 1
                await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even
    
    
    @commands.command()
    async def destroy(self, ctx: commands.Context, *args):
        """Erasing all messages present in the channel"""
        await ctx.channel.purge()
    

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, cause=None):
        """Kick a member for misconduct, also provide reason"""
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


    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, cause=None):
        """ban a member from this discord server, also provide reason"""
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


    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx: commands.Context, *, member: discord.Member):
        """bring back a banned member into the guild"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
