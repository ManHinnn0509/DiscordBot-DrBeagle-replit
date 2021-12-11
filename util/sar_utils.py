from config import BOT_COLOR, STEAM_WEB_API_KEY
from commands.sar.sar_player import SAR_Player
from commands.steam import SteamUser

import discord
from util.str_utils import escapeMD_Text
from util.time_utils import convertTime
from util.embed_utils import setAuthorBot, setRequestFooter_ctx

def createSAR_Embed(ctx, steamID: str, player: SAR_Player):
    steamUser = SteamUser(STEAM_WEB_API_KEY, steamID)

    embed = discord.Embed(
        title = escapeMD_Text(steamUser.personaName),
        url = steamUser.profileURL,
        color = BOT_COLOR,
        description = """

        Date joined: **{0}**
        Level: **{1}** | EXP: **{2}** / **{3}**
        """.format(
            convertTime(str(player.accountCreateDateTime_UTC), returnString=True).split("+")[0],
            player.currentLevel, player.currentEXP, player.currentLevelTotalEXP
        )
    )

    # Set Embed info
    setAuthorBot(embed)
    setRequestFooter_ctx(ctx, embed)
    embed.set_thumbnail(url=steamUser.avatarFullURL)

    # Add fields to the Embed

    '''
    # Old version
    dataPairs = {
        "單排 (Solo)": player.getSoloStat(),
        "雙排 (Duos)": player.getDuosStat(),
        "團隊 (Squads)": player.getSquadsStat(),
        "S.A.W. vs 反抗軍 (32 vs 32)": player.getSAW_RebellionStat(),
        "神秘模式 (Mystery Mode)": player.getMysteryModeStat(),
        "行雞走肉（感染模式）": player.getSuperHowloweenStat()
    }
    '''

    dataPairs = {
        "單排 (Solo)": player.getSoloStat(),
        "雙排 (Duos)": player.getDuosStat(),
        "團隊 (Squads)": player.getSquadsStat(),
        "S.A.W. vs 反抗軍": player.getSAW_RebellionStat(),
        "神秘模式": player.getMysteryModeStat(),
        "行雞走肉 (感染模式)": player.getSuperHowloweenStat()
    }
    __formatSAR_EmbedFields(embed, dataPairs, True)

    '''
    Update (06/12/2021):
    This part has been disabled from the update of Halloween mode
    SAR_Player object doesn't have getTotalKills() and getTotalDeaths()

    # Some other data...
    totalKills = player.getTotalKills()
    totalDeaths = player.getTotalDeaths()
    totalKD = "%.2f" % (totalKills / totalDeaths)

    embed.add_field(
        name ="__其他__",
        value = f"""
        生涯總撃殺數: **{totalKills}**
        生涯總死亡數: **{totalDeaths}**
        生涯 K/D: **{totalKD}**
        """,
        inline = False
    )
    '''

    embed.add_field(
        name = '__備註__',
        value = f"""
        - 行雞走肉 (感染模式) 中，**S** 為 **倖存者**，而 **Z** 為 **殭屍**
        """
    )

    return embed

def hideSAR_EmbedInfo(embed: discord.Embed):
    "Removes info & data in SAR Embed"
    
    embed.url = ""
    embed.title = "**資料已隱藏 | Data has been hidden**"

    embed.description = "**資料已隱藏**" + "\n" + "**Data has been hidden**"
    embed.description += "\n\n"
    embed.description +=  "Thanks for using this bot!" + "\n" + "感謝使用！"

    embed.clear_fields()
    embed.set_thumbnail(url = discord.Embed.Empty)

    return embed

def __formatSAR_EmbedFields(embed: discord.Embed, dataPairs: dict, underline=True):
    """
        Formats all the data fields for the SAR Embed
        For the formatting order, see __getData() method in class 'SAR_Player'
    """
    for k, v in dataPairs.items():
        # The v in here is actually a dict.
        # So we need to extract the value out

        '''
        v = list(v.values())

        embed.add_field(
            name = k if (underline == False) else ("__" + str(k) + "__"),
            value = f"""
            Wins: **{v[0]}**
            Played: **{v[1]}**
            Kills: **{v[2]}**
            Deaths: **{v[3]}**
            K/D: **{v[4]}**
            Win rate: **{v[5]}**
            Top: **{v[6]}**
            Most Kills: **{v[7]}**
            """,
            inline = True
        )
        '''

        l = []
        for statName, statValue in v.items():
            temp = f"{statName}: **{statValue}**"
            l.append(temp)
        
        s = '\n'.join(l)

        embed.add_field(
            name = k if (underline == False) else ("__" + str(k) + "__"),
            value = s,
            inline = True
        )