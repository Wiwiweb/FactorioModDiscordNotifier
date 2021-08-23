import requests
from bs4 import BeautifulSoup
import re

URL_FORMAT = "https://mods.factorio.com/mod/{}/changelog"

def check_changelog_for_mod(modname):
    full_url = URL_FORMAT.format(modname)
    req = requests.get(full_url)
    request_text = req.text
    soup = BeautifulSoup(request_text, 'html.parser')

    last_changelog = soup.find(class_="panel-hole-inner").string
    first_line = last_changelog.partition('\n')[0]
    version_number = re.search(r'[\d\.]+', first_line).group(0)
    
    return version_number, last_changelog
