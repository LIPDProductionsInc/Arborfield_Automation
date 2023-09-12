import discord
import aiosqlite
import typing

from discord.ext import commands
from discord import app_commands
from typing import Literal

class StoretoDBCog(commands.Cog, name="Store to Database Group Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    group = app_commands.Group(name="store", description="Store to Database Group Commands")

    @group.command(name="decree", description="Store a mayoral decree to the database")
    @app_commands.checks.has_any_role(583496754712805376, 1087922383698014279)
    @app_commands.guild_only()
    @app_commands.describe(decree_name="Name of the decree", decree_number="Number of the decree", signed_by="Who signed the decree?", decree_status="Status of the decree", decree_link="Link to the decree")
    async def decree(self, interaction: discord.Interaction, decree_name:str, decree_number:int, signed_by:str, decree_status:Literal["Active", "Inactive", "Repealed"], decree_link:str):
        if decree_link.startswith("https://drive.google.com/file/d/") or decree_link.startswith("https://forums.stateoffirestone.com/") or decree_link.startswith("https://docs.google.com/document/d/"):
            async with aiosqlite.connect("/home/pi/Documents/Arborfield_Automation/db/arborfield_backup.db") as db:
                try:
                    await db.execute(f"INSERT INTO decrees values('{decree_name}', {decree_number}, '{decree_status}', '{signed_by}', '{decree_link}')")
                    print(f'Added Mayoral Decree {decree_number} - {decree_name} to database')
                    await db.commit()
                    print('Saved')
                    await interaction.response.send_message(content="Decree stored to database!", ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(content=f"Error: {e}", ephemeral=True)
                    print(f'Ignoring exception in command decree: {e}')
                    pass
                pass
        else:
            await interaction.response.send_message("Use a Google Drive or Forums link", ephemeral=True)
            pass
        pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StoretoDBCog(bot))