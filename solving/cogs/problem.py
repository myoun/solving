import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Problem(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="search-problem", description="search problems in solved.ac")
    @app_commands.guilds(discord.Object(id=832156790782165004))
    @app_commands.describe(
        problem_name="The name of problem you want to search."
    )
    async def search_problem(self, ctx: Context, *, problem_name: str) -> None:
        async with aiohttp.ClientSession() as session:
            print(problem_name)
            async with session.get(f"https://solved.ac/api/v3/search/problem?query={problem_name}") as request:
                if request.status == 200:
                    data = await request.json()
                    count = data['count']
                    addition = " (생략됨)" if count > 10 else ""
                    embed = discord.Embed(
                        description=f"{count}개의 문제를 찾았습니다."+addition
                    )
                    for p in data['items'][:10]:
                        tags = []
                        for tag in p["tags"]:
                            for displayName in tag["displayNames"]:
                                if displayName["language"] == "ko":
                                    tags.append(displayName["name"])
                        tagstring = ", ".join(tags)
                        embed.add_field(name=f"{p['problemId']}-{p['titleKo']}", value=f"[바로가기](https://acmicpc.net/problem/{p['problemId']})\nTags: {tagstring}\n\u200B", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("error!")

async def setup(bot) -> None:
    await bot.add_cog(Problem(bot))