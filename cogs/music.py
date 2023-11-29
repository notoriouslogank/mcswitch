from discord.ext import commands
from discord.utils import get
from discord import FFmpegAudio
import youtube_dl
from harbinger import Harbinger

bot = Harbinger.bot
players = {}


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(commands.Bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @bot.command()
    async def play(self, ctx, url):
        YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }
        voice = get(commands.Bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info["url"]
            voice.play(FFmpegAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send("Playing...")
        else:
            await ctx.send("Already playing...")
            return

    @commands.command()
    async def stop(self, ctx):
        voice = get(commands.Bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.send("Stopping...")


async def setup(bot):
    """Load cogs into bot."""
    await bot.add_cog(Music(bot))
