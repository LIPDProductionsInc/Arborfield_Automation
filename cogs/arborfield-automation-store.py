import discord
import aiosqlite

from discord.ext import commands
from discord import app_commands

class StoretoDBCog(commands.Cog, name="Store to Database Group Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    group = app_commands.Group(name="store", description="Store to Database Group Commands")

    @group.command(name="decree", description="Store a mayoral decree to the database")
    @app_commands.checks.has_any_role(583496754712805376, 1087922383698014279)
    async def decree(self, interaction: discord.Interaction, decree_name: str, decree_number: int, signed_by: str, decree_status: str, decree_link: str):
        if decree_link.startswith("https://drive.google.com/file/d/") or decree_link.startswith("https://forums.stateoffirestone.com/") or decree_link.startswith("https://docs.google.com/document/d/"):
            async with aiosqlite.connect("/home/pi/Documents/Arborfield_Automation/arborfield_backup.db") as db:
                message = await interaction.response.send_message("Storing decree to database...", ephemeral=True)
                try:
                    await db.execute(f"INSERT INTO decrees values('{decree_name}', {decree_number}, '{decree_status}', '{signed_by}', '{decree_link}')")
                    print(f'Added Mayoral Decree {decree_number} - {decree_name} to database')
                    await db.commit()
                    print('Saved')
                    await message.edit(content="Decree stored to database!", ephemeral=True)
                except Exception as e:
                    await message.edit(content=f"Error: {e}", ephemeral=True)
                    print(f'Ignoring exception in command decree: {e}')
                    pass
                pass
        else:
            await interaction.response.send_message("Use a Google Drive or Forums link", ephemeral=True)
            pass
        pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StoretoDBCog(bot))