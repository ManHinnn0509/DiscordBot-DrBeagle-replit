# In replit.com
# In Console
# Run subprocess.run(['python', 'main.py'])

import time
from util.msg_utils import tagAuthor
from util.utils import getCommands
import discord

from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.errors import CommandInvokeError, UnexpectedQuoteError

from util.utils import logCommandCall
from util.time_utils import getDateTimeNow
from config import BOT_TOKEN, BOT_PREFIX, BOT_ACTIVITY
from replNeverSleep import awake
from variables import commandCallHistory

def main():

    print(f"[{getDateTimeNow()}] Launching Bot...")
    startTime = time.time()

    # These 2 lines are for the "$py" command
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix = BOT_PREFIX, intents=intents)

    # --------------------
    @bot.event
    async def on_ready():

        await bot.change_presence(activity = BOT_ACTIVITY)

        dt = time.time() - startTime
        # print("[{}] Bot launched in around {:.2f} seconds.".format(getDateTimeNow(), dt))
        print(f"[{getDateTimeNow()}] Bot launched in around {dt:.2f} seconds.")
    
    @bot.event
    async def on_command_error(ctx, error):
        # From: https://stackoverflow.com/questions/52900101/remove-command-not-found-error-discord-py
        if isinstance(error, CommandNotFound):
            return

        elif (isinstance(error, UnexpectedQuoteError)):
            errorMsg = tagAuthor(ctx) + "\n" + "Exception caught in on_command_error() with following log: "
            errorMsg = "```" + "\n" + repr(error) + "\n" + "```"
            await ctx.send(errorMsg)

        else:
            raise error

        """
        if isinstance(error, CommandInvokeError):
            print(">>> CommandInvokeError detected. Please remove this block of code if you're debugging")
            # print(error)
            return
        """

    @bot.event
    async def on_command(ctx):
        cmdCall = logCommandCall(ctx)
        
        global commandCallHistory
        commandCallHistory.append(cmdCall)
        
    # --------------------

    for cmd in getCommands():
        bot.load_extension(cmd)

    bot.run(BOT_TOKEN)
    
    print("--- End of Program ---")

'''
if (__name__ == "__main__"):
    # From: https://replit.com/talk/share/NEVER-have-your-Python-Repls-go-to-sleep-again/34645
    from keep_alive import awake
    awake(
        'http://DiscordBot-DrBeagle.manhinnn0509.repl.co',
        True
    )    # Has to be True?

    # from keep_alive import keep_alive
    # keep_alive()

    main()
'''

if (__name__ == '__main__'):

    # From: https://replit.com/@105303058/Husky-Bot?v=1

    awake(
        'https://DrBeagle.manhinnn0509.repl.co',
        True
    )

    main()