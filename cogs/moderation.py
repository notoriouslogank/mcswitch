import random
from aiohttp import content_disposition_filename
import discord
from discord.ext import commands
import base64
from config.read_configs import ReadConfigs as configs
from harbinger import Harbinger

MODERATOR_ROLE_ID = str("Admin")
DELETION_TIME = configs.delete_time()
CUSTOM_COLOR = configs.custom_color()


class Moderation(commands.Cog):
    """Server moderation commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def caeser_cipher(key, *, message):
        message = message.upper()
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        for letter in message:
            if letter in alpha:
                letter_index = (alpha.find(letter) + key) % len(alpha)
                result = result + alpha[letter_index]
            else:
                result = result + letter
        return result

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def clear(self, ctx: commands.Context, amount: int = 2) -> None:
        """Delete a number of messages in channel."""
        cmd = f"!clear({amount})"
        cmd_msg = f"Deleted {amount} messages."
        amount = amount + 1
        if amount > 100:
            await ctx.send("Cannot delete more than 100 messages.")
        else:
            await ctx.channel.purge(limit=amount)
            Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def whisper(self, ctx, member: discord.Member, *, content) -> None:
        """Send a Direct Message to a member as Harbinger."""
        cmd = f"!whisper({member})"
        cmd_msg = f"Whispered: {content}"
        channel = await member.create_dm()
        await ctx.channel.purge(limit=1)
        Harbinger.timestamp(ctx.author, cmd, cmd_msg)
        await channel.send(content)

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def code_whisper(
        self, ctx: commands.Context, code, member: discord.Member, *, content
    ) -> None:
        """Send an encoded DM to a given member as Harbinger."""
        cmd = f"!whisper({member})"
        cmd_msg = f"Whispered: {content}"
        channel = await member.create_dm()
        await ctx.channel.purge(limit=1)
        if code == "bin":
            binary_message = "".join(
                format(i, "08b") for i in bytearray(content, encoding="utf-8")
            )
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await channel.send(f"``{binary_message}``")
        elif code == "csr":
            key = random.randint(1, 26)
            message_record = f"Sent message to {member} using Caeser Cipher:\n``{content}``\nKey: {key}"
            caeser_message = Moderation.caeser_cipher(key, content)
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await channel.send(f"``{caeser_message}``")
            await Harbinger.send_dm(
                ctx=ctx, member=ctx.message.author, content=message_record
            )
        elif code == "hex":
            hex_message = content.encode("utf-8").hex()
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await channel.send(f"``{hex_message}``")
        elif code == "b64":
            content_bytes = content.encode("ascii")
            base64_bytes = base64.b64encode(content_bytes)
            base64_message = str(base64_bytes, encoding="utf-8")
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await channel.send(f"``{base64_message}``")
        else:
            await ctx.send(
                "Please choose a valid encoding schema: binary [bin], hexadecimal [hex], or base64 [b64]."
            )

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def serverinfo(self, ctx: commands.Context):
        """Create embeds containing server details and member information and send them to the channel."""
        cmd = "!serverinfo"
        cmd_msg = "Get details about the server."
        owner = str(ctx.guild.owner)
        guild_id = str(ctx.guild.id)
        member_count = str(ctx.guild.member_count)
        # icon = str(ctx.guild.icon_url)
        desc = ctx.guild.description

        embed = discord.Embed(
            title=ctx.guild.name + "Server Information",
            description=desc,
            color=CUSTOM_COLOR,
        )
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        await ctx.send(embed=embed)

        members = []
        async for member in ctx.guild.fetch_members(limit=150):
            members_embed = discord.Embed(
                title=f"{member.display_name}",
                description=f"Status: {member.status}",
                color=member.color,
            )
            members_embed.add_field(name="Member Since: ", value=f"{member.joined_at}")
            members_embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=members_embed)

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def whois(self, ctx: commands.Context, member: discord.Member) -> None:
        """Get detailed information about given member.

        Args:
            member (discord.Member): Member to get info for (must be exact)
        """
        cmd = "!whois"
        cmd_msg = f"Got whois info for {member}."
        whois_embed = discord.Embed(
            title=f"{member.display_name}",
            description=f"{member.status}",
            color=member.color,
        )
        whois_embed.add_field(name="Roles:", value=f"{member.roles}")
        whois_embed.add_field(name="Joined:", value=f"{member.joined_at}", inline=True)
        whois_embed.set_image(url=member.display_avatar.url)
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        await ctx.send(embed=whois_embed)

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def code_say(self, ctx: commands.Context, code, *, content) -> None:
        cmd = f"!code_say {code}"
        cmd_msg = f"{content}"
        await ctx.channel.purge(limit=1)
        if code == "bin":
            binary_message = "".join(
                format(i, "08b") for i in bytearray(content, encoding="utf-8")
            )
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await ctx.send(f"``{binary_message}``")
        elif code == "csr":
            key = random.randint(1, 26)
            message_record = f"Sent message to {ctx.channel} using Caeser Cipher:\n``{content}``\nKey: {key}"
            caeser_message = Moderation.caeser_cipher(key, content)
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await ctx.send(f"``{caeser_message}``")
            await Harbinger.send_dm(
                ctx=ctx, member=ctx.message.author, content=message_record
            )
        elif code == "hex":
            hex_message = content.encode("utf-8").hex()
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await ctx.send(f"``{hex_message}``")
        elif code == "b64":
            content_bytes = content.encode("ascii")
            base64_bytes = base64.b64encode(content_bytes)
            base64_message = str(base64_bytes, encoding="utf-8")
            Harbinger.timestamp(ctx.author, cmd, cmd_msg)
            await ctx.send(f"``{base64_message}``")

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def say(self, ctx: commands.Context, *message: str) -> None:
        """Send a message as the bot.

        Args:
            message (str): Message to send as the bot
        """
        cmd = f"!say({message})"
        string_message = ""
        for word in message:
            string_message = string_message + str(word) + " "
        content = string_message.strip()
        await ctx.channel.purge(limit=1)
        cmd_msg = f"Harbinger says: {content}"
        Harbinger.timestamp(ctx.author, cmd, cmd_msg)
        await ctx.send(f"{content}")

    @commands.command()
    async def playing(
        self, ctx: commands.Context, game, description, field, value
    ) -> None:
        """Create game info embed."""
        cmd = f"!playing({game}, {field}, {value})"
        cmd_msg = f"Created playing embed with these values: {game},{field},{value}"
        playing_embed = discord.Embed(title=f"{game}", description=f"{description}")
        playing_embed.add_field(name=f"{field}", value=f"{value}")
        await ctx.send(embed=playing_embed)
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)

    # ERRORS
    @clear.error
    async def clear_error(self, ctx, error) -> None:
        """Error raised when !clear command fails

        Args:
            error (MissingRole): Raised if user does not have developer role.
        """
        cmd = f"ERROR: ClearError"
        cmd_msg = f"User does not have mod role."
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        message = await ctx.send("You must be a moderator to do that!")
        await ctx.message.delete()
        if isinstance(error, commands.MissingRole):
            await message.edit(delete_after=DELETION_TIME)

    @say.error
    async def say_error(self, ctx, error) -> None:
        """Error raised when !say command fails

        Args:
            error (MissingRole): Raised if user does not have developer role.
        """
        cmd = f"ERROR: SayError"
        cmd_msg = f"User does not have mod role."
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        message = await ctx.send("You must be a moderator to do that!")
        await ctx.message.delete()
        if isinstance(error, commands.MissingRole):
            await message.edit(delete_after=DELETION_TIME)

    @whois.error
    async def whois_error(self, ctx, error) -> None:
        """Error raised when !whois command fails

        Args:
            error (MissingRole): Raised if user does not have developer role.
        """
        cmd = f"ERROR: WhoisError"
        cmd_msg = f"User does not have mod role."
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        message = await ctx.send("You must be a moderator to do that!")
        await ctx.message.delete()
        if isinstance(error, commands.MissingRole):
            await message.edit(delete_after=DELETION_TIME)

    @serverinfo.error
    async def serverinfo_error(self, ctx, error) -> None:
        """Error raised when !serverinfo command fails

        Args:
            error (MissingRole): Raised if user does not have developer role.
        """
        cmd = f"ERROR: ServerinfoError"
        cmd_msg = f"User does not have mod role."
        Harbinger.timestamp(ctx.message.author, cmd, cmd_msg)
        message = await ctx.send("You must be a moderator to do that!")
        await ctx.message.delete()
        if isinstance(error, commands.MissingRole):
            await message.edit(delete_after=DELETION_TIME)


async def setup(bot):
    """Load cogs into bot."""
    await bot.add_cog(Moderation(bot))
