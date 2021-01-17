from aiohttp import request

from discord import Member, Embed, File
from discord.errors import HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.errors import BadArgument

from ..riotapi import player
from cassiopeia import Queue

QUEUE = dict(
    soloq = Queue.ranked_solo_fives, 
    flexq = Queue.ranked_flex_fives,
)

QUEUE_ANNOTATE = dict(
    soloq = "5v5 Ranked Solo",
    flexq = "5v5 Ranked Flex",
)

class League(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="rank", aliases=["r"])
    async def rank(self, ctx, summoner_name, mode, region='NA'):
        try:
            p = player.Player(summoner_name, QUEUE[mode], region)
        except KeyError:
            await ctx.send(f"{mode} is invalid. There are: soloq and flexq supported at the moment.")
            return
        embed = Embed(title=summoner_name, description=f"{QUEUE_ANNOTATE[mode]}")
        embed.set_thumbnail(url=p.icon_url)
        if (p.winrate != -1):
            embed.add_field(name=f"Overall WR", value=f"{p.winrate:.2f}%", inline=False)
            embed.add_field(name=f"Wins", value=f"{p.wins}", inline=False)
            embed.add_field(name=f"Losses", value=f"{p.losses}", inline=False)
            embed.add_field(name=f"Rank", value=f"{p.rank}", inline=False)
        else:
            embed.add_field(name=f"Overall WR", value=f"Unknown", inline=False)
            embed.add_field(name=f"Wins", value=f"Unknown", inline=False)
            embed.add_field(name=f"Losses", value=f"Unknown", inline=False)
            embed.add_field(name=f"Rank", value=f"Unknown", inline=False)
            embed.set_footer(text="This summoner hasn't started or finished placement")
        await ctx.send(embed=embed)

    @command(name="ingame", aliases=["ig"])
    async def ingame_check(self, ctx, summoner_name, region='NA'):
        await ctx.send(embed=player.Match.ingame_info(summoner_name, region))

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("league")


def setup(bot):
    bot.add_cog(League(bot))
