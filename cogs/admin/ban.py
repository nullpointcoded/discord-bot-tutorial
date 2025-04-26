import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID


class BanView(discord.ui.View):
    def __init__(self, target: discord.Member, reason: str):
        super().__init__(timeout=30)
        self.target = target
        self.reason = reason
        self.value = None


    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        server_name = interaction.guild.name
        moderator = interaction.user


        embed = discord.Embed(
            title="🔨 Ban Notice",
            description=f"You were banned from **{server_name}** for:\n```{self.reason}```",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Banned by {moderator}")


        try:
            await self.target.send(embed=embed)
        except discord.Forbidden:
            pass  


        await interaction.guild.ban(self.target, reason=self.reason)
        await interaction.response.edit_message(content=f"✅ **{self.target} has been banned.**", embed=None, view=None)

    @discord.ui.button(label="No", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Ban cancelled.", embed=None, view=None)
      

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="ban", description="Ban a user from the server.")
    @app_commands.describe(user="The user to ban", reason="The reason for the ban")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ban_user(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return


        embed = discord.Embed(
            title="Ban Confirmation",
            description=f"Are you sure you want to ban **{user}** for:\n```{reason}```",
            color=discord.Color.red()
        )
        embed.set_footer(text="Click a button below to confirm or cancel.")
        view = BanView(target=user, reason=reason)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
  await bot.add_cog(Ban(bot))
