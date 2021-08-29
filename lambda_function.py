from changelog_checker import get_updated_mods
from ddb_proxy import get_known_mods
from ddb_proxy import set_latest_version
from discord_poster import send_changelog_messages

def lambda_handler(_event, _lambda_context):

    known_mods_versions = get_known_mods()
    new_changelogs = get_updated_mods(known_mods_versions)

    if new_changelogs:
        for changelog in new_changelogs:
            set_latest_version(changelog.mod_id, changelog.latest_version)
        send_changelog_messages(new_changelogs)


if __name__ == '__main__':
    lambda_handler(None, None)
