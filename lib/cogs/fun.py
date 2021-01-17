from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed, File
from discord.errors import HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import BadArgument

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"], hidden=True)
    async def somecommand(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Howdy', 'Good day'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    @cooldown(1, 60, BucketType.user) # attempts, seconds 
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.lower().split("d"))
        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
        else:
            await ctx.send("I cannot roll that many dices. 25 is max.")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason:Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member.")

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="fact_animal", aliases=["animal_fact"])
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None


            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")
        else:
            await ctx.send(f"No fact about {animal.title()} is available.")         

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))