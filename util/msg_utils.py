import os
import uuid

from discord import File as DiscordFile
from discord import Forbidden

from util.json_utils import writeJSON_File
from config import OWNER_ID

def tagAuthor(ctx):
    return "<@{}>".format(ctx.message.author.id)

def getAuthor(ctx):
    return ctx.message.author

def getAuthorName(ctx):
    return ctx.author.name

def getAuthorDiscriminator(ctx):
    return ctx.message.author.discriminator

def getAuthorID(ctx):
    return ctx.message.author.id

def getAuthorDisplayName(ctx):
    return ctx.author.display_name

def getAuthorAvatarURL(ctx):
    return ctx.message.author.avatar_url

def getContent(ctx):
    return ctx.message.content

def isOwner(ctx):
    return str(getAuthorID(ctx)) == OWNER_ID

async def deleteSenderMessage(ctx):
    try:
        await ctx.message.delete()
    except Forbidden:
        # print("No permission to delete message")
        pass
    except:
        pass

async def getMessageByID(ctx, msgID):
    try:
        msgID = int(msgID)
        msg = await ctx.fetch_message(msgID)
        return msg
    except:
        # Not found
        # See https://discordpy.readthedocs.io/en/latest/api.html#discord.abc.Messageable.fetch_message
        return None

async def sendTextFileMessage(channel, textMessage, fileName, fileContent):
    """
        Creates a temp .txt file with input content.
        Send the file and delete it afterward
    """
    try:
        # Random file name
        p = f"./{uuid.uuid4()}.txt"

        # Write the content into the .txt file first
        with open(p, "w+", encoding="utf-8") as f:
            f.write(fileContent)
        
        msg, result = await sendFileMessage(channel, textMessage, fileName, p, True)

        return msg, result
    except Exception as e:
        # print(e)
        return None, False

async def sendJsonFileMessage(channel, textMessage, fileName, jsonContent: dict):
    """
        Creates a temp .json file with input dict.
        Send the json file and delete it afterward
    """
    try:
        # Write the dict / json data into the file first
        p = f"./{uuid.uuid4()}.txt"
        r = writeJSON_File(p, jsonContent)
        if not (r):
            raise Exception
        
        msg, result = await sendFileMessage(channel, textMessage, fileName, p, True)

        return msg, result
    except Exception as e:
        # print(e)
        return None, False

async def sendFileMessage(channel, textMessage, fileName, filePath, removeFile=False):
    """
        Send a file to target text channel
    """
    try:
        with open(filePath, "rb") as f:
            msg = await channel.send(textMessage, file = DiscordFile(f, fileName))
        
        if (removeFile):
            os.remove(filePath)
        
        return msg, True
    except:
        return None, False