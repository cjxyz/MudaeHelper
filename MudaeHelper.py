from time import sleep
import discum
import re
import pandas as pd
from decouple import config

tokenbot = config('tokenbot')
bot = discum.Client(token=str(tokenbot), log={"console":False, "file":False})
mudae = 432610292342587392
channel = config('channel')

descriptionFinder = re.compile("Reaccione con cualquier emoji para reclamar")

@bot.gateway.command
def onMessage(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        aId = m['author']['id']
        channelid = m['channel_id']

        if int(channelid) == int(channel):
            if int(aId) == mudae:

                if m['embeds'] == []:
                    return

                roll = m['embeds'][0]
                name = roll['author']['name']
                description = roll["description"]
                find = descriptionFinder.findall(description)

                if len(find) != 0:
                    df = pd.read_csv('Top.csv', index_col='Name')
                    try:
                        valor = str(df.loc[name, 'Value'])
                        print(name+": "+valor)
                        # bot.sendMessage(channel, name+": "+valor)
                    except:
                        print(name+": F")
                        # bot.sendMessage(channel, name+": F")

bot.gateway.run(auto_reconnect=True)