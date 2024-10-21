import os
import re
import requests
from ddb_proxy import set_last_known_version
from ddb_proxy import set_version_and_changelog
from common import ChangelogDetails

ALL_MODS_URL = "https://mods.factorio.com/api/mods?version=2.0&page_size=max"
MOD_DETAILS_URL = "https://mods.factorio.com/api/mods/{}/full"
THUMBNAIL_BASE_URL = "https://mods-data.factorio.com"
VERSION_SEPARATOR = "---------------------------------------------------------------------------------------------------"

OWNER = os.environ.get('MOD_AUTHOR')


def get_updated_mods(known_mods_saved_info):
    new_changelog_details = []
    owner_mods = get_all_mods_by_owner()

    for mod in owner_mods:
        current_version = mod['latest_release']['version']
        known_version = known_mods_saved_info[mod['name']].last_known_version if mod['name'] in known_mods_saved_info else None
        compared_value = compare_versions(mod['latest_release']['version'], known_version)

        if compared_value == 1:
            print('New version of {}: {} -> {}'.format(mod['name'], known_version, current_version))
            new_changelog = get_details_for_mod(mod['name'])
            new_changelog_details.append(new_changelog)
        elif compared_value == -1:
            print('WARN - Mod {} was downgraded! {} -> {}'.format(mod['name'], known_version, current_version))
            set_last_known_version(mod['name'], current_version)
    return new_changelog_details


def compare_versions(version_a, version_b):
    """
        0 if a == b
        -1 if a < b
        1 if a > b
    """
    if version_a is None:
        return -1
    if version_b is None:
        return 1

    split_a = version_a.split('.')
    split_b = version_b.split('.')
    for a_element, b_element in zip(split_a, split_b):
        if int(a_element) < int(b_element):
            return -1
        if int(a_element) > int(b_element):
            return 1

    if len(split_a) < len(split_a):
        return -1
    if len(split_a) > len(split_a):
        return 1
    return 0


def get_all_mods_by_owner():
    req = requests.get(ALL_MODS_URL)
    request_json = req.json()
    return (mod for mod in request_json['results'] if mod['owner'] == OWNER)


def get_details_for_mod(mod_id):
    full_url = MOD_DETAILS_URL.format(mod_id)
    req = requests.get(full_url)
    request_json = req.json()

    mod_name = request_json['title']
    last_version = request_json['releases'][-1]['version']
    if 'thumbnail' in request_json:
        image_url = THUMBNAIL_BASE_URL + request_json['thumbnail']
    else:
        image_url = None

    if 'changelog' in request_json:
        all_changelogs = request_json['changelog']
        _, _, all_changelogs = all_changelogs.partition('\n')  # Remove first line
        last_changelog, _, _ = all_changelogs.partition(VERSION_SEPARATOR)
        _version_line, _, last_changelog = last_changelog.partition('\n')
    else:
        last_changelog = None

    return ChangelogDetails(mod_id, mod_name, last_version, image_url, last_changelog)
