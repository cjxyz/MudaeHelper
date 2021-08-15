from time import sleep
import discum
import re
import pandas as pd
from decouple import config

tokenbot = config('tokenbot')
bot = discum.Client(token=tokenbot, log={"console":False, "file":False})
mudae = 432610292342587392
channel = config('channel')

bot.sendMessage(channel, "Starting Top")

nameFinder = re.compile(" \*\*(.+?)\*\* (?!ka)")
kakeraFinder = re.compile("\*\*??([0-9]+)")
pageFinder = re.compile("[0-9]+")

def parseValues(resp):
    m = resp.parsed.auto()
    aId = m['author']['id']
    messageid = m['id']
    channelid = m['channel_id']

    if int(channelid) == int(channel):
        if int(aId) == mudae:
            embed = m['embeds'][0]
            names, kakeras = getValue(embed)
            
            tuple = zip(names, kakeras)
            df = pd.DataFrame(tuple, columns=['Name','Value'])

            pages = embed['footer']['text']
            CurPage = pageFinder.findall(pages)[0]
            LastPage = pageFinder.findall(pages)[1]

            print(CurPage+" / "+LastPage)

            if int(CurPage) != int(LastPage):
                if int(CurPage) == 1:
                    df.to_csv('Top.csv', mode='w', index=False)
                    sleep(3)
                else:
                    df.to_csv('Top.csv', mode='a', index=False)
                    sleep(1)

                if int(CurPage)%2 == 1:
                    bot.addReaction(channel, messageid, 'wright:847502746025459792')
                else:
                    bot.removeReaction(channel, messageid, 'wright:847502746025459792')

def getValue(embed):
    description = embed["description"]
    names = nameFinder.findall(description)
    kakeras = kakeraFinder.findall(description)
    return names, kakeras

@bot.gateway.command
def onMessage(resp):
    if resp.event.message or resp.event.message_updated:
        parseValues(resp)

bot.gateway.run(auto_reconnect=True)