from util.embed_utils import createDefaultEmbed

def createHelpEmbed(ctx):
    embed = createDefaultEmbed(ctx)

    embed.title = "__**$sar help**__"
    embed.description = f"""
    **$sar**
    - View your own SAR data, require account bonding with "$sar bond" first.
    - 查自己的戰績、數據之類的，需先用"$sar bond"綁定帳號

    **$sar bond [STEAM_PROFILE_URL]**
    - Bond a Steam profile to your Discord account
    - 綁定Steam帳號至Discord帳號

    **$sar search [STEAM_PROFILE_URL]**
    - Search SAR player's data with a Steam Profile URL
    - 用Steam個人檔案連結去搜尋對方的戰績
    """

    return embed