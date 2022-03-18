import os
import asyncio
import re

import discord

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL'))
URL_FORMAT = "https://mods.factorio.com/mod/{}/changelog"

DESCRIPTION_LIMIT = 4096


class MyClient(discord.Client):
    def __init__(self, changelogs):
        super().__init__()
        self.changelogs = changelogs

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        channel = self.get_channel(CHANNEL_ID)
        for changelog in self.changelogs:
            print('Posting in: {}'.format(channel.name))
            embeds = format_embeds(changelog)
            for embed in embeds:
                message = await channel.send(embed=embed)
                print('Posted message: {}'.format(message.jump_url))
                await message.publish()
                print('Published message')
        await self.close()


def send_changelog_messages(changelogs):
    client = MyClient(changelogs)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(DISCORD_TOKEN))


def format_embeds(changelog):

    formatted_changelog = []
    for line in changelog.changelog.splitlines():
        line = line[2:] # Remove first 2 spaces
        final_line = []
        for i, char in enumerate(line):
            if char == " ":
                # Prefix each leading whitespaces with zero-length char to prevent Discord from removing them
                final_line += "\u200B "
            else:
                # Add the rest and break
                final_line.append(line[i:])
                break
        final_line = ''.join(final_line)
        formatted_changelog.append(final_line)

    formatted_changelog = formatted_changelog[1:] # Remove date line
    formatted_changelog = '\n'.join(formatted_changelog)

    # Bold all sub-headers
    subheader_regex = re.compile(r'^(\w+:)\s*$', re.MULTILINE)
    formatted_changelog = subheader_regex.sub(r'**\1**', formatted_changelog)

    changelogs_posts = [formatted_changelog]
    while len(changelogs_posts[-1]) > DESCRIPTION_LIMIT:
        first_half, second_half = split_in_two_at_line_break(changelogs_posts[-1])
        changelogs_posts[-1] = first_half
        changelogs_posts.append(second_half)

    embeds = []
    for i, changelog_post in enumerate(changelogs_posts):
        title = changelog.last_version
        if i > 0:
            title += " - Continued"
        embed = discord.Embed(
            title=title,
            description=changelog_post
        )
        embed.set_author(
            name=changelog.mod_name,
            url=URL_FORMAT.format(changelog.mod_id),
            icon_url=changelog.image_url
        )
        embeds.append(embed)
    return embeds


def split_in_two_at_line_break(string):
    split_point = DESCRIPTION_LIMIT - 1
    split_char = string[split_point]
    while split_char != '\n':
        split_point -= 1
        split_char = string[split_point]

    first_part = string[:split_point]  # Don't include the actual line break
    second_part = string[split_point:]
    return first_part, second_part
