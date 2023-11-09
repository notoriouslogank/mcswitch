import discord
from discord.ext import commands

from utils.helpers import getVer, purple

VERSION = getVer()
PURPLE = purple


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog online.")

    @commands.command()
    async def help(self, ctx, *, command=None):
        """Return help embed with command descriptions."""
        if command == None:
            help_embed = discord.Embed(
                title="Command Help",
                description=f"Commands for bot v{VERSION}",
                color=PURPLE,
            )
            # MODERATION
            help_embed.add_field(
                name="!clear", value="Delete a number of messages.", inline=True
            )
            help_embed.add_field(
                name="!joined", value="Get datetime user joined.", inline=True
            )
            help_embed.add_field(name="!say", value="Send message as bot.", inline=True)
            help_embed.add_field(
                name="!playing",
                value="Embed and send game info to channel.",
                inline=True,
            )
            # STATUS
            help_embed.add_field(
                name="!status", value="Confirm bot online and reachable.", inline=True
            )
            help_embed.add_field(
                name="!info", value="Get details about this bot.", inline=True
            )
            help_embed.add_field(
                name="!ping", value="Get network latency.", inline=True
            )
            help_embed.add_field(name="!uptime", value="Get bot uptime.", inline=True)
            help_embed.add_field(
                name="!shutdown", value="Gracefully shutdown the bot.", inline=True
            )
            # TOOLS
            help_embed.add_field(
                name="!define", value="Get the definition of a given word.", inline=True
            )
            help_embed.add_field(
                name="!lmgtfy", value="Let me Google that for you...", inline=True
            )
            help_embed.add_field(name="!add", value="Add two numbers.", inline=True)
            help_embed.add_field(name="!roll", value="Roll NdN dice.", inline=True)
            help_embed.add_field(
                name="!rps",
                value="Play rock, paper, scissors against the bot.",
                inline=True,
            )
            # OTHER
            help_embed.add_field(
                name="Need Help?",
                value="[Join the Bot-Dev Server](https://discord.gg/9zAW8DfV)",
                inline=True,
            )
            help_embed.add_field(
                name="Find a Problem?",
                value="[Submit a Bug Report](https://github.com/notoriouslogank/mcswitch/issues)",
                inline=True,
            )
            help_embed.set_footer(
                text=f"Requested by {ctx.author}>.", icon_url=ctx.author.avatar
            )

            await ctx.send(embed=help_embed)

        elif command == "clear":
            usage_embed = discord.Embed(
                title="clear",
                description="Delete some amount of messages in the channel.",
            )
            usage_embed.add_field(name="Usage: ", value="!clear <amount>", inline=False)
            usage_embed.add_field(
                name="<amount: int>",
                value="The number of messages to be deleted.",
                inline=True,
            )
            await ctx.send(embed=usage_embed)
        elif command == "joined":
            usage_embed = discord.Embed(
                title="joined", description="Get the datetime a given member joined."
            )
            usage_embed.add_field(name="Usage:", value="!joined <member>", inline=False)
            usage_embed.add_field(
                name="<member: discord.Member>",
                value="Member to fetch join date of.",
                inline=True,
            )
            await ctx.send(embed=usage_embed)
        elif command == "say":
            usage_embed = discord.Embed(
                title="say", description="Send a message to the channel as the bot."
            )
            usage_embed.add_field(
                name="Usage:", value="!say <'message'> ", inline=False
            )
            usage_embed.add_field(
                name="<message: str>",
                value="The message to send as the bot.",
                inline=True,
            )
            usage_embed.set_footer(
                text="Note: multiword arguments must be surrounded by double quotes."
            )
            await ctx.send(embed=usage_embed)
        elif command == "playing":
            usage_embed = discord.Embed(
                title="playing", description="Send an embed with game info, etc."
            )
            usage_embed.add_field(
                name="Usage:", value="!playing <game> <field> <value>", inline=False
            )
            usage_embed.add_field(
                name="<game: str>",
                value="The game or application that will title the embed.",
                inline=True,
            )
            usage_embed.add_field(
                name="<field>",
                value="A field to store data in, eg IP Adress or Room Code",
                inline=True,
            )
            usage_embed.add_field(
                name="<value>",
                value="The value for the field, eg 127.0.0.1.",
                inline=True,
            )
            usage_embed.set_footer(
                text="Note: multiword arguments must be surrounded by double quotes."
            )
            await ctx.send(embed=usage_embed)
        elif command == "status":
            usage_embed = discord.Embed(
                title="status",
                description="Confirm that the bot is online and reachable.",
            )
            usage_embed.add_field(name="Usage:", value="!status", inline=False)
            await ctx.send(embed=usage_embed)
        elif command == "info":
            usage_embed = discord.Embed(
                title="info", description="Get detailed information about the bot."
            )
            usage_embed.add_field(name="Usage:", value="!info", inline=False)
            await ctx.send(embed=usage_embed)
        elif command == "ping":
            usage_embed = discord.Embed(
                title="ping", description="Get network latency."
            )
            usage_embed.add_field(name="Usage:", value="!ping", inline=False)
            await ctx.send(embed=usage_embed)
        elif command == "uptime":
            usage_embed = discord.Embed(
                title="uptime", description="Get time since bot instance was started."
            )
            usage_embed.add_field(name="Usage:", value="!uptime", inline=False)
            await ctx.send(embed=usage_embed)
        elif command == "shutdown":
            usage_embed = discord.Embed(
                title="shutdown", description="Gracefully shut down the bot."
            )
            usage_embed.add_field(name="Usage:", value="!shutdown", inline=False)
            await ctx.send(embed=usage_embed)
        elif command == "define":
            usage_embed = discord.Embed(
                title="define",
                description="Get the Meriam-Webster definition of a word.",
            )
            usage_embed.add_field(name="Usage:", value="!define <word>", inline=False)
            usage_embed.add_field(
                name="<word: str>", value="The word to be defined.", inline=True
            )
            await ctx.send(embed=usage_embed)
        elif command == "lmgtfy":
            usage_embed = discord.Embed(
                title="lmgtfy", description="Let Me Google That For You"
            )
            usage_embed.add_field(name="Usage:", value="!lmgtfy <query>", inline=False)
            usage_embed.add_field(
                name="<query: str>",
                value="The term(s) to beb searched on Google.",
                inline=True,
            )
            usage_embed.set_footer(
                text="Note: Multiword queries must be separated with (+) characters: !lmgtfy 'one+two'."
            )
            await ctx.send(embed=usage_embed)
        elif command == "add":
            usage_embed = discord.Embed(title="add", description="Add two numbers.")
            usage_embed.add_field(
                name="Usage:", value="!add <num1> <num2>", inline=False
            )
            usage_embed.add_field(
                name="<num1: int>", value="First addend.", inline=True
            )
            usage_embed.add_field(name="<num2: int>", value="Second addend.")
            await ctx.send(embed=usage_embed)
        elif command == "roll":
            usage_embed = discord.Embed(title="roll", description="Roll some dice.")
            usage_embed.add_field(name="Usage:", value="!roll <NdN>", inline=False)
            usage_embed.add_field(
                name="<NdN: str>",
                value="Number of n-sided dice to roll, eg 3d20.",
                inline=True,
            )
            usage_embed.set_footer(text="Note: Format should be NdN *only*.")
            await ctx.send(embed=usage_embed)
        elif command == "rps":
            usage_embed = discord.Embed(
                title="rps", description="Play rock, paper, scissors with the bot."
            )
            usage_embed.add_field(
                name="Usage:", value="!rps <rock|paper|scissors>", inline=False
            )
            usage_embed.add_field(
                name="<rock|paper|scissors : str>",
                value="Which move to play.",
                inline=True,
            )
            await ctx.send(embed=usage_embed)
        else:
            print("Something probably went wrong.")


async def setup(bot):
    """Load cog into bot."""
    await bot.add_cog(HelpCommand(bot))