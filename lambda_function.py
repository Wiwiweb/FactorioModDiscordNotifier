from changelog_checker import check_and_get_changelog_for_mod
from ddb_proxy import get_all_mods
from ddb_proxy import set_latest_version
from discord_poster import send_changelog_messages

def lambda_handler():

    new_changelogs = []
    mods = get_all_mods()

    for mod_name, latest_known_version in mods.items():
        new_changelog = check_and_get_changelog_for_mod(mod_name, latest_known_version)
        if new_changelog:
            print("New update: " + str(new_changelog))
            new_changelogs.append(new_changelog)
            set_latest_version(mod_name, new_changelog.latest_version)

    if new_changelogs:
        send_changelog_messages(new_changelogs)


if __name__ == '__main__':
    lambda_handler()
