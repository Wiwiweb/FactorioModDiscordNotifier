import os
import asyncio
import discord

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = 880885326195851268


class MyClient(discord.Client):
    def __init__(self, changelogs):
        super().__init__()
        self.changelogs = changelogs

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        channel = self.get_channel(CHANNEL_ID)
        for changelog in self.changelogs:
            await channel.send(changelog)
        await self.close()


def send_changelog_messages(changelogs):
    client = MyClient(changelogs)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(DISCORD_TOKEN))
