from datetime import datetime
from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv


class Mcswitch:
    cogs = "cogs.moderation", "cogs.status", "cogs.help", "cogs.tools"
    custom_color = 0x884EA0
    sTime = datetime.now()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    def __init__(self, bot):
        self.bot = bot
        sTime = datetime.now()

    @bot.event
    async def setup_hook() -> None:
        print(f"Loading cogs")
        for cog in cogs:
            await bot.load_extension(cog)

    def get_token():
        load_dotenv()
        token = str(getenv("TOKEN"))
        return token

    def get_mc_host():
        mc_host = str(getenv("MC_HOST"))
        return mc_host

    def get_channel():
        channel = getenv("CHANNEL")
        return channel

    def get_ver():
        with open("docs/CHANGELOG.md", "r") as f:
            changes = f.readlines()
            vLine = changes[6]
            version = vLine[4:9]
            return version

    def timestamp(user, cmd, cmd_msg):
        """Print timestamp and end-of-command separator."""
        nl = "\n"
        cTime = datetime.now()
        print(f"++++")
        print(f"{cTime}")
        print(f"USR| {user}")
        print(f"CMD| {cmd}")
        print(f"MSG| {cmd_msg}")

    def start():
        bot.run(Mcswitch.get_token())

    async def send_dm(ctx, member: discord.Member, *, content):
        """Create a Direct Message channel with a given member."""
        channel = await member.create_dm()
        await channel.send(content)


bot = Mcswitch.bot
cogs = Mcswitch.cogs

def main():
    Mcswitch.start()


if __name__=='__main__':
    Mcswitch.start()
