import datetime
import os
import subprocess
import tarfile
from time import sleep

import discord
from discord.ext import commands

from config.read_configs import ReadConfigs as configs
from harbinger import Harbinger

CUSTOM_COLOR = configs.custom_color()
SERVER_PUBLIC_IP = configs.server_public_ip()
SERVER_STARTUP_SCRIPT = configs.startup_script()
SERVER_DIR = configs.server_dir()
# BACKUP_DIR = configs.backup_dir()
LOG_NAME = r"logs/latest.log"
fname = os.path.join(SERVER_DIR, LOG_NAME)
bot = Harbinger.bot


class Minecraft(commands.Cog):
    """Class of commands for the Minecraft server."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def get_cmd_stdout(self):
        """Print final line of latest.log (simulating STDOUT).

        Returns:
            str: Final line of log file
        """
        with open(fname) as f:
            for line in f:
                pass
            last_line = line
            return last_line

    def get_mc_version(self) -> str:
        """Retrieve Minecraft client version from log file.

        Returns:
            str: Minecraft client version
        """
        with open(fname) as f:
            line = f.readlines()
            version = line[3]
            return version[-7:-1]

    def make_backup_tarball(output, source):
        with tarfile.open(output, "w:gz") as tar:
            tar.add(source, arcname=output)

    @commands.command()
    async def backmc(self, ctx: commands.Context):
        source = SERVER_DIR
        backup_name = datetime.datetime.strftime(
            datetime.datetime.now(), f"%d%m%Y-%H%M"
        )
        # stop the server
        subprocess.run(["tmux", "send", "-t", "Harbinger.1", "stop", "ENTER"])
        sleep(10)
        # create backup
        try:
            os.makedirs("backups", exist_ok=False)
        except:
            Exception()
        backup_fname = os.path.join("backups", backup_name)
        self.make_backup_tarball(f"{backup_fname}", source)

    @commands.command()
    async def startmc(self, ctx: commands.Context):
        """Start the Minecraft server."""
        cmd = f"!startmc"
        cmd_msg = f"Started Minecraft server."
        subprocess.run(
            [
                "tmux",
                "send",
                "-t",
                "Harbinger.1",
                f"zsh {SERVER_STARTUP_SCRIPT}",
                "ENTER",
            ]
        )
        await ctx.send(f"Starting Minecraft server...")
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)

    @commands.command()
    async def mc(self, ctx: commands.Context, command=None) -> None:
        """Send an arbitrary command to the Minecraft server.

        Args:
            command (str): Command to send to the server.
        """
        cmd = f"!mccmd({command})"
        cmd_msg = f"Sent following command to server: {command}"
        if command == None:
            mc_embed = discord.Embed(
                title="Minecraft Server",
                description="",
                color=CUSTOM_COLOR,
            )
            mc_embed.add_field(
                name="Client Version", value=f"``{self.get_mc_version()}``"
            )
            mc_embed.add_field(name="Server Address", value=f"``{SERVER_PUBLIC_IP}``")
            await ctx.send(embed=mc_embed)
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        else:
            subprocess.run(
                ["tmux", "send", "-t", "Harbinger.1", f"{command}", "C-m"],
            )
            await ctx.channel.purge(limit=1)
            await ctx.send(f"``> {command}``")
            stdout = self.get_cmd_stdout()
            await ctx.send(f"``{stdout}``")
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)


async def setup(bot):
    """Load cog into bot."""
    await bot.add_cog(Minecraft(bot))
