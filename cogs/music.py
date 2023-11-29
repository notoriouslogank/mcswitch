import asyncio

import discord
import yt_dlp
from discord.ext import commands

from harbinger import Harbinger

bot = Harbinger.bot
players = {}


ytdl_format_options = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logstostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    """Class to configure FFMpeg and yt-dlp to interact with commands.

    Args:
        discord (obj): discord.PCMVolumeTransformer
    """

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        """Download or stream data from provided URL.

        Args:
            url (str): URL to be downloaded
            loop (optional): Defaults to None.
            stream (bool, optional): Whether to download or stream the data. Defaults to False.

        Returns:
            cls: An FFmpeg object?
        """
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    """A class of commands for streaming music via the bot in the voice channel."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx) -> None:
        """Join the bot to the contextual voice channel."""
        cmd = "!join"
        cmd_msg = f"Added bot to voice channel."
        channel = ctx.message.author.voice.channel
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        await channel.connect()

    @commands.command()
    async def leave(self, ctx) -> None:
        """Leave the voice channel."""
        cmd = "!leave"
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            cmd_msg = f"Removed bot from voice channel."
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
            await voice_client.disconnect()
        else:
            cmd_msg = f"Failed to remove bot from channel (not in channel)."
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
            await ctx.send("Bot is not currently in a channel...")

    @commands.command()
    async def pause(self, ctx) -> None:
        """Pause the currently-playing song/video."""
        cmd = "!pause"
        cmd_msg = "Paused playback."
        voice_client = ctx.message.guild.voice_client
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        await voice_client.pause()

    @commands.command()
    async def play(self, ctx) -> None:
        """Resume playback of a previously-paused video/song."""
        cmd = "!play"
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            cmd_msg = "Resumed playback."
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
            await voice_client.resume()
        else:
            cmd_msg = "Tried to resume playback; nothing playing."
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
            await ctx.send("Bot not paused...")

    #    @commands.command()  # Felt cute, might delete later
    #    async def yt(self, ctx, *, url) -> None:
    #        async with ctx.typing():
    #            player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #            ctx.voice_client.play(
    #                player, after=lambda e: print(f"Player error: {e}") if e else None
    #            )
    #        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def stream(self, ctx, *, url) -> None:
        """Stream, rather than download and playback, a given URL.

        Args:
            url (str): The URL to be streamed to the voice channel.
        """
        cmd = "!stream"
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            cmd_msg = f"Started playing {url}"
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        await ctx.send(f"Now playing: {player.title}")

    # @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx) -> None:
        """Ensure that the ctx.message.author is actively in a voice channel.

        Raises:
            commands.CommandError: Raises when the command is invoked by someone not in a voice channel.
        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You must be connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(bot):
    """Load cogs into bot."""
    await bot.add_cog(Music(bot))