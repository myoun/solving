import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from types import CoroutineType
from solving import colors

users = {}

class UserInfoModal(discord.ui.Modal):
    user_id = discord.ui.TextInput(label="USER ID")

    def __init__(self, callback: CoroutineType) -> None:
        super().__init__(title="유저 정보를 입력해주세요", custom_id="user_info_modal")
        self.callback = callback

    async def on_submit(self, interaction: discord.Interaction) -> None:
        users[interaction.user.id] = self.user_id
        await self.callback(interaction)



class User(commands.Cog, name="user"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="info", description="check user info")
    async def info(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        if user.id not in users:
            await interaction.response.send_modal(UserInfoModal(self.__info))
        else:
            await self.__info(interaction)

    async def __info(self, interaction: discord.Interaction) -> None:
        url = f"https://solved.ac/api/v3/user/show?handle={users[interaction.user.id]}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request.status == 200:
                    json = await request.json()
                    await interaction.response.send_message(str(json))
                else:
                    await interaction.response.send_message(embed=discord.Embed(description="알수없는 오류가 발생했습니다.", color=colors.color_failed))



async def setup(bot) -> None:
    await bot.add_cog(User(bot))