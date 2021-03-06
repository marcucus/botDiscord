import os
import asyncio
import functools
import itertools
import math
import publicip
import random
from idlelib import query
from os import listdir
from os.path import isfile, join
import ffmpeg
import discord
import youtube_dl
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from async_timeout import timeout

load_dotenv()

intents = discord.Intents().all()
client = commands.Bot(command_prefix='z#')

players = {}


@client.event
async def on_ready():
    print("Le bot est prêt à planter")


@client.command(name='vasco')
async def squid(ctx):
    await ctx.message.delete()
    await ctx.send("SA MÈRE LA PUTE A LUI")


@client.command(name='supp')
async def delete(ctx, number_of_message: int, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    count = 0
    messages = await ctx.channel.history(limit=number_of_message).flatten()
    async for _ in channel.history(limit=None):
        count += 1
    if count == 0:
        print("Il n'y a aucun messages dans ce channel !")
    else:
        for each_message in messages:
            await each_message.delete()
        print("Les messages ont été supprimés")


@client.command(name='supp@')
async def message_count(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    count = 0
    number_msg = 0
    async for _ in channel.history(limit=None):
        count += 1
    number_msg = count
    message = await ctx.channel.history(limit=number_msg).flatten()
    if number_msg == 0:
        print("Il n'y a aucun message dans ce channel !")
    else:
        for each_message in message:
            await each_message.delete()
        print('Tout les messages ont été supprimés !')


@client.command(name='nbmsg')
async def message_count(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.send("Il y a {} messages dans {}".format(count, channel.mention))


@client.command(name='cut')
async def cut(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    await ctx.channel.send("ÇA C'EST DES VRAIS COUTEAUX !")


@client.command(name='songs')
async def cut(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    fi = os.listdir("C:/Users/marqu/Downloads/musique")
    embeds = discord.Embed(
        title='Voici la liste des sons stockés localement, mettre la commande puis le nom du son .mp3',
        colour=0x6600ff)
    for i in range(len(fi)):
        embeds.add_field(name=i,
                         value=fi[i],
                         inline=True)
    await ctx.author.send(embed=embeds)
    await ctx.message.delete()


@client.command(name='gang')
async def gang(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    await ctx.channel.send("EH GANG !")


@client.command(name='eheh')
async def eheh(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    await ctx.channel.send("EH EH !")


@client.command(name='fixette')
async def fixette(ctx, channel: discord.TextChannel = None):
    await ctx.message.delete()
    channel = channel or ctx.channel
    await ctx.channel.send("HAN, 3ENDI SEM FI DEM")


client.remove_command('help')


@client.command(name='help')
async def help_(ctx):
    await ctx.message.delete()
    '''Envoie la liste des commandes et leurs fonctions'''
    embed = discord.Embed(
        title='Liste des commandes avec "z#" obligatoirement avant la commande (ex : z#cut pour cut) !',
        colour=0x6600ff)
    embed.add_field(name="**supp**",
                    value="Pour supprimer un certain nombre de messages, mettre le nombre voulu après supp",
                    inline=True)
    embed.add_field(name="**supp@**", value="Pour supprimer tout les messages d'un channel", inline=True)
    embed.add_field(name="**nbmsg**", value="Pour afficher le nombre de message d'un channel", inline=True)
    embed.add_field(name="**cut**", value="Afficher un message", inline=True)
    embed.add_field(name="**gang**", value="Afficher un message", inline=True)
    embed.add_field(name="**eheh**", value="Afficher un message", inline=True)
    embed.add_field(name="**Fixette**", value="Afficher un message", inline=True)
    embed.add_field(name="**help**", value="Pour afficher ce message", inline=True)
    embed.add_field(name="**join**", value="Pour que le bot rejoint ton salon", inline=True)
    embed.add_field(name="**play**", value="Pour que le bot lance une musique (mettre un URL après play)",
                    inline=True)
    embed.add_field(name="**local**", value="Pour lire une musique stockée localement",
                    inline=True)
    embed.add_field(name="**songs**", value="Pour voir les sons stockés lisibles par le bot",
                    inline=True)
    embed.add_field(name="**leave**", value="Pour que le bot quitte le salon", inline=True)
    embed.add_field(name="**volume**", value="Pour ajuster le volume du bot en %", inline=True)
    embed.add_field(name="**now**", value="Pour afficher le son qui passe actuellement", inline=True)
    embed.add_field(name="**pause**", value="Pour mettre pause au son", inline=True)
    embed.add_field(name="**resume**", value="Pour enlever la pause", inline=True)
    embed.add_field(name="**stop**", value="Pour arreter la musique", inline=True)
    embed.add_field(name="**skip**", value="Pour passer à la musique suivante", inline=True)
    embed.add_field(name="**queue**", value="Pour afficher la file d'attente des sons", inline=True)
    embed.add_field(name="**remove**", value="Pour enlever un son de la file d'attente, spécifier le numéro du son",
                    inline=True)
    embed.add_field(name="**vasco**", value="Pour insulter la pute de mère de vasco",
                    inline=True)
    embed.set_footer(text="Par Adrien Marques")
    await ctx.author.send(embed=embed)


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': False,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Titre joué :',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Durée', value=self.source.duration)
                 .add_field(name='Demandé par', value=self.requester.mention)
                 .add_field(name='Par', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='Lien', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(520):  # 12 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Cette commande ne peut pas être utilisée en messages privés ! EH-EH')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join')
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.message.delete()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.message.delete()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Le bot n\' est connecté à aucun channels !')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]
        await ctx.message.delete()

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')
            await ctx.message.delete()

    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')
            await ctx.message.delete()

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')
            await ctx.message.delete()

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('File d\'attente vide EH GANG !')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('Erreur dans le processus: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('J\'AIME BEAUCOUP CE QUE TU AJOUTES EH GANG {}'.format(str(source)))

    @commands.command()
    async def local(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        qeri = "C:/Users/marqu/Downloads/musique/" + query
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(qeri))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send("LIBEREZ TOUT MES COPAINS EH GANG : " + query)
        await ctx.message.delete()

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Tu n'est pas connecté dans un channel ! ")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Le bot est déjà dans un channel !')


client.add_cog(Music(client))

client.run(os.getenv("TOKEN"))
