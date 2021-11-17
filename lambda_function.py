from changelog_checker import get_updated_mods
from ddb_proxy import get_known_mods
from ddb_proxy import set_version_and_changelog
from discord_poster import send_changelog_messages


def lambda_handler(_event, _lambda_context):

    known_mods_saved_info = get_known_mods()
    new_changelogs = get_updated_mods(known_mods_saved_info)

    changelogs_to_post = []
    
    if new_changelogs:
        for changelog in new_changelogs:
            set_version_and_changelog(changelog.mod_id,
                                      changelog.last_version,
                                      changelog.changelog)
            last_posted_changelog = known_mods_saved_info[changelog.mod_id].last_posted_changelog if changelog.mod_id in known_mods_saved_info else None
            if (changelog.changelog != last_posted_changelog):
                # Only post if the actual changelog text is different from the last one we posted
                changelogs_to_post.append(changelog)
            else:
                print('WARN - Mod {} was upgraded but with the same changelog!'.format(changelog.mod_id))

    if changelogs_to_post:
        send_changelog_messages(changelogs_to_post)


if __name__ == '__main__':
    lambda_handler(None, None)
