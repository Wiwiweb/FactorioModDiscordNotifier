import os
import asyncio
import re

import discord

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL'))
URL_FORMAT = "https://mods.factorio.com/mod/{}/changelog"

class MyClient(discord.Client):
    def __init__(self, changelogs):
        super().__init__()
        self.changelogs = changelogs

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        channel = self.get_channel(CHANNEL_ID)
        for changelog in self.changelogs:
             print('Posting in: {}'.format(channel.name))
             message = await channel.send(embed=format_embed(changelog))
             print('Posted message: '.format(message.jump_url))
             await message.publish()
             print('Published message')
        await self.close()


def send_changelog_messages(changelogs):
    client = MyClient(changelogs)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(DISCORD_TOKEN))


def format_embed(changelog):
    formatted_changelog = ""
    # Remove left padding
    for line in changelog.changelog.splitlines():
        formatted_changelog += line.lstrip() + '\n'
    formatted_changelog = formatted_changelog.partition('\n')[2] # Remove date line

    # Bold all sub-headers
    subheader_regex = re.compile(r'(\w+:)\s*$', re.MULTILINE)
    formatted_changelog = subheader_regex.sub(r'**\1**', formatted_changelog)

    embed = discord.Embed(
        title=changelog.latest_version,
        description=formatted_changelog
    )
    embed.set_author(
        name=changelog.mod_name,
        url=URL_FORMAT.format(changelog.mod_id),
        icon_url=changelog.image_url
    )
    return embed
