from discord import Member, Embed, File
from discord.errors import HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.errors import BadArgument

from ..riotapi.player import Player
from ..riotapi.match import Match, CurrentMatch
from ..riotapi.data import QUEUE_ANNOTATES, RANKED_QUEUE_IDS

class League(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="rank", aliases=["r"])
    async def rank(self, ctx, summoner_name, mode, region='NA'):
        try:
            p = Player(summoner_name, RANKED_QUEUE_IDS[mode], region)
        except KeyError:
            await ctx.send(f"{mode} is invalid. There are: solo and flex supported at the moment.")
            return
        embed = Embed(title=summoner_name, description=f"{QUEUE_ANNOTATES[RANKED_QUEUE_IDS[mode]]}")
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

    @command(name="current_match_stats", aliases=["crs"])
    async def current_match_stats(self, ctx, summoner_name, region='NA'):
        embed = Embed(title=f"Current match with {summoner_name}")
        if Match.current_match_check(summoner_name, region):
            current_match = CurrentMatch(summoner_name, region)
            queue = current_match.queue
            teams = current_match.teams
            embed.description = QUEUE_ANNOTATES[current_match.queue]

            blue_team = []
            for participant in teams["blue_team"]:
                p = Player(participant.summoner.name, queue, region)
                blue_team.append(f"{p.name} - {p.rank}")
            blue_team_str = '\n'.join(blue_team)
            embed.add_field(name="Blue team", value=blue_team_str)
            
            red_team = []
            for participant in teams["red_team"]:
                p = Player(participant.summoner.name, queue, region)
                red_team.append(f"{p.name} - {p.rank}")
            red_team_str = '\n'.join(red_team)
            embed.add_field(name="Blue team", value=red_team_str)
        else:
            embed.description = "This summoner is currently not in match"
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("league")


def setup(bot):
    bot.add_cog(League(bot))
