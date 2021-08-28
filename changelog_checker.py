import requests
from bs4 import BeautifulSoup
import re

from common import ChangelogDetails

URL_FORMAT = "https://mods.factorio.com/mod/{}/changelog"

def check_and_get_changelog_for_mod(mod_id, latest_known_version):
    full_url = URL_FORMAT.format(mod_id)
    req = requests.get(full_url)
    request_text = req.text
    soup = BeautifulSoup(request_text, 'html.parser')

    last_changelog = soup.find(class_="panel-hole-inner").string
    first_line = last_changelog.partition('\n')[0]
    latest_version = re.search(r'[\d\.]+', first_line).group(0)

    if latest_version == latest_known_version:
        return None

    mod_name = soup.find('h2').find('a').string
    image_url = soup.find('div', class_='mod-thumbnail').find('img')['src']
    
    return ChangelogDetails(mod_id, mod_name, latest_version, image_url, last_changelog)
