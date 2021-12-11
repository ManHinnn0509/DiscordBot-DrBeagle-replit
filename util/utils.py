import os
import io
import contextlib
import textwrap
import traceback
import discord

from discord.ext import commands

from util.time_utils import getDateTimeNow
from util.msg_utils import getAuthorDiscriminator, getAuthorID, getAuthorName, getContent

def getCommands():
    commandsFolderName = "commands"
    p = "./" + commandsFolderName

    l = []
    for fileName in os.listdir(p):
        if (fileName.endswith(".py")):
            n = '{}.{}'.format(commandsFolderName, fileName[:-3])
            l.append(n)
    
    return l

def logCommandCall(ctx):
    """
        Displays info on console when a command is called
    """
    authorName = getAuthorName(ctx)
    authorDiscriminator = getAuthorDiscriminator(ctx)
    authorID = getAuthorID(ctx)

    authorInfo = f"{authorName} #{authorDiscriminator} (ID: {authorID})"
    dateTimeNow = getDateTimeNow()

    s = ""
    content = getContent(ctx)
    if ("\n" not in content):
        s = f"[{dateTimeNow}] User [{authorInfo}] executed command [{content}]"
        print(s)

    else:
        cmdName = content.split(" ")[0]
        content = content[len(cmdName) + 1::]

        s = f"[{dateTimeNow}] User [{authorInfo}] executed command with name [{cmdName}] and content:\n{content}"
        print(s)
    
    return s

async def execPythonCode(bot, ctx, code):
    if (code == None):
        return None

    def cleanCode(c: str):
        if (c.startswith("```") and c.endswith("```")):
            return "\n".join(c.split("\n")[1:])[:-3]
        else:
            return c

    code = cleanCode(code)
    localVariables = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message
    }

    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", localVariables
            )
            obj = await localVariables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
    except Exception as e:
        result = "".join(traceback.format_exception(e, e, e.__traceback__))

    return result