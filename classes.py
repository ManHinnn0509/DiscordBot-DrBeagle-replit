from discord.ext import commands
from discord.ext.buttons import Paginator

class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        # except discord.HTTPException as e:
        #     print(e)
        except Exception as e:
            print(e)