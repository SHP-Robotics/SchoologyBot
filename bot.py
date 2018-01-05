import json

from discord.ext.commands import Bot

from schoology_client import SchoologyClient, Attachment

bot = Bot('!')
sch = SchoologyClient('schoology_cred.json')

DISCORD_CRED = {'token': ''}
ANNOUNCEMENT_CHAN_ID = "357221559061970954"
# ANNOUNCEMENT_CHAN_ID = "238798447388524547"
ROBOTICS_GROUP_ID = "725319913"

with open('discord_cred.json') as f:
    DISCORD_CRED['token'] = json.load(f)['token']


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    if not message.channel.id == ANNOUNCEMENT_CHAN_ID:
        return
    attachments = None
    if message.attachments:
        attachments = [Attachment.from_discord_attachment(a) for a in message.attachments]
    resp = await sch.post_update(ROBOTICS_GROUP_ID, message.content, attachments=attachments)
    print(resp)


if __name__ == '__main__':
    bot.run(DISCORD_CRED['token'])
