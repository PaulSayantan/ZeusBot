from time import sleep
import os
import asyncio
import discord
from random import choice
from discord.ext import commands, tasks
import youtube_dl
from googlesearch import search


youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


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

    @tasks.loop(seconds=5)
    async def change_status():
        movies = [] # add some best movie names, mark the ActivityType to watching
        songs = ['93.5 FM Radio', 'Spotify', 'SoundCloud', 'Rap Music']  # add some songs and mark the ActivityType to listening
        games = ['Call of Duty Mobile', 'Valorant', 'PUBG Mobile', 'Counter Strike', 'Krunker.io']  # add some games and mark the ActivityType to gaming
        await ZeusBot.bot.change_presence(activity=discord.Activity(name=choice(games), type=getattr(discord.ActivityType, 'playing')), afk=True)

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


if __name__ == '__main__':
    token: str = os.getenv('BOT_TOKEN')
    zbot = ZeusBot()
    zbot.start(token)
