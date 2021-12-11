import os

from socket import getaddrinfo
from discord.ext import commands
from classes import Cog_Extension, Pag

from util.utils import getCommands, execPythonCode
from util.msg_utils import isOwner, tagAuthor, sendTextFileMessage
from util.time_utils import getDateTimeNow, getTimestampNow

from config import BOT_INVITE_URL

class Core(Cog_Extension):

    # --- Public commands

    @commands.command(
        brief = "Shows latency of bot"
    )
    async def ping(self, ctx):
        msg = tagAuthor(ctx) + "\n" + f"Bot latency: `{self.bot.latency:.2f}` seconds"
        await ctx.send(msg)

    @commands.command(
        aliases = ["inv"],
        brief = "Get invite link of this bot"
    )
    async def invite(self, ctx):
        """
        if (isOwner(ctx)):
            print(">>> " + BOT_INVITE_URL)
        """
        await ctx.send(tagAuthor(ctx) + "\n" + BOT_INVITE_URL)

    # --- Owners only commands

    @commands.command(
        name = "clear", aliases = ["cls"],
        brief = "Clears screen for console", hidden = True
    )
    async def clear(self, ctx):
        if (isOwner(ctx)):
            os.system("cls")

    @commands.command(
        brief = "nslookup", hidden = True
    )
    async def nslookup(self, ctx, url=None):
        if not (isOwner(ctx)):
            return
        await nslookup(ctx, url)
    
    @commands.command(
        brief = "Execute Python code. Return / show results using Discord message",
        aliases = ['eval'], hidden = True
    )
    async def evalPython(self, ctx, *, code=None):
        if not (isOwner(ctx)):
            return
        await sendPyCodeResult(self.bot, ctx, code)
    
    @commands.command(
        brief = "Execute Python code. Return / show results using FILE",
        aliases = ['evalf'], hidden = True
    )
    async def evalPython_File(self, ctx, *, code=None):
        if not (isOwner(ctx)):
            return
        await sendPyCodeResult_File(self.bot, ctx, code)

    @commands.command(
        name = "reload", aliases = ["rl"],
        brief = "Reload commands", hidden = True
    )
    async def reload(self, ctx):
        if not (isOwner(ctx)):
            return
        await reload(self.bot)

def setup(bot):
    bot.add_cog(Core(bot))

# ----- Functions extracted from Core class after finished

async def nslookup(ctx, url):
    tag = tagAuthor(ctx)
    if (url == None):
        await ctx.send(tag + "\n" + "Please provide a url")
        return
    
    ipList = []
    try:
        # Sorts by IPv4 then IPv6
        ipList = list({addr[-1][0] for addr in getaddrinfo(url, 0, 0, 0, 0)})
        ipv4List = [ip for ip in ipList if (":" not in ip)]
        ipv6List= [ip for ip in ipList if (":" in ip)]
        ipv4List.extend(ipv6List)

        ipList = ipv4List
    except Exception as e:
        # print(e)
        await ctx.send(tag + "\n" + "Unable to get info. Please make sure the input url is correct.")
        return
    
    # Format the info
    s = f"Name: {url}" + "\n" + "\n"
    s += "Address(es): " + "\n"
    s += "\n".join(ipList)
    s = "```\n" + s + "\n```"

    await ctx.send(tag + "\n" + s)

async def reload(bot):
    # ----- Inner functions
    def unloadExt(ext):
        try:
            bot.unload_extension(ext)
        except:
            pass
    
    def loadExt(ext):
        try:
            bot.load_extension(ext)
        except:
            pass
    
    # Log
    print(f">>> Reload command called on [{getDateTimeNow()}]")

    for c in getCommands():
        unloadExt(c)
        loadExt(c)

        name = c.split(".")[-1]
        print(f"[RELOAD] Extension [{name}] reloaded!")

async def sendPyCodeResult(bot, ctx, code):
    result = await execPythonCode(bot, ctx, code)
    if (result == None):
        return

    pager = Pag(
        timeout = 100,
        entries = [result[i: i + 2000] for i in range(0, len(result), 2000)],
        length = 1,
        prefix = "```py\n",
        suffix = "```"
    )
    await pager.start(ctx)

async def sendPyCodeResult_File(bot, ctx, code):
    result = await execPythonCode(bot, ctx, code)
    if (result == None):
        return
    tag = tagAuthor(ctx)
    fileName = f"result_{getTimestampNow()}.txt"
    await sendTextFileMessage(ctx, tag, fileName, result)