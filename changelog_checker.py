import os
import re
import requests
from common import ChangelogDetails

ALL_MODS_URL = "https://mods.factorio.com/api/mods?version=1.1&page_size=max"
MOD_DETAILS_URL = "https://mods.factorio.com/api/mods/{}/full"
THUMBNAIL_BASE_URL = "https://mods-data.factorio.com"
VERSION_SEPARATOR = "---------------------------------------------------------------------------------------------------"

OWNER = os.environ.get('MOD_AUTHOR')

def get_updated_mods(known_mods_versions):
    new_changelog_details = []
    owner_mods = get_all_mods_by_owner()
    for mod in owner_mods:
        if mod['name'] not in known_mods_versions or mod['latest_release']['version'] != known_mods_versions[mod['name']]:
            known_version = known_mods_versions[mod['name']] if mod['name'] in known_mods_versions else None
            print('New version of {}: {} -> {}'.format(mod['name'], known_version, mod['latest_release']['version']))
            new_changelog = get_details_for_mod(mod['name'])
            new_changelog_details.append(new_changelog)
    return new_changelog_details


def get_all_mods_by_owner():
    req = requests.get(ALL_MODS_URL)
    request_json = req.json()
    return (mod for mod in request_json['results'] if mod['owner'] == OWNER)


def get_details_for_mod(mod_id):
    full_url = MOD_DETAILS_URL.format(mod_id)
    req = requests.get(full_url)
    request_json = req.json()

    mod_name = request_json['title']
    image_url = THUMBNAIL_BASE_URL + request_json['thumbnail']

    all_changelogs = request_json['changelog']
    _, _, all_changelogs = all_changelogs.partition('\n') # Remove first line
    last_changelog, _, _ = all_changelogs.partition(VERSION_SEPARATOR)
    version_line, _, last_changelog = last_changelog.partition('\n')
    latest_version = re.search(r'[\d\.]+', version_line).group(0)

    return ChangelogDetails(mod_id, mod_name, latest_version, image_url, last_changelog)
