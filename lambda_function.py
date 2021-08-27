from changelog_checker import check_changelog_for_mod
from ddb_proxy import get_all_mods
from ddb_proxy import set_latest_version
from discord_poster import send_changelog_messages


def lambda_handler():

    # mods = get_all_mods()
    # for mod_name, latest_version in mods.items():
    #     current_version, changelog = check_changelog_for_mod(mod_name)
    #     if current_version != latest_version:
    #         set_latest_version(mod_name, current_version)
    send_changelog_messages({"hey", "yo"})

if __name__ == '__main__':
    lambda_handler()
